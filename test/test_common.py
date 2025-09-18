import unittest

from env.common import get_accumulated_stack_penalty, rank_best_cards_for_num, nbr_cards_between_a_and_b

class TestCommon(unittest.TestCase):

    def test_accum_stack_penalties(self):
        self.assertEqual(get_accumulated_stack_penalty([(1, 3), (2, 6)] ), 9)

    def test_rank_cards(self):
        ranked_cards_idx = rank_best_cards_for_num([(8, 1), (11, 1), (10, 1), (12, 1), (7, 1)], 9)
        self.assertEqual([(0, 2, 10), (1, 1, 11), (2, 3, 12)], ranked_cards_idx)
        ranked_cards_idx = rank_best_cards_for_num([(8, 1), (11, 1), (10, 1), (12, 1), (7, 1)], 13)
        self.assertEqual([], ranked_cards_idx)

    def test_diff_cards(self):
        self.assertEqual(nbr_cards_between_a_and_b( 1, 4), 2)  # 2, 3 in between
        self.assertEqual(nbr_cards_between_a_and_b(1, 2), 0)  # no card in bet
        self.assertEqual(nbr_cards_between_a_and_b(1, 1), -1)  # invalid
        self.assertEqual(nbr_cards_between_a_and_b(4, 2), -1)  # invalid
        self.assertEqual(nbr_cards_between_a_and_b(1, 4, {3: True, 5: True}), 1)  # 2 in between, as 3 already seen


if __name__ == '__main__':
    unittest.main()
