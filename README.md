# Ex4_pokemon

## Theme
Forth assignement of the OOP course , we need to implement a "pokemon" game where we communicate with a server that update and give us data about trainer and pokemons on a given graph
We choose to implement this assgignement in python

## How to run
To run the game :
- 1. Download the file zip from the release 
- 2. Extract all the files in the zip
- 3. open a terminal/cmd from the directory and run <java -jar Ex4_Server_v0.0.jar x > where x is the number of the case you want to check [0-15] 
- 4. open a terminal from src/Game/
- 5. run python3 our_codes.py

## Structure 
[![uml.jpg](https://i.postimg.cc/dQy5VG7G/uml.jpg)](https://postimg.cc/t793rZNg)

The most Useful files in this assignement are :
- ### Graph/gui_graph.py this file create all the GUI from the json file that we get from the server with pygame
- ### All the files from the Graph directory that create the graph from the json files
- ### In the poke_files directory there is all the relevent files to handle the json files from the server and the process to find the best path to "catch them all":
> - poke_nodes.py represent pokemon
> - poke_trainer.py represent the trainer (agent)
> - game_boy.py represent the info/parameters for the game 
> - play.py manage all the data from the server and find on each edge lean pokemon , allocate pokemmon to the trainers etc..(the algorithm part)

- ### our_code.py :
this file is our "main" it is our executable file , the client that connect to the server and connect between every files 


## Algorithm 
- ### dispatch()
From the others assignement we already use the dijkstra algorithm to find the best path beetwen 2 nodes .
We use this algorithm to find for each trainer in the game the best path to all the pokemons . Once we get all those results we choose the better to be the target of the trainer until we reach the wanted pokemon.
It's possible that with multiple trainers there more than one trainer that want to reach the target , then we create a data that represent the ratio of the cost of the path  and the value of the targeted pokemon.
with this data we compare all the trainers once and choose the trainer with the best ratio . After that we reset the path and the cost of the rest of the trainers and repeat this until the pokemon list or the trainer list is empty.

- ### on_which_edge()
This function is used to find on wich edge the pokemon lean on , sometimes there two edge from node to another (a->b , b->a) then to differentiate the two of them the pokemon have type .
Knowing this to find the edge ok the pokemon , we calculate the geometric distance between all the nodes(a,b) and the pokemon(p) (a->b , p->b , p->a) , if the distance from the pokemone two the two other nodes is the same than the distance between the two nodes then the pokemon lean on the edge from two of them .


## Results
| Cases | Moves | Grade
| ----------- | ----------- | ----------- |
| 0 | 296 | 115 |
| 1 | 594 | 464 |
| 2 | 296 | 161 | 
| 3 | 599 | 613 |
| 4 | 293 | 200 |
| 5 | 588 | 576 |
| 6 | 296 | 79 |
| 7 | 596 | 302 |
| 8 | 286 | 125 |
| 9 | 576 | 458 |
| 10 | 286 | 104 |
| 11 | 520 | 1511 |
| 12 | 286 | 40 |
| 13 | 561 | 201 |
| 14 | 269 | 67 |
| 15 | 571 | 250 |

The results we get where with sleep time set to 0.090.
The computer specification : 8GB Ram , Processor(Intel(R) Core(TM) i5-8265U CPU @ 1.60GHz   1.80 GHz)

## pics 
[![exemple1.png](https://i.postimg.cc/HnyhfsPM/exemple1.png)](https://postimg.cc/kR7sS9CM)
[![exemple2.png](https://i.postimg.cc/qBNVspQ4/exemple2.png)](https://postimg.cc/vDwNMFpN)


## video
https://youtu.be/offNGf9Q0bA



