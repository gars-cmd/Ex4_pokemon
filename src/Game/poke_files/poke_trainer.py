from typing import Dict, Tuple


class PokeTrainer:
    def __init__(self , id=0 , value=0 , src=0 , dest=0 , speed=1 , pos=(0,0,0)) -> None:
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
        self.target = [-1,-1]
        self.path = []


    def get_value(self) -> int :
        return self.value

    def get_pos(self) -> Tuple:
        return self.pos

    def get_id(self) -> int :
        return self.id

    def get_src(self) -> int:
        return self.src

    def get_dest(self) -> int:
        return self.dest

    def get_speed(self) ->float:
        return self.speed

    #  convert from dictionary to trainer 
    def dict_to_trainer(dict:Dict):
        value = int(dict['Agent'].get("value"))
        id = int(dict['Agent'].get("id"))
        src = int(dict['Agent'].get("src"))
        dest = int(dict['Agent'].get("dest"))
        speed = float(dict['Agent'].get("speed"))
        posS:str = dict['Agent'].get("pos")
        posS = posS.split(',')
        pos = (float(posS[0]) , float(posS[1]) , float(posS[2]))
        return PokeTrainer(id=id , value=value , src=src , dest=dest , speed=speed , pos=pos)