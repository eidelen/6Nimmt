
from typing import Tuple, List
import heapq
import random
from env.arena import Arena, Player
from env.common import rank_best_cards_for_num, get_accumulated_stack_penalty

class CardCountingPlayer(Player):

    def __init__(self):
        super().__init__()
        self.played_cards = {}

    def call_select_card(self, own_cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]], all_penalty_cards: List[List[Tuple[int, int]]]) -> int:
        # this player memorizes all played cards and computes an accurate probability
        # in order to not hit the sixth card

        self._memorize_played_cards(own_cards, board, all_penalty_cards)

        number_of_players = len(all_penalty_cards)

        stack_solutions = []
        for slot_idx in range(len(board)):
            current_slot_size = len(board[slot_idx])
            current_top_num, _ = board[slot_idx][-1]
            current_penalty_on_slot = get_accumulated_stack_penalty(board[slot_idx])

            # find a card to play on that slot
            rank_best_cards = rank_best_cards_for_num(own_cards, current_top_num, self.played_cards)
            if len(rank_best_cards) > 0:
                stack_diff, best_card_idx, _ = rank_best_cards[0]
                expected_stack_location = stack_diff + current_slot_size + 1
                heapq.heappush(stack_solutions, (expected_stack_location, best_card_idx))

        if len(stack_solutions) > 0:
            _, card_idx = heapq.heappop(stack_solutions)
            return card_idx

        # if no card to play choose random
        return random.randint(0, len(own_cards) - 1)


    def _memorize_played_cards(self, own_cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]], all_penalty_cards: List[List[Tuple[int, int]]]) -> None:
        for ll in [[own_cards], board, all_penalty_cards]:
            for l in ll:
                for n, _ in l:
                    self.played_cards[n] = True

    def _was_card_played(self, card_num: int) -> bool:
        return card_num in self.played_cards