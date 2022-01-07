"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""

import sys
from types import SimpleNamespace
from client_python.client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from game_boy import GameBoy
from poke_node import PokeNode
from poke_trainer import PokeTrainer
from Graph.graph_algo import GraphAlgo
from Graph.node_class import Nodes
from Graph.di_graph import DiGraph


# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

# FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object
GraphA = GraphAlgo()
GraphA.load_from_json(graph_json)

#  get data proportions
# min_x = min(list(GraphA.diGraph.get_all_v), key=lambda n: n.pos[0]).pos[0]
# min_y = min(list(GraphA.diGraph.get_all_v), key=lambda n: n.pos[1]).pos[1]
# max_x = max(list(GraphA.diGraph.get_all_v), key=lambda n: n.pos[0]).pos[0]
# max_y = max(list(GraphA.diGraph.get_all_v), key=lambda n: n.pos[1]).pos[1]
MAXx = sys.float_info.min
MAXy = sys.float_info.min
MINy = sys.float_info.max
MINx = sys.float_info.max

def findRatio(graph:DiGraph):
    
    listNode = graph.get_all_v()
    global MINx , MINy , MAXx , MAXy
    for node in listNode:
        curr = listNode[node]
        
        # if the node don't have coordinate 
        if curr[0] == None or curr[1] == None:
            continue
        else:
            # print(curr)
            if curr[0] < MINx:
                # global MINx
                MINx = curr[0]
            if curr[0] > MAXx:
                # global MAXx
                MAXx = curr[0]
            if curr[1] < MINy:
                # global MINy
                MINy = curr[1]
            if curr[1] > MAXy:
                # global MAXy 
                MAXy = curr[1]
    
# def scale(data, min_screen, max_screen, min_data, max_data):
#     # """
#     # get the scaled data with proportions min_data, max_data
#     # relative to min and max screen dimentions
#     # """
#     return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# # decorate scale with the correct values

# def my_scale(data, x=False, y=False):
#     if x:
#         return scale(data, 50, screen.get_width() - 50, min_x, max_x)
#     if y:
#         return scale(data, 50, screen.get_height()-50, min_y, max_y)

def scale(data , min_screen , max_screen , min_data , max_data):
    data_ratio = ((data - min_data) / (max_data - min_data))
    screen_ratio = ((max_screen - min_screen) + min_screen)
    return (data_ratio * screen_ratio)

def myScale(data , x=False , y=False):
    if x:
        return scale(data , 50 , screen.get_width()-30 , MINx , MAXx )+10
    if y:
        return scale(data , 50 , screen.get_height()-30 , MINy , MAXy)+10

# radius = 15

client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
pokemon_dict = {}
trainer_dict = {}
while client.is_running() == 'true':
    pygame.init()
    pokemons = json.loads(client.get_pokemons())
  
    for pokemon in pokemons['Pokemons']:
        new_poke = PokeNode.dict_to_poke(pokemon)
        pokemon = new_poke
    print(pokemons)
        
    agents = json.loads(client.get_agents())
   
    for agent in agents['Agents']:
        new_agent = PokeTrainer.dict_to_trainer(agent)
        trainer_dict[new_agent.id] = new_agent
    print(trainer_dict)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

     
    
    # draw agents
    for agent in trainer_dict.values():
        agent:PokeTrainer
        x = myScale(agent.pos[0] ,x=True)
        y = myScale(agent.pos[1] ,y=True)
        pygame.draw.circle(screen, Color(122, 61, 23),(x,y), 10)
                           
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemon_dict.values():
        p:PokeNode
        pygame.draw.circle(screen, Color(0, 255, 255), ((p.pos[0]),(p.pos[1])), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)
    GraphA.plot_graph()
    # # choose next edge
    # for agent in agents:
    #     if agent.dest == -1:
    #         next_node = (agent.src - 1) % len(graph.Nodes)
    #         client.choose_next_edge(
    #             '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
    #         ttl = client.time_to_end()
    #         print(ttl, client.get_info())
    
    # client.move()
# game over:
