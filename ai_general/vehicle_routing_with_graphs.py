# -*- coding: utf-8 -*-
"""Vehicle-routing experiment that adds graph structure and visualization to the Q-learning prototype."""

from math import sqrt

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

COORDS = np.array(
    [
        [1.7592675, 92.4836507],
        [17.549836, 32.457398],
        [23.465896, 45.0],
        [25.195462, 37.462742],
        [42.925274, 63.234028],
        [2.484631, 5.364871],
        [50.748376, 36.194797],
    ]
)

START_STATE = 0
GOAL_STATE = len(COORDS) - 1
GAMMA = 0.9
TRAINING_EPISODES = 10000
SHOW_PLOT = False


def distance_between_coords(point_a, point_b):
    """Return the Euclidean distance between two waypoint coordinates."""
    return sqrt(((point_a[0] - point_b[0]) ** 2) + ((point_a[1] - point_b[1]) ** 2))


def build_reward_matrix(coords):
    """Build a dense reward matrix with travel cost and a shaped goal reward."""
    reward_matrix = np.full((len(coords), len(coords)), -np.inf)
    for i in range(len(coords)):
        for j in range(len(coords)):
            if i == j or j == START_STATE:
                continue
            distance = distance_between_coords(coords[i], coords[j])
            reward = -distance
            if j == GOAL_STATE:
                reward += 100.0
            reward_matrix[i, j] = reward
    return reward_matrix


REWARD_MATRIX = build_reward_matrix(COORDS)


def all_actions(state):
    """Return the valid next actions for the given state."""
    return np.where(~np.isneginf(REWARD_MATRIX[state]))[0]


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
    """Train a Q-matrix for the waypoint-routing example."""
    q_matrix = np.zeros_like(REWARD_MATRIX)
    for _ in range(episodes):
        current_state = np.random.randint(0, q_matrix.shape[0])
        action = next_action(all_actions(current_state))
        q_matrix[current_state, action] = update(q_matrix, current_state, action, gamma)
    return q_matrix


def extract_path(q_matrix, start_state=START_STATE, goal_state=GOAL_STATE):
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


def build_graph():
    """Build a directed graph view of the routing problem for optional plotting."""
    graph = nx.DiGraph()
    for idx, coord in enumerate(COORDS):
        graph.add_node(idx, pos=(coord[0], coord[1]))
    for i in range(len(COORDS)):
        for j in all_actions(i):
            graph.add_edge(i, j, weight=round(distance_between_coords(COORDS[i], COORDS[j]), 2))
    return graph


def plot_graph(path):
    """Plot the waypoint graph and highlight the learned route."""
    graph = build_graph()
    positions = nx.get_node_attributes(graph, "pos")
    plt.figure(figsize=(8, 6))
    nx.draw(graph, positions, with_labels=True, node_color="lightblue", node_size=700)
    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=nx.get_edge_attributes(graph, "weight"),
        font_size=7,
    )
    route_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=route_edges,
        edge_color="crimson",
        width=2.5,
    )
    plt.title("Learned routing path")
    plt.tight_layout()
    plt.show()


def main():
    """Train the routing example, print the path, and optionally plot it."""
    np.random.seed(0)
    q_matrix = train()
    print("Q matrix trained:")
    print(q_matrix)
    path = extract_path(q_matrix)
    print("Shortest path:")
    print(path)
    if SHOW_PLOT:
        plot_graph(path)


if __name__ == "__main__":
    main()
