"""
Progress Tracker
Class for tracking and printing progress of long calculations
Written by Dan Oates (WPI Class of 2020
"""

from time import time


class ProgressTracker:

    def __init__(self, interval):
        """
        Constructs and starts new progress tracker
        :param interval: Print interval [s]
        """
        self._interval = interval
        self._time_init = 0.0
        self._time_print = 0.0
        self.start()

    def start(self):
        """
        Resets progress tracking
        :return: None
        """
        self._time_init = time()
        self._time_print = self._time_init

    def update(self, progress):
        """
        Updates tracker and periodically prints
        :param progress: Progress ratio [0,1]
        :return: True if printout occurred
        """
        time_now = time()
        if time_now - self._time_print > self._interval:
            self._time_print = time_now
            time_left = (1.0 - progress) * (time_now - self._time_init) / progress
            print(f'Progress: {progress * 100.0:.3f}%, Time left: {time_left / 60.0:.1f} min')
