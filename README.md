# Project 1: Books

Web Programming with Python and JavaScript

## Description

This flask-based app stores a database of books and allows users to leave reviews about the books on the site.

## What is in each file

* application.py
    * This file contains all the server-side Flask logic that the web application needs.
    * It handles each route and redirects users to the appropriate page or renders the appropriate template.
    * It handles any look-ups or updates needed by the database.
* import.py
    * This file takes a csv file called books.csv and inserts each book into the database.
* .gitignore
    * This file tells git which files to ignore when submitting.
    * Useful for setting up a virtual environment.
    * Also useful for ignoring a .env file holding environmental variables such as my goodreads api key.
* requirements.txt
    * Holds the app's dependencies.
    * Added python-dotenv (to handle using a .env file) and requests (to handle the api calls)
* books.csv
    * List of books that was provided with the distribution code.
* templates/layout.html
    * Layout template that is the base for all the other pages
    * Contains the navbar as well as a header for flashed alert messages
* templates/index.html
    * Contains a form allowing users to search books based on ISBN, author, or title.
    * After a search, displays of table or returned results with a link for each book.
* templates/register.html
    * A form for users to register with the site, requiring a unique username, a password, and the password typed again.
* templates/login.html
    * A form for previously registered users to sign in.
* templates/book.html
    * A page displaying information about a specific book including reviews left by other users.
    * A form allowing a user to submit their own review or update a previous review they submitted.
