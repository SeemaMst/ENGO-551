# Project 1

ENGO 551: Lab 1 (Book Review Site Part 1)
Created by: Group 7 (Seema Mustaqeem and Luc Nicolet)
Last updated: February 7, 2023

Project Description: The created FLASK APP is a web app book database, where users are able to register/log in and search for a book, get more info about the book, get access to Google Books API review information, and leave their own reviews. They are also able to call /api/<isbn> to get a JSON file for their requested book information. 

File List:
├───templates
    - book.html: template for book page - contains more info and reviews for the individual book
    - homepage.html: Main search page for site - user is taken here after login
    - index.html: Landing (login) page for the website
    - registrationpage.html: Registration page for the site (can be accessed through login page)

application.py: FLASK_APP
books.csv: Given csv with list of books
import.py: Python function for importing book csv
testfunction.py: Python file function for testing the use of Google API in a separate file, prior to adding to Flask App
requirements.txt: Given requirements file for python libraries

Important Notes:
    The import.py function currently has a hardcoded DATABASE_URL value in create_engine(), this must be changed for the function to work with other databases.

    The following sql commands were used to initially create tables within the database:
        CREATE TABLE booklist(
            isbn VARCHAR PRIMARY KEY NOT NULL,
            title VARCHAR,
            author VARCHAR,
            year INT
        );
        CREATE TABLE reviews(
            id_pl SERIAL PRIMARY KEY,
            id VARCHAR NOT NULL,
            starrating INT NOT NULL,
            description VARCHAR,
            currentuser VARCHAR NOT NULL,
            reviewdate DATE
        );
        CREATE TABLE users(
            id SERIAL,
            username VARCHAR NOT NULL PRIMARY KEY,
            password VARCHAR NOT NULL,
            email VARCHAR
        );

