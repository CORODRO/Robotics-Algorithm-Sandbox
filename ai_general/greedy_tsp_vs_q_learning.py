# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:20:08 2020

@author: jasmi
https://stackoverflow.com/questions/59230049/find-the-shortest-distance-between-sets-of-gps-coordinates-python
https://towardsdatascience.com/optimization-with-python-how-to-make-the-most-amount-of-money-with-the-least-amount-of-risk-1ebebf5b2f29
https://towardsdatascience.com/linear-programming-and-discrete-optimization-with-python-using-pulp-449f3c5f6e99
https://github.com/tirthajyoti/Optimization-Python/blob/master/Portfolio_optimization.ipynb
https://github.com/tirthajyoti/Optimization-Python/blob/master/Portfolio_optimization.ipynb
https://or.stackexchange.com/questions/3288/branch-and-bound-implementation
"""


from collections import defaultdict
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np
import random
from copy import deepcopy
import time

# Shortest path to all coordinates from any node
# Coordinates must be provided as a list containing lists of
# x/y pairs. ie [[23.2321, 58.3123], [x.xxx, y.yyy]]


def distance_between_coords(x1, y1, x2, y2):
    distance = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return distance


# Adds "names" or better "numbers" to coordinates to use as keys for edge detection
def name_coords(coords):
    coord_count = 0
    for coord in coords:
        coord_count += 1
        coord.append(coord_count)
    return coords

# Adds rewards to coordinates to use as keys for edge detection
def rewards_coords(coords, reward_vector):
    coord_count = 0
    for coord in coords:
        coord.append(reward_vector[coord_count])
        coord_count += 1
        
    return coords

# Creates a weighted and undirected graph
# Returns named coordinates and their connected edges as a dictonary
def graph(coords):
    coords = name_coords(coords)
    graph = defaultdict(list)
    edges = {}
    for current in coords:
        for comparer in coords:
            if comparer == current: # pair (1,1) - (2,2) - (3,3)- etc.
                continue
            else:
                weight = distance_between_coords(current[0], current[1],
                                                 comparer[0], comparer[1])
                graph[current[2]].append(comparer[2])
                edges[current[2], comparer[2]] = weight
   

    return coords, edges


# Returns a path to all nodes with least weight as a list of names
# from a specific node
def shortest_path(node_list, edges, start):
    neighbor = 0
    unvisited = []
    visited = []
    total_weight = 0
    total_weight_v = []
    current_node = start
    reward_value = 0
    # the visited node is the starting one
    # the unvisited are all the others
    for node in node_list:
        if node[2] == start:
            visited.append(start)
            total_weight_v.append(0)
            # current_reward = node_list[node[2]-1][-1]
            # reward_value_v.append(current_reward)   
        else:
            unvisited.append(node[2])
      
    while unvisited:
        for index, neighbor in enumerate(unvisited):
            if index == 0:
                current_weight = edges[start, neighbor]
                # current_reward = node_list[neighbor-1][-1]
                current_node = neighbor   
            elif edges[start, neighbor] < current_weight:
                current_weight = edges[start, neighbor]
                # current_reward = node_list[neighbor-1][-1]
                current_node = neighbor
        total_weight += current_weight
        total_weight_v.append(current_weight)
        unvisited.remove(current_node)
        visited.append(current_node)
        # reward_value_v.append(current_reward)
        
    for ii in visited:
        reward_value += (node_list[ii-1][-1])
        
    
    return visited, total_weight, reward_value, total_weight_v

def reward_TSP(coords,reward_vector,start_point):
    
    coords, edges = graph(coords)
    coords = rewards_coords(coords, reward_vector)
    shortest_path_taken, shortest_path_weight, shortest_path_reward, total_weight_v = shortest_path(coords, edges, start_point)
    # shortest_path_taken = []
    # shortest_path_weight = 0

    # for index, node in enumerate(coords):
    #     path, weight, reward = shortest_path(coords, edges, index + 1)
    #     print('--------------------------------------')
    #     print("Path", index + 1, "=", path)
    #     print("Weight =", weight)
    #     print("Reward =", reward)
    #     if index == 0:
    #         shortest_path_weight = weight
    #         shortest_path_taken = path
    #         shortest_path_reward = reward
    #     elif weight < shortest_path_weight:
    #         shortest_path_weight = weight
    #         shortest_path_taken = path
    #         shortest_path_reward = reward

    
    return shortest_path_taken, shortest_path_weight, shortest_path_reward, total_weight_v


# def choose_action(state, max_number_actions,eps):
#     if random.uniform(0, 1) < eps:
#         return random.choice( max_number_actions) 
#     else:
#         return np.argmax(q(state))

   
# def q(state, action=None, max_number_actions):
    
#     if state not in q_table:
#         q_table[state] = np.zeros(len(max_number_actions))
        
#     if action is None:
#         return q_table[state]
    
#     return q_table[state][action]

# A naive recursive implementation 
# of 0-1 Knapsack Problem 
  
# Returns the maximum value that  
# can be put in a knapsack of  
# capacity W 
    
# To test above function 
# val = [60, 100, 120] 
# wt = [10, 20, 30] 
# W = 50
# n = len(val) 
# print (knapSack(W, wt, val, n))
    
# def knapSack(W, wt, val, n): 
  
#     # Base Case 
#     if n == 0 or W == 0 : 
#         return 0
  
#     # If weight of the nth item is  
#     # more than Knapsack of capacity W,  
#     # then this item cannot be included  
#     # in the optimal solution 
#     if (wt[n-1] > W): 
#         return knapSack(W, wt, val, n-1) 
  
#     # return the maximum of two cases: 
#     # (1) nth item included 
#     # (2) not included 
#     else: 
#         return max( 
#             val[n-1] + knapSack( 
#                 W-wt[n-1], wt, val, n-1),  
#                 knapSack(W, wt, val, n-1)) 
    


# class Env():
#     # def __init__(self,coords):
#     #     self.height = len(coords);
#     #     self.width = len(coords);
#     #     self.posX = 0;
#     #     self.posY = 0;
#     #     self.endX = self.width-1;
#     #     self.endY = self.height-1;
#     #     self.actions = [0, 1, 2, 3];
#     #     self.stateCount = self.height*self.width;
#     #     self.actionCount = len(self.actions);

#     def reset(self):
#         self.posX = 0;
#         self.posY = 0;
#         self.done = False;
#         return 0, 0, False;

#     # take action
#     def step(self, action):
#         if action==0: # left
#             self.posX = self.posX-1 if self.posX>0 else self.posX;
#         if action==1: # right
#             self.posX = self.posX+1 if self.posX<self.width-1 else self.posX;
#         if action==2: # up
#             self.posY = self.posY-1 if self.posY>0 else self.posY;
#         if action==3: # down
#             self.posY = self.posY+1 if self.posY<self.height-1 else self.posY;

#         done = self.posX==self.endX and self.posY==self.endY;
#         # mapping (x,y) position to number between 0 and 5x5-1=24
#         nextState = self.width*self.posY + self.posX;
#         reward = 1 if done else 0;
#         return nextState, reward, done;

#     # return a random action
#     def randomAction(self):
#         return np.random.choice(self.actions);

#     # display environment
#     def render(self):
#         for i in range(self.height):
#             for j in range(self.width):
#                 if self.posY==i and self.posX==j:
#                     print("O", end='');
#                 elif self.endY==i and self.endX==j:
#                     print("T", end='');
#                 else:
#                     print(".", end='');
#             print("");


# def AllActions(state, RMatrix):
#     """The state of the environment is passed and the numpy library's
#        where function is used to select all the available actions contained
#        in the RMatrix row specified by the state that satisfies the
#        CurrentState >= 0 condition
#        """
#     CurrentState = RMatrix[state,]
#     AllAct = np.where(CurrentState > 0)[0]
#     return AllAct


