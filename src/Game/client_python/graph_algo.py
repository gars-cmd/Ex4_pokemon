from typing import List, Tuple

# from src.Game.client_python import gui_graph
import GraphInterface
import GraphAlgoInterface
from src.Game.client_python.di_graph import DiGraph
# from src.Game.client_python.node_class import Nodes
import json
from src.Game.client_python import gui_graph
from src.Game.client_python.node_class import Nodes


class GraphAlgo():
    
    # constructor
    def __init__(self,graph:DiGraph=None) -> None:
        GraphAlgoInterface.__init__(self)
        if graph == None: 
            self.diGraph:DiGraph = DiGraph()
        else:
            self.diGraph = graph

            
    # return the graph from graphAlgo
    def get_graph(self) -> GraphInterface:     
        return self.diGraph
    
    #  load json file to graph
    def load_from_json(self, file_name) -> bool:
        self.diGraph= DiGraph()
        try:
            # f = open(file_name)
            datas = json.loads(file_name)
            for node in datas['Nodes']:
                #split and cast location values
                try:
                    values = node['pos'].split(",")
                    pos = (float(values[0]) , float(values[1]) , float(values[2]))
                except:
                    pos = (None,None,None)
                self.diGraph.add_node(node['id'],pos)
            for edge in datas['Edges']:
                self.diGraph.add_edge(edge['src'],edge['dest'],edge['w'])

            #f.close()
            return True
        except:
            return False
       
    # save the graph to a json file  
    def save_to_json(self, file_name: str) -> bool:
        
        
            
        # initialize temp List for nodes and edges 
        node_list:List[Nodes] = []
        edges_list:List[Tuple] = []
        dic_graph = {}
        
        # run over the nodes in the graph +
        for id in self.get_graph().get_all_v():
            node_dict = {}
            
            # convert pos from float tuple to string
            curr_pos = self.get_graph().get_all_v()[id]
            
            phrase = str(curr_pos[0])
            phrase+=','
            phrase+=str(curr_pos[1])
            phrase+=','
            phrase+=str(curr_pos[2])
            
            # add the node with his personnal element into the list 
            node_dict["id"] = id
            node_dict["pos"] = phrase
            node_list.append(node_dict)
            
            # run over the edges from the node to those it points to
            for edges in self.get_graph().all_out_edges_of_node(id):
                edge_dic = {}
                
                # add the values to the edges list 
                edge_dic["src"] = id
                edge_dic["w"] = self.get_graph().all_out_edges_of_node(id)[edges][1]
                edge_dic["dest"] = edges
                edges_list.append(edge_dic)
                
        # add the lists to the main dic that represent the entire graph
        dic_graph["Edges"] = edges_list
        dic_graph["Nodes"] = node_list
        
        # write the data into the target file
        try: 
            with open (file_name , 'w') as f:
                json.dump(dic_graph,f)
                return True
        except:
            return False
  
    def shortest_path(self, src: int, dest: int) -> (float, list):

        return self.dijikstra(src,dest)[0]

    def centerPoint(self) -> (int, float):
        if self.isConnected() == False:
            return -1
        else:
            temID = -1
            tempList={}
            tempOption={}
            for src,node1 in self.diGraph.get_all_v().items():
                max = -1
                
                tempOption = self.dijikstra(src,None)[1]
                
                
                for key in tempOption:
                        
                    if tempOption[key]>max:
                        max = tempOption[key]
                                        
                        tempList[src] = max
            minWeight=float('inf')
            
            ans = -1
            for center,weight in tempList.items():
                if weight<minWeight:
                    minWeight=weight
                    ans = center
            return(ans,minWeight)

    def dijikstra(self, src:int, dest:int):
        if dest == None:
            dest = src+3
            dest = (dest*2)%self.get_graph().v_size()
        test=self.diGraph
        mylist_ver=[]
        ans=[]
        weight_dic = {}
        if dest == src:
            return (float('inf'),[])
        if len(test.NodesMap[src].me_to_other) == 0:
            return (float('inf'),[])
       
        
        for id,node in test.get_all_v().items():
            test.NodesMap[id].tag=0
            test.NodesMap[id].weight= float('inf')
            test.NodesMap[id].dist=0
              
        test.NodesMap[src].weight=0
        test.NodesMap[src].tag=1

        mylist_ver.append(test.NodesMap[src].id)
    
        test.NodesMap[src].prev=src
        while(len(mylist_ver)):
           
            nodeTemp=mylist_ver.pop(0)

            for id,weight in test.NodesMap[nodeTemp].me_to_other.items():

                tempWeight=test.NodesMap[nodeTemp].weight+weight[1]
                if (tempWeight<test.NodesMap[id].weight):
                    test.NodesMap[id].weight=tempWeight
                    weight_dic[id] = tempWeight
                    test.NodesMap[id].prev=test.NodesMap[nodeTemp].id
                if(test.NodesMap[id].tag!=1):    
                    mylist_ver.insert(len(mylist_ver),id)

            test.NodesMap[nodeTemp].tag=1

        boolean=True
        ans.append(dest)
        tempONlist=dest
        while(boolean):
                
            ans.append(test.NodesMap[tempONlist].prev)
            if tempONlist== test.NodesMap[tempONlist].prev:
                break
            tempONlist = test.NodesMap[tempONlist].prev
            
            if(tempONlist==src):

                boolean=False

        
        ans.reverse()
        
        
        return (test.NodesMap[dest].weight,ans),weight_dic

    def plot_graph(self) -> None:
        gui_graph.main(self.get_graph())


    def BFS(self,graph , s:int):
        # initialize all the nodes to be in tag=0 as !visited
        for key , node in graph.NodesMap.items():
            node:Nodes
            node.tag=0
        
        queue = []
        queue.append(s)
        graph.NodesMap[s].tag = 1

        while queue:
            s = queue.pop(0)
            

            for i in graph.NodesMap[s].me_to_other:
                if graph.NodesMap[i].tag==0:
                    queue.append(i)
                    graph.NodesMap[i].tag = 1


    def isConnected(self):
        
        self.BFS(self.get_graph() , next(iter(self.get_graph().NodesMap)))
        for key,nodes in self.get_graph().NodesMap.items():
            if nodes.tag == 0:
                return False
        
        reverse_NodesMap = {}
        for key , nodes in self.get_graph().NodesMap.items():
            reverse_NodesMap[key] = Nodes(key,nodes.pos)
            reverse_NodesMap[key].me_to_other = self.get_graph().NodesMap[key].other_to_me
            reverse_NodesMap[key].other_to_me = self.get_graph().NodesMap[key].me_to_other

        reverseGRaph = DiGraph()
        reverseGRaph.NodesMap = reverse_NodesMap

        self.BFS(reverseGRaph,next(iter(self.get_graph().NodesMap)))
        for key,nodes in reverseGRaph.NodesMap.items():
            if nodes.tag == 0:
                return False
        
        return True


if __name__ == "__main__":
    graphT = GraphAlgo()
    graphT.load_from_json("src\Game\Graph\A0.json")
    graphT.plot_graph()