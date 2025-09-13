import unittest

from env.common import get_accumulated_stack_penalty, rank_best_cards_for_num

class TestCommon(unittest.TestCase):

    def test_accum_stack_penalties(self):
        self.assertEqual(get_accumulated_stack_penalty([(1, 3), (2, 6)] ), 9)

    def test_rank_cards(self):
        ranked_cards_idx = rank_best_cards_for_num([(8, 1), (11, 1), (10, 1), (12, 1), (7, 1)], 9)
        self.assertEqual(ranked_cards_idx, [(1, 2, 10), (2, 1, 11), (3, 3, 12)])
        ranked_cards_idx = rank_best_cards_for_num([(8, 1), (11, 1), (10, 1), (12, 1), (7, 1)], 13)
        self.assertEqual(ranked_cards_idx, [])

if __name__ == '__main__':
    unittest.main()
