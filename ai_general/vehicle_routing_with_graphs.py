# -*- coding: utf-8 -*-
"""Vehicle-routing experiment that adds graph structure and visualization to the Q-learning prototype."""

import networkx as nx
import  matplotlib.pyplot as plt
import numpy as np
import random
from math import sqrt

def distance_between_coords(x1, x2):
    distance = sqrt(((x1[0] - x2[0]) ** 2) + ((x1[1] - x2[1]) ** 2))
    return distance

w1 = np.array([1.7592675, 92.4836507])
w2 = np.array([17.549836, 32.457398])
w3 = np.array([23.465896, 45])
w4 = np.array( [25.195462, 37.462742])
w5 = np.array([42.925274, 63.234028])
w6 = np.array([2.484631, 5.364871])
w7 = np.array([50.748376, 36.194797])

coords_w = np.array([w1,w2,w3,w4,w5,w6,w7])

RMatrix = np.zeros([len(coords_w),len(coords_w)])
for ii in range(0,len(coords_w)):
    for jj in range (0,len(coords_w)):
        if ii == jj:
            RMatrix[ii,jj] = -100
        elif jj == 0:
            RMatrix[ii,jj] = -100
        else:
            RMatrix[ii,jj]= distance_between_coords(coords_w[ii], coords_w[jj])
            

# RMatrix = np.matrix([ [-1,50,1,-1,-1,-1],
# [-1,-1,-1,1,50,-1],
# [-1,-1,-1,1,-1,-1],
# [-1,-1,-1,-1,-1,100],
# [-1,-1,-1,50,-1,-1],
# [-1,-1,-1,-1,-1,100] ])



QMatrix = np.zeros([len(coords_w),len(coords_w)])
gamma = 0.9
InitialState = 0

def AllActions(state):
    CurrentState = RMatrix[state,]
    AllAct = np.where(CurrentState >= 0)#[1]
    return AllAct

def NextAction(AvActRange):
    NextAct = int(np.random.choice(AvActRange[0],1))
    return NextAct

AvAct = AllActions(InitialState)
Action = NextAction(AvAct)

def Update(CurrentState, Action, gamma):
    MaxIndex = np.where(QMatrix[Action,] == np.max(QMatrix[Action,]))#[1]
    if MaxIndex[0].shape[0] > 1:
        MaxIndex = int(np.random.choice(MaxIndex[0], size = 1))
    else:
        MaxIndex = int(MaxIndex[0])
        
    MaxValue = QMatrix[Action, MaxIndex]
    QMatrix[CurrentState, Action] = \
    RMatrix[CurrentState, Action] + gamma * MaxValue
  
    return QMatrix[CurrentState, Action]
       
for i in range(10000):
   CurrentState = np.random.randint(0, int(QMatrix.shape[0]))
   AvAct = AllActions(CurrentState)
   Action = NextAction(AvAct)
   QMatrix[CurrentState,Action]=Update(CurrentState,Action,gamma)       
       
# Update(InitialState,Action,gamma)
print("Q matrix trained :")
print(QMatrix/np.max(QMatrix)*100)

CurrentState = 0
Steps = [CurrentState]
while CurrentState != 7:
        NextStepIndex = np.where(QMatrix[CurrentState,] == np.max(QMatrix[CurrentState,]))#[1]
        if NextStepIndex[0].shape[0] > 1:
            NextStepIndex = int(np.random.choice(NextStepIndex, size = 1))
        else:
            NextStepIndex = int(NextStepIndex[0])
            Steps.append(NextStepIndex)
            CurrentState = NextStepIndex
    
print("Shortest path:")   
print(Steps)