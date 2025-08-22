from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime, timedelta, date
import uuid

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# functions
def add_app(titel, begin, eind, prijs, desc_prijs, extra, desc_extra, info, adres_id, interval, reeks):
    from app import db
    begindates = [begin]
    enddates = [eind]
    if int(reeks) > 0:
        # Yield error if repeat-values are incorrect
        if int(reeks) > 52 or int(interval) < 1 or int(interval) > 52:
            raise ValueError("Ongeldige herhaling ingesteld")
        
        #generate unique reeks_id
        id = uuid.uuid1().int * 4
        # Calculate next dates
        for i in range(int(reeks)):
            begindates.append(begindates[i] + timedelta(weeks=int(interval)))
            enddates.append(enddates[i] + timedelta(weeks=int(interval)))
        
        for b, e in zip(begindates, enddates):
            db.execute("""INSERT INTO afspraken
                        (titel, begin, eind, prijs, omschrijving_prijs, extra, omschrijving_extra, info, adres_id, reeks_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                        titel, b.isoformat(), e.isoformat(), prijs, desc_prijs, extra, desc_extra, info, adres_id, id)
    # If no repetition, just add one appointment with reeks_id set to NULL 
    else:
        db.execute("""INSERT INTO afspraken
                    (titel, begin, eind, prijs, omschrijving_prijs, extra, omschrijving_extra, info, adres_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    titel, begin.isoformat(), eind.isoformat(), prijs, desc_prijs, extra, desc_extra, info, adres_id)
        
# Function for searching for duplicates
def check_duplicate(start, end):
    # Based on the boolean algebra logic stated in the following Stack Overflow discussion:
    # https://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap#325964
    from app import db
    # Return every overlapping appointment
    apps = db.execute("""SELECT titel, strftime("%d-%m-%Y", begin) as n_begin
                      FROM afspraken
                      WHERE datetime(begin) <= ? AND datetime(eind) >= ?""", 
                      end.strftime("%Y-%m-%d %H:%M:%S"), start.strftime("%Y-%m-%d %H:%M:%S"))
    
    # The list isnt empty if a overlapping appointment is found
    if len(apps) > 0:
        m = "Conflict: "
        for app in apps:
            m = m + f" [{app['titel']} ({app['n_begin']})] "
        return m
    else:
        return False