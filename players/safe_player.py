import random
import heapq
from env.arena import Arena, Player
from typing import Tuple, List

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
            lowest_diff = 100
            lowest_card_idx = -1
            for card_idx in range(len(cards)):
                card_num, _ = cards[card_idx]
                diff = card_num - top_num
                if diff > 0 and diff < lowest_diff:
                    lowest_diff = diff
                    lowest_card_idx = card_idx

            if lowest_card_idx != -1:
                return lowest_card_idx

        # if no card to play choose random
        return random.randint(0, len(cards) - 1)

