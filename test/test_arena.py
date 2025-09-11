import unittest
from env.arena import Arena, Player
from typing import Tuple, List

class TestPlayer(Player):

    def __init__(self):
        super().__init__()
        self.cnt_calls = 0

    def call_select_card(self, cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]]) -> int:
        # count the calls and always select the first card
        self.cnt_calls += 1
        return 0


class TestArena(unittest.TestCase):

    def test_arena_basic(self):

        test_player_a = TestPlayer()
        test_player_b = TestPlayer()
        test_player_c = TestPlayer()
        test_player_d = TestPlayer()

        arena = Arena([test_player_a, test_player_b, test_player_c, test_player_d])

        self.assertEqual(test_player_a.cnt_calls, 0)
        self.assertEqual(test_player_b.cnt_calls, 0)

        penalties = arena.play()

        self.assertEqual(test_player_a.cnt_calls, 10)
        self.assertEqual(test_player_b.cnt_calls, 10)

        self.assertGreater(max(penalties), 0)


if __name__ == '__main__':
    unittest.main()