# def NextAction(AvActRange):
#     """Random Actions"""
#     NextAct = int(np.random.choice(AvActRange,1))
#     return NextAct


# def Update(CurrentState, Action, gamma, Q_Matrix, RMatrix, reward_vector, contraints_path_length, weight_penality_total, visited):
    
#     # Q_matrix[CurrentState,Action] = 1
#     weight_penalty = R_matrix[CurrentState,Action]
    
#     if visited == True:
#          already_visited_penality = -100
#     else:
#          already_visited_penality = 0
    
#     visited[CurrentState,Action] = True
#     weight_reward = reward_vector[Action]+reward_vector[CurrentState]
#     Q_matrix[CurrentState,Action] = Q_matrix[CurrentState,Action] + (weight_reward - weight_penalty + already_visited_penality)
#     weight_penality_total = weight_penality_total+weight_penalty
#     if weight_penality_total >= contraints_path_length:
#         done = 1
#         Q_matrix[CurrentState,Action] = Q_matrix[CurrentState,Action] - abs(weight_penality_total-contraints_path_length)
#     # done = weight_penality_total >= contraints_path_length
#     newState = 1
#     return next_state, reward, done, visited
    
    
def Update(CurrentState, Action, gamma, QMatrix, RMatrix, visited, reward_vector, contraints_path_length):
    
    if shortest_path_weight >= contraints_path_length:
        done = True
        path_overshoot_penality = shortest_path_weight-contraints_path_length
        
    return  done
    

    
    
    # MaxIndex = np.where(QMatrix[Action,] == np.max(QMatrix[Action,]))[0]
    # if MaxIndex.shape[0] > 1:
    #     MaxIndex = int(np.random.choice(MaxIndex, size = 1))
    # else:
    #     MaxIndex = int(MaxIndex)
        
    # MaxValue = QMatrix[Action, MaxIndex]
    # QMatrix[CurrentState, Action] = \
    # RMatrix[CurrentState, Action] + gamma * MaxValue
  
    # return total_reward, next_state, done
        

