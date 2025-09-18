
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
        self.players = [RandomPlayer(), SafePlayer(), SafePlayer()]

    def make_observation(self) -> np.ndarray:

        o = np.zeros((34, 2), dtype=np.float32)

        scale_card_number = 100.0
        scale_penalty_number = 10.0

        # first 10 entries are players own cards
        player_cards = self.game.players_cards
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

        reward = 0.0

        # other players choose their cards
        cards_to_play = []
        for player_idx in range(len(self.players)):
            player_cards = self.game.players_cards[player_idx]
            board_cards = self.game.board
            all_penalty_cards = self.game.players_penalties_cards
            chosen_card_idx = self.players[player_idx].call_select_card(player_cards, board_cards, all_penalty_cards)
            cards_to_play.append(chosen_card_idx)

        # agent selects his cards
        nbr_of_player_cards = len(self.game.players_cards)
        if action < nbr_of_player_cards:
            cards_to_play.append(action)

        else:
            # invalid action

        if action < 4: # move actions
            if action == 0: # up
                next_pos = (self.agent_pos[0]-1, self.agent_pos[1])
            elif action == 1: # right
                next_pos = (self.agent_pos[0], self.agent_pos[1]+1)
            elif action == 2:  # down
                next_pos = (self.agent_pos[0]+1, self.agent_pos[1])
            elif action == 3:  # left
                next_pos = (self.agent_pos[0], self.agent_pos[1]-1)

            if self.can_move_to_pos(next_pos):
                self.agent_pos = next_pos
                reward += self.current_move_penalty # penalty for each move
            else:
                reward += self.current_collision_penalty
                if self.dead_when_colliding:
                    agent_killed = True

        elif action == 4: # drop bomb at agent location
            reward += self.current_bomb_penalty  # penalty for each dropped bomb
            placed_bomb = self.agent_pos
            if self.indestructible_agent:
                self.active_bombs.append((self.agent_pos, 0)) # immediate detonation
            else:
                self.active_bombs.append((self.agent_pos, 2))  # detonation two steps later

        #go through all active bombs
        still_active_bombs = []
        for bomb_pos, step_timer in self.active_bombs:
            if step_timer <= 0:
                reward += self.current_rock_reward * self.bomb_3x3(bomb_pos) # detonate bomb
                exploded_bomb = bomb_pos

                if not self.indestructible_agent:
                    # check that agent is in safe distance
                    squared_dist = (bomb_pos[0]-self.agent_pos[0])**2 + (bomb_pos[1]-self.agent_pos[1])**2
                    if squared_dist < 4.0:
                        reward += self.current_close_bomb_penalty
                        if self.dead_near_bomb:
                            agent_killed = True
            else:
                still_active_bombs.append((bomb_pos, step_timer - 1))

        self.active_bombs = still_active_bombs

        # mission completed when every rock was bombed
        if (self.stones == False).all():
            reward += self.current_end_game_reward
            terminated = True
        else:
            terminated = False

        if self.current_step > self.current_max_steps or agent_killed: # end game when max step reached or agent killed
            truncate = True
        else:
            truncate = False

        self.current_step += 1

        return self.make_observation(), reward, terminated, truncate, {"placed_bomb": placed_bomb, "exploded_bomb": exploded_bomb}