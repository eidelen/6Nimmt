
from env.arena import Arena
from players.random_player import RandomPlayer
from players.lazzy_player import LazzyPlayer


if __name__ == "__main__":

    n_games = 1000000

    n_players = 6
    accumulated_penalties = [0] * n_players

    for k in range(n_games):

        players = []
        for _ in range(n_players):
            players.append(LazzyPlayer())
        arena = Arena(players)
        penalties = arena.play()

        for i in range(len(penalties)):
            accumulated_penalties[i] += penalties[i]

    # normalize
    for i in range(len(accumulated_penalties)):
        accumulated_penalties[i] = accumulated_penalties[i] / n_games
    print(accumulated_penalties)