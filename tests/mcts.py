"""
random_.py
Test script for Square Stacker Random Agent
"""

from agents.mcts.mcts import MCTS
from agents.mcts import Node
from square_stacker_game import SquareStackerGame
from tests.agent import test_agent

# Test Settings
test_num_games = 1

# Test Agent
agent = MCTS(max_sims=50)
test_agent(agent, num_games=test_num_games)



