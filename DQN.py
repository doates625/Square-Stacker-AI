"""
DQN.py
Square Stacker Deep Q Network trainer
"""

from SquareStackerGame import *
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam
from ProgressTracker import ProgressTracker
from ScoreTracker import ScoreTracker
import matplotlib.pyplot as plt
import csv

# Initial Printout
print('Square Stacker DQN Trainer')

# DQN Settings
dqn_discount = 0.0
dqn_input_dim = len(SquareStackerGame().get_state_vector())
dqn_output_dim = len(move_to_vector([0, 0, 0]))

# Training Settings
train_num_games = 10000
train_epsilon = 0.1

# Create DQN Model
dqn = Sequential([
    Dense(128, input_dim=dqn_input_dim),
    Activation('relu'),
    Dense(128),
    Activation('relu'),
    Dense(dqn_output_dim),
])
dqn.compile(optimizer=Adam(), loss='mse', metrics=['accuracy'])

# Progress Trackers
time_print_interval = 2.0
progress_tracker = ProgressTracker(time_print_interval)
game_print_interval = 50
score_tracker = ScoreTracker(game_print_interval)
game_show_interval = 100

# Score Plotting
plot_game_count = []
plot_mean_score = []
plot_min_score = []
plot_max_score = []
fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)

# CSV Logger
csv_file = open('Log.csv', 'w', newline='')
csv_writer = csv.writer(csv_file, delimiter=',')

# Play Games to Train Model
print("Beginning Training Model")
progress_tracker.start()
for game_i in range(train_num_games):

    # Create batch of training data
    training_data = []  # List of (state, move, reward, next state, done)

    # Simulate the game until loss
    game = SquareStackerGame()
    valid_moves = game.get_valid_moves()
    num_valid_moves = len(valid_moves)
    done = num_valid_moves == 0

    while not done:

        # Display game GUI
        if not (game_i + 1) % game_show_interval:
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

        # Add data to batch
        next_state = game.get_state_vector()
        training_data.append((state, move, reward, next_state, done))

        # Exit game if lost
        if done:
            break
    game.close_window()

    # Update CSV and plots
    score = game.get_score()
    csv_writer.writerow([str(game_i + 1), str(score)])

    # Progress Printouts
    progress_tracker.update(float(game_i) / train_num_games)
    if score_tracker.update(score):

        # Update score lists
        plot_mean_score.append(score_tracker.get_mean_score())
        plot_min_score.append(score_tracker.get_min_score())
        plot_max_score.append(score_tracker.get_max_score())
        plot_game_count.append(game_i)

        # Update progress plots
        axes.clear()
        axes.set_title('Score Progress')
        axes.set_xlabel('Game')
        axes.set_ylabel('Score')
        axes.plot(plot_game_count, plot_mean_score, label='Mean')
        axes.plot(plot_game_count, plot_min_score, label='Min')
        axes.plot(plot_game_count, plot_max_score, label='Max')
        axes.legend()
        axes.grid()
        plt.draw()
        plt.pause(1e-6)

        # Reset score tracker
        score_tracker.reset()

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
    dqn.fit(np.array(states), np.array(q_vectors), verbose=0)
