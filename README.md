# Web application for 'De Turfschuur'
#### Video Demo:  <https://youtu.be/8-Vm3p2q0Sg>
## Description:
My name is Simon, I'm from the Netherlands and this is a web application I made as a solution for the final project of the CS50 course. The assignment was that "you build something of interest to you, that you solve an actual problem, that you impact your community, or that you change the world".
I decided to help out my community. In my neighbourhoud is a building which is being used for room rental and i noticed that it took quite some time for them to make all the invoices. First i wanted to solve just that problem, but ended up making a whole calendar and address database too.

> [!NOTE]
In my code i'm switching between Dutch and English. Some basic translations are at [the end of the README](#translations). And please don't mind my english.

## Explanation of the files
### `app.py`:
This is the the main program. This contains the Flask application and all the other backend logic such as updating the database and generating invoices. I moved a few functions to another file: `helpers.py`.
As you can see I've used some third-party libraries such as:
- `CS50 Library for python` (For updating the database).
- `Python-docx` (For opening the template and generating invoices).
- `Email-validator` (Used for checking the users email input).

I 've also used libraries such as `Werkzeug`, `OS`, `Datetime` and `ZipFile`. Those are either a dependency to make other libraries work or built in Python-libraries for calculating with datetimes or saving/modifying files.

### `turfschuur.db`:
This is the database in which the appointments and addresses are stored. The database is made with `SQLite3`. It contains four tables (the standard `sqlite_sequence` table not included): `adressenbestand` (En: address database), `afspraken` (En: appointments), `bestuursleden` (En: board members) and `facturen` (En: invoices).

Every appointment contains a `reeks_id` field and `adres_id` field. If the appointment is repeated, all the appointments in sequence get the same `reeks_id`, so that the appointments are linked together.
The `adres_id` is a foreign key to link an appointment to a name in the address database. It's also possible to have a nameless appointment in which `adres_id` is set to NULL.

The Dutch law requires that every invoice number needs to be sequentially incremented. To keep track of those numbers, the `facturen` (En: invoices) table is addded. Then inside `app.py`, there's a query for the highest number using the `MAX()` function of SQLite. Every invoice also has the foreign key `adres_id` for linking the invoice with a specific person.

Inside `bestuursleden` the username, email and password of every board member is stored. The password is hashed using the `Werkzeug` library.
An important note: every board member has a field called `toegelaten` (En: permitted). A member can only login if his/her status is set to 1 which means that he/she is permitted to login. Standard the field will be 0, but another board member can set it to 1 if he/she trusts the person.

The `adressenbestand` (address database) contains things like initials, surname, address and country.

### `template/`:
Inside this folder are all of the html pages. There are two layouts: `layout.html` and `layout_bestuur.html`. The latter is for the board members since the menu looks a little different for them than for normal website visitors.

All the files are checked by W3CValidator and most of the errors/warnings are removed. There are a few exceptions. The month input field on `factuur.html` has a placeholder to show the user that the correct format is YYYY-MM. For browsers such as chrome this isn't neccesary because the input field is very user-friendly there (you can type in the month in your own language for example). This however isn't the case for other browsers such as Firefox as they appear completely empty. I used the placeholder for these browsers to show the correct format. Now does W3CValidator say that a placeholder isn't valid on input type Month, but as I explained, I ignored this error on purpose and it renders correctly on the browsers.

Another thing is a width value I set to a percentage. This is not valid syntax and you must use pixels. However, every browser seems to render it correctly and I wanted a percentage value based on the width of the screen.

Then all the other pages are linked to the layouts using Jinja. The following code is an example (code based on CS50 Finance problem set):

```Jinja
{% extends "layout.html" %}

{% block title %}
    De Turfschuur | Example
{% endblock %}

{% block main %}
{% endblock %}
```

There's also a `apology.html` file which is used for showing error messages to the user. The backend can yield an error like:
```Python
import flask

@app.route("/")
def index():
    return render_template("apology.html", apology="Example error message"), 400 # HTTP error code
```