if __name__ == '__main__':
    os.system('clear')
    
    w1 = np.array([1.7592675, 92.4836507])
    w2 = np.array([17.549836, 32.457398])
    w3 = np.array([23.465896, 45])
    w4 = np.array( [25.195462, 37.462742])
    w5 = np.array([42.925274, 63.234028])
    w6 = np.array([2.484631, 5.364871])
    w7 = np.array([50.748376, 36.194797])
    
    coords_w = np.array([w1,w2,w3,w4,w5,w6,w7])

    coords = np.array([[1.7592675, 92.4836507], 
              [17.549836, 32.457398],
              [23.465896, 45], 
              [25.195462, 37.462742],
              [42.925274, 63.234028], 
              [2.484631, 5.364871],
              [50.748376, 36.194797]])  
    
    # the algorith works better with list! --> Remember lists are changed in functions, they are pointers like C++
    # coords_list = coords.tolist()
    
    reward_vector = [10,11,5,4,6,7,8]
    jj = 2
    start_point = 1
    constrain_distance = 200
    constrain_reward = 0
    chosen_weight_it = constrain_distance
    
    # dummy_coords = coords
    ii = 1
    # Brute Force
    while ii < (len(coords)-1):
        dummy_coords = np.concatenate([[coords[0]],coords[ii::]])
        while jj < (len(dummy_coords)+1):
            coords_list = dummy_coords[0:jj].tolist()
            # coords_list, edges = graph(coords_list)
            # coords_list = rewards_coords(coords_list, reward_vector)
            shortest_path_taken, shortest_path_weight, shortest_path_reward, total_weight_v = reward_TSP(coords_list,reward_vector, start_point)
            print("The shortest path to all nodes is:", shortest_path_taken)
            print("The weight of the path is:", shortest_path_weight)
            print("The reward of the path is:", shortest_path_reward)
            
            if (shortest_path_weight <= constrain_distance) and (shortest_path_weight <= chosen_weight_it)  and (shortest_path_reward >= constrain_reward):
                chosen_path = coords[0:jj]
                chosen_weight = shortest_path_weight
                chosen_reward = shortest_path_reward
                constrain_reward = chosen_reward
                chosen_shortest_path_taken = shortest_path_taken
 
            coords_list.clear()
            jj = jj+1
        print('--------------------------------------')
        print("Chosen Path:", chosen_path)
        print("The shortest path to all nodes is:", chosen_shortest_path_taken)
        print("The weight of the path is:", chosen_weight)
        print("The reward of the path is:", chosen_reward)
        print('--------------------------------------')
        jj = 2
        ii = ii+1
        chosen_weight_it = chosen_weight
        
        
            
    
    
    
    # each action earase a point in coords 
    # max_number_actions = np.arange(len(coords))+1
    
    # # hyperparameters
    # epochs = 200
    # gamma = 0.5
    # epsilon = 0.08
    # decay = 0.1
    
    # contraints_path_length = 100
    
    # start_point = 1
    # coords_list, edges = graph(coords_list)
    # coords_list = rewards_coords(coords_list, reward_vector)
    
    # # # Mask Matrix that state the connections between the nodes
    # RMatrix_distance = np.zeros((len(coords),len(coords)))
    # RMatrix_weight = np.zeros((len(coords),len(coords)))
    # for ii in range(len(coords)):
    #     for jj in range(len(coords)):
    #         if ii == jj:
    #             RMatrix_distance[ii,jj] = -np.inf
    #             RMatrix_weight[ii,jj] = -1
    #         else:
    #             RMatrix_distance[ii,jj] = -edges[ii+1,jj+1]
    #             RMatrix_weight[ii,jj] = RMatrix_distance[ii,jj]+reward_vector[ii]+reward_vector[jj] 
    
    
    
    
    
    # shortest_path_taken, shortest_path_weight, shortest_path_reward, total_weight_v = reward_TSP(coords_list,reward_vector, start_point)
    # print("The shortest path to all nodes is:", shortest_path_taken)
    # print("The weight of the path is:", shortest_path_weight)
    # print("The reward of the path is:", shortest_path_reward)
    # coords_list.clear()
    # # x = knapSack(contraints_path_length, total_weight_v, reward_vector, len(reward_vector))
    
    # # # Matrix that should learn the best policy
    # # QMatrix = np.zeros((len(coords),len(coords)))
    
    # # # Mask Matrix that state the connections between the nodes
    # RMatrix = np.zeros((len(coords),len(coords)))
    # # # RMatrix_inv = np.zeros((len(coords),len(coords)))
    # for ii in range(len(coords)):
    #     for jj in range(len(coords)):
    #         if ii == jj:
    #             RMatrix[ii,jj] = -np.inf
    #             # RMatrix_inv[ii,jj] = -1
    #         else:
    #             RMatrix[ii,jj] = -edges[ii+1,jj+1]+reward_vector[ii]+reward_vector[jj]
    #             # RMatrix_inv[ii,jj] = edges[ii+1,jj+1]
                
    # # AvAct = AllActions(start_point-1, RMatrix)
    # # Action = NextAction(AvAct)
    # visited = []
    # CurrentState = 0
    # visited.append(CurrentState)
    # # Update(CurrentState, Action, gamma, Q_matrix, R_matrix, reward_vector, contraints_path_length) 
    # for i in range(epochs):
    #    CurrentState = np.random.randint(0, int(QMatrix.shape[0]))
    #    AvAct = AllActions(CurrentState, RMatrix)
    #    Action = NextAction(AvAct)
       
    #    QMatrix[CurrentState,Action] = Update(CurrentState,Action,gamma, QMatrix, RMatrix, visited)       
       
    # # Update(InitialState,Action,gamma)
    # print("Q matrix trained :")
    # print(QMatrix) 
    
    # CurrentState = start_point-1
    # Steps = [CurrentState]
    # while CurrentState != 6:
    #     NextStepIndex = np.where(QMatrix[CurrentState,] == np.max(QMatrix[CurrentState,]))[0]
    #     if NextStepIndex.shape[0] > 1:
    #         NextStepIndex = int(np.random.choice(NextStepIndex, size = 1))
    #     else:
    #         NextStepIndex = int(NextStepIndex)
    #         Steps.append(NextStepIndex)
    #         CurrentState = NextStepIndex
    
    # print("Shortest path:")   
    # print(Steps)
    
    
    
    # for kk in range(epochs):
    #     steps = 0
    #     # os.system('clear')
    #     # time.sleep(0.05)
    #     done = False
    #     CurrentState = start_point-1
        
    #     while not done: 
    #         # count steps to finish game
    #          steps += 1
             
    #          # act randomly sometimes to allow exploration
    #          AvAct = AllActions(CurrentState, R_matrix)
    #          Action = NextAction(AvAct)
             
    #          # take next action 
    #          next_state, reward, done, visited = Update()
             
    #          # update table
    #          Q_matrix[CurrentState][Action] = reward + gamma*max(Q_matrix[next_state])
             
    #          #update state 
    #          CurrentState = next_state
    
    #     epsilon -= decay*epsilon
    #     print("\nDone in", steps, "steps".format(steps))
    #     time.sleep(0.8)
        
        # The more we learn, the less we take random actions
        
        
    
    
    
    
    
    
    
    # for ii in range(len(coords)-1):
    #     coords_sample = np.delete(coords,ii+1,0)
    #     coords_list = coords_sample.tolist()
    #     shortest_path_taken, shortest_path_weight, shortest_path_reward = reward_TSP(coords_list,reward_vector, start_point)
    #     shortest_path_take = shortest_path_take
    #     print('--------------------------------------')
    #     print("The shortest path to all nodes is:", shortest_path_taken)
    #     print("The weight of the path is:", shortest_path_weight)
    #     print("The reward of the path is:", shortest_path_reward)
    #     coords_list.clear()
    
    
    
    
    # shortest_path_taken, shortest_path_weight, shortest_path_reward = reward_TSP(coords_list,reward_vector, start_point)
    # coords_list.clear()

    

        
        
    
    
    
    
    
    
    
    # Different nodes considered, different length and different rewards
    # path_constraint_distance = 200
    # path_constraints_max_reward = 0
    # coords, edges = graph(coords)
    # coords = rewards_coords(coords, reward_vector)

    
    # for ii in range(len(coords)):
    #     start_sample = ii
        
    #     for jj in range (len(coords)-ii):
    #         end_sample = len(coords)-jj
            
            
    #         shortest_path_taken_sample = []
    #         shortest_path_weight_sample = 0
    #         path_1, weight_1, reward_1 = shortest_path(coords[start_sample: end_sample], edges, start_sample+1)
    #         print('--------------------------------------')
    #         print("Path", ii + 1, "=", path_1)
    #         print("Weight =", weight_1)
    #         print("Reward =", reward_1) 
    #         coords_sample = []
    #         # coords_sample.remove(2,3)


            
            
        
        
        
        
        
           
    
    
    
    
    # for ii in range(len(coords)):
    #     path_1, weight_1, reward_1 = shortest_path(coords[start_1-1:-1+ii], edges, start_1)
    #     print('--------------------------------------')
    #     print("Path", ii + 1, "=", path_1)
    #     print("Weight =", weight_1)
    #     print("Reward =", reward_1)
    


   
# if __name__ == '__main__':
#     driver()