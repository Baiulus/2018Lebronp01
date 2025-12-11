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
    poketypes =[]

    for i in pokedata["types"]:
        poketypes.append(i["type"]["name"])

    return poketypes

def get_pokemon():
    pokelist = []
    for j in range(1,152):
        pokemon = poke_api_format(j)

        pokehp = get_stat(pokemon, 'hp')
        pokeattack = get_stat(pokemon, 'attack')
        pokeid = j
        pokename = get_name(pokemon)
        pokeimage = get_image(pokemon)
        poketype = get_type(pokemon)
        genre = 'Pokemon'

        pokedata = [pokename, pokeimage, pokeid, poketype, pokeattack, pokehp, genre]

        pokelist.append(pokedata)

    return pokelist


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

#returns list ([charname, imagelink, id, type, attack, hp, universe]) from a random D&D card
def get_dndcard(index): #index should be within 0 and 333
    urlone = "https://www.dnd5eapi.co/api/2014/monsters"
    with urllib.request.urlopen(urlone) as pageone:
        urlpart = json.load(pageone)
        urlpart = urlpart["results"][index]["url"]
    urltwo = "https://www.dnd5eapi.co" + urlpart
    with urllib.request.urlopen(urltwo) as pagetwo:
        data = json.load(pagetwo)
        charname = data["name"]
        imagelink = "https://www.dnd5eapi.co" + data["image"]
        id = index
        type = data["type"]
        dice = data["hit_dice"]
        dicearray = dice.split("d")
        dicearray = [ int(x) for x in dicearray ] 
        attack = int(dicearray[0] * dicearray[1] / 2)
        hp = data["hit_points"]
        universe = "D&D"
        list = [charname, imagelink, id, type, attack, hp, universe]
        #print(list)
        return list

for i in range(10):
    print(get_dndcard(i))
