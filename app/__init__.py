from flask import Flask, render_template, request, session, url_for, redirect, flash
from auth import bp as auth_bp
import sqlite3, os, random
import build_db
from showdown_character import showdowner

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.secret_key = os.urandom(24)

DB_FILE = "Lebron.db"
db = sqlite3.connect(DB_FILE)
cursor = db.cursor()

# Type advantage system 
def calculate_type_advantage(attacker_type, defender_type, move_type):
    # Simple type chart to expand
    type_chart = {
        "fire": {"water": 0.5, "grass": 2.0, "normal": 1.0},
        "water": {"fire": 2.0, "grass": 0.5, "normal": 1.0},
        "grass": {"water": 2.0, "fire": 0.5, "normal": 1.0},
        "electric": {"water": 2.0, "grass": 1.0, "normal": 1.0},
        "normal": {"normal": 1.0},
    }

    # Get multiplier, default to 1.0
    multiplier = type_chart.get(move_type, {}).get(defender_type, 1.0)

    # Same type attack bonus (STAB)
    if move_type == attacker_type:
        multiplier *= 1.0

    return multiplier


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
        cursor = db.cursor()
        lists = []
        
        if filter == "all":
            cursor.execute("SELECT * FROM chars")
        else:
            cursor.execute("SELECT * FROM chars WHERE universe = ?", (filter,))
        
        chars = cursor.fetchall()
        
        for char in chars:
            temp = [
                char[0],  # charname
                char[1],  # imagelink
                char[2],  # id
                char[3],  # type
                char[4],  # hp
                char[5],  # moves
                char[6]   # universe
            ]
            lists.append(temp)
        
        db.close()
        return render_template("roster.html", lists=lists)
    else:
        return redirect(url_for("auth.login_get"))

