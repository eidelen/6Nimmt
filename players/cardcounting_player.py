
from typing import Tuple, List
from env.arena import Arena, Player
from env.common import rank_best_cards_for_num

class CardCountingPlayer(Player):

    def __init__(self):
        super().__init__()

    def call_select_card(self, cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]]) -> int:
        # todo: also forward the penalty card of all players, as these were seen by all players.
        # this player memorizes all played cards and computes an accurate probability
        # in order to not hit the sixth card



        # todo: implement
        return 0

    def _memorize_played_cards(self, board: List[List[Tuple[int, int]]]) -> None:
        pass

    def _was_card_played(self, card_num: int) -> bool:
        pass