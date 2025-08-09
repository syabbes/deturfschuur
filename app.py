from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta, datetime
from helpers import login_required, add_app
from email_validator import validate_email, EmailNotValidError
import re

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
        return render_template("dashboard.html")
    # post for posting appointments
    else:
        # Check if the form has an input field called flag
        flag = request.form.get("updatedelete-flag")
        print(f"flag: {flag}")
        if flag is not None:
            # Handle the update/delete appointment form
            # Update alle = 0
            # Update enkele = 1
            # Verwijder alle = 2
            # Verwijder enkele = 3

            # Get all info
            id = request.form.get("id")
            titel = request.form.get("app-titel")
            begin = datetime.strptime(request.form.get("app-begin"), "%Y-%m-%dT%H:%M")
            eind = datetime.strptime(request.form.get("app-eind"), "%Y-%m-%dT%H:%M")
            prijs = request.form.get("app-prijs")
            info = request.form.get("app-info")
            if not titel or not begin or not eind:
                return render_template("apology.html", apology="Afspraak moet minstens een titel, begin- en eindtijd bevatten")
            if eind <= begin:
                return render_template("apology.html", apology="Eindtijd moet later dan begintijd zijn")
            if ((eind - begin) >= timedelta(days=1)):
                return render_template("apology.html", apology="Afspraak duurt te lang")
            
            # Switch case for the different cases like updating/deleting and all/single
            match int(flag):
                case 0:
                    # Update all
                    # Select all targeted appointments
                    appointments = db.execute("""SELECT afspraak_id, begin, eind
                                              FROM afspraken
                                              WHERE reeks_id = (
                                              SELECT reeks_id
                                              FROM afspraken
                                              WHERE afspraak_id = ?
                                              )""", id)
                    if len(appointments) <= 0:
                        appointments = [{"afspraak_id": id}]
                    
                    print(appointments)
                    # Calculate time difference
                    # Get correct appointment for comparing
                    right_app_time = db.execute("""SELECT begin, eind
                                                FROM afspraken WHERE afspraak_id = ?""", id)
                    original_begin = datetime.fromisoformat(right_app_time[0]["begin"])
                    original_end = datetime.fromisoformat(right_app_time[0]["eind"])
                    timediff_begin = begin - original_begin
                    timediff_eind = eind - original_end
                    # For every appointment in the series, update everything
                    for app in appointments:
                        # Calculate the new datetimes
                        new_begin = datetime.fromisoformat(app["begin"]) + timediff_begin
                        new_eind = datetime.fromisoformat(app["eind"]) + timediff_eind
                        db.execute("""UPDATE afspraken
                                   SET titel = ?, begin = ?, eind = ?, prijs = ?, info = ?
                                   WHERE afspraak_id = ?""", titel, new_begin.isoformat(), new_eind.isoformat(), prijs, info, app["afspraak_id"])
                case 1:
                    # Update single
                    return render_template("apology.html", apology="Nog niet geimplementeerd")
                case 2:
                    # Delete all
                    return render_template("apology.html", apology="Nog niet geimplementeerd")
                case 3:
                    # Delete single
                    return render_template("apology.html", apology="Nog niet geimplementeerd")
                case _:
                    return render_template("apology.html", apology="Gelieve niet aan de code lopen prutsen")

            return redirect("/dashboard")



        if not request.form.get("titel") or not request.form.get("begin") or not request.form.get("einde"):
            return render_template("apology.html", apology="Minstens een titel, begin- en eindtijd instellen")
        # check if end time is later than begin time
        begintijd = datetime.strptime(request.form.get("begin"), "%Y-%m-%dT%H:%M")
        eindtijd = datetime.strptime(request.form.get("einde"), "%Y-%m-%dT%H:%M")
        if eindtijd <= begintijd:
            return render_template("apology.html", apology="Eindtijd moet later dan begintijd zijn")
        if ((eindtijd - begintijd) >= timedelta(days=1)):
            return render_template("apology.html", apology="Afspraak duurt te lang")
        
        titel = request.form.get("titel").strip()
        prijs = float(request.form.get("prijs"))
        contact = request.form.get("contactgegevens").strip()
        info = request.form.get("info").strip()
        
        vl_raw = request.form.get("voorletter")
        if vl_raw is None:
            vl = None
        else:
            # Get all of the letters
            letters = re.findall("[a-zA-Z]", vl_raw)
            # make everything uppercase and add a dot after every letter
            vl = ((".".join(letters)) + ".").upper()
        an = request.form.get("achternaam").upper().strip()
        
        straat = request.form.get("straat").lower().strip()
        if not straat:
            straat = None
        hn = request.form.get("huisnummer").lower().split()
        huisnummer = "".join(hn)
        if not huisnummer:
            huisnummer = None
        post = request.form.get("postcode").lower().split()
        postcode = "".join(post)
        if not postcode:
            postcode = None
        plaats = request.form.get("woonplaats").lower().strip()
        if not plaats:
            plaats = None
        land = request.form.get("land").lower().strip()
        if not land:
            land = "Nederland"

        repeat = request.form.get("interval")
        repeatx = request.form.get("reeks")

        # If address is filled in, check if the address/person is yet in the database
        if (an or vl) and postcode and huisnummer:
            # Check if initial or surname is empty
            if not an or not vl:
                return render_template("apology.html", apology="Moet zowel een voorletter als een achternaam zijn opgegeven om in het adressenbestand te zoeken")
            # Querie database for right address id
            adres_id = db.execute("""SELECT adres_id
                                    FROM adressenbestand
                                    WHERE voorletter = ? AND achternaam = ? AND postcode = ? AND huisnummer = ?""",
                                    vl, an, postcode, huisnummer)
            # If not, add new address/person to address table (fields cant be null)
            if len(adres_id) <= 0:
                try:
                    id = db.execute("""INSERT INTO adressenbestand
                                    (voorletter, achternaam, straat, huisnummer, woonplaats, land, postcode, contact)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                                    vl, an, straat, huisnummer, plaats, land, postcode, request.form.get("contactgegevens"))
                except ValueError:
                    return render_template("apology.html", apology="Niet alle benodigde gegevens zijn ingevuld")
                
                try:
                    add_app(titel, begintijd, eindtijd, prijs, info, id, repeat, repeatx)
                except ValueError:
                    return render_template("apology.html", apology="Ongeldige herhaling ingesteld")
            # Else if there's a name/address, add appointment with adres_id set to name/address
            else:
                try:
                    add_app(titel, begintijd, eindtijd, prijs, info, adres_id[0]["adres_id"], repeat, repeatx)
                except ValueError:
                    return render_template("apology.html", apology="Ongeldige herhaling ingesteld")
                
        # Else if address isnt filled in, just add appointment to database with the adres_id set to null
        else:
            try:
                add_app(titel, begintijd, eindtijd, prijs, info, None, repeat, repeatx)
            except ValueError:
                    return render_template("apology.html", apology="Ongeldige herhaling ingesteld")
        return redirect("/dashboard")

# Route for ajax calendar request
@app.route("/app_month", methods=["GET"])
@login_required
def get_appointments_month():
    # Get the month of which the appointments should be loaded
    month = request.args.get("month")
    year = request.args.get("year")
    mstring = str(month).zfill(2)
    myear = str(year)
    months = db.execute("""SELECT afspraak_id, begin, eind FROM afspraken
                        WHERE strftime('%m', begin) = ? AND strftime('%Y', begin) = ?
                        ORDER BY begin ASC""",
                        mstring, myear)
    return jsonify(months)

# Route for ajax request for appointments on a day
@app.route("/app_day", methods=["GET"])
@login_required
def get_appointments_day():
    # Get the day
    day_str = request.args.get("day")
    # If something went wrong with the ajax request, just return an empty list
    if day_str is None:
        jsonify([])
    day = datetime.strptime(day_str, '%a %b %d %Y')
    
    # Get end of day (or start new day)
    endday = day + timedelta(days=1)
    # Convert both back to iso 8601 format
    day.replace(microsecond=0).isoformat()
    endday.replace(microsecond=0).isoformat()
    print(f"day: {day} endday: {endday}")
    # Query database for every appointment where the starttime <= endday and endtime >= day
    day_appointments = db.execute("""SELECT afspraken.*, adressenbestand.adres_id, adressenbestand.voorletter, adressenbestand.achternaam
                                  FROM afspraken
                                  LEFT JOIN adressenbestand ON afspraken.adres_id = adressenbestand.adres_id
                                  WHERE begin <= ? AND eind >= ?""",
                                  endday, day)
    print(day_appointments)
    
    return jsonify(day_appointments)


