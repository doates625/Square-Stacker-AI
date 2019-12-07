"""
dlrgs.py
Test script for Square Stacker Depth-Limited Random Search Agent
"""

from agents.search.dlrgs import DepthLimitedRandomSearchAgent
from tests.agent import test_agent

# Test Settings
search_depth = 2
games_per_move = 15
test_num_games = 1000

# Test Agent
agent = DepthLimitedRandomSearchAgent(search_depth, games_per_move)
test_agent(agent, num_games=test_num_games)
