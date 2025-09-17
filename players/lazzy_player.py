from env.arena import Arena, Player
from typing import Tuple, List

class LazzyPlayer(Player):

    def __init__(self):
        super().__init__()

    def call_select_card(self, cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]], all_penalty_cards: List[List[Tuple[int, int]]]) -> int:
        # play always top card
        return 0
