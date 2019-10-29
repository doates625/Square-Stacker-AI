"""
DQN.py
Square Stacker Deep Q Network trainer
"""
import random

import numpy as np

from SquareStackerGame import *
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam
# from keras.callbacks import TensorBoard
import csv
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initial Printout
print('Square Stacker DQN Trainer')

# DQN Settings
dqn_discount = .4
dqn_input_dim = len(SquareStackerGame().get_state_vector())
dqn_output_dim = len(move_to_vector([0, 0, 0]))

# Training Settings
train_num_games = 50000
train_fail_reward = -500
train_epsilon = 0.1
MIN_REPLAY_MEMORY_SIZE = 1000
MINIBATCH_SIZE = 64

# Create DQN Model
dqn = Sequential([
    Dense(128, input_dim=dqn_input_dim),
    Activation('relu'),
    Dense(128),
    Activation('relu'),
    Dense(128),
    Activation('relu'),
    Dense(dqn_output_dim),
])
dqn.compile(optimizer=Adam(), loss='mse', metrics=['accuracy'])

# TensorBoard Object
# board = TensorBoard(log_dir='TensorBoard')

# CSV Logger
csv_file = open('Log.csv', 'w', newline='')
csv_writer = csv.writer(csv_file, delimiter=',')

plot_game, plot_score = [], []

fig = plt.figure()
# ax1 = fig.add_subplot(1, 1, 1)

print("Beginning Training Model")
last_time = time.time()
start = last_time
wait_time = 5  # time in seconds between outputs

# Play Games to Train Model
for game_i in range(train_num_games):

    # Game Printout
    now = time.time()
    if now - last_time > wait_time:
        print(f'Simulating game {game_i + 1}/{train_num_games}...')
        last_time = now

    # Create batch of training data
    training_data = []  # List of (state, move, reward, next state, done)

    # Simulate the game until loss
    game = SquareStackerGame()
    valid_moves = game.get_valid_moves()
    num_valid_moves = len(valid_moves)
    done = num_valid_moves == 0
    while not done:
        if not (game_i + 1) % 5000:
            game.show(game_i + 1)

        # Get game state vector
        state = game.get_state_vector()

        # Select best or random move
        if np.random.random() > train_epsilon:
            all_q_values = dqn.predict(np.array([state]))[0]
            q_values = []
            for move in valid_moves:
                q_values.append(all_q_values[move_to_index(move)])
            move = valid_moves[np.argmax(q_values)]
        else:
            move = valid_moves[np.random.randint(0, num_valid_moves)]

        # Apply move
        reward = game.make_move(move)
        valid_moves = game.get_valid_moves()
        num_valid_moves = len(valid_moves)
        done = num_valid_moves == 0
        if done:
            reward = train_fail_reward

        # Add data to batch
        next_state = game.get_state_vector()
        training_data.append((state, move, reward, next_state, done))

        # Start training only if certain number of samples is already saved
        if len(training_data) < MIN_REPLAY_MEMORY_SIZE:
            pass
        else:
            minibatch = random.sample(training_data, MINIBATCH_SIZE)
            current_states = np.array([transition[0] for transition in minibatch])
            current_qs_list = dqn.predict(current_states)

            new_current_states = np.array([transition[3] for transition in minibatch])
            future_qs_list = dqn.predict(future_qs_list)

            # Form training data
            states = []
            q_vectors = []
            for (state, move, reward, next_state, done) in training_data:
                states.append(state)
                move_index = move_to_index(move)
                q_vector = dqn.predict(np.array([state]))[0]
                if not done:
                    max_future_q = np.max(dqn.predict(np.array([next_state]))[0])
                    q_vector[move_index] = reward + dqn_discount * max_future_q
                else:
                    q_vector[move_index] = reward
                q_vectors.append(q_vector)

            # Train network
            # dqn.fit(np.array(states), np.array(q_vectors), verbose=0, callbacks=[board])
            dqn.fit(np.array(states), np.array(q_vectors), verbose=0)

        # Exit game if lost
        if done:
            break

    # Log game number and score in CSV
    plot_game.append(game_i + 1)
    plot_score.append(game.get_score())

    csv_writer.writerow([str(game_i + 1), str(game.get_score())])



