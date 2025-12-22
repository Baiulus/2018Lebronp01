import requests
import json
import random
import urllib.request
import sqlite3, os
from typing import List, Dict, Optional

DB_FILE = "Lebron.db"

num_pokemon = 25


# Pokemon API
def poke_api_format(
    pokeid: int,
) -> Optional[Dict]:  # example: apiformat("https://pokeapi.co/api/v2/pokemon/mew")
    pokeurl = "https://pokeapi.co/api/v2/pokemon/" + str(pokeid)

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
    local_db = sqlite3.connect(DB_FILE)
    local_cursor = local_db.cursor()
    pokedata = poke_api_format(id)
    move_list = []

    for i in range(len(pokedata["moves"])):
        current_move = pokedata["moves"][i]["move"]["name"]
        local_cursor.execute(
            "SELECT name FROM moves WHERE name = ? AND universe = ?",
            (current_move, "Pokemon"),
        )
        if local_cursor.fetchone() != None:
            continue
        else:
            move_data = move_api_format(current_move)

            move_name = move_data["name"]
            move_id = move_data["id"]
            move_type = move_data["type"]["name"]
            move_power = move_data["power"]
            move_accuracy = move_data["accuracy"]

            move_list.append(current_move)
            local_cursor.execute(
                """
                INSERT OR IGNORE INTO moves (name, id, damage, type, accuracy, universe)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (move_name, move_id, move_power, move_type, move_accuracy, "Pokemon"),
            )

    local_db.commit()
    local_db.close()
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
def yugioh_api_format(name: str):
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name=" + name

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


def get_yugioh(name: str):
    response = yugioh_api_format(name)
    card = response["data"][0]

    charname = yugioh_get_name(card)
    imagelink = yugioh_get_image(card)
    id = card["id"]
    type = yugioh_get_type(card)
    hp = yugioh_get_stat(card, "hp")
    attack = yugioh_get_stat(card, "attack")
    universe = "Yugioh"

    yugiohdata = [charname, imagelink, id, type, hp, attack, universe]

    return yugiohdata


# DND API
def dnd_moves(name: str):
    local_db = sqlite3.connect(DB_FILE)
    local_cursor = local_db.cursor()
    dnddata = dnd_api_format(name)
    move_list = []

    for i in range(len(dnddata["actions"])):
        current_move = dnddata["actions"][i]["name"]
        local_cursor.execute(
            "SELECT name FROM moves WHERE name = ? AND universe = ?",
            (current_move, "DND"),
        )
        if local_cursor.fetchone() != None:
            continue
        else:
            move_name = dnddata["actions"][i]["name"]
            if (
                "damage" in dnddata["actions"][i]
                and dnddata["actions"][i]["damage"]
                and len(dnddata["actions"][i]["damage"]) > 0
            ):
                move_type = dnddata["actions"][i]["damage"][0]["damage_type"]["name"]
            else:
                move_type = "None"
            move_power = dnddata["actions"][i].get("attack_bonus", 0) * 10.0
            move_accuracy = 100

            move_list.append(current_move)
            local_cursor.execute(
                """
                INSERT OR IGNORE INTO moves (name, id, type, damage, accuracy, universe)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (move_name, 0, move_type, move_power, move_accuracy, "DND"),
            )

    local_db.commit()
    local_db.close()
    return move_list


def dnd_api_format(name: str):
    url = "https://www.dnd5eapi.co/api/2014/monsters/" + str(name)

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
    imagelink = "https://www.dnd5eapi.co" + card["image"]

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
    id = abs(hash(charname) % 10000000)
    type = dnd_get_type(card)
    hp = dnd_get_stat(card, "hp")
    attack = dnd_get_moves(card)
    universe = "DND"

    dnddata = [charname, imagelink, id, type, hp, attack, universe]

    return dnddata


def db_insert(data: list):
    local_db = sqlite3.connect(DB_FILE)
    local_cursor = local_db.cursor()

    local_cursor.execute(
        "INSERT or IGNORE INTO chars (charname, imagelink, id, type, hp, moves, universe) values (?, ?, ?, ?, ?, ?, ?)",
        (data[0], data[1], data[2], data[3], data[4], data[5], data[6]),
    )
    local_db.commit()
    local_db.close()


# Build Databse

db = sqlite3.connect(DB_FILE)
cursor = db.cursor()

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
    type TEXT,
    damage INTEGER,
    accuracy INTEGER,
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
    moves TEXT,
    universe TEXT
    );
    """
)

db.commit()
db.close()


def populate_yugioh(name: str):
    db_insert(get_yugioh(name))


def populate_dnd(name: str):
    db_insert(get_dnd(name))
    dnd_moves(name)


def populate_db():
    for i in range(num_pokemon):
        data = get_pokemon(i + 1)
        db_insert(data)
        poke_moves(i + 1)

    populate_yugioh("Black Luster Soldier")
    populate_yugioh("Blue-Eyes White Dragon")
    populate_yugioh("Hundred Eyes Dragon")
    populate_yugioh("Mystical Elf")
    populate_yugioh("First of the Dragonlords")
    populate_yugioh("Dark Magician Girl")

    populate_dnd("adult-black-dragon")
    populate_dnd("chimera")
    populate_dnd("medusa")
    populate_dnd("berserker")
    populate_dnd("fire-giant")
    populate_dnd("wyvern")


if __name__ == "__main__":
    populate_db()
    populate_db()
