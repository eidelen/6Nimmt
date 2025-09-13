import unittest

from env import game
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

    def test_slot_penalty_functions(self):
        game = Game(2)
        game.board[1] = [(1, 3), (2, 6)] # penalty sum is 9
        game.board[0] = [(5, 3), (2, 6)]
        game.board[2] = [(80, 1), (81, 1)] # this is the slot with lowest penalty
        game.board[3] = [(90, 3), (91, 6)]
        self.assertEqual(game._get_slot_with_lowest_penalty(), 2)

    def test_move_slot_to_players_penalty(self):
        game = Game(2)
        game.board[0] = [(5, 3), (6, 6)]
        game.board[1] = [(1, 3), (2, 6)]    # penalty sum is 9
        game.board[2] = [(80, 1), (81, 1)]  # this is the slot with lowest penalty
        game.board[3] = [(90, 3), (91, 6)]

        self.assertEqual(game.players_penalties_cards[0], [])
        game._move_slot_cards_to_players_penalty(2, 0)
        self.assertEqual(game.players_penalties_cards[0],  [(80, 1), (81, 1)] )

    def test_insert_card(self):
        game = Game(2)
        game.board[0] = [(10, 3)]
        game.board[1] = [(20, 3)]
        game.board[2] = [(50, 1)]
        game.board[3] = [(90, 3), (91, 6)]
        self.assertEqual(game.board[0], [(10, 3)])
        game._insert_card((11, 0), 0)
        self.assertEqual(game.board[0], [(10, 3), (11, 0)])
        game._insert_card((12, 0), 0)
        game._insert_card((13, 0), 0)
        game._insert_card((14, 0), 0)
        self.assertEqual(game.board[0], [(10, 3), (11, 0), (12, 0), (13, 0), (14, 0)])
        game._insert_card((15, 0), 0)
        self.assertEqual(game.board[0], [(15, 0)])
        self.assertEqual(game.players_penalties_cards[0], [(10, 3), (11, 0), (12, 0), (13, 0), (14, 0)])

    def test_choose_cards(self):
        game = Game(2)
        game.board[0] = [(10, 3)]
        game.board[1] = [(20, 3)]
        game.board[2] = [(50, 1)]
        game.board[3] = [(90, 3), (91, 6)]

        game.players_cards[0] = [(11, 1), (12, 4), (14, 2), (16, 1)]
        game.players_cards[1] = [(13, 3), (52, 2), (15, 1), (17, 2)]

        # player 1 chooses card 1, player 2 chooses card 0
        game.step_players_choose_cards([1, 0])

        self.assertEqual(game.players_cards[0], [(11, 1), (14, 2), (16, 1)])
        self.assertEqual(game.players_cards[1], [(52, 2), (15, 1), (17, 2)])
        self.assertEqual(game.board[0], [(10, 3), (12, 4), (13, 3)])
        self.assertEqual(game.board[1], [(20, 3)])
        self.assertEqual(game.board[2], [(50, 1)])
        self.assertEqual(game.board[3], [(90, 3), (91, 6)])

        game.step_players_choose_cards([1, 1])

        self.assertEqual(game.players_cards[0], [(11, 1), (16, 1)])
        self.assertEqual(game.players_cards[1], [(52, 2), (17, 2)])
        self.assertEqual(game.board[0], [(10, 3), (12, 4), (13, 3), (14, 2), (15, 1)])
        self.assertEqual(game.board[1], [(20, 3)])
        self.assertEqual(game.board[2], [(50, 1)])
        self.assertEqual(game.board[3], [(90, 3), (91, 6)])

        game.step_players_choose_cards([1, 1])
        # player 0 reaches 6nimmt

        self.assertEqual(game.players_cards[0], [(11, 1)])
        self.assertEqual(game.players_cards[1], [(52, 2)])
        self.assertEqual(game.board[0], [(16, 1), (17, 2)])
        self.assertEqual(game.board[1], [(20, 3)])
        self.assertEqual(game.board[2], [(50, 1)])
        self.assertEqual(game.board[3], [(90, 3), (91, 6)])

        self.assertEqual(game.players_penalties_cards[0], [(10, 3), (12, 4), (13, 3), (14, 2), (15, 1)])
        self.assertEqual(game.players_penalties_cards[1], [])

    def test_game_over_return(self):
        game = Game(2)
        game.board[0] = [(10, 3)]
        game.board[1] = [(20, 3)]
        game.board[2] = [(50, 1)]
        game.board[3] = [(90, 3), (91, 6)]

        game.players_cards[0] = [(11, 1), (13, 4), (15, 2), (17, 1)]
        game.players_cards[1] = [(12, 3), (14, 2), (16, 1), (18, 2)]

        for i in range(2):
            game_on, penalties = game.step_players_choose_cards([0, 0])
            self.assertTrue(game_on)
            self.assertEqual(penalties, [0, 0])

        game_on, penalties = game.step_players_choose_cards([0, 0])
        self.assertTrue(game_on)
        self.assertEqual(penalties, [13, 0])

        game_on, penalties = game.step_players_choose_cards([0, 0])
        self.assertFalse(game_on)



if __name__ == '__main__':
    unittest.main()
