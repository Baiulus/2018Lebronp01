

# import
from flask import Flask, render_template, request, session, url_for, redirect, flash
from auth import bp as auth_bp
import sqlite3, os, random
import build_db
from showdown_character import showdowner

# Flask app creation
app = Flask(__name__)
app.register_blueprint(auth_bp)
app.secret_key = os.urandom(24)

# db cursor
DB_FILE = "Lebron.db"
db = sqlite3.connect(DB_FILE)
cursor = db.cursor()

# dummy characters to add into table to test formatting on website, leave this pls tyty
cursor.execute("""insert or ignore into chars
    (charname,
    imagelink,
    id,
    type,
    atk,
    hp,
    universe)
    values
    ('Lebron James',
    'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pngall.com%2Fwp-content%2Fuploads%2F12%2FLebron-James-Basketball-Player-PNG-Free-Image.png&f=1&nofb=1&ipt=023cda4e59b314393a042362367eff50c06dbad8dd6b2240e63ec9a92ea454aa',
    23,
    'Cavs',
    500,
    1000,
    'NBA')""")

cursor.execute("""insert or ignore into chars
    (charname,
    imagelink,
    id,
    type,
    atk,
    hp,
    universe)
    values
    ('Luka Doncic',
    'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fathlonsports.com%2F.image%2Far_8%3A10%252Cc_fill%252Ccs_srgb%252Cfl_progressive%252Cg_faces%3Acenter%252Cq_auto%3Agood%252Cw_620%2FMjE0NDY3ODg1NDUwNDA0ODg3%2Fluka-doncic.jpg&f=1&nofb=1&ipt=fd1f2789c9a64264dbda4d835fafd7fefe4c5b12fe01dcd9d6ed2044484cf8d5',
    77,
    'Lakers',
    500,
    1000,
    'NBA')""")

cursor.execute("""insert or ignore into chars
    (charname,
    imagelink,
    id,
    type,
    atk,
    hp,
    universe)
    values
    ('Jalen Brunson',
    'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flivesport-ott-images.ssl.cdn.cra.cz%2Fr900xfq60%2F29d1f8e5-186f-4e21-a601-b4341a35f804.jpeg&f=1&nofb=1&ipt=0f88ae2fddf4ca6929075c5deb8447cc6a60e9fde1fdac35ca5eed1a2f089fec',
    11,
    'Knicks',
    500,
    1000,
    'NBA')""")

# ^ creates the [chars] table, with columns [charactername], [imagelink] (just a link to the image URL), [primary key]-[id], [type], [atk], [hp], [universe]
# DEVNOTE - CREATE A WAY TO COUNT IDS SO THERES NO OVERLAP WITH ID NUMBERS


# --------------------------------------------------------------------------

# Flask commands
@app.route("/")
def disp_homepage():
    if session.get("username"):
        return render_template("homepage.html")
    else:
        session['username'] = 'a'
        return redirect(url_for("auth.login_get"))

@app.route("/roster")
def disp_roster():
    if session.get("username"):
        filter = request.args.get("filter", "all")
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        #Yu-Gi-Oh! API
        # for i in range(5): #adds 5 random Yu-Gi-Oh! cards to the table
        #     data = build_db.get_yugiohcard()
        #     c.execute(
        #         "insert into chars (charname, imagelink, id, type, atk, hp, universe) values (?, ?, ?, ?, ?, ?, ?)",
        #         (data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        #     )
        # db.commit()
        lists = []
        if (filter == 'all'):
            chars = c.execute("select * from chars")
        else:
            chars = c.execute("select * from chars where universe = ?", (filter, ))
        for char in chars:
            temp = [char[0], char[1], char[2], char[3], char[4], char[5], char[6]]
            lists.append(temp)
        return render_template("roster.html", lists = lists)
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/teamselect", methods = ['GET', 'POST'])
def disp_teamselect():
    if session.get("username"):
        if (request.method == 'POST'):
            selected = request.form.getlist("team")
            if (len(selected) != 3):
                flash("Please select exactly 3 team members.")
                return(redirect(url_for('disp_teamselect')))
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute("insert into teams (teamuser, teamslot1, teamslot2, teamslot3) values(?, ?, ?, ?)", (session.get('username'), selected[0], selected[1], selected[2]))
            db.commit()
            db.close()
            return redirect(url_for('disp_showdownselect'))
        else:
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            filter = request.args.get("filter", "all")
            lists = []
            if (filter == 'all'):
                chars = c.execute("select * from chars")
            else:
                chars = c.execute("select * from chars where universe = ?", (filter,))
            for char in chars:
                temp = [char[0], char[1], char[2]]
                lists.append(temp)
            db.close()
            return render_template("teamselect.html", lists = lists)
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/viewteam", methods = ['GET', 'POST'])
def disp_viewteam():
    if session.get("username"):
        filter = request.args.get("filter", "all")
        lists = []
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        if (filter == 'all'):
            teams = c.execute("select * from teams")
        else:
            teams = c.execute("select * from teams where teamuser = ?", (session.get('username'),))
        for team in teams:
            temp = [team[0]]
            chars = [team[1], team[2], team[3]]
            db2 = sqlite3.connect(DB_FILE)
            c2 = db.cursor()
            for char in chars:
                c2.execute("select charname from chars where id = ?", (char,))
                name = c2.fetchone()[0]
                temp.append(name)
            db2.close()
            temp.append(team[4])
            lists.append(temp)
        db.close()
        return render_template("viewteam.html", lists = lists)
    else:
        return redirect(url_for("auth.login_get"))

