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


def poke_moves(pokedata: Dict, moveindex: int): #returns move type, power, and accuracy
    moveurl = pokedata["moves"][moveindex]["move"]["url"]
    
    movedataraw = requests.get(moveurl) #creates a request, USE SPARINGLY
    movedata = movedataraw.json()
    
    move_type = movedata["type"]["name"]
    move_power = movedata["power"]
    move_accuracy = movedata["accuracy"]
    
    return [move_type, move_power, move_accuracy]

def dnd_moves(dnddata: Dict, moveindex: int):
    move_power_str = dnddata["actions"][moveindex]["damage"][0]["damage_dice"] #work on this later ngl 

# formats api data into a dictionary
def poke_api_format(pokeid: int) -> Optional[Dict]:  # example: apiformat("https://pokeapi.co/api/v2/pokemon/mew")
    pokeurl = "https://pokeapi.co/api/v2/pokemon/" + str(pokeid + 1)

    dataraw = requests.get(pokeurl)
    data = dataraw.json()

    return data


# POKEMON
def get_stat(pokedata: Dict, statname: str):
    for i in pokedata["stats"]:
        stat = i["stat"]["name"]
        if stat == statname:
            statvalue = i["base_stat"]

    return statvalue


def get_image(pokedata: Dict):
    pokeimage = pokedata["sprites"]["front_default"]

    return pokeimage


def get_name(pokedata: Dict):
    pokeid = pokedata["name"]

    return pokeid


def get_type(pokedata: Dict):
    poketypes = []

    for i in pokedata["types"]:
        poketypes.append(i["type"]["name"])
    
    poketypes = ", ".join(poketypes)

    return poketypes


def get_pokemon(pokeid: int):
    pokemon = poke_api_format(pokeid)

    pokehp = get_stat(pokemon, "hp")
    pokeattack = get_stat(pokemon, "attack")
    pokename = get_name(pokemon)
    pokeimage = get_image(pokemon)
    poketype = get_type(pokemon)
    genre = "Pokemon"

    pokedata = [pokename, pokeimage, pokeid, poketype, pokeattack, pokehp, genre]

    return pokedata


# Yu-Gi-Oh! API
# 20 requests per 1 second


# returns list ([charname, imagelink, id, type, attack, hp, universe]) from a random Yu-Gi-Oh! card
def get_yugiohcard(index: int):
    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?type=Normal%20monster"  # all normal monster cards
    dataraw = requests.get(url)
    data = dataraw.json()
    monster = data["data"][index]
#     while True: commented out due to being unneeded with new search peramaters
#         try:
#             with urllib.request.urlopen(url) as page:
#                 data = json.load(page)  # data is a dictionary
#                 card = data["data"][0]
#                 if (
#                     "name" not in card
#                     or "id" not in card
#                     or "type" not in card
#                     or "atk" not in card
#                     or "def" not in card
#                 ):  # keeps getting a new url card until all values are present
#                     continue
    charname = card["name"]
    imagelink = card["card_images"][0]["image_url"]
    id = index + num_pokemon + num_dnd
    type = card["type"]
    attack = card["atk"]
    hp = card["def"]  # use def as hp for now
    universe = "Yu-Gi-Oh!"
    list = [charname, imagelink, id, type, attack, hp, universe]
    # print(list)
    return list
#         except:
#             continue


# returns list ([charname, imagelink, id, type, attack, hp, universe]) from a random D&D card
def get_dndcard(index: int):  # index should be within 0 and 333
    urlone = "https://www.dnd5eapi.co/api/2014/monsters"
    with urllib.request.urlopen(urlone) as pageone:
        urlpart = json.load(pageone)
        urlpart = urlpart["results"][index]["url"]
    urltwo = "https://www.dnd5eapi.co" + urlpart
    with urllib.request.urlopen(urltwo) as pagetwo:
        data = json.load(pagetwo)
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


# def db_insert(data: list):
#     dataformat = str(data).replace('[', ']', '')
#     datastring = ', '.join(dataformat)
#     print(f"insert into chars (" + datastring + ")")
#     cursor.execute(f"insert into chars (" + datastring + ")")
#
# db_insert(get_pokemon(151))

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
    damage INTEGER,
    type TEXT
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
    atk INTEGER,
    hp INTEGER,
    moves TEXT,
    universe TEXT,
    FOREIGN KEY (moves) REFERENCES moves(id)
    );
    """
)

db.commit()
db.close()