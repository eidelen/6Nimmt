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
        all_penalty_cards = [[(90, 1)], [], [], [(95, 1), (98, 1)]] # they were seen when played

        # before play, no cards were seen
        for i in range(1, 105):
            self.assertFalse(m_player._was_card_played(i))

        _ = m_player.call_select_card(cards, boards, all_penalty_cards)

        # check if all cards were memorized which are visible to the player
        played_cards = [(10, 1), (20, 1), (30, 1), (15, 1), (16, 1), (19, 1), (50, 1), (51, 1), (60, 1), (61, 1), (90, 1), (95, 1), (98, 1)]

        for n, p in played_cards:
            self.assertTrue(m_player._was_card_played(n))

        # add a new card and check again
        boards2 = [[(13, 1), (16, 1)], [(19, 1)], [(50, 1), (51, 1)], [(60, 1), (61, 1)]]
        _ = m_player.call_select_card(cards, boards2, all_penalty_cards)
        played_cards2 = [(10, 1), (20, 1), (30, 1), (15, 1), (16, 1), (19, 1), (50, 1), (51, 1), (60, 1), (61, 1),
                        (90, 1), (95, 1), (98, 1), (13, 1)]

        for n, p in played_cards2:
            self.assertTrue(m_player._was_card_played(n))




if __name__ == '__main__':
    unittest.main()
