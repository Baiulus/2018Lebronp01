import requests
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
    
get_hp("charizard")