# GLOBALS

# import
from flask import Flask, render_template, request, session, url_for, redirect
from auth import bp as auth_bp
import sqlite3, os

# Flask app creation
app = Flask(__name__)
app.register_blueprint(auth_bp)
app.secret_key = os.urandom(24)

# db cursor
DB_FILE = "Lebron.db"
db = sqlite3.connect(DB_FILE)
cursor = db.cursor()

# db - table creation
cursor.execute(
    f"create table if not exists users (username text primary key unique, password text)"
)  # creates the [users] table, with columns: [unique primary key]-[username] and [password]
cursor.execute(
    f"create table if not exists teams (teamuser text references users(username), teamslot1 integer references chars(id), teamslot2 integer references chars(id), teamslot3 integer references chars(id))"
)
# ^ creates the [teams] table, with columns [foreign key [username] from users table]-[teamuser], [foreign key [id] from chars table]-[teamslot1, 2, 3]
# teamuser is taken from a username in the users table and is the name of the user that owns/made the team, the teamslots 1-3 is made to link a pokemon/digimon/yugioh monster from the chars table by id
cursor.execute(
    f"create table if not exists chars (charname text, imagelink text, id integer primary key, type text, attack integer, hp integer, genre text)"
)
# ^ creates the [chars] table, with columns [charactername], [imagelink] (just a link to the image URL), [primary key]-[id], [type], [attack], [hp], [genre]
# DEVNOTE - CREATE A WAY TO COUNT IDS SO THERES NO OVERLAP WITH ID NUMBERS


# --------------------------------------------------------------------------
# CODE


# Flask commands
@app.route("/")
def disp_homepage():
    # we dont have a proper session username set up so this is used for testing !!
    # session['username'] = "bronbron"
    if session.get("username"):
        return render_template("homepage.html")
    else:
        return redirect(url_for("auth.login_get"))

@app.route("/roster")
def disp_roster():
    if session.get("username"):
        return render_template("roster.html") 
    else:
        return redirect(url_for("auth.login_get"))


# QoL db commands
def accessitem(
    tablename, columnname
):  # accesses "columnname" from a chosen "tablename" in db
    cursor.execute(
        f"Select" + columnname + "from" + tablename
    )  # input: select [__COLUMNNAME__] from [__TABLENAME__]


def accessitem_s(
    tablename, columnname, itemname
):  # accesses a single item from a given column
    cursor.execute(
        f"Select * from" + tablename + "where" + columnname + "= '" + itemname + "'"
    )  # input: select * from [__TABLENAME__] where [__COLUMNNAME__] = '[__ITEMNAME__]'


def accessitem_s_m(
    tablename, columnname1, itemname1, columnname2, itemname2
):  # accesses a single item from a given column
    cursor.execute(
        f"Select * from"
        + tablename
        + "where"
        + columnname
        + "= '"
        + itemname
        + "' and "
        + columnname2
        + "= '"
        + itemname2
        + "')"
    )  # input: select * from [__TABLENAME__] where [__COLUMNNAME__] = '[__ITEMNAME__]'


def accessitem_m(
    tablename, columnname, itemarray
):  # accesses any item from the itemarray in a given column

    for (
        item
    ) in itemarray:  # adds [']s to each item in itemarray to make it readable by sqlite
        item = "'" + item + "'"

    items = ", ".join(
        map(str, itemarray)
    )  # removes the brackets from itemarray to make items readable by sqlite

    cursor.execute(
        f"Select * from" + tablename + "where" + columnname + "in (" + items + ")"
    )  # input: select * from [__TABLENAME__] where [__COLUMNNAME__] in [__ITEMS__]


# --------------------------------------------------------------------------
# TESTS


if __name__ == "__main__":
    app.debug = True
    app.run()
