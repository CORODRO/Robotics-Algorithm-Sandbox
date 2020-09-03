"""from numpy import zeros 
from numpy import random 

def mapgenerator(N,x_start,y_start,x_target,y_target,x_dim,y_dim):
    # mapgenerator(N) take a real number N , that represent the number of
    # obstacle in a map and create a random matrix of dafault size with N obstacles.

    ## Space Dimension

    # Discretization of the space
    dx = 1 # meters
    dy = 1 # meters

    # Map Generation
    x_MAP = len(range(0,x_dim,dx))
    y_MAP = len(range(0,y_dim,dy))

    # Set as "Obstacle Free" all the space
    M = zeros((x_MAP,y_MAP))
    
    # Initialize the obstacles vector
    obst = zeros((2,N))
   
    # Check if there are too obstacle compared to the size of the space, 
    if N > ((x_MAP*y_MAP)-2):
        print('The Number the of obstacles is too high! Reduce it!! \n')
        return [[],[]]   
    # Add Obstacle in Random Position
    else:
        i=0
        while i < N:
            # Random number generation between x_MAP and y_MAP, this will be the position of random obstacles 
            x_r = random.randint(x_MAP)
            y_r = random.randint(y_MAP)
            
            # Check to avoid inserting an obstacle where another is already present
            if M[x_r,y_r] == 1 or (x_r == x_start and y_r == y_start) or (x_r == x_target and y_r == y_target):
                # If in this position there is already an obstacle, we will try
                # again
                i -= 1
            else:
                # If in this position there is not an obstacle, we can add him.
                M[x_r,y_r] = 1
                # Add also the node to the obstacles vector
                obst[0,i] = x_r
                obst[1,i] = y_r
            
            i += 1
    return(M,obst)"""
import numpy as np

def mapgenerator():

    obst = np.array([[0, 2],
                    [1, 2], 
                    [2, 2], 
                    [3, 2], 
                    [8, 3], 
                    [9, 3], 
                    [1, 4], 
                    [6, 4], 
                    [1, 5], 
                    [5, 5], 
                    [6, 5], 
                    [4, 6], 
                    [9, 6], 
                    [0, 7], 
                    [6, 7], 
                    [4, 8], 
                    [5, 8], 
                    [8, 8], 
                    [0, 9], 
                    [4, 9]])

    # Aggiunta bordi mappa sotto forma ostacoli
    for i in range(-1,11):
        obst = np.vstack([obst, [i,-1]])
        obst = np.vstack([obst, [-1,i]])
        obst = np.vstack([obst, [i,11]])
        obst = np.vstack([obst, [11,i]])
   # Creazione mappa grafica
 
    M = np.zeros((10,10))
    
    for i in range(0,20):
        M[obst[i,0], obst[i,1]] = 1
    obst = np.transpose(obst)
    return(M,obst)


if __name__ == '__main__':
    mapgenerator()