### `static/`:
This folder contains some graphics as well as the `script.js` and `styles.css`. Most of the graphics are made by myself except for the Garfield image, which i got from the following website:
[https://pngimg.com/image/109393](https://pngimg.com/image/109393).

#### `script.js`:
This contains all of the JavaScript functions for generating the calendar and sending the AJAX requests. For stuff like AJAX requests, the `JQuery` library is used.

I had a little dillema whether the calendar had to be generated server side or client side. I ended up generating it client side and sending AJAX requests back to the server to get every appointment. The `generate_calendar()` function does the work of generating the calendar. With `get_appointments()` the appointments are being requested via AJAX and then displayed onto the calendar with a little circle with the number of apppointments on that day. The upside for generating it server-side was that Python has a function built in which generates a calendar automatically and the appointments could've been send with it immediately. However, I thought this would probably put a lot of stress on the server, and it wouldn’t feel as interactive as using JavaScript (since a full page reload would be required). 

#### `styles.css`:
This contains all of the websites styling. You will see that the first lines are comments containing hex colour codes. Those colours are the five main colours of the websites brand identity. For other styling i used the `Bootstrap` library.

### `facturen/`:
In this folder will the template for the invoices and the zip file containing the generated invoices be saved. Inside `generated/` will the generated invoices be saved.

### Other files:
Those are either for testing or notes to myself. Not important.
> [!IMPORTANT]
The `requirements.txt` file **is** important. That file you use for installing the dependencies.

## Try out
While this code isn't meant to be cloned and installed, you're welcome to try out the prototype website. Here are the instructions.

Clone the repository.
```bash
git clone https://github.com/syabbes/deturfschuur.git
```

Go to the folder.
```bash
cd deturfschuur
```

Make and activate a virtual environment.
```bash
python -m venv venv
source venv/bin/activate # MacOS/Linux
venv\Scripts\Activate # Windows
```

Install dependencies.
```bash
pip install -r requirements.txt
```

Run the website.
```bash
flask run
```
Go into your favourite browser and type the following link:
http://127.0.0.1:5000.

### Test board member
Now you might want to test the dashboard for the board members. To do that, you must mark yourself as 'permitted' in the database. The easiest way is to sign up via the website. Then change the `toegelaten` field in the database.

open SQLite3 in a new terminal in the same directory.
```bash
sqlite3 turfschuur.db
```

Then execute the following SQLite query:
```sql
UPDATE bestuursleden
SET toegelaten = 1
WHERE email = [your email] AND naam = [your name];
```

Make sure to replace `[your email]` with the email you have used when signing up and replace `[your name]` with the username you typed in.

## Future improvements
As much as I wished that my prototype is perfect, it unfortunately isn't :). Here are some ways i might expand and improve the website.

- Fixing clicking on appointments-indicator.
Right now, when you click on the circle that indicates that there is an appointment, the computer thinks you're clicking on the date january 1st 1970. It would be nice if it would just show the appointments.

- Adding the ability to update people in the address database. Right now when someone gets a new address, the old one has to be removed and then a new one can be added. The ability to update would make this process easier.

- Adding a search function for all the appointments would be really cool and would come in handy.

## Sources

### Documentation & Tutorials
- [W3Schools](https://www.w3schools.com/)
- [GeeksforGeeks](https://www.geeksforgeeks.org/)
- [Stack Overflow](https://stackoverflow.com/questions)
- [Reddit](https://www.reddit.com/)
- [Python documentation](https://docs.python.org/3/library/functions.html)
- [Flask documentation](https://flask.palletsprojects.com/en/stable/)
- [Jinja documentation](https://jinja.palletsprojects.com/en/stable/)
- [MDN Web Docs documentation](https://developer.mozilla.org/en-US/)
- [Bootstrap 5 documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [SQLite documentation](https://sqlite.org/index.html)
- [python-docx documentation](https://python-docx.readthedocs.io/en/latest/)
- [python-email-validator documentation](https://github.com/JoshData/python-email-validator)
- [CS50 Python documentation](https://cs50.readthedocs.io/libraries/cs50/python/?highlight=sql#cs50.SQL)

### AI Tools
I also used AI which i found really helpful for debugging and other purposes. However, I never copied full code directly from those sources.
- [CS50 Duck Debugger](https://cs50.ai/chat)
- [ChatGPT](https://chatgpt.com)

### Design Resources
- [Google Fonts](https://fonts.google.com/)
- [Garfield Image (pngimg.com)](https://pngimg.com/image/109393) 

The remaining design is made by myself.


## Translations
Here you might find some useful translations to understand the website better.

Naam <---> Name

Wachtwoord <---> Password

Facturering <---> Invoicing

Adressenbestand <---> Address database

Bestuursleden <---> Board members

Nieuwe afspraak <---> New appointment

Titel <---> Title

Begin <---> Start

Eind <---> End

Prijs <---> Price

Omschrijving <---> Description

Wordt herhaald om zoveel weken <---> Repeats every so many weeks

Wordt zoveel keer herhaald <---> Is repeated so many times

Adres <---> Address

Voorletters <---> Initials

Achternaam <---> Surname

Straat <---> Street

Postcode <---> Zip code

Woonplaats <---> Place

Land <---> Country

Overige informatie <---> Extra info

Opslaan <---> Save

Bijwerken <---> Update

Verwijderen <---> Delete

Welke afspraken moeten worden bijgewerkt/verwijderd? <---> Which appointments need to be updated/deleted?

Allemaal <---> All

Alleen deze <---> Only this one

Upload hieronder een factuur-template (".docx" formaat). Als u er geen upload wordt het meest recente template gebruikt. <---> Upload an invoice template (.docx) below. If you don't upload one, the most recent template will be used.

Selecteer maand <---> Select month

Genereer facturen <---> generate invoices

Er is een verzoek gestuurd naar de bestuursleden om uw account aan te maken. Als uw account is goedgekeurd, kunt u een bericht verwachten van een van onze bestuursleden. <---> A request has been sent to the board members to create your account. If your account is approved, you can expect a message from one of our board members.
