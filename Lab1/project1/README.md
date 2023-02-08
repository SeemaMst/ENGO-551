# Project 1

ENGO 551: Lab 1 (Book Review Site Part 1)
Created by: Group 7 (Seema Mustaqeem and Luc Nicolet)
Last updated: February 7, 2023

File List:
├───templates
    - book.html
    - homepage.html
    - index.html
    - registrationpage.html

application.py
books.csv
import.py
requirements.txt

Important Notes:
    The import.py function currently has a hardcoded DATABASE_URL value, this must be changed for the function to work.

    The following sql commands were used to initially create tables within the database:
        CREATE TABLE booklist(
            isbn VARCHAR PRIMARY KEY NOT NULL,
            title VARCHAR,
            author VARCHAR,
            year INT
        );
        CREATE TABLE reviews(
            Id_pl SERIAL PRIMARY KEY,
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

