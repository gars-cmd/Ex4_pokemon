import unittest
from Game.poke_files.game_boy import GameBoy
from Game.poke_files.play import Play
from Game.poke_files.poke_node import PokeNode
from Game.poke_files.poke_trainer import PokeTrainer
import json

class TestGraphAlgo(unittest.TestCase):

    def pokemon_test(self):

        file_poke = json.loads("pokemon.json")
        pokemon = PokeNode.dict_to_poke(file_poke)
        self.assertEqual(pokemon.get_value(),5.0)
        self.assertEqual(pokemon.get_type,-1)

    def trainer_test(self):
        file_trainer = json.loads("trainer.json")
        trainer = PokeTrainer.dict_to_trainer(file_trainer)
        self.assertEqual(trainer.get_dest(),1)
        self.assertEqual(trainer.get_id(),0)
        self.assertEqual(trainer.get_src(),0)
        self.assertEqual(trainer.get_value(),0.0)

    def game_boy_test(self):
        file_game = json.loads("server.json")
        game = GameBoy.dict_to_game(file_game)
        self.assertEqual(game.get_grade(),0)
        self.assertEqual(game.get_id(),0)
        self.assertEqual(game.get_is_logged_in(),False)
        self.assertEqual(game.get_pokemons(),1)
        self.assertEqual(game.get_moves(),1)
        self.assertEqual(game.get_agents(),1)







if __name__ == '__main__':
    unittest.main()