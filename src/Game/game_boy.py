
from typing import Dict


class GameBoy:
    def __init__(self , pokemons=0 ,  is_logged_in=False , moves=0 , grade=0 , game_level=0 , max_user_level=0 , id=0 , graph="" , agents=0 ) -> None:
        self.pokemons = pokemons
        self.is_logged_in = is_logged_in
        self.moves = moves
        self.grade = grade
        self.game_level = game_level
        self.max_user_level = max_user_level
        self.id = id
        self.graph = graph
        self.agents = agents


    def get_pokemons(self) -> int:
        return self.pokemons

    def get_is_logged_in(self) ->bool:
        return self.is_logged_in
    
    def get_moves(self) -> int:
        return self.moves

    def get_grade(self) ->int:
        return self.grade

    def get_game_level(self) -> int:
        return self.get_game_level

    def get_max_user_level(self) -> int:
        return self.max_user_level

    def get_id(self) -> int:
        return self.id

    def get_graph(self) -> str:
        return self.graph

    def get_agents(self) -> int:
        return self.agents

    
    # convert from dictionary to Game
    def dict_to_game(dict:Dict)  :
        pokemons = int(dict.get("pokemons"))
        is_logged_in = bool(dict.get("is_logged_in"))
        moves = int(dict.get("moves"))
        grade = int(dict.get("grade"))
        game_level = int(dict.get("game_level"))
        max_user_level = int(dict.get("max_user_level"))
        id = int(dict.get("id"))
        graph = dict.get("graph")
        agents =  int(dict.get("agents"))
        return GameBoy(pokemons=pokemons , is_logged_in=is_logged_in , moves=moves , grade=grade , game_level=game_level , max_user_level=max_user_level , id=id , graph=graph , agents=agents)

        