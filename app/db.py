# Lucas Zheng, Emily Mai, Mycroft Lee, Shafin Kazi
# SoftDev
# P01
# Last updated: 12-10-25
# 12-22-25

import sqlite3
from typing import List, Dict, Optional

DB_FILE = "Lebron.db"

#Could change to be in method if multiple users to prevent them from using same cursor
db = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = db.cursor()
db.row_factory = sqlite3.Row 

# General QOL

def accessitem(table: str, column: str) -> None:
    cursor.execute(
        f"Select" + column + "from" + table
    )

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

# User Methods


# Get user by username
def get_user(username: str) -> Optional[Dict]: #can return [dict] or [none]

    cursor.execute(
        "SELECT username, created_at FROM users WHERE username = ?", (username,)
    )
    row = cursor.fetchone()
    db.close()

    return dict(row) if row else None


# Creates new unique user
def create_user(username: str, password_hash: str) -> bool: #return [boolean]

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password_hash),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        cursor.close()


# Charater Methods


# Get character by ID
def get_character_by_id(char_id: int) -> Optional[Dict]:

    cursor.execute("SELECT * FROM chars WHERE id = ?", (char_id,))
    row = cursor.fetchone()
    cursor.close()

    return dict(row) if row else None


# Get characters by universe
def get_characters_by_universe(
    universe: str, limit: int = 50 #can only return max 50 items
) -> List[Dict]:  # Change limit?

    cursor.execute(
        "SELECT * FROM chars WHERE universe = ? ORDER BY charname LIMIT ?",
        (universe, limit),
    )
    rows = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in rows]


# Search characters by name
def search_characters(query: str, limit: int = 20) -> List[Dict]:  # Change limit?

    cursor.execute(
        "SELECT * FROM chars WHERE charname LIKE ? ORDER BY charname LIMIT ?",
        (f"%{query}%", limit), #from page query
    )
    rows = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in rows]


# Get all characters
def get_all_characters(limit: int = 100) -> List[Dict]:  # Change limit?

    cursor.execute("SELECT * FROM chars ORDER BY universe, charname LIMIT ?", (limit,))
    rows = cursor.fetchall()
    cursor.close()

    return [dict(row) for row in rows]


# Add new character to database
def add_character(character_data: Dict) -> int: #character_data as dictionary data from the api

    try:
        cursor.execute(
            """
                INSERT OR IGNORE INTO chars 
                (charname, universe, type, hp, attack, defense, speed, 
                 special_attack, special_defense, image_url, api_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """, # ? to be chosen
            (
                character_data["charname"], #API COMMANDS
                character_data["universe"],
                character_data.get("type", "Unknown"), #gets all characters with a type of Unknown (get is a command used for the dict data)
                character_data.get("hp", 50), #gets all characters with an hp of 50 
                character_data.get("attack", 50),
                character_data.get("defense", 50),
                character_data.get("speed", 50),
                character_data.get("special_attack", character_data.get("attack", 50)),
                character_data.get(
                    "special_defense", character_data.get("defense", 50)
                ),
                character_data.get("image_url", ""),
                character_data.get("api_id", ""),
            ),
        )

        char_id = cursor.lastrowid
        db.commit()
        return char_id
    except: # Needed? 
        cursor.rollback()
        print("An error has occured")
    finally:
        cursor.close()


# Deck Building Methods


# Get user's team
def get_user_team(username: str) -> Optional[Dict]:

    cursor.execute("SELECT * FROM teams WHERE teamuser = ?", (username,))
    row = cursor.fetchone()

    # Get character stats for each slot
    if row:
        team = dict(row)
        team["characters"] = []
        for i in range(1, 4):
            char_id = team.get(f"teamslot{i}")
            if char_id:
                cursor.execute("SELECT * FROM chars WHERE id = ?", (char_id,))
                char = cursor.fetchone()
                if char:
                    team["characters"].append(dict(char))
    else:
        team = None

    cursor.close()
    return team

# Create new team
def create_team(username: str, character_ids: List[int], teamname: str = "Placeholder") -> None: # Can change hint for debugging

    cursor.execute(
        """
            INSERT INTO teams (teamuser, teamname, teamslot1, teamslot2, teamslot3)
            VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            teamname,
            character_ids[0],
            character_ids[1],
            character_ids[2],
        ),
     )

    db.commit()
    cursor.close()

# Edit user team
def edit_team(username: str, character_ids: List[int]) -> None: # Can change hint for debugging
    cursor.execute(
        """
            UPDATE teams SET
            teamname = ?,
            teamslot1 = ?,
            teamslot2 = ?,
            teamslot3 = ?
            WHERE teamuser = ?
            """,
            (
             teamname,
             character_ids[0],
             character_ids[1],
             character_ids[2],
             username,
            )
        )

    db.commit()
    cursor.close()            


    
