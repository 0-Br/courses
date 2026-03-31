"""
Evaluation functions
"""


def dummy_evaluation_func(state):
    return 0.0


def distance_evaluation_func(state):
    player = state.get_current_player()
    info = state.get_info()
    score = 0.0
    for p, info_p in info.items():
        if p == player:
            score -= info_p["max_distance"]
        else:
            score += info_p["max_distance"]
    return score

def detailed_evaluation_func(state):
    player = state.get_current_player()
    info = state.get_info()
    score = 0.0
    for p, info_p in info.items():
        if p == player:
            score += (info_p["live_two"] * 2 + info_p["three"] * 2
                        + info_p["live_three"] * 50 + info_p["four"] * 50 + info_p["live_four"] * 100)
            score -= info_p["max_distance"] * 5
        else:
            score -= (info_p["live_two"] * 3 + info_p["three"] * 3
                        + info_p["live_three"] * 20 + info_p["four"] * 40 + info_p["live_four"] * 200)
            score += info_p["max_distance"] * 5
    score = score / 1000
    return score

def get_evaluation_func(func_name):
    if func_name == "dummy_evaluation_func":
        return dummy_evaluation_func
    elif func_name == "distance_evaluation_func":
        return distance_evaluation_func
    elif func_name == "detailed_evaluation_func":
        return detailed_evaluation_func
    else:
        raise KeyError(func_name)
