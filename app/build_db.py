import requests
import json
import urllib.request
from typing import List, Dict, Optional

#formats api data into a dictionary
def apiformat(link: str) -> Optional[Dict]: #example: apiformat("https://pokeapi.co/api/v2/pokemon/mew")
    dataraw = requests.get(link)
    data = dataraw.json()
    
    return data

#POKEMON
def get_hp(pokemon: str):
    pokemonurl = "https://pokeapi.co/api/v2/pokemon/" + pokemon
    pokedata = apiformat(pokemonurl)
    
    statname = pokedata
    
    hp = pokedata["stats"][0]
    print(hp)
    
#get_hp("charizard")


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