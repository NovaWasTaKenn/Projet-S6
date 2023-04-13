

def alphaBetaSearch(state):
    v = maxValue(state, float('-inf'), float('inf'))
    return actions(v)


def maxValue(state, aplha, beta):
    if finParti(state):
        return utility(state)
    v = float('-inf')
    for a in actions(state):
        v = max(v, minValue(result(state, a), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def minValue(state, alpha, beta):
    if finParti(state):
        return utility(state)
    v = float('inf')
    for a in actions(state):
        v = max(v, maxValue(result(state, a), alpha, beta))
        if v <= alpha:
            return v
        beta = max(beta, v)
    return v


def finParti(state):
    pass


def result(state):
    pass


def utility(state):
    pass


def actions(state):
    pass
