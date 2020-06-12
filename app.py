import os
import re
import requests

from flask import Flask, flash, session, request, render_template, redirect, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
GOODREADS_KEY = os.getenv("GOODREADS_KEY")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if session.get("user_id") is None:
        return redirect("/login")

    query = request.args.get("q")
    field = request.args.get("field")

    if query == "":
        flash("Search may not be empty.", "danger")
        return render_template("index.html")
    elif field == "":
        flash("Search type must be specified", "danger")
        return render_template("index.html")
    elif field and field not in ('isbn', 'author', 'title'):
        flash("Invalid search type specified", "danger")
        return render_template("index.html")

    books = None
    if query and field:
        books = db.execute(
            f"SELECT * FROM books WHERE {field} ILIKE :search",
            {
                "search": f"%{query}%"
            }
        ).fetchall()

        if not books:
            flash("Search returned no results.", "danger")

    return render_template("index.html", books=books)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Username may not be left blank.", "danger")
            return render_template("register.html")
        elif not password:
            flash("Password may not be left blank.", "danger")
            return render_template("register.html")
        elif not confirmation:
            flash("Confirm Password may not be left blank.", "danger")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)

        user_id = db.execute(
            "INSERT INTO users (username, hash) VALUES(:username, :hash) ON CONFLICT DO NOTHING RETURNING id",
            {
                "username": username,
                "hash": hashed_password
            }
        ).fetchone()
        db.commit()

        pattern = re.compile(r'\d.*?[A-Z].*?[a-z].*[^\da-zA-Z]')

        if not user_id:
            flash("Username already taken.", "danger")
            return render_template("register.html")
        elif pattern.search(password) and len(password) >= 8:
            flash("Password must be at least 8 characters; must contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character.", "danger")
            return render_template("register.html")
        elif password != confirmation:
            flash("Passwords must match.", "danger")
            return render_template("register.html")

        session["user_id"] = user_id[0]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/check")
def check():
    username = request.args.get("username")
    if username:
        user = db.execute(
            "SELECT username FROM users WHERE username = :username", {
                "username": username
            }
        ).fetchone()
        db.close()
        if user:
            return jsonify(False)

    return jsonify(True)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("Username may not be left blank.", "danger")
            return render_template("login.html")
        elif not password:
            flash("Password may not be left blank.", "danger")
            return render_template("login.html")

        user = db.execute(
            "SELECT * FROM users WHERE username = :username", {
                "username": username
            }
        ).fetchone()

        if not user or not check_password_hash(user["hash"], password):
            flash("Invalid username and/or password", "danger")
            return render_template("login.html")

        session["user_id"] = user["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/<isbn>", methods=["GET", "POST"])
def book(isbn):
    if session.get("user_id") is None:
        return redirect("/login")

    reviews = db.execute(
        "SELECT books.id, isbn, title, author, year, rating, review, username FROM books LEFT JOIN reviews ON reviews.book_id = books.id LEFT JOIN users ON reviews.user_id = users.id WHERE isbn = :isbn",
        {
            "isbn": isbn
        }
    ).fetchall()

    if not reviews:
        flash(f"Could not find book with ISBN: {isbn}", "danger")
        return redirect("/")

    book = reviews[0]

    user_id = session.get("user_id")

    if request.method == "POST" and user_id:
        rating = request.form.get("rating")
        review = request.form.get("review")

        if not rating:
            flash("Rating may not be left blank.", "danger")
            return redirect(f"/{isbn}")
        elif not review:
            flash("Review may not be left blank.", "danger")
            return redirect(f"/{isbn}")
        elif rating not in ('1', '2', '3', '4', '5'):
            flash("Invalid rating submitted.", "danger")
            return redirect(f"/{isbn}")

        db.execute(
            "INSERT INTO reviews (rating, review, user_id, book_id) VALUES(:rating, :review, :user_id, :book_id) ON CONFLICT (user_id, book_id) DO UPDATE SET (rating, review) = (EXCLUDED.rating, EXCLUDED.review)",
            {
                "rating": rating,
                "review": review,
                "user_id": user_id,
                "book_id": book['id']
            }
        )
        db.commit()

        flash("Review submitted or updated!", "success")
        return redirect(f"/{isbn}")

    else:
        goodreads = None
        if GOODREADS_KEY:
            response = requests.get(
                "https://www.goodreads.com/book/review_counts.json",
                params={
                    "key": GOODREADS_KEY,
                    "isbns": isbn
                }
            ).json()

            if 'books' in response and len(response['books']) > 0:
                goodreads = response['books'][0]

        if book['review'] is None:
            reviews = None

        return render_template("book.html", book=book, goodreads=goodreads, reviews=reviews)


@app.route("/api/<isbn>")
def api(isbn):
    book = db.execute(
        "SELECT isbn, title, author, year, AVG(rating), COUNT(review) FROM books LEFT JOIN reviews ON reviews.book_id = books.id GROUP BY books.id HAVING isbn = :isbn",
        {
            "isbn": isbn
        }
    ).fetchone()

    if not book:
        abort(404)

    avg_rating = None
    if book['avg']:
        avg_rating = float(round(book['avg'], 1))

    response = {
        "title": book['title'],
        "author": book['author'],
        "year": book['year'],
        "isbn": book['isbn'],
        "review_count": book['count'],
        "average_score": avg_rating
    }

    return response
