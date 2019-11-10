"""
random_.py
Test script for Square Stacker Random Agent
"""

from agents.random import RandomAgent
from tests.agent import test_agent

# Test Settings
test_num_games = 1000

# Test Agent
agent = RandomAgent()
test_agent(agent, num_games=test_num_games)
