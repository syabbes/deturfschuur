import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta, datetime
from helpers import login_required
from email_validator import validate_email, EmailNotValidError
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

# configure database connection
db = SQL("sqlite:///turfschuur.db")
db.execute("PRAGMA foreign_keys = ON")


# home
@app.route("/")
def index():
    # TODO
    return render_template("index.html")

# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        # check if user is already logged in
        if session.get("user_id") is not None:
            return redirect("/dashboard")
        return render_template("login.html")
    else:
        # TODO
        if not request.form.get("name"):
            return render_template("apology.html", apology="Naam is niet ingevuld"), 400
        if not request.form.get("password"):
            return render_template("apology.html", apology="Wachtwoord is niet ingevuld"), 400
        
        # query database for name
        rows = db.execute(
            "SELECT * FROM bestuursleden WHERE naam = ?", request.form.get("name")
        )

        # check if name and password are correct and if he/she is an approved board member
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")) or rows[0]["toegelaten"] < 1:
            return render_template("apology.html", apology="Inloggen mislukt"), 400
        
        # if everything is correct, store id inside session
        session["user_id"] = rows[0]["bestuurslid_id"]
        return redirect("/dashboard")
    
# register for an account
@app.route("/registreren", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("registreren.html")
    else:
        # TODO
        if not request.form.get("name"):
            return render_template("apology.html", apology="Geen naam ingevuld")
        if not request.form.get("email"):
            return render_template("apology.html", apology="E-mailadres niet ingevuld")
        # Check if the email is valid
        try:
            v = validate_email(request.form.get("email"))
            # use normalized form of emailadress
            email = v["email"]
        except EmailNotValidError as e:
            return render_template("apology.html", apology="E-mailadres wordt niet herkend")
        # check if password and password-repeat are the same
        if not request.form.get("password") == request.form.get("password_repeat"):
            return render_template("apology.html", apology="Wachtwoorden komen niet overeen")
        
        # update database with new user
        # "toegelaten" must be set to zero (also happens automatically if no value is specified), as you dont want anyone being able to register
        try:
            db.execute(
                """INSERT INTO bestuursleden
                (naam, email, hash, toegelaten)
                VALUES (?, ?, ?, ?)""",
                request.form.get("name"), request.form.get("email"), generate_password_hash(request.form.get("password")), 0
            )
        except:
            return render_template("apology.html", apology="Naam of e-mailadres is al in gebruik")
        # If user is registered, show a page with explaination that another member has to accept him/her
        return render_template("succes.html")
    
# dashboard for members
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "GET":
        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        cal = calendar.HTMLCalendar(firstweekday=0)
        month_calendar = cal.formatmonth(current_year, current_month)

        return render_template("dashboard.html", calendar=month_calendar)