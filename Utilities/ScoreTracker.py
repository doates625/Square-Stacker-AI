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
        self._num_scores = 0
        self._mean_score = 0.0
        self._min_score = float_info.max
        self._max_score = float_info.min

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
        do_update = self._num_scores == self._interval
        if do_update:
            self._mean_score /= self._interval
            print(f'Scores: Mean: {self._mean_score:.3f}, Min: {self._min_score:.3f}, Max: {self._max_score:.3f}')

        # Return update flag
        return do_update

    def get_mean_score(self):
        """
        :return: Mean score from game batch
        """
        return self._mean_score

    def get_min_score(self):
        """
        :return: Min score from game batch
        """
        return self._min_score

    def get_max_score(self):
        """
        :return: Max score from game batch
        """
        return self._max_score

    def reset(self):
        """
        Resets score tracking stats
        :return: None
        """
        self._num_scores = 0
        self._mean_score = 0.0
        self._min_score = float_info.max
        self._max_score = float_info.min
