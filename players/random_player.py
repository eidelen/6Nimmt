from env.arena import Arena, Player
from typing import Tuple, List
import random

class RandomPlayer(Player):

    def __init__(self):
        super().__init__()

    def call_select_card(self, cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]], all_penalty_cards: List[List[Tuple[int, int]]]) -> int:
        # play random card
        return random.randint(0, len(cards) - 1)
