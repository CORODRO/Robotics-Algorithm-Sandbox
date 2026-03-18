# -*- coding: utf-8 -*-
"""Experiment that combines NetworkX graphs with Q-learning for shortest-path-style problems."""

import networkx as nx
import  matplotlib.pyplot as plt
import numpy as np
import random


 
# The algorithm is usable only for a Typical TPS --> Once trained the matrix can just tell you which
# is the shortest path to go from one point to another considering a series of waypoint. 
w1 = np.array([1.7592675, 92.4836507])
w2 = np.array([17.549836, 32.457398])
w3 = np.array([23.465896, 45])
w4 = np.array( [25.195462, 37.462742])
w5 = np.array([42.925274, 63.234028])
w6 = np.array([2.484631, 5.364871])
w7 = np.array([50.748376, 36.194797])
edges = [(1,2),(1,3),(1,4),(1,5),(2,3),
         (2,4),(2,6),(3,7),(7,5),(6,7),
         (6,5),(6,4),(5,4)]
# edges = [(1,2,weight=2),(1,3,weight=2),(1,4,weight=2),(1,5,weight=1),(2,3,weight=3),
#          (2,4,weight=4),(2,6,weight=1),(3,7,weight=6),(7,5,weight=4),(6,7,weight=1),
#          (6,5,weight=5),(6,4,weight=1),(5,4,weight=2)]
G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos)
plt.show()