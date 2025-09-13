# handy function for game, deck and players

def get_accumulated_stack_penalty(stack):
    sum_penalty = 0
    for _, penalty in stack:
        sum_penalty += penalty
    return sum_penalty