from typing import Dict
from typing import Tuple



class Nodes:
    def __init__(self , id:int , pos:tuple ):
        self.id = id
        self.pos:Tuple[float,float,float] = pos
        self.other_to_me:Dict[int,(int,float)] = {}
        self.me_to_other:Dict[int,(int,float)] = {}
        self.weight=0
        self.tag=0
        self.prev=id
        self.dist=0
