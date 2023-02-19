import os
import requests
import geojson as gpd 
import json

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker

from datetime import datetime

app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

# Landing page - Website login
@app.route("/", methods=["POST", "GET"])
def login():
    geojson_url="https://data.calgary.ca/resource/c2es-76ed.geojson"


    if request.method=="POST":
        fromdate=request.form.get("FromDate")
        todate=request.form.get("ToDate")
        str(fromdate)
        str(todate)

        testagain = str(fromdate)
        geojson_url=geojson_url+"?issueddate=" + testagain + "T00:00:00.000" # This works! (passing into javascript)
        geojson_url="https://data.calgary.ca/resource/c2es-76ed.geojson?$where=issueddate between'"
        geojson_url= geojson_url+ fromdate + "'and '" + todate + "'"


        requeststring=geojson_url + "?$where=issueddate > '2020-01-21' and issueddate < '2020-01-23'"
        requeststring=str(requeststring)
        requeststring="https://data.calgary.ca/resource/c2es-76ed.geojson?$where=issueddate > '2020-01-21' and issueddate < '2020-01-23'"

        res = requests.get("https://data.calgary.ca/resource/c2es-76ed.geojson",\
            params={"$where": "issueddate between '2020-01-21'"+" and "+"'2020-01-23'"})
        gsdata=res.json()
        
        f = open("demofile2.geojson", "w")
        f.write(json.dumps(gsdata))
        f.close()
        
        if res.status_code==200:
            js_data=res.json()
        else:
            js_data=""

        return render_template("index.html", add=geojson_url, fromdate=fromdate, todate=todate)
        
    return render_template("index.html", add=geojson_url)