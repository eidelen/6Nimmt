import unittest
from env.deck import Deck


class TestDeck(unittest.TestCase):

    def test_deck_number(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 104)

    def test_that_all_card_are_there(self):
        mandatory_idx = {}
        for i in range(1, 105):
            mandatory_idx[i] = False

        deck = Deck()

        for nbr, pen in deck.cards:
            self.assertGreater(nbr, 0)
            self.assertLess(nbr, 105)
            self.assertGreater(pen, 0)
            self.assertLess(pen, 8)

            already_seen = mandatory_idx[nbr]
            self.assertFalse(already_seen)
            mandatory_idx[nbr] = True

        # check that all cards has been seen
        for i in range(1, 105):
            self.assertTrue(mandatory_idx[i])

    def __find_card(self, card_list, card_nbr):
        for i in range(0, 104):
            n, p = card_list[i]
            if n == card_nbr:
                return card_list[i]
        return None

    def test_some_special_cards(self):
        deck = Deck()

        penalty_1 = (1, 14, 27, 36, 48, 54, 61, 78, 82, 97, 104)
        for i in penalty_1:
            _, p = self.__find_card(deck.cards, i)
            self.assertEqual(p, 1)

        penalty_2 = (5, 15, 25, 35, 45, 65, 75, 85, 95)
        for i in penalty_2:
            n, p = self.__find_card(deck.cards, i)
            self.assertEqual(p, 2)

        penalty_5 = (11, 22, 33, 44, 66, 77, 88, 99)
        for i in penalty_5:
            _, p = self.__find_card(deck.cards, i)
            self.assertEqual(p, 5)

        _, p = self.__find_card(deck.cards, 55)
        self.assertEqual(p, 7)

if __name__ == '__main__':
    unittest.main()
