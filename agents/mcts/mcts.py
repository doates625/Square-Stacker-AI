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

    def __init__(self):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.

        Agent.__init__(self)

        self.total_simulations = 0
        self.root_node = None
        self.if_debug = False

        # parameters to change for how deep it goes
        self.max_sims = 200

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

            self.debug("Simulation number: " + str(self.total_simulations))

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

        # if not self.total_simulations % 50:
        #     print("current depth " + str(depth))

        if self.non_terminal(node):
            return self.pick_unvisited(node)
        else:
            return node  # in case no children are present / node is terminal

    # EXPLORATION
    def fully_expanded(self, node):
        """
        does node have children
        :param node: Node
        :return: bool
        """
        if len(node.children) == len(node.visited_children) and node.children:
            return True
        else:
            return False

    def pick_unvisited(self, node):
        """
        create children for the node and choose one at random
        :param node: Node
        :return: Node
        """
        self.debug("EXPAND CHILDREN")
        valid_moves = node.valid_moves

        if not node.children:
            for move in valid_moves:
                new_game = node.game_state.deepcopy()
                new_game.make_move(move)

                child = Node(new_game)
                child.move = move
                child.parent = node
                node.children.append(child)

        chosen_one = choice(node.children)

        node.visited_children.append(chosen_one)
        return chosen_one

    # SIMULATION
    def simulation(self, node):
        self.debug("SIMULATION")
        # creates copy of game to run simulation on
        sim_game = node.game_state.deepcopy()
        sim_node = deepcopy(node)
        sim_node.game_state = sim_game
        node.traversed += 1
        num = 0

        while self.non_terminal(sim_node):
            sim_node = self.sim_random(sim_node)
            num += 1

            # if not self.total_simulations % 10:
            #     sim_node.game_state.show(num)

        return sim_node.state_score

    # randomly select child
    def sim_random(self, node):
        valid_moves = node.valid_moves
        rand_move = choice(valid_moves)
        node.game_state.make_move(rand_move)

        node.update_state(node.game_state)
        return node

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

    # BACKPROPAGATION
    def backpropagate(self, node, result):
        """
        recursively call function to go up the chain of branch and update scores
        :param node: Node()
        :param result: Int
        :return: None
        """
        if node == self.root_node:
            return
        node.score = result
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

        # print(scores)
        return best

    def uct(self, node):
        return node.score + math.sqrt(2 * math.log(node.traversed) / self.total_simulations)

    def best_child(self, root):
        # type: (Node) -> None

        # select the best child from the tree
        jesse = self.best_uct(root)

        return jesse

    def debug(self, msg):
        if self.if_debug:
            print(msg)
