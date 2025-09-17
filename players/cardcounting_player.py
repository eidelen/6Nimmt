
from typing import Tuple, List
from env.arena import Arena, Player
from env.common import rank_best_cards_for_num

class CardCountingPlayer(Player):

    def __init__(self):
        super().__init__()
        self.played_cards = {}

    def call_select_card(self, own_cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]], all_penalty_cards: List[List[Tuple[int, int]]]) -> int:
        # this player memorizes all played cards and computes an accurate probability
        # in order to not hit the sixth card

        self._memorize_played_cards(own_cards, board, all_penalty_cards)

        # todo: implement
        return 0

    def _memorize_played_cards(self, own_cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]], all_penalty_cards: List[List[Tuple[int, int]]]) -> None:
        for ll in [[own_cards], board, all_penalty_cards]:
            for l in ll:
                for n, _ in l:
                    self.played_cards[n] = True

    def _was_card_played(self, card_num: int) -> bool:
        return card_num in self.played_cards