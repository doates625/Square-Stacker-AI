"""
Score Tracker
Class for tracking and printing score summary statistics for RL algorithms
Written by Dan Oates (WPI Class of 2020)
"""

from sys import float_info


class ScoreTracker:

    def __init__(self, interval):
        """
        Makes score tracker interface
        :param interval: Number of games to min, max, mean over
        """
        self._interval = interval
        self._reset()

    def update(self, score):
        """
        Updates score statistics and periodically prints
        :param score: Most recent game score
        :return: True if print and reset occurred
        """

        # Update stats
        self._mean_score += score
        self._min_score = min(self._min_score, score)
        self._max_score = max(self._max_score, score)

        # Print check
        self._num_scores += 1
        if self._num_scores == self._interval:
            self._mean_score /= self._interval
            print(f'Scores: Mean: {self._mean_score:.3f}, Min: {self._min_score:.3f}, Max: {self._max_score:.3f}')
            self._reset()

    def _reset(self):
        """
        Resets score tracking stats
        :return: None
        """
        self._num_scores = 0
        self._mean_score = 0.0
        self._min_score = float_info.max
        self._max_score = float_info.min
