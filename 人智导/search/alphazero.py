import copy
from game import State, Player
from mcts import MCTS

class AlphaZero(MCTS):
    """
    A modification based on pure MCTS, replacing randomly playout with using an evaluation function.
    """
    def __init__(self, start_state: State, evaluation_func, c=5, n_playout=10000):
        """
        Parameters:
            evaluation_func: a function taking a state as input and
                outputs the value in the current player's perspective.
        """
        super().__init__(start_state, c, n_playout)
        self.evaluation_func = evaluation_func

    def get_leaf_value(self, state: State):
        player = state.get_current_player()
        info = state.get_info()
        score = 0.0
        for p, info_p in info.items():
            if p == player:
                score += (info_p["live_two"] * 1 + info_p["three"] * 1
                            + info_p["live_three"] * 3 + info_p["four"] * 10 + info_p["live_four"] * 30)
                score -= info_p["max_distance"] * 10
            else:
                score -= (info_p["live_two"] * 1 + info_p["three"] * 1
                            + info_p["live_three"] * 3 + info_p["four"] * 50 + info_p["live_four"] * 100)
                score += info_p["max_distance"] * 10
        if state.game_end()[1] == player:
            score += 100
        score = score / 10
        return score

class AlphaZeroPlayer(Player):
    """AI player based on MCTS"""
    def __init__(self, evaluation_func, c=0.1, n_playout=2000):
        super().__init__()
        self.evaluation_func = evaluation_func
        self.c = c
        self.n_playout = n_playout

    def get_action(self, state: State):
        mcts = AlphaZero(state, self.evaluation_func, self.c, self.n_playout)
        for n in range(self.n_playout):
            state_copy = copy.deepcopy(state)
            mcts.playout(state_copy)
        return max(mcts.root.children.items(),
                    key=lambda act_node: act_node[1].n_visits)[0]
