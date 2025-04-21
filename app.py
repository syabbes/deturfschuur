import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import timedelta
from helpers import login_required
import calendar

# Configure application
app = Flask(__name__)

#secret key
app.secret_key = b'\x07)\x11\x08\xc8Z|u`*\xefG#\x88>J\xb7\x12\xbe\x99[\xf7\x88+'

#configure session so users stay logged in for the duration of the browser
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# home
@app.route("/")
def index():
    # TODO
    return render_template("index.html")

# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # TODO
        return render_template("apology.html", apology="Dit is een work in progress")
    
# register for an account
@app.route("/registreren", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("registreren.html")
    else:
        # TODO
        # If user is registered, show a page with explaination that another member has to accept him/her
        return render_template("succes.html")
    
# dashboard for members
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.html")