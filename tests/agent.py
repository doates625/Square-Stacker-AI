"""
agent.py
Test function for evaluating Square Stacker AI agents
"""

import numpy as np
import matplotlib.pyplot as plt
from utils.progress_tracker import ProgressTracker
from agents.search.agent import SearchAgent
from square_stacker_game import SquareStackerGame


def test_agent(agent, num_games=10000, num_bins=20):
    """
    tests given Square Stacker agent by running games
    :param agent: Square Stacker AI agent
    :param num_games: Number of games to test
    :param num_bins: Number of histogram bins
    :return: None
    """

    # Play games and track scores
    progress = ProgressTracker(1.0)
    progress.start()
    scores_list = [0] * num_games

    # search agent data
    is_search_agent = issubclass(type(agent), SearchAgent)
    moves_searched_list = []

    # Initial printout
    print('Square Stacker Agent Test')
    print(f'Playing {num_games} games...\n')

    for i in range(num_games):

        # Play game until no valid moves exist
        game = SquareStackerGame()
        move_num = 0
        while True:

            # Generate valid moves
            valid_moves = game.get_valid_moves()
            num_valid_moves = len(valid_moves)

            if num_valid_moves > 0:
                # Make move according to agent
                if is_search_agent:
                    move, moves_tried = agent.select_move(game)
                    moves_searched_list.append(moves_tried)
                else:
                    move = agent.select_move(game)
                game.make_move(move)
                move_num += 1

                # if not move_num % 20:
                print("Move Number: " + str(move_num))
            else:
                # Log score and exit game
                scores_list[i] = game.get_score()
                break

        # Update progress printer
        progress.update(float(i + 1) / num_games)

    print('\nComplete!\n')

    # Summary statistics
    print('Score Stats:')
    print(f'Mean: {np.mean(scores_list):.2f}')
    print(f'Std: {np.std(scores_list):.2f}')
    print(f'Min: {np.min(scores_list)}')
    print(f'Max: {np.max(scores_list)}')

    # search agent stats
    if is_search_agent:
        print('\nMove Search Stats:')
        print(f'Mean: {np.mean(moves_searched_list):.2f}')
        print(f'Std: {np.std(moves_searched_list):.2f}')
        print(f'Min: {np.min(moves_searched_list)}')
        print(f'Max: {np.max(moves_searched_list)}')

    # Plot histogram of scores
    fig, axs = plt.subplots(1, 1)
    axs.hist(scores_list, bins=num_bins)
    axs.set_title('Agent Scores')
    axs.set_xlabel('Score')
    axs.set_ylabel('Frequency')

    # Moves tried histogram
    if is_search_agent:
        fix, axs = plt.subplots(1, 1)
        axs.hist(moves_searched_list, bins=num_bins)
        axs.set_title('Moves Tried')
        axs.set_xlabel('Moves')
        axs.set_ylabel('Frequency')

    # Show plots
    plt.show()
