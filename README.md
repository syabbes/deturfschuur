# Web application for 'De Turfschuur'
#### Video Demo:  <URL HERE>
## Description:
My name is Simon, I'm from the Netherlands and this is a web application I made as a solution for the final project of the CS50 course. The assignment was that "you build something of interest to you, that you solve an actual problem, that you impact your community, or that you change the world".
I decided to help out my community. In my neighbourhoud is a building which is being used for room rental and i noticed that it took quite some time for them to make all the invoices. First i wanted to solve just that problem, but ended up making a whole calendar and address database too.

In my code i'm switching between Dutch and English. Some basic translations are at [the end of the README](#translations). And please don't mind my english.

## Explanation of the files
### `app.py`:
This is the the main program. This contains the Flask application and all the other backend logic such as updating the database and generating invoices. I moved a few functions to another file: `helpers.py`.
As you can see I've used some third-party libraries such as:
- `CS50 Library for python` (For updating the database).
- `Python-docx` (For opening the template and generating invoices).
- `Email-validator` (Used for checking the users email input).

I Also use libraries such as `Werkzeug`, `OS`, `Datetime` and `ZipFile`. Those are either a dependency to make other libraries work or built in Python-libraries for calculating with datetimes or saving/modifying files.

### `turfschuur.db`:
This is the database in which the appointments and addresses are stored. The database is made with `SQLite3`. It contains four tables (the standard `sqlite_sequence` table not included): `adressenbestand` (En: address database), `afspraken` (En: appointments), `bestuursleden` (En: board members) and `facturen` (En: invoices).

Every appointment contains a `reeks_id` field and `adres_id` field. If the appointment is repeated, all the appointments in sequence get the same `reeks_id`, so that the appointments are linked together.
The `adres_id` is a foreign key to link an appointment to a name in the address database. It's also possible to have a nameless appointment in which `adres_id` is set to NULL.

The Dutch law requires that every invoice number needs to be sequentially incremented. To keep track of those numbers, the `facturen` (En: invoices) table is addded. then inside `app.py`, there's a query for the highest number using the `MAX()` function of SQLite. Every invoice also has the foreign key `adres_id` for linking the invoice with a specific person.

Inside `bestuursleden` the username, email and password of every board member is stored. The password is hashed using the `Werkzeug` library.
An important note: every board member has a field called `toegelaten` (En: permitted). A member can only login if his/her status is set to 1 which means that he/she is permitted to login. Standard the field will be 0, but another board member can set it to 1 if he/she trusts the person.

The `adressenbestand` (address database) contains things like initials, surname, address and country.

### `template/`:
Inside this folder are all of the html pages. There are two layouts: `layout.html` and `layout_bestuur.html`. the latter is for the board members since the menu looks a little different for them than for normal website visitors.

All the files are checked by W3CValidator and most of the errors/warnings are removed. there are a few exceptions. The month input field on `factuur.html` has a placeholder to show the user that the correct format is YYYY-MM. For browsers such as chrome this isn't neccesary because the input field is very user-friendly there (You can type in the month in your own language for example). This however isn't the case for other browsers such as Firefox as they appear complete empty. I used the placeholder for these browsers to show the correct format. Now does W3CValidator say that a placeholder isn't valid on input type Month, but as I explained, I ignored this error on purpose and it renders correctly on the browsers.

Another thing is a width value i set to a percentage. This is not valid syntax and you must use pixels. However, every browser seems to render it correctly and I wanted a percentage value based on the width of the screen.

Then all the other pages are linked to the layouts using Jinja2. The following code is an example (code based on CS50 Finance problem set):

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

#### `styles.css`:
This contains all of the websites styling. You will see that the first lines are comments containing hex colour codes. Those colours are the five main colours of the websites brand identity. For other styling i used the `Bootstrap` library.

### `facturen/`:
In this folder will the template for the invoices and the zip file containing the generated invoices be saved. Inside `generated/` will the generated invoices be saved.