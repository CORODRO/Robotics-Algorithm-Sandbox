# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 08:28:14 2020

@author: Jasmine Rimani
https://stackoverflow.com/questions/38868205/0-1-knapsack-with-dependent-item-weight
https://gist.github.com/shshemi/a16893b885bb2b31da9c9839619e5a65
"""

import numpy as np
from keras.models import Model
from keras.layers import Dense, Activation, Lambda, Input, Concatenate, Multiply
from keras.metrics import binary_accuracy
from keras.losses import binary_crossentropy
import keras.backend as K


def test_knapsack(x_weights, x_prices, x_capacity, picks):
    total_price = np.dot(x_prices, picks)
    total_weight = np.dot(x_weights, picks)
    return total_price, max(total_weight - x_capacity, 0)


def brute_force_knapsack(x_weights, x_prices, x_capacity):
    picks_space = 2 ** x_weights.shape[0]
    best_price = 0
    best_picks = None
    for p in range(picks_space):
        picks = np.zeros((x_weights.shape[0]))
        for i, c in enumerate("{0:b}".format(p)[::-1]):
            picks[i] = c
        price, violation = test_knapsack(x_weights, x_prices, x_capacity, picks)
        if violation == 0:
            if price > best_price:
                best_price = price
                best_picks = picks
    return best_price, best_picks


def create_knapsack(item_count=5):
    x_weights = np.random.randint(1, 15, item_count)
    x_prices = np.random.randint(1, 10, item_count)
    x_capacity = np.random.randint(15, 50)
    _, y_best_picks = brute_force_knapsack(x_weights, x_prices, x_capacity)
    return x_weights, x_prices, x_capacity, y_best_picks

def metric_overprice(input_prices):
    def overpricing(y_true, y_pred):
        y_pred = K.round(y_pred)
        return K.mean(K.batch_dot(y_pred, input_prices, 1) - K.batch_dot(y_true, input_prices, 1))

    return overpricing

def metric_space_violation(input_weights, input_capacity):
    def space_violation(y_true, y_pred):
        y_pred = K.round(y_pred)
        return K.mean(K.maximum(K.batch_dot(y_pred, input_weights, 1) - input_capacity, 0))

    return space_violation

def metric_pick_count():
    def pick_count(y_true, y_pred):
        y_pred = K.round(y_pred)
        return K.mean(K.sum(y_pred, -1) - K.sum(y_true, -1))

    return pick_count

x_weights, x_prices, x_capacity, y_best_picks = create_knapsack()
print("Weights:", x_weights)
print("Prices:", x_prices)
print("Capacity:", x_capacity)
print("Best picks:", y_best_picks)


def create_knapsack_dataset(count, item_count=5):
    x = [[], [], []]
    y = [[]]
    for _ in range(count):
        p = create_knapsack(item_count)
        x[0].append(p[0])
        x[1].append(p[1])
        x[2].append(p[2])
        y[0].append(p[3])
    return x, y
train_x, train_y = create_knapsack_dataset(10000)
test_x, test_y = create_knapsack_dataset(200)

def train_knapsack(model):
    from keras.callbacks import ModelCheckpoint
    import os
    if os.path.exists("best_model.h5"): os.remove("best_model.h5")
    model.fit(train_x, train_y, epochs=96, verbose=0, callbacks=[ModelCheckpoint("best_model.h5", monitor="loss", save_best_only=True, save_weights_only=True)])
    model.load_weights("best_model.h5")
    train_results = model.evaluate(train_x, train_y, 64, 0)
    test_results = model.evaluate(test_x, test_y, 64, 0)
    print("Model results(Train/Test):")
    print(f"Loss:               {train_results[0]:.2f} / {test_results[0]:.2f}")
    print(f"Binary accuracy:    {train_results[1]:.2f} / {test_results[1]:.2f}")
    print(f"Space violation:    {train_results[2]:.2f} / {test_results[2]:.2f}")
    print(f"Overpricing:        {train_results[3]:.2f} / {test_results[3]:.2f}")
    print(f"Pick count:         {train_results[4]:.2f} / {test_results[4]:.2f}")
    




# G = nx.Graph()
# # G.add_nodes_from(['w1','w2','w3','w4','w5','w6','w7'])
# G.add_edges_from([(1, 2, weight=d_12), 
#                   # ('w1', 'w3'), ('w1', 'w4'),('w1', 'w5'),('w1', 'w6'),('w1', 'w7'),
#                   # ('w2', 'w3'), ('w2', 'w4'),('w2', 'w5'),('w2', 'w6'),('w2', 'w7'),
#                   # ('w3', 'w4'),('w3', 'w5'),('w3', 'w6'),('w3', 'w7'),
#                   # ('w4', 'w5'),('w4', 'w6'),('w4', 'w7'),
#                   # ('w5', 'w6'),('w5', 'w7'),
#                   (3, 4)])

# Alternative Method G.add_node(['A', 'B'])

# G.add_edge('A', 'B')
# G.add_edge('A', 'C')
# G.add_edge('A', 'D')
# G.add_edge('A', 'E')
# G.add_edge('A', 'G')
# G.add_edge('B', 'C')
# G.add_edge('C', 'D')
# G.add_edge('D', 'E')
# G.add_edge('F', 'G')

# nx.draw(G,with_labels=True, font_weight='bold')
# plt.show()
# # Upper Bound --> Pure Traveling Salesman: all items have minimum weight and all dependecies exist
# # Lower Bound --> All the points have the maximum weight --> no dependecies
# # Calculate the real weights

# # Python3 program to solve  
# # Traveling Salesman Problem using  
# # Branch and Bound. 
# G = nx.Graph()
# G.add_node(1)
# G.add_node(2)
# G.add_node(3)
# G.add_node(4)
# G.add_edge(1, 2, weight=2)
# G.add_edge(2, 3, weight=2)
# G.add_edge(3, 4, weight=3)
# G.add_edge(1, 3, weight=5)
# G.add_edge(2, 4, weight=6)
# pos = nx.spring_layout(G, scale=3)
# nx.draw(G, pos,with_labels=True, font_weight='bold')
# edge_labels = nx.get_edge_attributes(G,'r')
# nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
# plt.show()
# print(nx.shortest_path(G,1,4,weight='weight'))
# print(nx.nx.shortest_path_length(G,1,4,weight='weight'))