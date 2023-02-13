import os
import json
import requests

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker

from datetime import datetime
from urllib.request import urlopen

stringtest="isbn:" + "1250012570"

res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": stringtest}) # YAY! stringtest works
responsedict = res.json()
volume_info = responsedict["items"][0]["volumeInfo"]
author = volume_info["authors"]
# testword=responsedict["items"]["authors"]
averagerating=volume_info["averageRating"]
ratingscount=volume_info["ratingsCount"]
test1=volume_info["industryIdentifiers"][0]["type"]
more_info=volume_info["industryIdentifiers"]
print(more_info)
print(type(more_info))
print(len(more_info))

if more_info[1] is not None:
    check=more_info[0]
    print(check)
    print("Looks good!")
else:
    print("No bueno :(")

print(ratingscount)

# So we've figured out from this that not all ISBN's work - even if a book actually does exist under it
# Proposed workflow:
# Start by searching ISBN, if no results found (totalItems=0) then search for title, if no results found we can say Google doesn't have this book
# To double check (there may be more than one book with the same title), check that the totalItems=1, if greater than 1 then query both to check
# for author as well