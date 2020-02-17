# Books

This flask-based app stores a database of books and allows users to leave
reviews about the books on the site.

## Set-up

Set-up a virtual environment and activate it:
```
python3 venv venv
source /venv/bin/activate
```
You should see (venv) before your command prompt now. (You can type `deactivate`
to exit the virtual environment any time.)

Install the requirements:
```
pip install -r requirements.txt
```

Set up your environment variables:
```
touch .env
echo FLASK_APP="application.py" >> .env
echo DATABASE_URL="postgres://XXX" >> .env
echo GOODREADS_KEY="XXX" >> .env
```

## Usage

Make sure you are in the virtual environment (you should see (venv) before your
command prompt). If not `source /venv/bin/activate` to enter it.

```
Usage: flask run
```

#### import.py

Included is an import script that takes as an input books.csv and imports each
entry as a book in the database.  Below is an example books.csv to illustrate
the format the file should be in.

```
isbn,title,author,year
0380795272,Krondor: The Betrayal,Raymond E. Feist,1998
1416949658,The Dark Is Rising,Susan Cooper,1973
```

A books.csv file is included in this repo with 5000 books.  You may add or
replace with your own books.csv.

```
Usage: import.py
```

## Credit

[HarvardX: CS50's Web Programming with Python and JavaScript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript)

## License

Books is licensed under the [MIT license](https://github.com/danrneal/books/blob/master/LICENSE).
