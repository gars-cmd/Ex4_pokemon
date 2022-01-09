import unittest
from Game.Graph.di_graph import DiGraph
from Game.Graph.graph_algo import GraphAlgo

class TestDiGraph(unittest.TestCase):
    

    def test_v_size(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph 
        self.assertEqual(graph_test.v_size(),11)   

        graph_test.remove_node(2)
        self.assertEqual(graph_test.v_size(),10)

        graph_test.add_node(12,(1,1,1))
        graph_test.add_node(13,(1,2,3))
        self.assertEqual(graph_test.v_size() , 12)


    def test_e_size(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph
        self.assertEqual(graph_test.e_size(),22)

        graph_test.remove_edge(10,0)
        graph_test.remove_edge(9,10)
        self.assertEqual(graph_test.e_size(),20)

        graph_test.add_edge(8,4,1)
        graph_test.add_edge(8,5,1)
        graph_test.add_edge(5,7,1)
        self.assertEqual(graph_test.e_size(),23)


    def test_get_all_v(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph
        
        reference = []
        for i in range(11):
            reference.append(i)
        
        for key in graph_test.get_all_v():
            self.assertEqual(reference[key],key)
        

        for key,values in graph_test.get_all_v().items():
                self.assertEqual(type(key),int)
                self.assertEqual(type(values),tuple)
                for key in values:
                    self.assertEqual(type(values[0]),float)
                    self.assertEqual(type(values[1]),float)
                    self.assertEqual(type(values[2]),float)

        graph_test.remove_node(9)

        for key in graph_test.get_all_v():
            self.assertEqual(reference[key],key)


    def test_all_in_edges_of_node(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph

        zero_list = [(1,1.8884659521433524) , (10,1.1761238717867548)]
        i = 0 
        for key , values in graph_test.all_in_edges_of_node(0).items():
            self.assertEqual(values , zero_list[i])
            i+=1
        
        five_list = [(4,1.9442789961315767),(6, 1.6677173820549975)]
        j = 0
        for key , values in graph_test.all_in_edges_of_node(5).items():
            self.assertEqual(values , five_list[j])
            j+=1
            

    def test_all_out_edges_of_node(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph
        zero_list = [(1,1.4004465106761335),(10,1.4620268165085584)]
        five_list = [(4,1.4622464066335845),(6,1.160662656360925)]
        
        i = 0
        j = 0
        for key , values in graph_test.all_out_edges_of_node(0).items():
            self.assertEqual(values , zero_list[i])
            i+=1
        for key , values in graph_test.all_out_edges_of_node(5).items():
            self.assertEqual(values , five_list[j])
            j+=1
        
        
    def test_get_mc(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph
        actual = graph_test.get_mc()
        
        graph_test.remove_edge(8,7)
        self.assertEqual(graph_test.get_mc(),actual+1)

        graph_test.remove_edge(4,5)
        self.assertEqual(graph_test.get_mc(),actual+2)


    def test_add_edge(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph
        

        graph_test.add_edge(9,3,1)
        self.assertEqual(graph_test.all_out_edges_of_node(9)[3],(3,1))

        graph_test.add_edge(3,10,2)
        self.assertEqual(graph_test.all_in_edges_of_node(10)[3],(3,2))

        graph_test.add_edge(5,8,3)
        self.assertEqual(graph_test.all_in_edges_of_node(8)[5],(5,3))

    
    def test_add_node(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph

        point = (35.55555,35.55556,35.55557)
        graph_test.add_node(12,point)

        self.assertEqual(graph_test.v_size(),12)
        self.assertEqual(graph_test.get_all_v()[12],point)


    def test_remove_node(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph

        graph_test.remove_node(9)
        self.assertEqual(graph_test.v_size(),10)
        self.assertEqual((len(graph_test.all_out_edges_of_node(10))),1)
        self.assertEqual((len(graph_test.all_out_edges_of_node(8))),1)



    def test_remove_edge(self):
        test1 = GraphAlgo()
        test1.load_from_json("A0.json")
        graph_test = test1.get_graph()
        graph_test:DiGraph

        graph_test.remove_edge(4,5)
        self.assertEqual(graph_test.e_size() , 21)
        self.assertEqual(len(graph_test.all_out_edges_of_node(4)),1)

        graph_test.remove_edge(4,3)
        self.assertEqual(graph_test.e_size() , 20)
        self.assertEqual(len(graph_test.all_out_edges_of_node(4)),0)
        

if __name__ == '__main__':
    unittest.main()
        
        
        