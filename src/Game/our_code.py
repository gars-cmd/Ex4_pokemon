"""
@author Avidan & Gal 
OOP - Ex4
Not Very simple GUI example for python client to communicates with the server and "catch them all!"
"""

from os import waitpid
import sys
from types import SimpleNamespace

from poke_files.game_boy import GameBoy
from client import Client
import json
import pygame
from pygame import *
from Graph import gui_graph
from Graph.gui_graph import button
from poke_files.poke_node import PokeNode
from poke_files.poke_trainer import PokeTrainer
# from Graph.graph_algo import GraphAlgo
from Graph.graph_algo import GraphAlgo
from Graph.di_graph import DiGraph
from poke_files.play import Play
import time


# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
background = pygame.image.load("media\safari_zone.gif")
clock = pygame.time.Clock()
pygame.font.init()

# button = pygame.image.load("src\Game\media\menu.png").convert_alpha()
# # button class
# class Button():
#     def __init__(self , x, y , image ,scale) -> None:
#         width = image.get_width()
#         height = image.get_height()
#         self.image = pygame.surface((0,0) , pygame.SRCALPHA)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x,y)
#     def draw(self):
#         screen.blit(self.image,(self.rect.x , self.rect.y))

# menu = Button(0,0 , button ,0.8 )




client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
WHITE = (255, 255, 255)
BLUE = (0 , 0 , 255)
GREY = (128,128,128)
BLACK = (0 , 0 , 0)
RED = (255, 0, 0)
VIOLET = (238,130,238)
YELLOW =(255, 255, 0)
graph_json = client.get_graph()

GraphA = GraphAlgo()
GraphA.load_from_json(graph_json)
graph = GraphA

client.add_agent("{\"id\":0}")
client.add_agent("{\"id\":1}")
client.add_agent("{\"id\":2}")
client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
mixer.music.load("media\Pokémon Theme.wav")
mixer.music.play(-1)


trainer_dict = {}
while client.is_running() == 'true':
    pokemon_dict = {}
    trainer_dict = trainer_dict
    
    
    screen.blit(background,(0,0))
    # screen=menu.image.sce
    # menu.draw()

    pygame.init()
    pokemons = json.loads(client.get_pokemons())
    # time.sleep(0.090)  
    client.move()
    i =0
    for pokemon in pokemons['Pokemons']:
        new_poke = PokeNode.dict_to_poke(pokemon)
        new_poke.id = i
        i+=1
        pokemon_dict[new_poke.id] = new_poke
    # print(len(pokemon_dict))
        
    agents = json.loads(client.get_agents())

    for agent in agents['Agents']:
        new_agent = PokeTrainer.dict_to_trainer(agent)
        if new_agent.id  in trainer_dict.keys():
            # print("exist")
            trainer_dict[new_agent.id].id = new_agent.id
            trainer_dict[new_agent.id].pos = new_agent.pos
            trainer_dict[new_agent.id].value = new_agent.value
            trainer_dict[new_agent.id].src = new_agent.src
            trainer_dict[new_agent.id].dest = new_agent.dest
            trainer_dict[new_agent.id].speed = new_agent.speed
        else:
            trainer_dict[new_agent.id] = new_agent
    # print(trainer_dict)

    game_info = json.loads(client.get_info())
    game = GameBoy.dict_to_game(game_info)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # display all the things
    gui_graph.draw_graph(screen,graph.get_graph())
    gui_graph.draw_trainer(screen,trainer_dict)
    gui_graph.draw_pokemon(screen,pokemon_dict)
    gui_graph.print_data(screen , str(game.get_moves()) , str(game.get_grade()) , str(int(int(client.time_to_end())/1000)))
    clock.tick(60)
    redbutton = button(RED , 200 , 50 , 100 , 40 , "STOP")
    gui_graph.redrawWindows(screen , redbutton)
    display.update()

    # if our button clicked then we stop the game 
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            if redbutton.isOver(pos):
                client.stop()
                client.stop_connection()

    # we allocate to all the trainer a pokemon  
    Play.dispatch(graph,trainer_dict,pokemon_dict)
    for trainer in trainer_dict.values():
        trainer:PokeTrainer
        # if len(trainer.path)>0 and trainer.get_src() == trainer.path[0]:
        #     trainer.path.pop(0)
        if trainer.dest == -1 :
            client.choose_next_edge('{"agent_id":'+str(trainer.id)+', "next_node_id":'+str(trainer.path[0])+'}')
            ttl = client.time_to_end()
            
            print(ttl, client.get_info())
