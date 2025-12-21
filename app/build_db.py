import requests
import json
import urllib.request
import sqlite3, os
from typing import List, Dict, Optional

DB_FILE = "Lebron.db"
db = sqlite3.connect(DB_FILE)
cursor = db.cursor()

num_pokemon = 151
num_dnd = 334


# Pokemon API
def poke_api_format(
    pokeid: int,
) -> Optional[Dict]:  # example: apiformat("https://pokeapi.co/api/v2/pokemon/mew")
    pokeurl = "https://pokeapi.co/api/v2/pokemon/" + str(pokeid + 1)

    dataraw = requests.get(pokeurl)
    data = dataraw.json()

    return data


def move_api_format(movename: str) -> Optional[Dict]:
    pokeurl = "https://pokeapi.co/api/v2/move/" + movename

    dataraw = requests.get(pokeurl)
    data = dataraw.json()

    return data


# Return list of added moves to the database
def poke_moves(id: int) -> Optional[Dict]:
    pokedata = poke_api_format(id)
    move_list = []

    for i in range(len(pokedata["moves"])):
        current_move = pokedata["moves"][i]["move"]["name"]
        cursor.execute(
            "SELECT name FROM moves WHERE name = ? AND universe = ?",
            (current_move, "Pokemon"),
        )
        if cursor.fetchone() != None:
            continue
        else:
            move_data = move_api_format(current_move)

            move_name = move_data["name"]
            move_type = move_data["type"]["name"]
            move_power = move_data["power"]
            move_accuracy = move_data["accuracy"]

            move_list.append(current_move)
            cursor.execute(
                """
                INSERT OR IGNORE INTO moves (name, id, damage, type, accuracy, universe)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (move_name, i, move_power, move_type, move_accuracy, "Pokemon"),
            )

    db.commit()
    db.close()

    return move_list


def poke_get_stat(pokedata: Dict, statname: str):
    for i in pokedata["stats"]:
        stat = i["stat"]["name"]
        if stat == statname:
            statvalue = i["base_stat"]

    return statvalue


def poke_get_name(pokedata: Dict):
    pokeid = pokedata["name"]

    return pokeid


def poke_get_image(pokedata: Dict):
    pokeimage = pokedata["sprites"]["front_default"]

    return pokeimage


def poke_get_type(pokedata: Dict):
    poketypes = []

    for i in pokedata["types"]:
        poketypes.append(i["type"]["name"])

    poketypes = ", ".join(poketypes)
    return poketypes


def poke_get_moves(pokedata: Dict):
    pokemoves = []
    for i in pokedata["moves"]:
        pokemoves.append(i["move"]["name"])

    pokemoves = ", ".join(pokemoves)
    return pokemoves


def get_pokemon(pokeid: int):
    pokemon = poke_api_format(pokeid)

    pokename = poke_get_name(pokemon)
    pokeimage = poke_get_image(pokemon)
    poketype = poke_get_type(pokemon)
    pokehp = poke_get_stat(pokemon, "hp")
    pokemoves = poke_get_moves(pokemon)
    universe = "Pokemon"

    pokedata = [pokename, pokeimage, pokeid, poketype, pokehp, pokemoves, universe]

    return pokedata


# Yu-Gi-Oh! API
def yugioh_api_format(id: int):
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?id=" + str(id)

    dataraw = requests.get(url)
    data = dataraw.json()

    return data


def yugioh_get_stat(card: Dict, statname: str):
    if statname == "attack":
        statvalue = card["atk"]
    elif statname == "hp":
        statvalue = card["def"]

    return statvalue


def yugioh_get_name(card: Dict):
    charname = card["name"]

    return charname


def yugioh_get_type(card: Dict):
    type = card["attribute"]

    return type


def yugioh_get_image(card: Dict):
    imagelink = card["card_images"][0]["image_url"]

    return imagelink


def get_yugioh(id: int):
    card = yugioh_api_format(id)

    charname = yugioh_get_name(card)
    imagelink = yugioh_get_image(card)
    type = yugioh_get_type(card)
    hp = yugioh_get_stat(card, "hp")
    attack = yugioh_get_stat(card, "attack")
    universe = "Yugioh"

    yugiohdata = [charname, imagelink, id, type, hp, attack, universe]

    return yugiohdata


# DND API
def dnd_moves(name: str):
    dnddata = dnd_api_format(name)
    move_list = []

    for i in range(len(dnddata["actions"])):
        current_move = dnddata["actions"][i]["name"]
        cursor.execute(
            "SELECT name FROM moves WHERE name = ? AND universe = ?",
            (current_move, "DND"),
        )
        if cursor.fetchone() != None:
            continue
        else:
            move_name = dnddata["actions"][i]["name"]
            move_type = dnddata["actions"][i]["damage"][0]["damage_type"]
            move_power = dnddata["actions"][i]["attack_bonus"] * 10.0
            move_accuracy = 100

            move_list.append(current_move)
            cursor.execute(
                """
                INSERT OR IGNORE INTO moves (name, id, type, damage, accuracy, universe)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (move_name, i, move_type, move_power, move_accuracy, "DND"),
            )

    db.commit()
    db.close()

    return move_list


def dnd_api_format(name: str):
    url = "https://www.dnd5eapi.co/api/2014/monsters/" + name

    dataraw = requests.get(url)
    data = dataraw.json()

    return data


def dnd_get_stat(card: Dict, statname: str):
    if statname == "hp":
        statvalue = card["hit_points"]

    return statvalue


def dnd_get_name(card: Dict):
    charname = card["name"]

    return charname


def dnd_get_type(card: Dict):
    type = card["type"]

    return type


def dnd_get_image(card: Dict):
    imagelink = card["image"]

    return imagelink


def dnd_get_moves(card: Dict):
    dndmoves = []
    for i in card["actions"]:
        dndmoves.append(i["name"])

    dndmoves = ", ".join(dndmoves)
    return dndmoves


def get_dnd(name: str):
    card = dnd_api_format(name)

    charname = dnd_get_name(card)
    imagelink = dnd_get_image(card)
    type = dnd_get_type(card)
    hp = dnd_get_stat(card, "hp")
    attack = dnd_get_moves(card)
    universe = "DND"

    dnddata = [charname, imagelink, id, type, hp, attack, universe]

    return dnddata


# returns list ([charname, imagelink, id, type, attack, hp, universe]) from a random D&D card
def get_dndcard(index: int):  # index should be within 0 and 333
    urlone = "https://www.dnd5eapi.co/api/2014/monsters"
    with urllib.request.urlopen(urlone) as pageone:
        urlpart = json.load(pageone)
        urlpart = urlpart["results"][index]["url"]
    urltwo = "https://www.dnd5eapi.co" + urlpart
    with urllib.request.urlopen(urltwo) as pagetwo:
        data = json.load(pagetwo)

        # print(dnd_moves(data, 0))
        charname = data["name"]
        imagelink = "https://www.dnd5eapi.co" + data["image"]
        id = index + num_pokemon
        type = data["type"]
        dice = data["hit_dice"]
        dicearray = dice.split("d")
        dicearray = [int(x) for x in dicearray]
        attack = int(dicearray[0] * dicearray[1] / 2)
        hp = data["hit_points"]
        universe = "DND"
        list = [charname, imagelink, id, type, attack, hp, universe]
        # print(list)
        return list


def db_insert(data: list):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()

    cursor.execute(
        "INSERT or IGNORE INTO chars (charname, imagelink, id, type, hp, moves, universe) values (?, ?, ?, ?, ?, ?, ?)",
        (data[0], data[1], data[2], data[3], data[4], data[5], data[6]),
    )
    db.commit()
    db.close()


# Build Databse

cursor.executescript(
    """
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT
    );
    """
)

cursor.executescript(
    """
    DROP TABLE IF EXISTS teams;
    CREATE TABLE teams (
    teamuser TEXT,
    teamslot1 INTEGER,
    teamslot2 INTEGER,
    teamslot3 INTEGER,
    teamid INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY (teamuser) REFERENCES users(username),
    FOREIGN KEY (teamslot1) REFERENCES chars(id)
    FOREIGN KEY (teamslot2) REFERENCES chars(id)
    FOREIGN KEY (teamslot3) REFERENCES chars(id)
    );
    """
)

cursor.executescript(
    """
    DROP TABLE IF EXISTS moves;
    CREATE TABLE moves (
    name TEXT UNIQUE,
    id TEXT PRIMARY KEY,
    type TEXT
    damage INTEGER,
    accuracy INTEGER
    universe TEXT
    );
    """
)

cursor.executescript(
    """
    DROP TABLE IF EXISTS chars;
    CREATE TABLE chars (
    charname TEXT,
    imagelink TEXT,
    id INTEGER PRIMARY KEY,
    type TEXT,
    hp INTEGER,
    atk INTEGER,
    moves TEXT,
    universe TEXT,
    FOREIGN KEY (moves) REFERENCES moves(id)
    );
    """
)

# print(get_dndcard(3))
db.commit()
db.close()
