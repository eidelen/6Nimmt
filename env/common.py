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
        card_diff = card_num - num
        if card_diff > 0:
            heapq.heappush(ranking, (card_diff, card_idx, card_num))
    return [heapq.heappop(ranking) for i in range(len(ranking))]