# -*- coding: utf-8 -*-
"""Minimal Q-learning example for students learning value updates and policy improvement."""

from copy import deepcopy
import random

import numpy as np

ZOMBIE = "z"
CAR = "c"
ICE_CREAM = "i"
EMPTY = "*"

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
ACTIONS = [UP, DOWN, LEFT, RIGHT]


class State:
    """Simple grid-world state storing the current map and the agent position."""

    def __init__(self, grid, pos):
        self.grid = grid
        self.pos = pos

    def __eq__(self, other):
        return isinstance(other, State) and self.grid == other.grid and self.pos == other.pos

    def __hash__(self):
        return hash((str(self.grid), tuple(self.pos)))

    def __str__(self):
        return f"State(grid={self.grid}, pos={self.pos})"


def act(state, action):
    """Apply one action in the grid world and return the next state and reward."""

    p = deepcopy(state.pos)
    if action == UP:
        p[0] = max(0, p[0] - 1)
    elif action == DOWN:
        p[0] = min(len(state.grid) - 1, p[0] + 1)
    elif action == LEFT:
        p[1] = max(0, p[1] - 1)
    elif action == RIGHT:
        p[1] = min(len(state.grid[0]) - 1, p[1] + 1)
    else:
        raise ValueError(f"Unknown action {action}")

    grid_item = state.grid[p[0]][p[1]]
    new_grid = deepcopy(state.grid)

    if grid_item == ZOMBIE:
        reward = -100
        done = True
        new_grid[p[0]][p[1]] += CAR
    elif grid_item == ICE_CREAM:
        reward = 1000
        done = True
        new_grid[p[0]][p[1]] += CAR
    elif grid_item == EMPTY:
        reward = -1
        done = False
        old = state.pos
        new_grid[old[0]][old[1]] = EMPTY
        new_grid[p[0]][p[1]] = CAR
    elif grid_item == CAR:
        reward = -1
        done = False
    else:
        raise ValueError(f"Unknown grid item {grid_item}")

    return State(grid=new_grid, pos=p), reward, done


def q_value(q_table, state, action=None):
    """Return a state's Q row or a single action value, creating it if needed."""
    if state not in q_table:
        q_table[state] = np.zeros(len(ACTIONS))

    if action is None:
        return q_table[state]

    return q_table[state][action]


def choose_action(q_table, state, eps):
    """Choose an epsilon-greedy action."""
    if random.uniform(0, 1) < eps:
        return random.choice(ACTIONS)
    return int(np.argmax(q_value(q_table, state)))


def main():
    """Train the toy agent and print the learned Q-values for two states."""
    grid = [
        [ICE_CREAM, EMPTY],
        [ZOMBIE, CAR],
    ]
    start_state = State(grid=grid, pos=[1, 1])

    random.seed(42)

    n_episodes = 20
    max_episode_steps = 100
    min_alpha = 0.02
    gamma = 1.0
    eps = 0.2
    alphas = np.linspace(1.0, min_alpha, n_episodes)
    q_table = {}

    for episode in range(n_episodes):
        state = start_state
        total_reward = 0
        alpha = alphas[episode]

        for _ in range(max_episode_steps):
            action = choose_action(q_table, state, eps)
            next_state, reward, done = act(state, action)
            total_reward += reward

            q_row = q_value(q_table, state)
            q_row[action] = q_row[action] + alpha * (
                reward + gamma * np.max(q_value(q_table, next_state)) - q_row[action]
            )

            state = next_state
            if done:
                break

        print(f"Episode {episode + 1}: total reward -> {total_reward}")

    start_values = q_value(q_table, start_state)
    print(
        f"up={start_values[UP]}, down={start_values[DOWN]}, "
        f"left={start_values[LEFT]}, right={start_values[RIGHT]}"
    )
    next_state, _, _ = act(start_state, UP)
    next_values = q_value(q_table, next_state)
    print(
        f"up={next_values[UP]}, down={next_values[DOWN]}, "
        f"left={next_values[LEFT]}, right={next_values[RIGHT]}"
    )


if __name__ == "__main__":
    main()
