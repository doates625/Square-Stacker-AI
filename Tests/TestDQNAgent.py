"""
TestDQNAgent.py
Test script for Square Stacker Deep Q Network Agent
"""

from Agents.DQNAgent import DQNAgent
from Tests.TestAgent import test_agent

# Test Settings
num_fits = 20
games_per_fit = 5000
discount = 0.0
epsilon = 0.1
test_num_games = 1000

# Test Agent
agent = DQNAgent()
agent.train(num_fits, games_per_fit, discount, epsilon)
test_agent(agent, num_games=test_num_games)