@app.route("/createteam", methods=["GET", "POST"])
def disp_createteam():
    if session.get("username"):
        if request.method == "POST":
            selected = request.form.getlist("team")
            if len(selected) != 3:
                flash("Please select exactly 3 team members.")
                return redirect(url_for("disp_createteam"))
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute(
                "insert into teams (teamuser, teamslot1, teamslot2, teamslot3) values(?, ?, ?, ?)",
                (session.get("username"), selected[0], selected[1], selected[2]),
            )
            db.commit()
            db.close()
            return redirect(url_for("disp_showdownselect"))
        else:
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            filter = request.args.get("filter", "all")
            lists = []
            if filter == "all":
                chars = c.execute("select * from chars")
            else:
                chars = c.execute("select * from chars where universe = ?", (filter,))
            for char in chars:
                temp = [char[0], char[1], char[2]]
                lists.append(temp)
            db.close()
            return render_template("createteam.html", lists=lists)
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/viewteam", methods=["GET", "POST"])
def disp_viewteam():
    if session.get("username"):
        filter = request.args.get("filter", "all")
        lists = []
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        if filter == "all":
            teams = c.execute("select * from teams")
        else:
            teams = c.execute(
                "select * from teams where teamuser = ?", (session.get("username"),)
            )
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
        return render_template("viewteam.html", lists=lists)
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/deleteteam", methods=["GET", "POST"])
def delteteam():
    if session.get("username"):
        id = request.form.get("id")
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute(
            "delete from teams where teamid = ? and teamuser = ?",
            (id, session.get("username")),
        )
        db.commit()
        db.close()
        return redirect(url_for("disp_viewteam"))
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/showdownselect", methods=["GET", "POST"])
def disp_showdownselect():
    if session.get("username"):
        if request.method == "POST":
            selected = request.form.getlist("team")
            type = request.form.get("type")
            print(selected)
            if len(selected) != 1:
                flash("Please select exactly 1 team", "error")
                return redirect(url_for("disp_showdownselect"))

            if type == "user":
                session["team1"] = selected[0]
                flash("Team selected. Please choose enemy team.", "success")
                return redirect(url_for("disp_showdownselect"))
            elif type == "enemy":
                if not (session.get("team1")):
                    flash("Select your team first.", "error")
                    return redirect(url_for("disp_showdownselect"))
                session["team2"] = selected[0]
                return redirect(url_for("setup_teams"))
        else:
            filter = request.args.get("filter", "all")
            lists = []
            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            if filter == "all":
                teams = c.execute("select * from teams")
            else:
                teams = c.execute(
                    "select * from teams where teamuser = ?", (session.get("username"),)
                )
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
            return render_template("showdownselect.html", lists=lists)
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/setup")
def setup_teams():
    if session.get("username"):
        team1 = []
        team2 = []
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        c.execute("select * from teams where teamid = ?", (session.get('team1'),))
        temp1 = c.fetchone()
        team1_ids = [temp1[1], temp1[2], temp1[3]]
        for id in team1_ids:
            c2 = db.cursor()
            c2.execute("select * from chars where id = ?", (id,))
            char = c2.fetchone()
            moves = [m.strip() for m in char[5].split(",")]
            if (char[6] == 'Yugioh'):
                hp = int(0.2 * char[4])
            else:
                hp = char[4]
            temp = showdowner(char[0], char[1], char[3], hp, moves, char[6])
            team1.append(temp.to_dict())

        c.execute("select * from teams where teamid = ?", (session.get('team2'),))
        temp2 = c.fetchone()
        team2_ids = [temp2[1], temp2[2], temp2[3]]
        for id in team2_ids:
            c2 = db.cursor()
            c2.execute("select * from chars where id = ?", (id,))
            char = c2.fetchone()
            moves = [m.strip() for m in char[5].split(",")]
            if (char[6] == 'Yugioh'):
                hp = int(0.2 * char[4])
            else:
                hp = char[4]
            temp = showdowner(char[0], char[1], char[3], hp, moves, char[6])
            team2.append(temp.to_dict())

        session['team1'] = team1
        session['team2'] = team2
        db.close()
        return redirect(url_for("disp_showdown"))
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/showdown", methods = ['GET', 'POST'])
def disp_showdown():
    if session.get("username"):
        team1 = [showdowner.from_dict(member) for member in session.get('team1')]
        team2 = [showdowner.from_dict(member) for member in session.get('team2')]

        team1_messages = []
        team2_messages = []

        user_attacked = False

        for i in range(len(team1)):
            target = request.form.get(f"target_{i}")
            attack = request.form.get(f"move_{i}")
            if target is None or attack is None:
                continue
            
            target = int(target)
            if (team1[i].universe == "Yugioh"):
                adjusted = int(0.02 * int(team1[i].moves[0]))
                team1[i].attack(team2[target], adjusted)
                team1_messages.append(f"{team1[i].name} attacked {team2[target].name} for {adjusted} damage!")
                continue

            db = sqlite3.connect(DB_FILE)
            c = db.cursor()
            c.execute("select * from moves where name = ?", (attack,))
            temp = c.fetchone()
            if temp is None:
                team1_messages.append(f"{team1[i].name}'s move failed!")
                continue

            # type, damage, accuracy, universe
            attributes = [temp[2], temp[3], temp[4], temp[5]]
            if (temp[2] is None or temp[3] is None or temp[4] is None or temp[5] is None):
                team1_messages.append(f"{team1[i].name}'s move failed!")
                continue

            if (random.randint(0, 100) < attributes[2]):
                team1[i].attack(team2[target], attributes[1])
                team1_messages.append(f"{team1[i].name} used {attack} on {team2[target].name} for {attributes[1]} damage!")
            else:
                team1_messages.append(f"{team1[i].name} missed!")
            db.close()
        
            user_attacked = True


        if (user_attacked):
            for member in team2:
                target = random.randint(0, len(team1) - 1)
                if (member.universe == 'Yugioh'):
                    adjusted = int(0.02 * int(member.moves[0]))
                    member.attack(team1[target], adjusted)
                    team2_messages.append(f"{member.name} attacked {team1[target].name} for {adjusted} damage!")
                    continue

                db = sqlite3.connect(DB_FILE)
                c = db.cursor()
                attack = random.choice(member.moves)
                c.execute("select * from moves where name = ?", (attack,))
                temp = c.fetchone()
                if temp is None:
                    team2_messages.append(f"{member.name}'s move failed!")
                    continue

                # type, damage, accuracy, universe
                attributes = [temp[2], temp[3], temp[4], temp[5]]
                if (temp[2] is None or temp[3] is None or temp[4] is None or temp[5] is None):
                    team2_messages.append(f"{member.name}'s move failed!")
                    continue

                if (random.randint(0, 100) < attributes[2]):
                    member.attack(team1[target], attributes[1])
                    team2_messages.append(f"{member.name} used {attack} on {team1[target].name} for {attributes[1]} damage!")
                else:
                    team2_messages.append(f"{member.name} missed!")
                db.close()

        team1 = [member for member in team1 if member.hp > 0]
        team2 = [member for member in team2 if member.hp > 0]

        if (len(team1) == 0 and len(team2) != 0):
            return redirect(url_for("disp_results", result = "loss"))
        if (len(team2) == 0 and len(team1) != 0):
            return redirect(url_for("disp_results", result = "win"))
        if (len(team2) == 0 and len(team1) == 0):
            return redirect(url_for("disp_results", result = "draw"))

        session['team1'] = [member.to_dict() for member in team1]
        session['team2'] = [member.to_dict() for member in team2]

        return render_template("showdown.html", team1 = team1, team2 = team2, team1_messages = team1_messages, team2_messages = team2_messages)
    else:
        return redirect(url_for("auth.login_get"))


@app.route("/results", methods=["GET"])
def disp_results():
    if session.get("username"):
        result = request.args.get("result")
        return render_template("results.html", result=result)
    else:
        return redirect(url_for("auth.login_get"))


db.commit()
db.close()

if __name__ == "__main__":
    build_db.populate_db()
    build_db.populate_db()
    app.debug = True
    app.run()
