"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""

import sys
from types import SimpleNamespace
from client import Client
import json
import pygame
from pygame import *
from Graph import gui_graph

from poke_files.poke_node import PokeNode
from poke_files.poke_trainer import PokeTrainer
# from Graph.graph_algo import GraphAlgo
from Graph.graph_algo import GraphAlgo
from Graph.di_graph import DiGraph
from poke_files.play import Play


# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
background = pygame.image.load("src\Game\media\safari_zone.gif")
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()

graph_json = client.get_graph()

GraphA = GraphAlgo()
GraphA.load_from_json(graph_json)
graph = GraphA

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
mixer.music.load("src/Game/media/song.wav")
mixer.music.play(-1)

pokemon_dict = {}
trainer_dict = {}
while client.is_running() == 'true':
    
    screen.blit(background,(0,0))

    pygame.init()
    pokemons = json.loads(client.get_pokemons())
  
    for pokemon in pokemons['Pokemons']:
        new_poke = PokeNode.dict_to_poke(pokemon)
        new_poke.id = Play.generate_id(pokemon_dict)
        pokemon_dict[new_poke.id] = new_poke
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

    # display all the things
    gui_graph.draw_graph(screen,graph.get_graph())
    gui_graph.draw_trainer(screen,trainer_dict)
    gui_graph.draw_pokemon(screen,pokemon_dict)
    
    display.update()
    clock.tick(60)

    Play.dispatch(graph,trainer_dict,pokemon_dict)
    for trainer in trainer_dict.values():
        trainer:PokeTrainer
        if trainer.target[1] != -1:
            client.choose_next_edge('{"agent_id":'+str(trainer.id)+ ', "next_node_id":' +str(trainer.path[1])+ '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
    client.move()


    # update screen changes
   
    # refresh rate


# game over:
