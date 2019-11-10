"""
exhaustive.py
Test script for Square Stacker Exhaustive search Agent
"""

from agents.search.exhaustive import ExhaustiveSearchAgent
from tests.agent import test_agent

# Test Settings
search_depth = 2
test_num_games = 50

# Test Agent
agent = ExhaustiveSearchAgent(search_depth)
test_agent(agent, num_games=test_num_games)
