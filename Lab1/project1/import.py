import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://postgres:Seema2001@localhost/books")
db= scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)

    for isbn, title, author, year in reader:
        data = ( { "isbn": isbn, "title": title, "author": author, "year": year },)
        statement = text("INSERT INTO booklist (isbn, title, author, year) VALUES (:isbn, :title, :author, :year);")
        db.execute(statement, data)
    db.commit()

if __name__=="__main__":
    main()