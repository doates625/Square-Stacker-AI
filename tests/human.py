"""
human.py
Makes histogram of human play-testing
"""

import matplotlib.pyplot as plt

# Human scores
scores = [
    401,
    282,
    129,
    417,
    86,
    145,
    222,
    797,
    206,
    1073,
]

# Histogram
fig, axs = plt.subplots(1, 1)
axs.hist(scores, bins=6)
axs.set_title('Human Scores')
axs.set_xlabel('Score')
axs.set_ylabel('Frequency')
plt.show()
