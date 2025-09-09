import heapq
from env.deck import Deck

class Game:

    def __init__(self, n_players):

        nbr_of_cards_per_player = 10
        nbr_of_board_slots = 4

        self.deck = Deck()
        self.deck.shuffle_deck()

        self.players_cards = []
        self.players_penalties_cards = []

        for _ in range(n_players):
            self.players_cards.append([])
            self.players_penalties_cards.append([])

        # give 10 cards to players
        for _ in range(nbr_of_cards_per_player):
            for p in range(n_players):
                self.players_cards[p].append(self._get_next_card())

        # give 4 cards to the board
        self.board = []
        for k in range(nbr_of_board_slots):
            self.board.append([self._get_next_card()])

    def _get_next_card(self):
        return self.deck.cards.pop(0)

    def get_players_cards(self):
        return self.players_cards.copy()

    def step_players_choose_cards(self, cards):
        sorted_actions = []
        for player_idx in range(len(cards)):
            chosen_card_idx = cards[player_idx]
            chosen_card_number, _ = self.players_cards[player_idx][chosen_card_idx]
            heapq.heappush(sorted_actions, (chosen_card_number, chosen_card_idx, player_idx))

        # process actions
        while len(sorted_actions) > 0:
            chosen_card_number, chosen_card_idx, player_idx = sorted_actions[0]
            card_to_play = self.players_cards[player_idx][chosen_card_idx]
            self.insert_card(card_to_play)

        return sorted_actions

    def insert_card(self, card, player_idx):
        # find best slot to insert -> smallest positive difference
        card_num, card_pen = card
        best_slot_idx = -1
        best_slot_diff = 200
        for slot_idx in range(len(self.board)):
            # get last card
            num, _ = self.board[slot_idx][-1]
            diff = card_num - num

            # card to add must be larger than card in slot
            if 0 < diff < best_slot_diff:
                best_slot_diff = diff
                best_slot_idx = slot_idx

        if best_slot_idx < 0:
            # no slot could be found for card -> player action needed
            return False

        # insert card into determined slot
        num_of_cards_in_slot = len(self.board[best_slot_idx])
        if num_of_cards_in_slot > 5:
            # put all cards in that stack to the players penalty stack
            while len(self.board[best_slot_idx]) > 0:
                self.players_penalties_cards[player_idx].append(self.board[best_slot_idx].pop())

        # add played card to the slot
        self.board[best_slot_idx].append(card)
        return True




