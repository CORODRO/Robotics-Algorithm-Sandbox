# -*- coding: utf-8 -*-
"""Vehicle-routing experiment that applies Q-learning ideas to a simplified logistics problem."""

import numpy as np

REWARD_MATRIX = np.array(
    [
        [-1, 50, 1, -1, -1, -1],
        [-1, -1, -1, 1, 50, -1],
        [-1, -1, -1, 1, -1, -1],
        [-1, -1, -1, -1, -1, 100],
        [-1, -1, -1, 50, -1, -1],
        [-1, -1, -1, -1, -1, 100],
    ],
    dtype=float,
)

GAMMA = 0.9
GOAL_STATE = 5
TRAINING_EPISODES = 10000


def all_actions(state):
    """Return the valid next actions for the given state."""
    return np.where(REWARD_MATRIX[state] >= 0)[0]


def next_action(available_actions):
    """Pick one valid action at random."""
    return int(np.random.choice(available_actions))


def update(q_matrix, current_state, action, gamma):
    """Apply one Q-learning update step."""
    max_indices = np.where(q_matrix[action] == np.max(q_matrix[action]))[0]
    if max_indices.shape[0] > 1:
        max_index = int(np.random.choice(max_indices))
    else:
        max_index = int(max_indices[0])

    max_value = q_matrix[action, max_index]
    q_matrix[current_state, action] = REWARD_MATRIX[current_state, action] + gamma * max_value
    return q_matrix[current_state, action]


def train(episodes=TRAINING_EPISODES, gamma=GAMMA):
    """Train a Q-matrix for the toy routing problem."""
    q_matrix = np.zeros_like(REWARD_MATRIX)
    for _ in range(episodes):
        current_state = np.random.randint(0, q_matrix.shape[0])
        action = next_action(all_actions(current_state))
        q_matrix[current_state, action] = update(q_matrix, current_state, action, gamma)
    return q_matrix


def extract_path(q_matrix, start_state=0, goal_state=GOAL_STATE):
    """Extract a greedy path from the trained Q-matrix."""
    current_state = start_state
    steps = [current_state]
    while current_state != goal_state:
        next_step_candidates = np.where(
            q_matrix[current_state] == np.max(q_matrix[current_state])
        )[0]
        if next_step_candidates.shape[0] > 1:
            next_state = int(np.random.choice(next_step_candidates))
        else:
            next_state = int(next_step_candidates[0])
        steps.append(next_state)
        current_state = next_state
    return steps


def main():
    """Train the routing example and print the learned path."""
    np.random.seed(0)
    q_matrix = train()
    print("Q matrix trained:")
    print(q_matrix / np.max(q_matrix) * 100)
    print("Shortest path:")
    print(extract_path(q_matrix))


if __name__ == "__main__":
    main()
