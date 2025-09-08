import random

class Deck:

    cards = []

    def __init__(self):
        self.cards = []
        for i in range(1, 105):
            self.cards.append( (i, 1) )

        # overwrite special cards
        for k in range(1, 11):
            self.__overwrite_card(k * 10, 3)
        for q in range(1, 10):
            self.__overwrite_card(q * 11, 5)
        for z in range(0, 10):
            self.__overwrite_card(5 + z*10, 2)

        self.__overwrite_card(55, 7)

    def __overwrite_card(self, number, penalty):
        # can only be called on initial set
        # check idx...
        idx = number-1
        assert idx < len(self.cards)
        set_nbr, _ = self.cards[idx]
        assert set_nbr == number
        self.cards[idx] = (number, penalty)

    def shuffle_deck(self):
        random.shuffle(self.cards)



