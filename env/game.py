from env.deck import Deck

class Game:

    def __init__(self, n_players):
        self.deck = Deck()
        self.deck.shuffle_deck()

        self.players_initial_cards = []
        self.players_penalties_cards = []

        for _ in range(n_players):
            self.players_initial_cards.append([])
            self.players_penalties_cards.append([])

        # give 10 cards to players
        for _ in range(10):
            for p in range(n_players):
                self.players_initial_cards[p].append(self._get_next_card())

        # give 4 cards to the board
        self.board = [[], [], [], []]
        for k in range(4):
            self.board[k].append(self._get_next_card())


    def _get_next_card(self):
        return self.deck.cards.pop(0)
