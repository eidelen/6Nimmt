
from typing import Optional, Tuple, List

import gymnasium as gym
import numpy as np
import copy
from random import randrange

from env.game import Game
from players.random_player import RandomPlayer
from players.lazzy_player import LazzyPlayer
from players.safe_player import SafePlayer

class Game6NimmtEnv(gym.Env):

    def __init__(self):

        self.invalid_reward = -1
        self.end_game_reward = 2
        self.winning_reward = 2

        self.current_step = 0

        # 10 own cards, 4 * 6 board cards
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(34 * 2,), dtype=np.float32)

        # agent needs to choose among 10 cards
        self.action_space = gym.spaces.Discrete(10)


    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[np.ndarray, dict]:
        super().reset(seed=seed)
        self.current_step = 0
        self.set_initial_game()
        return self.make_observation(), {}

    def set_initial_game(self):
        self.game = Game(4)
        self.other_players = [RandomPlayer(), SafePlayer(), SafePlayer()]

    def make_observation(self) -> np.ndarray:

        o = np.zeros((34, 2), dtype=np.float32)

        scale_card_number = 104.0
        scale_penalty_number = 10.0

        # first 10 entries are players own cards
        player_cards = self.game.players_cards[3] # the last player is the rl agent
        for i in range(0, 10):
            if len(player_cards) > i:
                cn, cp = player_cards[i]
                o[i, 0] = cn / scale_card_number
                o[i, 1] = cp / scale_penalty_number

        # 4 * 6 slots cards
        for slot_idx in range(0, 4):
            slot_cards = self.game.board[slot_idx]
            for i in range(0, 6):
                if len(slot_cards) > i:
                    cn, cp = slot_cards[i]
                    o_idx = 10 + slot_idx * 6 + i
                    o[o_idx, 0] = cn / scale_card_number
                    o[o_idx, 1] = cp / scale_penalty_number

        return o.flatten()


    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, dict]:

        invalid_action_reward = -1.0
        winning_reward = 4.0

        reward = 0.0
        truncate = False
        terminated = False

        # other players choose their cards
        cards_to_play = []
        for player_idx in range(len(self.other_players)):
            player_cards = self.game.players_cards[player_idx]
            board_cards = self.game.board
            all_penalty_cards = self.game.players_penalties_cards
            chosen_card_idx = self.other_players[player_idx].call_select_card(player_cards, board_cards, all_penalty_cards)
            cards_to_play.append(chosen_card_idx)

        # agent selects his cards
        current_player_penalty = 0
        nbr_of_player_cards = len(self.game.players_cards[3])
        if action < 0 or action > nbr_of_player_cards - 1:
            # invalid action -> stop play
            reward += invalid_action_reward
            truncate = True
        else:
            cards_to_play.append(action)

            # game simulation
            game_ongoing, current_penalties = self.game.step_players_choose_cards(cards_to_play)
            current_player_penalty = current_penalties[3]
            if not game_ongoing:
                # game ended
                terminated = True

                # ranking
                sorted_indices = sorted(range(len(current_penalties)), key=lambda i: current_penalties[i])
                agent_rank = sorted_indices.index(3)

                reward += (winning_reward - agent_rank)

        return self.make_observation(), reward, terminated, truncate, {"penalty": current_player_penalty}
