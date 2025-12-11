import requests
import json
import urllib.request
from typing import List, Dict, Optional

#formats api data into a dictionary
def poke_api_format(pokeid: int) -> Optional[Dict]: #example: apiformat("https://pokeapi.co/api/v2/pokemon/mew")
    pokeurl = "https://pokeapi.co/api/v2/pokemon/" + str(pokeid)

    dataraw = requests.get(pokeurl)
    data = dataraw.json()

    return data

#POKEMON
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
    for i in pokedata["types"]:
        poketype = pokedata["types"][i]["type"]["name"]


#Yu-Gi-Oh! API
#20 requests per 1 second

#returns list ([charname, imagelink, id, type, attack, hp, universe]) from a random Yu-Gi-Oh! card
def get_yugiohcard():
    url = "https://db.ygoprodeck.com/api/v7/randomcard.php" #url holds a random card, but we want monster cards specifically with all required values
    while True:
        try:
            with urllib.request.urlopen(url) as page:
                data = json.load(page) #data is a dictionary
                card = data["data"][0]
                if ("name" not in card or "id" not in card or "type" not in card or "atk" not in card or "def" not in card): #keeps getting a new url card until all values are present
                    continue
                charname = card["name"]
                imagelink = card["card_images"][0]["image_url"]
                id = card["id"]
                type = card["type"]
                attack = card["atk"]
                hp = card["def"] #use def as hp for now
                universe = "Yu-Gi-Oh!"
                list = [charname, imagelink, id, type, attack, hp, universe]
                #print(list)
                return list
        except:
            continue

#return string of a part of an url
def get_dndmonsterurl(index): #index should be within 0 and 333
    url = "https://www.dnd5eapi.co/api/2014/monsters"
    with urllib.request.urlopen(url) as page:
        data = json.load(page)
        data = data["results"][index]["url"]
        print(data)
        return data
get_dndmonsterurl(0)

#returns list ([charname, imagelink, id, type, attack, hp, universe]) from a random D&D card
def get_dndcard(urlpart):
    url = "https://www.dnd5eapi.co" + urlpart
    with urllib.request.urlopen(url) as page:
        data = json.load(page)
        
