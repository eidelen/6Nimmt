from abc import ABC, abstractmethod
from typing import Tuple, List

from env.game import Game

class Player(ABC):
    @abstractmethod
    def call_select_card(self, cards: List[Tuple[int, int]], board: List[List[Tuple[int, int]]]) -> int:
        """Compute area of the shape"""
        return 0


class Arena:

    def __init__(self, players: List[Player]):
        self.players = players
        self.game = Game(n_players=len(players))

    def play(self):
        go_on = True
        penalties = []
        while go_on:
            cards_to_play = []
            for player_idx in range(len(self.players)):
                player_cards = self.game.players_cards[player_idx]
                board_cards = self.game.board
                chosen_card_idx = self.players[player_idx].call_select_card(player_cards, board_cards)
                cards_to_play.append(chosen_card_idx)
            go_on, penalties = self.game.step_players_choose_cards(cards_to_play)
        return penalties
