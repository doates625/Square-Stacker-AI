"""
DQNAgent.py
Square Stacker Deep Q Network agent
"""

import csv

import matplotlib.pyplot as plt
from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.optimizers import Adam

from Agents.Agent import Agent
from Utilities.ProgressTracker import ProgressTracker
from Utilities.ScoreTracker import ScoreTracker
from SquareStackerGame import *


class DQNAgent(Agent):

    def __init__(self):
        """
        Initializes random DQN model
        """
        Agent.__init__(self)

        # Initialize DQN
        dqn_input_dim = len(SquareStackerGame().get_state_vector())
        dqn_output_dim = len(move_to_vector([0, 0, 0]))
        self._dqn = Sequential([
            Dense(128, input_dim=dqn_input_dim),
            Activation('relu'),
            Dense(128),
            Activation('relu'),
            Dense(dqn_output_dim),
        ])
        self._dqn.compile(optimizer=Adam(), loss='mse', metrics=['accuracy'])

    def train(self, num_fits, games_per_fit, discount, epsilon, csv_name=None):
        """
        Trains DQN via repeated game simulation
        :param num_fits: Number of times to fit network
        :param games_per_fit: Number of games to play fit each fit
        :param discount: DQN discount factor [0,1]
        :param epsilon: Probability of random action [0,1]
        :param csv_name: Name of log CSV file (or None)
        :return: None
        """

        # Initial printout
        print('Training Square Stacker DQN')

        # Progress trackers
        progress_tracker = ProgressTracker(5.0)
        score_tracker = ScoreTracker(100)
        num_games = num_fits * games_per_fit

        # Score plotting
        plot_game_count = []
        plot_mean_score = []
        plot_min_score = []
        plot_max_score = []
        fig = plt.figure()
        axes = fig.add_subplot(1, 1, 1)

        # CSV logger
        make_csv_log = (csv_name is not None)
        if make_csv_log:
            csv_file = open(csv_name, 'w', newline='')
            csv_writer = csv.writer(csv_file, delimiter=',')

        # Play games to train model
        game_count = 1
        progress_tracker.start()

        for fit_i in range(num_fits):

            # Create batch of training data (state, move, reward, next_state, done)
            training_data = []

            # Play multiple games in-between fits
            for game_i in range(games_per_fit):

                # Simulate the game until loss
                game = SquareStackerGame()
                valid_moves = game.get_valid_moves()
                num_valid_moves = len(valid_moves)
                done = num_valid_moves == 0

                while not done:

                    # Get game state vector
                    state = game.get_state_vector()

                    # Select best or random move
                    if np.random.random() > epsilon:
                        all_q_values = self._dqn.predict(np.array([state]))[0]
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

                # Write game to CSV file
                score = game.get_score()
                if make_csv_log:
                    csv_writer.writerow([str(game_count), str(score)])

                # Progress Printouts
                progress_tracker.update(float(game_count) / num_games)
                if score_tracker.update(score):

                    # Update score lists
                    plot_mean_score.append(score_tracker.get_mean_score())
                    plot_min_score.append(score_tracker.get_min_score())
                    plot_max_score.append(score_tracker.get_max_score())
                    plot_game_count.append(game_count)

                    # Update progress plot
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

                # Increment game count
                game_count += 1

            # Form training data from games
            print('Fitting Model...')
            states = []
            q_vectors = []
            for (state, move, reward, next_state, done) in training_data:
                states.append(state)
                move_index = move_to_index(move)
                q_vector = self._dqn.predict(np.array([state]))[0]
                if not done:
                    max_future_q = np.max(self._dqn.predict(np.array([next_state]))[0])
                    q_vector[move_index] = reward + discount * max_future_q
                else:
                    q_vector[move_index] = reward
                q_vectors.append(q_vector)

            # Train network
            self._dqn.fit(np.array(states), np.array(q_vectors), verbose=0)

        pass

    def select_move(self, game):
        """
        Selects move which maximizes Q-values predicted by DQN
        :param game: Current game [SquareStackerGame]
        :return: Move [k, i, j] or None if no moves exist
        """
        state = game.get_state_vector()
        valid_moves = game.get_valid_moves()
        if len(valid_moves) > 0:
            all_q_values = self._dqn.predict(np.array([state]))[0]
            q_values = []
            for move in valid_moves:
                q_values.append(all_q_values[move_to_index(move)])
            return valid_moves[np.argmax(q_values)]
        else:
            return None
