from typing import Dict, Tuple


class PokeNode:

    def __init__(self , value=0 , type=0 , pos=(0,0,0)) -> None:
        self.pos:Tuple[float,float,float] = pos
        self.value = value
        self.type = type
        self.id = -1

    def get_value(self) -> int :
        return self.value
        
    def get_type(self) -> int:
        return self.type

    def get_pos(self) -> Tuple:
        return self.pos

    # convert from dictionary to pokemon
    def dict_to_poke(dict:Dict):
        value = int(dict['Pokemon'].get('value'))
        type = int(dict['Pokemon'].get('type'))
        posS:str = dict['Pokemon'].get('pos')
        posS = (posS.split(','))
        pos = (float(posS[0]) , float(posS[1]) , float(posS[2]))
        return PokeNode(value=value , type=type , pos=pos)
    
    