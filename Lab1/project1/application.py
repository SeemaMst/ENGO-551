import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker

from datetime import datetime


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Landing page - Website login
@app.route("/", methods=["POST", "GET"])
def login():

    message =""
    if request.method == "POST":
        # record the user name and password
        session["name"] = request.form.get("name")
        name=request.form.get("name")
        passwordcheck=request.form.get("Password")
        data = ( { "firstname": name, "firstpassword": passwordcheck },)

        statement2 =text("SELECT 1 FROM users WHERE username=(:firstname);")
        count = db.execute(statement2, (data))

        if count.rowcount == 1: # if user exists

            passwordstatement=text("SELECT 1 FROM users WHERE password=(:firstpassword) AND username=(:firstname);")
            passcount=db.execute(passwordstatement, (data))

            if passcount.rowcount != 1: # if password is not correct
                message = "Password is Incorrect"
                return render_template("index.html", message=message)

            # If Username and Password match/exist
            return redirect("/test") 
        
        if count.rowcount == 0: # this means no user exists with this username
            message = "User Does Not Exist - Please Register"
            return redirect("/registration")
        
        db.commit()

    return render_template("index.html", message=message)

# Registration Page - for new users
@app.route("/registration", methods=["POST", "GET"])
def registration():
    message = ""
    if request.method=="POST":
        user = request.form.get("Name")
        password = request.form.get("Password")
        email = request.form.get("Email")

        data = ( { "firstname": user, "firstpassword": password, "email": email },)

        statement2 =text("SELECT 1 FROM users WHERE username=(:firstname);")
        count = db.execute(statement2, (data))

        if count.rowcount == 1: # if user exists
            message = "This username already exists, please choose a new one."
            return render_template("registrationpage.html", message=message)

        statement=text("""INSERT INTO users (username, password, email) VALUES (:firstname, :firstpassword, :email);""")
        db.execute(statement, data)
        db.commit()

        return render_template("index.html", message="User successfully created! Login Now")

    return render_template("registrationpage.html")

# Homepage - once users have logged in they land here
@app.route("/test", methods=["POST", "GET"])
def home():
    listtest = []
    num_results=0

    # Search Queries
    if request.method == "POST":
        isbncheck = '%' + request.form.get("isbn") + '%'
        titlecheck = '%' + request.form.get("title")+'%'
        authorcheck = '%'+request.form.get("author")+'%'
        yearcheck = '%'+request.form.get("year")+'%'
        result = ({"isbn": isbncheck, "title": titlecheck, "author": authorcheck, "year": yearcheck},) # need to fix year so that it matches the int type
        statement=text("SELECT isbn, title, author, year FROM booklist WHERE isbn ILIKE :isbn AND title ILIKE :title AND author ILIKE :author AND CAST(year AS TEXT) ILIKE :year") # Add year here
        row = db.execute(statement, result)
        rows=row.fetchall()
        num_results = row.rowcount

        for row in rows:
            listtest.append(row)

        db.commit()

        return render_template("homepage.html", result=listtest, result_count=num_results)
    return render_template("homepage.html", result=listtest, result_count = num_results)

reviews = []

# Book page - page with additional info per book, including book reviews
@app.route("/book/<record_id>", methods=["POST", "GET"])
def book(record_id):
    data = ({"isbn": record_id},)
    statement = text("SELECT isbn, title, author, year FROM booklist WHERE isbn ILIKE :isbn")
    row = db.execute(statement, data)
    rows = row.fetchall()

    # Here users can create a review
    if request.method == "POST":
        review = request.form.get("review")
        starrating = request.form.get("starrating")
        today=datetime.today().strftime('%Y-%m-%d')
        reviewdata=({"isbn": record_id, "starrating":starrating, "description":review, "currentuser": session["name"], "date": today })
        
        statement=text("""INSERT INTO reviews (id, starrating, description, currentuser, reviewdate) VALUES (:isbn, :starrating, :description, :currentuser, :date );""")
        db.execute(statement, reviewdata)

    statement2 = text("""SELECT starrating, description, currentuser, reviewdate FROM reviews WHERE id = (:isbn)""")
    reviewtest = db.execute(statement2, data)
    reviewtotal = reviewtest.fetchall()
    
    db.commit()
    return render_template("book.html", result=rows, reviews=reviewtotal)

# Route if users choose to logout
@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")