# GLOBALS

# import
from flask import Flask, render_template, request, session, url_for, redirect
from auth import bp as auth_bp
import sqlite3, os
import build_db

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

# dummy characters to add into table to test formatting on website, leave this pls tyty
cursor.execute("""insert or ignore into chars
    (charname,
    imagelink,
    id,
    type,
    attack,
    hp,
    genre)
    values
    ('Lebron James',
    'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pngall.com%2Fwp-content%2Fuploads%2F12%2FLebron-James-Basketball-Player-PNG-Free-Image.png&f=1&nofb=1&ipt=023cda4e59b314393a042362367eff50c06dbad8dd6b2240e63ec9a92ea454aa',
    23,
    'Cavs',
    1000,
    1000,
    'NBA')""")

cursor.execute("""insert or ignore into chars
    (charname,
    imagelink,
    id,
    type,
    attack,
    hp,
    genre)
    values
    ('Luka Doncic',
    'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fathlonsports.com%2F.image%2Far_8%3A10%252Cc_fill%252Ccs_srgb%252Cfl_progressive%252Cg_faces%3Acenter%252Cq_auto%3Agood%252Cw_620%2FMjE0NDY3ODg1NDUwNDA0ODg3%2Fluka-doncic.jpg&f=1&nofb=1&ipt=fd1f2789c9a64264dbda4d835fafd7fefe4c5b12fe01dcd9d6ed2044484cf8d5',
    77,
    'Lakers',
    7777,
    7777,
    'NBA')""")

# ^ creates the [chars] table, with columns [charactername], [imagelink] (just a link to the image URL), [primary key]-[id], [type], [attack], [hp], [genre]
# DEVNOTE - CREATE A WAY TO COUNT IDS SO THERES NO OVERLAP WITH ID NUMBERS


# --------------------------------------------------------------------------
# CODE


# Flask commands
@app.route("/")
def disp_homepage():
    if session.get("username"):
        return render_template("homepage.html")
    else:
        return redirect(url_for("auth.login_get"))

@app.route("/roster")
def disp_roster():
    if session.get("username"):
        filter = request.args.get("filter", "all")
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        #Yu-Gi-Oh! API
        # for i in range(1): #adds 5 random Yu-Gi-Oh! cards to the table
        #     data = build_db.get_yugiohcard()
        #     c.execute(
        #         "insert into chars (charname, imagelink, id, type, attack, hp, genre) values (?, ?, ?, ?, ?, ?, ?)",
        #         (data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        #     )
        # db.commit()

        lists = []
        if (filter == 'all'):
            chars = c.execute("select * from chars")
        else:
            chars = c.execute("select * from chars where genre = ?", (filter, ))
        for char in chars:
            temp = [char[0], char[1], char[2], char[3], char[4], char[5], char[6]]
            lists.append(temp)
        return render_template("roster.html", lists = lists)
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/teamselect")
def disp_teamselect():
    if session.get("username"):
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        # c.execute("insert or ignore into teams values (?, ?, ?, ?)", (session.get('username'), 23, 77, 75064463))
        filter = request.args.get("filter", "all")
        lists = []
        if (filter == 'all'):
            chars = c.execute("select * from chars")
        else:
            chars = c.execute("select * from chars where genre = ?", (filter, ))
        for char in chars:
            temp = [char[0], char[1], char[2]]
            lists.append(temp)
        return render_template("teamselect.html", lists = lists)
    else:
        return redirect(url_for("auth.login_get"))

db.commit()
db.close()

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

# build_db.db_insert(build_db.get_pokemon(151))

if __name__ == "__main__":
    app.debug = True
    app.run()
