import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    with open('books.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for isbn, title, author, year in reader:
            author_id = db.execute(
                "INSERT INTO authors (name) VALUES(:name) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id", {
                    "name": author
                }
            ).fetchone()[0]
            db.execute(
                "INSERT INTO books (isbn, title, author_id, year) VALUES(:isbn, :title, :author_id, :year) ON CONFLICT (isbn) DO NOTHING", {
                    "isbn": isbn,
                    "title": title,
                    "author_id": author_id,
                    "year": year
                }
            )
            print(f"Added book: {isbn}, {title}, {author}, {year}")
        db.commit()


if __name__ == "__main__":
    main()
