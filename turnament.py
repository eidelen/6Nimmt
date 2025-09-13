
from env.arena import Arena
from players.random_player import RandomPlayer
from players.lazzy_player import LazzyPlayer
from players.safe_player import SafePlayer

if __name__ == "__main__":

    n_games = 10000

    n_players = 4
    accumulated_penalties = [0] * n_players

    for k in range(n_games):

        players = []
        players.append(RandomPlayer())
        players.append(RandomPlayer())
        players.append(LazzyPlayer())
        players.append(SafePlayer())

        arena = Arena(players)
        penalties = arena.play()

        for i in range(len(penalties)):
            accumulated_penalties[i] += penalties[i]

    # normalize
    for i in range(len(accumulated_penalties)):
        accumulated_penalties[i] = accumulated_penalties[i] / n_games
    print(accumulated_penalties)
