
from typing import Dict
import pygame
import math
from pygame import Color, Rect, draw
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
YELLOW =(255, 255, 0)

# title of the graph
pygame.display.set_caption("Pokemon_Discover_Ariel")

FONT = pygame.font.SysFont("Ariel" , 32)


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
        pygame.draw.circle(screen, Color(YELLOW), (x,y), 10)
        if p.id == 0%4:
            pikachu = pygame.image.load("media\pikachu.png")
            pikachu = pygame.transform.scale(pikachu,(30,50))
            screen.blit(pikachu , (x-10 , y-10))
        elif p.id == 1%4:
            carapuce = pygame.image.load("media\carapuce.png")
            carapuce = pygame.transform.scale(carapuce,(30,50))
            screen.blit(carapuce , (x-10 , y-10))
        elif p.id ==2%4:
            bulbizar = pygame.image.load("media\pulbizar.png")
            bulbizar = pygame.transform.scale(bulbizar,(30,50))
            screen.blit(bulbizar , (x-10 , y-10))
        else:
            spectrum = pygame.image.load("media\spectrum.png")
            spectrum = pygame.transform.scale(spectrum,(30,50))
            screen.blit(spectrum , (x-10 , y-10))

def draw_trainer(screen,trainer_dict:Dict):
     # draw agents
    for agent in trainer_dict.values():
        agent:PokeTrainer
        x = myScale(screen, agent.pos[0] ,x=True)
        y = myScale(screen,agent.pos[1] ,y=True)
        
        pygame.draw.circle(screen, Color(RED),(x,y), 10)
        ash = pygame.image.load("media\sacha.png")
        ash = pygame.transform.scale(ash,(40,80))
        screen.blit(ash,(x-10,y-10))
        

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

# draw the data_info
def print_data(screen ,moves , grade , remain_time ) :
    # draw the moves
    font = pygame.font.SysFont("Alfa Slab One" , 24 , True , False  )
    moves_txt = 'Moves : ' + str(moves)
    surface_moves = font.render(moves_txt , True , BLACK)
    moves_rec = pygame.Rect(0 ,0 , 130 , 32)
    pygame.draw.rect(screen , WHITE , Rect(2,2,174,34))
    screen.blit(surface_moves,(15, 15) )
    pygame.draw.rect(screen , RED , Rect(0,0,180,40) , 4)
 
    

# draw the grades
    grade_txt = 'Grade : ' + str(grade)
    surface_grades = font.render(grade_txt , True , BLACK)
    grade_rec = pygame.Rect(0 ,34 , 130 , 64)
    pygame.draw.rect(screen , WHITE , Rect(2,42,174,34))
    screen.blit(surface_grades, (10, 50))
    pygame.draw.rect(screen , RED , Rect(0,40,180,40) , 4)


# draw the remain time
    time_txt = 'Remain time : ' + str(remain_time)
    surface_time = font.render(time_txt , True , BLACK)
    time_rec = pygame.Rect(0 ,64 , 130 , 86)
    pygame.draw.rect(screen , WHITE , Rect(182,2,174,34))
    screen.blit(surface_time,(190, 15))
    pygame.draw.rect(screen , RED , Rect(180,0,180,40) , 4)

class button():
    def __init__(self , color ,x , y , width , height , text ='') -> None:
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self , screen , outline = None):
        if outline:
            pygame.draw.rect(screen , self.color , (self.x-2 , self.y-2 ,self.width+4 , self.height+4),0)
        pygame.draw.rect(screen , self.color , (self.x , self.y , self.width , self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Impact', 30)
            text = font.render(self.text , 1 , (0,0,0))
            screen.blit(text , (210 , 55))
        
    def isOver(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

def redrawWindows(screen, button):
    button.draw(screen , (0,0,0))



