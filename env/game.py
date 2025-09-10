import heapq
from typing import Tuple, List

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

    def step_players_choose_cards(self, cards) -> Tuple[bool, List[int]]:
        """
        Simulates a plays round.
        :param cards: Chosen Card indices
        :return: Bool if play ongoing or ended, accumulated penalites for each player
        """
        sorted_actions = []
        for player_idx in range(len(cards)):
            chosen_card_idx = cards[player_idx]
            chosen_card_number, _ = self.players_cards[player_idx][chosen_card_idx]
            heapq.heappush(sorted_actions, (chosen_card_number, chosen_card_idx, player_idx))

        # process actions
        while len(sorted_actions) > 0:
            chosen_card_number, chosen_card_idx, player_idx = sorted_actions.pop(0)
            card_to_play = self.players_cards[player_idx].pop(chosen_card_idx)
            self._insert_card(card_to_play, player_idx)

        # create return values
        play_ongoing = len(self.players_cards[0]) > 0
        current_penalties = []
        for player_idx in range(len(self.players_penalties_cards)):
            current_penalties.append(self._get_accumulated_stack_penalty(self.players_penalties_cards[player_idx]))

        return play_ongoing, current_penalties

    def _insert_card(self, card, player_idx):
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
            # no valid slot could be found for card -> take the stack with lowest penalty and place card there
            replace_slot_idx = self._get_slot_with_lowest_penalty()
            self._move_slot_cards_to_players_penalty(replace_slot_idx, player_idx)
            self.board[replace_slot_idx].append(card)
            return

        num_of_cards_in_slot = len(self.board[best_slot_idx])
        if num_of_cards_in_slot > 4:
            # reached the sixth card!
            self._move_slot_cards_to_players_penalty(best_slot_idx, player_idx)

        # add played card to the slot
        self.board[best_slot_idx].append(card)
        return

    def _move_slot_cards_to_players_penalty(self, slot_idx, player_idx):
        while len(self.board[slot_idx]) > 0:
            self.players_penalties_cards[player_idx].append(self.board[slot_idx].pop(0))

    def _get_accumulated_stack_penalty(self, stack):
        sum_penalty = 0
        for _, penalty in stack:
            sum_penalty += penalty
        return sum_penalty

    def _get_slot_with_lowest_penalty(self):
        lowest_penalty = 100
        lowest_penalty_idx = -1
        for slot_idx in range(len(self.board)):
            penalty = self._get_accumulated_stack_penalty(self.board[slot_idx])
            if penalty < lowest_penalty:
                lowest_penalty = penalty
                lowest_penalty_idx = slot_idx
        return lowest_penalty_idx


