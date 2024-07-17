from fastapi import FastAPI, HTTPException, Path 
from dataclasses import dataclass, asdict 
from typing import Union 
import json 
import math

#========= Structures de données : Dictionnaire indexé  par pokemon=================================

with open("pokemons.json") as f : 
    pokemons_list = json.load(f) 
    
list_pokemons = {k+1 : v for k, v in enumerate(pokemons_list)}


@dataclass
class Pokemon(): 
    id:int
    name : str
    types : list[str]
    total: int 
    hp: int 
    attack : int 
    defense: int 
    attack_special: int
    defense_special: int
    speed : int 
    evolution_id : Union[int, None] = None 

#=======================================================================

app = FastAPI()

#========================GET===========================================

@app.get("/total_pokemons")
async def get_total_pokemons()-> dict:
    return {"total": len(list_pokemons)}
    

@app.get("/pokemons")
async def get_all_pokemons1()->list[Pokemon]:
    res = []
    for id in list_pokemons: 
        res.append(Pokemon(**list_pokemons[id]))
    return res

@app.get("/pokemons/{id}")
async def get_pokemon_by_id(id : int = Path(ge =1))-> Pokemon: 
    if id not in list_pokemons: 
        raise HTTPException (status_code = 404, detail = "Ce Pokemon n'existe pas")
    return Pokemon(**list_pokemons[id])

#========================POST===========================================

@app.post("/pokemon")
async def create_pokemon(pokemon: Pokemon)-> Pokemon: 
    if pokemon.id in list_pokemons: 
        raise HTTPException(status_code = 404, detail = f"Le pokemon {pokemon.id} existe déjà")
    
    ## Si le pokemon n'existe pas, ajoute le dans la liste 
    list_pokemons[pokemon.id] = asdict(pokemon)
    return pokemon

#========================PUT===========================================
@app.put("/pokemon/{id}")
async def update_pokemon (pokemon: Pokemon, id: int = Path(ge = 1))-> Pokemon: 
    if id not in list_pokemons: 
        raise HTTPException (status_code = 404, detail = f"The Pokemon is not exists")
    
    ## si le pokemon existe dans la liste, il faut le modifier 
    
    list_pokemons[id]  = asdict(pokemon)
    return pokemon 
        

#========================DELETE===========================================

@app.delete("/pokemon/{id}")
async def delete_pokemon(id: int = Path(ge = 1)) -> Pokemon: 
    if id in list_pokemons:
        pokemon = Pokemon(**list_pokemons[id])
        del list_pokemons[id]
        return pokemon
    raise HTTPException (status_code = 404, detail = f"Le pokemon {id} n'existe pas")


# ===================== GET===============================

@app.get("/types")
async def get_all_types()->list[str]:
    types = []
    for pokemon in pokemons_list: 
        for type in pokemon["types"]: 
            if type not in types: 
                types.append(type)
        ## sort types by letter
        types.sort()
    return types


## Tous les Pokémons avec ma pagination 
@app.get("/pokemons2/")
async def get_all_pokemons(page: int = 1, items : int = 10)-> list[Pokemon] :
    items = min(items, 20)
    max_page = math.ceil(len(list_pokemons) / items )
    current_page = min (page, max_page)
    start = (current_page -1)*page 
    stop = start + items if start + items <= len(list_pokemons) else len(list_pokemons)
    sublist = (list(list_pokemons))[start:stop]
    res = []
    
    for id in sublist:
        res.append(Pokemon(**list_pokemons[id]))
    return res

