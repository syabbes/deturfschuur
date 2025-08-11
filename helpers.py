from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime, timedelta
import uuid

print("helpers.py is being imported")

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
        print(id)
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