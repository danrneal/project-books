# Project: Books

This flask-based app stores a database of books and allows users to leave reviews about the books on the site.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

Install the requirements:

```bash
pip install -U pip
pip install -r requirements.txt
```

Obtain a Goodreads API key [here](https://www.goodreads.com/api/keys).

Set up your environment variables:

```bash
touch .env
echo DATABASE_URL="postgres://XXX" >> .env
echo GOODREADS_KEY="XXX" >> .env
```

### import.py

Included is an import script that takes as an input books.csv and imports each entry as a book in the database. A books.csv file is included in this repo with 5000 books. You may add or replace with your own books.csv. Below is an example books.csv to illustrate the format the file should be in.

```csv
isbn,title,author,year
0380795272,Krondor: The Betrayal,Raymond E. Feist,1998
1416949658,The Dark Is Rising,Susan Cooper,1973
```

Make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

Make sure .env variables are set:

```bash
set -a; source .env; set +a
```

Then run the script:

```bash
Usage: import.py
```

## Usage

Make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

```bash
Usage: flask run
```

## Screenshots

![Project: Books Login Page](https://i.imgur.com/ll4rUIB.png)

![Project: Books Search Page](https://i.imgur.com/Nt95oJA.png)

![Project: Books Book Detail Page](https://i.imgur.com/HQijpIM.png)

## Credit

[HarvardX: CS50's Web Programming with Python and JavaScript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript)

## License

Project: Books is licensed under the [MIT license](https://github.com/danrneal/project-books/blob/master/LICENSE).