@app.route("/deleteteam", methods = ['GET', 'POST'])
def delteteam():
    if session.get('username'):
        id = request.form.get('id')
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute("delete from teams where teamid = ? and teamuser = ?", (id, session.get('username')))
        db.commit()
        db.close()
        return redirect(url_for("disp_viewteam"))
    else:
        return redirect(url_for("auth.login_get"))

@app.route("/showdownselect", methods = ['GET', 'POST'])
def disp_showdownselect():
    if session.get("username"):
        if (request.method == 'POST'):
            selected = request.form.getlist("team")
            if (len(selected) != 2):
                flash("Please select exactly 2 teams")
                return redirect(url_for('disp_showdownselect'))
            team1 = selected[0]
            team2 = selected[1]
            return redirect(url_for('setup_teams', team1 = team1, team2 = team2))
        else:
            filter = request.args.get("filter", "all")
            lists = []
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            if (filter == 'all'):
                teams = c.execute("select * from teams")
            else:
                teams = c.execute("select * from teams where teamuser = ?", (session.get('username'),))
            for team in teams:
                temp = [team[0]]
                chars = [team[1], team[2], team[3]]
                db2 = sqlite3.connect(DB_FILE)
                c2 = db.cursor()
                for char in chars:
                    c2.execute("select charname from chars where id = ?", (char,))
                    name = c2.fetchone()[0]
                    temp.append(name)
                db2.close()
                temp.append(team[4])
                lists.append(temp)
            db.close()
            db.close()
            return render_template("showdownselect.html", lists = lists)
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/setup")
def setup_teams():
    if session.get("username"):
        team1_id = request.args.get("team1")
        team2_id = request.args.get("team2")
        team1 = []
        team2 = []
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        c.execute("select * from teams where teamid = ?", (team1_id,))
        temp1 = c.fetchone()
        team1_ids = [temp1[1], temp1[2], temp1[3]]
        for id in team1_ids:
            c2 = db.cursor()
            c2.execute("select * from chars where id = ?", (id,))
            char = c2.fetchone()
            temp = showdowner(char[0], char[1], char[4], char[5])
            team1.append(temp.to_dict())

        c.execute("select * from teams where teamid = ?", (team2_id,))
        temp2 = c.fetchone()
        team2_ids = [temp2[1], temp2[2], temp2[3]]
        for id in team2_ids:
            c2 = db.cursor()
            c2.execute("select * from chars where id = ?", (id,))
            char = c2.fetchone()
            temp = showdowner(char[0], char[1], char[4], char[5])
            team2.append(temp.to_dict())

        session['team1'] = team1
        session['team2'] = team2
        db.close()
        return redirect(url_for("disp_showdown"))
    else:
        return redirect(url_for("auth.login_get"))

@app.route("/showdown")
def disp_showdown():
    if session.get("username"):
        team1 = session.get('team1')
        team2 = session.get('team2')
        team1_messages = []
        team2_messages = []
        
        for i in range(len(team1)):
            member = showdowner.from_dict(team1[i])
            if (member.hp > 0):
                team1[i] = member
            else:
                team1.pop(i)

        for i in range(len(team2)):
            member = showdowner.from_dict(team2[i])
            if (member.hp > 0):
                team1[i] = member
            else:
                team1.pop(i)

        t1m1_attack = random.randint(0, len(team2) - 1)
        print(t1m1_attack)
        team1[0].attack(team2[t1m1_attack])
        team1_messages.append(f"{team1[0].name} attacked {team2[t1m1_attack].name}!")
        session['team1'] = [member.to_dict() for member in team1]
        session['team2'] = [member.to_dict() for member in team2]
        return render_template("showdown.html", team1 = team1, team2 = team2, team1_messages = team1_messages, team2_messages = team2_messages)
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
