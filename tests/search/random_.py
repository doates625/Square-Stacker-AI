"""
random_.py
Test script for Square Stacker Random search Agent
"""

from agents.search.random_ import RandomSearchAgent
from tests.agent import test_agent

# Test Settings
games_per_move = 1
test_num_games = 5

# Test Agent
agent = RandomSearchAgent(games_per_move)
test_agent(agent, num_games=test_num_games)
