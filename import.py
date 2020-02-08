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
        for row in reader:
            db.execute(
                "INSERT INTO books (isbn, title, author, year) VALUES(:isbn, :title, :author, :year)", {
                    "isbn": row[0],
                    "title": row[1],
                    "author": row[2],
                    "year": row[3]
                }
            )
            print(f"Added book: {', '.join(row)}")
        db.commit()


if __name__ == "__main__":
    main()
