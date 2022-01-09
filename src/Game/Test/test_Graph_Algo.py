import unittest
from Game.Graph.di_graph import DiGraph 
from Game.Graph.graph_algo import GraphAlgo

class TestGraphAlgo(unittest.TestCase):
    

    def test_get_graph(self):
        test1 = GraphAlgo()
        test1.load_from_json("data/A0.json")
        self.assertEqual(type(test1.get_graph()),DiGraph)

    def test_load_from_json(self):
        test1 = GraphAlgo()
        self.assertEqual(test1.load_from_json("data/A0.json"),True)

    
    def test_save_to_json(self):
        test1 = GraphAlgo()
        self.assertEqual(test1.save_to_json("data/AX.json"),True)

    def test_shortest_path(self):
        test1 = GraphAlgo()
        test1.load_from_json("data/A0.json")
        
        weight1 = 4.341260707031816
        ans1 = [10, 0, 1, 2]
        self.assertEqual(test1.shortest_path(10,2),(ans1,weight1))


        self.assertEqual(test1.shortest_path(9,8),([9,8],1.4575484853801393))


    def test_centerPoint(self):
        test1 = GraphAlgo()
        test1.load_from_json("data/A0.json")
        ans1 = [7, 6.806805834715163]    
        self.assertEqual(test1.centerPoint(),ans1)

        test2 = GraphAlgo()
        test2.load_from_json("data/A1.json")
        ans2 = [8, 9.925289024973141]
        self.assertEqual(test2.centerPoint(),ans2)

        test3 = GraphAlgo()
        test3.load_from_json("data/A2.json")
        ans3 = [0, 7.819910602212574]
        self.assertEqual(test3.centerPoint(),ans3)



if __name__ == '__main__':
    unittest.main()