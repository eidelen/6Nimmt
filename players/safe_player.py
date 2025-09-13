import random
import heapq
from typing import Tuple, List

from env.arena import Arena, Player
from env.common import rank_best_cards_for_num

class SafePlayer(Player):

    def __init__(self):
        super().__init__()

    def call_select_card(self, cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]]) -> int:
        # this player tries to play the slot with the least cards

        ascending_slots= []
        for slot_idx in range(len(board)):
            slot_size = len(board[slot_idx])
            heapq.heappush(ascending_slots, (slot_size, slot_idx))

        # try to play a card on the best slot and then move to the second best, and so on...
        while len(ascending_slots) > 0:

            _, this_slot_idx = heapq.heappop(ascending_slots)
            top_num, _ = board[this_slot_idx][-1]

            # find a card to play that slot
            rank_best_cards = rank_best_cards_for_num(cards, top_num)
            if len(rank_best_cards) > 0:
                _, best_card_idx, _ = rank_best_cards[0]
                return best_card_idx

        # if no card to play choose random
        return random.randint(0, len(cards) - 1)
