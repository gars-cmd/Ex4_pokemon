import json
from typing import Dict, List, Tuple
import sys
import math
import math
from Graph.di_graph import DiGraph
from Graph.graph_algo import GraphAlgo
from poke_files.poke_node import PokeNode
from poke_files.poke_trainer import PokeTrainer
import random
from Graph.node_class import Nodes
from poke_files.game_boy import GameBoy


class Play():
    def __init__(self) -> None:
        self.pokemon_dict:Dict[int , PokeNode]
        self.graph = GraphAlgo()
        self.trainer_dict:Dict[int,PokeTrainer] = {}
        self.game_server:GameBoy = {}

    
    # we get each time the graph , pokemons and agents of the game
    def refresh_data(self , pokemon_json , trainers_json , graph_json):
        pokemons = json.loads(pokemon_json)
        if pokemons!= None:
            for pokemon in pokemons['Pokemons']:
                new_poke:PokeNode = PokeNode.dict_to_poke(pokemon)
                new_poke.id = Play.generate_id()
                self.pokemon_dict[id] = new_poke
        
        trainers = json.loads(trainers_json)
        if trainers !=None:
            for trainer in trainers['Agents']:
                new_trainer:PokeTrainer = PokeTrainer.dict_to_trainer(trainer)
                self.trainer_dict[new_trainer.get_id()] = new_trainer
        
        self.graph = GraphAlgo.load_from_json(graph_json)


    # generate random id for the pokemon dictionnary 
    def generate_id(pokemon_dict:Dict) -> int:
        id =-1
        id = random.randint(0,len(pokemon_dict)+1)
        while(True):
            try:
                pokemon_dict[id]    
                id = random.randint(1,10000)
            except:
                return id

    # reset the target of all the trainers
    def reset_target(trainer_list:List):
        for trainer in trainer_list:
            trainer:PokeTrainer
            trainer.target=[-1,-1]
            trainer.path = [] 



    # set the target parameter for each trainer in the game
    def dispatch(graph:GraphAlgo,trainer_dict:Dict , pokemon_dict:Dict):
        temp_trainer_list:List = list(trainer_dict.values())
        
        temp_pokemon_list:List = list(pokemon_dict.values())

        while( len(temp_pokemon_list)> 0 and len(temp_trainer_list)>0):
            # set for all the trainers the best ratio catch 
            for trainer in temp_trainer_list:
                # print ("trainer= ",trainer.id,"path=",trainer.path,"cost= ",trainer.target)
                # if len(trainer.path)>1 and trainer.path[0] == trainer.path[1]:
                #     # print("here")
                #     trainer.path = []
                #     trainer.target = [-1,-1]
                # print(len(trainer.path))
                # print("test",trainer.path , " cost =",trainer.target)
                trainer:PokeTrainer
                result= Play.cost_value_pokemon(graph,trainer, temp_pokemon_list)
                # print(type(trainer.target))
                trainer.target[0] = result[0]
                trainer.target[1] = result[1]
            # we find the trainer with the best value/cost and 
            max =[-1 , -1]
            if len(temp_trainer_list)>0:
                for trainer in temp_trainer_list:
                    if trainer.target[1] > max[1]:
                        max[0] = trainer.id
                        max[1] = trainer.target[0]
            # we remove the trainer with the best value after allocation and the best pokemon cause there is a trainer to catch him 
            # print("the best next path  = ",max[0],"->",trainer_dict[max[0]].path)
                temp_trainer_list.remove(trainer_dict.get(max[0]))
                temp_pokemon_list.remove(pokemon_dict.get(trainer_dict.get(max[0]).target[0]))
            # reset all the target of the remain trainers COULD  BE IMPROVE 
                Play.reset_target(temp_trainer_list)

            


    # find on which edge the pokemon is in case of bidirectional edge return of which of theme he is 
    def on_which_edge(graph:GraphAlgo , pokemon:PokeNode) -> Tuple:
        ans = ()
        for keyN , nodes in graph.get_graph().NodesMap.items():
            nodes:Nodes
            for keyE , edge in nodes.me_to_other.items():
                # get geometric distance of the edge 
                a_b = Play.distance(nodes.pos , graph.get_graph().NodesMap.get(keyE).pos)
                # get geometric distance from a to pokemon
                a_k = Play.distance(nodes.pos , pokemon.pos)
                # get geometric distance from b to pokemon
                b_k = Play.distance(graph.get_graph().NodesMap.get(keyE).pos , pokemon.pos)
                # we check that the pokemon is between this edge
                if a_k<a_b and b_k<a_b and (a_k+b_k < a_b+sys.float_info.epsilon) and (a_k+b_k > a_b-sys.float_info.epsilon):
                    #  we check if the pokemon is on the upside edge or downside edge in the case of bidirectional edge
                    if pokemon.type < 0 and keyN>keyE:
                        ans = (keyN,keyE)
                        return ans
                    else:
                        ans = (keyE,keyN)
                        return ans
        # if the pokemon is not on an edge 
        return(-1,-1)







    # calc the distance between two pos (two tuples)
    def distance(a:Tuple , b:Tuple) -> float:
        x = (b[0] - a[0]) * (b[0] - a[0])
        y =  (b[1] - a[1]) * (b[1] - a[1])
        z = (b[2] - a[2]) * (b[2] - a[2])
        return math.sqrt(x+y+z)


    # find the best ratio value/cost pokemon to catch (return a tuple with the id of the pokemon and the cost of the travel)
    def cost_value_pokemon( graph:GraphAlgo ,agent:PokeTrainer , pokedex:List) -> Tuple:
        ans = [None , float('inf')]
        for pokemon in pokedex:
            pokemon:PokeNode
            # find the edge where the pokemon lean on
            pokeside = Play.on_which_edge(graph , pokemon=pokemon)
            misses_weight = 0
            
            if agent.get_src() == pokeside[0]:
                djisk = GraphAlgo.shortest_path(graph , agent.get_src() , pokeside[1])
            # find the path from the trainer to the src of the edge where the pokemon lean on
            else:
                djisk = GraphAlgo.shortest_path(graph , agent.get_src() , pokeside[0])
                misses_weight = graph.get_graph().NodesMap.get(pokeside[0]).me_to_other[pokeside[1]][1]
            path_cost = misses_weight + djisk[0]
            if (path_cost/pokemon.get_value()) < ans[1]:
                ans = [pokemon.id , path_cost/pokemon.get_value()]
                # we also save the path to the 
                agent.path = djisk[1]
                agent.path.append(pokeside[1])
                agent.path.pop(0)
        return (ans[0] , ans[1])


    
