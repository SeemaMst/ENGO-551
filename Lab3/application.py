import os
import requests
import geojson as gpd 

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker

from datetime import datetime

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Landing page - Website login
@app.route("/", methods=["POST", "GET"])
def login():
    geojson_url="https://data.calgary.ca/resource/c2es-76ed.geojson"

    if request.method=="POST":
        teststring = request.form.get("daterange")
        splitstring = teststring.split()
        startdate = splitstring[0]
        enddate = splitstring[2]
        startdatesplit=startdate.split("/")
        enddatesplit=enddate.split("/")
        startdate = startdatesplit[2] + "-" + startdatesplit[0] + "-" + startdatesplit[1]
        enddate = enddatesplit[2] + "-" + enddatesplit[0] + "-" + enddatesplit[1]
        print(startdate, enddate)
       
        geojson_url="https://data.calgary.ca/resource/c2es-76ed.geojson?$where=issueddate between'"
        geojson_url= geojson_url+ startdate + "'and '" + enddate + "'"

        return render_template("index.html", add=geojson_url, teststring=teststring) # , add=geojson_url, fromdate=fromdate, todate=todate)
        
    return render_template("index.html", add=geojson_url)