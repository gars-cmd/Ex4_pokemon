from typing import Dict
from src.Game.client_python.GraphInterface import GraphInterface
from src.Game.client_python.node_class import Nodes
import random


class DiGraph(GraphInterface):
    
    # constructor
    def __init__(self) -> None:
        GraphInterface.__init__(self)
        self.NodesMap:Dict[int,Nodes] = {}
        self.nbrNodes = 0
        self.nbrEdges = 0
        self.mc = 0

    def __str__(self):
        return f'DiGraph |V|={self.nbrNodes}, |E|={self.nbrEdges}'

    def __repr__(self):
        return f'DiGraph(|V|={self.nbrNodes}, |E|={self.nbrEdges})'
           
    # return number of vertices in the graph
    def v_size(self) -> int:
        return self.nbrNodes


    # return the numbers of edges in the graph
    def e_size(self) -> int:
        return self.nbrEdges


    # return a dictionnary of all the nodes in the graph
    def get_all_v(self) -> dict:
        nodeList ={}
        # create the dic that contain our answer
        for nodes in self.NodesMap:
            curr_tuple = (self.NodesMap[nodes].pos )
            nodeList[nodes] = curr_tuple
            
        return nodeList
    
    # return à dictionnary of all the edges to the node
    def all_in_edges_of_node(self, id1: int) -> dict:
        node = self.NodesMap[id1]
        return node.other_to_me


    # return a dictionnary of all the edges from the node
    def all_out_edges_of_node(self, id1: int) -> dict:
        node = self.NodesMap[id1]
        return node.me_to_other
    
    # return the number of modification made on the graph  
    def get_mc(self) -> int:
        return self.mc
    
    # add edge to the graph
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 in self.NodesMap and id2 in self.NodesMap:
            edge = (id1 , id2 , weight)
            node1 = self.NodesMap[id1]
            node2 = self.NodesMap[id2]
            node2.other_to_me[id1] = (id1,weight)
            node1.me_to_other[id2] = (id2,weight)
            self.nbrEdges+=1
            self.mc+=1
            return True
        else:
            return False
        
    # add node to the graph    
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.NodesMap:
            return False
        # if the node don't have pos then we create one randomaly
        if pos==(None,None,None) or pos == None:
           x = random.uniform(35.187 , 35.208)
           y = random.uniform(32.101 , 32.108)
           z = 0.0
           pos = (x,y,z)
        
        node = Nodes(node_id,pos)
        self.NodesMap[node_id] = node
        self.nbrNodes+=1
        self.mc+=1
        return True
        
    # remove node from the graph
    def remove_node(self , node_id: int ) ->bool:
        if node_id in self.NodesMap:
            node = self.NodesMap[node_id]
            for key in node.other_to_me:
                curr = self.NodesMap[key]
                curr.me_to_other.pop(node_id)
                self.nbrEdges-=1
            for key in node.me_to_other:
                curr = self.NodesMap[key]
                curr.other_to_me.pop(node_id)
                self.nbrEdges-=1
            self.NodesMap.pop(node_id)
            self.nbrNodes-=1
            self.mc+=1
            return True
        else:
            return False

 
                
    #remove edge from the graph
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        node1 = self.NodesMap[node_id1]
        if node_id2 in node1.me_to_other:
            node1.me_to_other.pop(node_id2)
            self.nbrEdges-=1
            self.mc+=1
            return True
        else:
            return False
            