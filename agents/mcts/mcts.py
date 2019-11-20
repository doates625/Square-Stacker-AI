"""
Class to implement Monte Carlo Tree Search (MCTS)

MCTS consists of 4 main steps
- Selection
    - selects which of the children nodes to search down
- Expansion
    - if child is a leaf (has no children) will expand the possible states
- Simulation
    - from a state, simulate random games until a terminal state is reached
- Backpropagation
    - update values of states on path back to the root node

Each round contributes to choosing the next move
Originally used for two-player games in which there is a time limit for each move
Will be abstracted out for our purposes

If this works, can be further implemented in ADI which will make an agent out of it
"""
from random import choice
from copy import deepcopy
import math
from agents.agent import Agent
from square_stacker_game import SquareStackerGame
from agents.mcts.Node import Node


class MCTS(Agent):

    def __init__(self, max_sims = 50):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.

        Agent.__init__(self)

        self.total_simulations = 0
        self.root_node = None
        self.if_debug = False
        self.loglevel = 0

        # parameters to change for how deep it goes
        self.max_sims = max_sims

    def select_move(self, game):
        # type: (SquareStackerGame) -> None
        """
        Causes the AI to calculate the best move from the current game state and return it.
        :param game: root state
        :return: best possible move
        """

        root = deepcopy(game)
        self.root_node = Node(root)
        self.total_simulations = 0
        # while within some limit (time or power)
        for i in range(self.max_sims):
            self.total_simulations += 1

            if not self.total_simulations % 50:
                self.debug("Simulation number: " + str(self.total_simulations), loglevel=1)

            leaf = self.selection(self.root_node)  # selection
            self.debug("Leaf chosen " + str(leaf))

            simulation_result = self.simulation(leaf)
            self.debug("Simulation result: " + str(simulation_result))

            self.backpropagate(leaf, simulation_result)

        self.debug("MOVE CHOSEN")
        jesse = self.best_child(self.root_node)
        return jesse.move

    # SELECTION
    def selection(self, node):
        # states encoded as state vectors
        self.debug("SELECTING")
        depth = 1

        while self.fully_expanded(node):
            depth += 1
            node = self.best_uct(node)

        if not self.total_simulations % 50:
            self.debug("current depth " + str(depth), loglevel=1)

        # if terminal -> return node and simulate again
        if self.non_terminal(node):
            if node.traversed == 0:     # if never traversed -> return node and simulate
                return node
            else:   # if has traversed but not expanded -> expand and return child
                return self.expand(node)
        else:
            return node

    # EXPLORATION
    def fully_expanded(self, node):
        """
        does node have children
        :param node: Node
        :return: bool
        """
        # if len(node.children) == len(node.visited_children) and node.children:
        if node.children:
            return True
        else:
            return False

    def expand(self, parent):
        """
        create children for the node and choose one at random
        :param parent: Node
        :return: Node
        """
        self.debug("EXPAND CHILDREN")
        valid_moves = parent.valid_moves

        # if not node.children:
        for move in valid_moves:
            new_game = parent.game_state.deepcopy()
            new_game.make_move(move)

            child = Node(new_game)
            child.move = move
            child.parent = parent
            parent.children.append(child)

        chosen_one = choice(parent.children)

        return chosen_one

    # SIMULATION
    def simulation(self, node):
        self.debug("SIMULATION")
        # creates copy of game to run simulation on
        sim_game = node.game_state.deepcopy()
        sim_node = deepcopy(node)
        sim_node.game_state = sim_game

        while self.non_terminal(sim_node):
            sim_node = self.sim_random(sim_node)

        return sim_node.state_score

    # randomly select child
    def sim_random(self, node):
        valid_moves = node.valid_moves
        rand_move = choice(valid_moves)

        node.game_state.make_move(rand_move)
        node.update_state(node.game_state)
        return node

    # BACKPROPAGATION
    def backpropagate(self, node, result):
        """
        recursively call function to go up the chain of branch and update scores
        :param node: Node()
        :param result: Int
        :return: None
        """
        node.score += result
        node.traversed += 1

        if node == self.root_node:
            return

        self.backpropagate(node.parent, result)

    def best_uct(self, node):
        """
        :param node: Node
        :return: Node() with best score
        """
        best = node.children[0]
        top_score = self.uct(best)
        scores = []
        for child in node.children:
            try_score = self.uct(child)
            scores.append(try_score)
            if try_score > top_score:
                best = child
                top_score = try_score

        self.debug(scores)
        return best

    def uct(self, node):
        if node.traversed == 0:
            return math.inf
        return (node.score / node.traversed) + 2 * math.sqrt(math.log(node.parent.traversed) / node.traversed)

    def best_child(self, root):
        # select the best child from the tree
        jesse = self.best_uct(root)

        return jesse

    # check if leaf has any moves left
    def non_terminal(self, leaf):
        """
        are there any legal moves from this state
        :param leaf: Node()
        :return: bool
        """
        if leaf.valid_moves:
            return True
        else:
            return False

    def debug(self, msg, loglevel=0):
        if self.if_debug:
            if loglevel >= self.loglevel:
                print(msg)
