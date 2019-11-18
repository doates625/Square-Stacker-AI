from square_stacker_game import SquareStackerGame


class Node:
    def __init__(self, game_state):
        # type: (SquareStackerGame) -> None
        # initialized with a state vector
        self.game_state = game_state
        self.state = game_state.get_state_vector()
        self.move = []
        self.score = 0
        self.state_score = game_state.get_score()
        self.valid_moves = game_state.get_valid_moves()
        self.traversed = 1
        self.parent = None
        self.children = []
        self.visited_children = []

    def update_state(self, game_state):
        self.game_state = game_state
        self.state = game_state.get_state_vector()
        self.valid_moves = game_state.get_valid_moves()
        self.state_score = game_state.get_score()
