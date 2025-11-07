from functools import lru_cache
from fractions import Fraction

'''
t  \  h | wait | swing |
ball    |  +b  |  +s   |
strike  |  +s  |  h    |

h {
    p:   +4 pts
    1-p: +s
}

b == 4 => +1 pt
s == 3 => -0 pt

full count when b == 3 and s == 2

t is thrower
h is hitter
'''

@lru_cache(None)
def pr_swing(balls, strikes, p):
    ep_strike = expected_points(balls, strikes + 1, p)
    ep_ball = expected_points(balls + 1, strikes, p)
    return ((ep_strike - ep_ball) / (2 * ep_strike - ep_ball - 4 * p - (1 - p) * ep_strike))

def pr_wait(balls, strikes, p):
    return 1 - pr_swing(balls, strikes, p)

def pr_strike(balls, strikes, p):
    return pr_swing(balls, strikes, p)

def pr_ball(balls, strikes, p):
    return 1 - pr_strike(balls, strikes, p)

@lru_cache(None)
def expected_points(balls, strikes, p):
    if (balls == 4):
        return Fraction("1")
    if (strikes == 3):
        return Fraction("0")

    res = (
        expected_points(balls + 1, strikes, p) + 
        pr_swing(balls, strikes, p) * expected_points(balls, strikes + 1, p)
        - pr_swing(balls, strikes, p) * expected_points(balls + 1, strikes, p)
    )

    return res

def pr_inc_balls(balls, strikes, p):
    return pr_wait(balls, strikes, p) * pr_ball(balls, strikes, p)

def pr_inc_strikes(balls, strikes, p):
    return (
        pr_swing(balls, strikes, p) * pr_ball(balls, strikes, p) + 
        pr_wait(balls, strikes, p) * pr_strike(balls, strikes, p) + 
        pr_swing(balls, strikes, p) * pr_strike(balls, strikes, p) * (1 - p)
    )

@lru_cache(None)
def pr_reaching_state(balls, strikes, p):
    if balls == strikes == 0:
        return 1
    if balls > 0 and strikes == 0:
        return pr_reaching_state(balls - 1, 0, p) * pr_inc_balls(balls - 1, 0, p)
    if balls == 0 and strikes > 0:
        return pr_reaching_state(0, strikes - 1, p) * pr_inc_strikes(0, strikes - 1, p)
    if balls > 0 and strikes > 0:
        return (pr_reaching_state(balls - 1, strikes, p) * pr_inc_balls(balls - 1, strikes, p) 
                + pr_reaching_state(balls, strikes - 1, p) * pr_inc_strikes(balls, strikes - 1, p))
    else:
        raise Exception("unreachable")

def calculate_q(p):
    return pr_reaching_state(3, 2, p)

def ternary_search(eval, left, right, eps=1e-12):
    while right - left > eps:
        m1 = left + (right - left) / 3
        m2 = right - (right - left) / 3
        if eval(m1) < eval(m2):
            left = m1
        else:
            right = m2
    p_max = (left + right) / 2
    return p_max, eval(p_max)

if __name__ == "__main__":
    p_max, q_max = ternary_search(calculate_q, 0, 1)
    print(f"p: {p_max}, q: {q_max}")