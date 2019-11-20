"""
exhaustive.py
Test script for Square Stacker Exhaustive search Agent
"""

from agents.memory.agent import MemoryAgent
from tests.agent import test_agent

# Test Settings
test_num_games = 5000

# Test Agent
agent = MemoryAgent(memory_length=10)
test_agent(agent, num_games=test_num_games, show=True)
