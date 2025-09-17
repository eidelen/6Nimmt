# handy functions for game, deck and players
import heapq

def get_accumulated_stack_penalty(stack):
    sum_penalty = 0
    for _, penalty in stack:
        sum_penalty += penalty
    return sum_penalty

def rank_best_cards_for_num(cards, num):
    # sorting following to closest bigger card than num. if no such card available, return empty list
    # returns a list of (diff, indexes, num)
    ranking = []
    for card_idx in range(len(cards)):
        card_num, _ = cards[card_idx]
        card_diff = nbr_cards_between(card_num, num)
        if card_diff > -1:
            heapq.heappush(ranking, (card_diff, card_idx, card_num))
    return [heapq.heappop(ranking) for i in range(len(ranking))]

def nbr_cards_between(a: int, b: int, exclude_known_cards = {}) -> int:

    if a == b or a > b:
        return -1 # invaldi

    cnt_cards = 0
    for i in range(a+1, b):
        if i not in exclude_known_cards:
            cnt_cards += 1

    return cnt_cards
