import unittest
from env.game import Game


class TestGame(unittest.TestCase):

    def test_game_creation(self):
        game = Game(2)

        # go through all the cards
        n_cards = len(game.deck.cards)
        for _ in range(n_cards):
            n, p = game._get_next_card()
            self.assertLess(n, 105)
            self.assertGreater(n, 0)

        # there should be no elements left in the stack
        self.assertEqual(0, len(game.deck.cards))

    def test_game_initial(self):
        game = Game(2)

        self.assertEqual(len(game.players_cards), 2)
        self.assertEqual(len(game.players_penalties_cards), 2)
        self.assertEqual(len(game.players_cards[0]), 10)
        self.assertEqual(len(game.players_cards[1]), 10)

        self.assertEqual(len(game.board), 4)
        self.assertEqual(len(game.board[0]), 1)
        self.assertEqual(len(game.board[1]), 1)
        self.assertEqual(len(game.board[2]), 1)
        self.assertEqual(len(game.board[3]), 1)





if __name__ == '__main__':
    unittest.main()
