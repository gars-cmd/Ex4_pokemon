
from typing import Dict
import pygame
import math
from pygame import Color, draw
from pygame import color
from pygame import display
from pygame.constants import DOUBLEBUF, HWSURFACE, RESIZABLE, SCRAP_SELECTION, VIDEORESIZE
from pygame.draw import line, rect
from pygame.font import Font
from pygame.time import Clock
from Graph.di_graph import DiGraph
import os
import sys
from Graph.node_class import Nodes
from pygame import mixer

from poke_files.poke_node import PokeNode
from poke_files.poke_trainer import PokeTrainer




# option to write text
pygame.font.init()

# display the main window
WIN = pygame.display.set_mode((1080,720) , flags=RESIZABLE)


# add song
# mixer.music.load("src\Game\media\song.wav")
# mixer.music.play(-1)


# add background
# background = pygame.image.load("src\Game\media\safari_zone.gif")


#the coordinate corners of the window
# global MAXx ,MINx ,MAXy , MINy
MAXx = sys.float_info.min
MAXy = sys.float_info.min
MINy = sys.float_info.max
MINx = sys.float_info.max

#colors
WHITE = (255, 255, 255)
BLUE = (0 , 0 , 255)
GREY = (128,128,128)
BLACK = (0 , 0 , 0)
RED = (255, 0, 0)
VIOLET = (238,130,238)

# title of the graph
pygame.display.set_caption("Pokemon_Discover_Ariel")

FONT = pygame.font.SysFont("Ariel" , 42)


def scale(data , min_screen , max_screen , min_data , max_data):
    data_ratio = ((data - min_data) / (max_data - min_data))
    screen_ratio = ((max_screen - min_screen) + min_screen)
    return (data_ratio * screen_ratio)

def myScale(screen , data , x=False , y=False):
    if x:
        return scale(data , 50 , screen.get_width()-30 , MINx , MAXx )+10
    if y:
        return scale(data , 50 , screen.get_height()-30 , MINy , MAXy)+10

#find the extremum points 
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
    
#  draw the line and the arrow to show the directed edge 
def arrow(screen,start , end , basis , height , color ):
    dx = float(end[0] - start[0])
    dy = float(end[1] - start[1])
    BASIS = float(math.sqrt(dx * dx + dy * dy))
    xm = float(BASIS - basis)
    xn = float(xm)
    ym = float(height)
    yn = -height
    sin = dy / BASIS
    cos = dx / BASIS
    x = xm * cos - ym *sin + start[0]
    ym = xm * sin + ym *cos + start[1]
    xm = x
    x = xn * cos - yn * sin + start[0]
    yn = xn * sin + yn * cos + start[1]
    xn = x 
    points = [(end[0] , end[1]) , (int(xm) , int(ym)) , (int (xn) , int(yn))] 
    pygame.draw.line(screen , color , start , end , width=2 )
    pygame.draw.polygon(screen , color , points)

def draw_graph(screen,graph:DiGraph):

        # print a graph 
        node_map = graph
        findRatio(node_map)
        
        # the reference values for the data we get
        for id , node in node_map.get_all_v().items():

            # if there is a node without coordinates
            if node[0]==None or node[1]==None:
                node = ()
                node[0] = (3/4)*MAXx
                node[1] = (3/4)*MAXy
            
            # scale the coordinate of the node
            x = myScale(screen,node[0] ,x=True)
            y = myScale(screen,node[1] ,y=True)

            # add id near to the node 
            src_text = FONT.render(str(id) , True , BLACK )
            screen.blit(src_text , (x,y))

            # print(x,y)
            point = pygame.draw.circle(screen , BLACK , (x,y) , radius=7 )
            
            # run over the node connected to this node by a directed edge
            for dest in node_map.NodesMap[id].me_to_other:
                curr:Nodes
                curr = node_map.get_all_v()[dest]
            
                # scale the coordinate of the target node
                dest_x = myScale(screen,curr[0] , x=True)
                dest_y = myScale(screen,curr[1] , y=True)
                arrow(screen,(x,y) , (dest_x,dest_y) ,basis=14 , height=6 , color=BLUE )

def draw_pokemon(screen,pokemon_dict:Dict):                    
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemon_dict.values():
        p:PokeNode
        x = myScale(screen,p.pos[0],x=True)
        y = myScale(screen,p.pos[1],y=True)
        pygame.draw.circle(screen, Color(RED), (x,y), 10)

def draw_trainer(screen,trainer_dict:Dict):
     # draw agents
    for agent in trainer_dict.values():
        agent:PokeTrainer
        x = myScale(screen, agent.pos[0] ,x=True)
        y = myScale(screen,agent.pos[1] ,y=True)
        pygame.draw.circle(screen, Color(VIOLET),(x,y), 10)

# window drawer
def draw_window(screen,graph:DiGraph):
    pygame.init()

    screen.blit(background,(0,0))
    
    pygame.display.update()
    for event in pygame.event.get():
        # allow to quit the GUI
        if event.type == pygame.QUIT:
            pygame.quit()
        # allow to resize the screen
        elif event.type == VIDEORESIZE:
            screen  = pygame.display.set_mode(event.dict['size'] , HWSURFACE | DOUBLEBUF | RESIZABLE)

    draw_graph(graph)
    display.update()
    Clock.tick(60)

    
       
        
    
