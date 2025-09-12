
from env.arena import Arena
from players.random_player import RandomPlayer
from players.lazzy_player import LazzyPlayer


if __name__ == "__main__":

    n_games = 10000

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

    #[13.004789, 13.018059, 13.388693, 12.601966, 12.885856, 14.44924]
    #[13.016749, 13.009984, 13.370666, 12.600412, 12.90129, 14.451634]

    #[12.98104, 13.03884, 13.4171, 12.63918, 12.87332, 14.4007]
    #[13.04049, 13.00952, 13.4091, 12.55055, 12.89053, 14.44541]