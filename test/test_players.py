import unittest

from env import game
from players.safe_player import SafePlayer
from players.cardcounting_player import CardCountingPlayer

class TestPlayers(unittest.TestCase):

    def test_safe_player(self):
        s_player = SafePlayer()

        cards = [(10, 1), (20, 1), (30,1)]
        boards = [ [(15, 1), (16, 1)], [(19, 1)], [(50, 1), (51, 1)] , [(60, 1), (61, 1)] ]
        all_penalty_cards = [[(90, 1)], [], [], [(95, 1), (98, 1)]]
        card_idx = s_player.call_select_card(cards, boards, all_penalty_cards)

        # SafePlayer would choose to play on slot 1 because there are the least cards. It would choose card 20 -> idx 1
        self.assertEqual(card_idx, 1)

    def test_memorize_played_cards(self):
        m_player = CardCountingPlayer()
        cards = [(10, 1), (20, 1), (30, 1)]
        boards = [[(15, 1), (16, 1)], [(19, 1)], [(50, 1), (51, 1)], [(60, 1), (61, 1)]]
        all_penalty_cards = [[(90, 1)], [], [], [(95, 1), (98, 1)]]
        pass




if __name__ == '__main__':
    unittest.main()
