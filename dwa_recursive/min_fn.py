from numpy import zeros
from numpy import vstack
from numpy import shape
from numpy import argmin
import numpy as np

def min_fn(OPEN,OPEN_COUNT,xTarget,yTarget):
    # Function to return the Node with minimum fn
    # This function takes the list OPEN as its input and returns the index of the nodethat has the least cost
    temp_array = zeros([9])
    flag = 0
    goal_index = 0
    for j in range(0,OPEN_COUNT):
        # Check if the actual node is active (it hasn't been expanded before)
        if (OPEN[j,0] == 1):
            # Salva il nodo in un array temporaneo apponogli in coda il
            # pedice che indica la posizione in cui si trova
            temp_array = vstack([temp_array,[OPEN[j,0],OPEN[j,1],OPEN[j,2],OPEN[j,3],OPEN[j,4],OPEN[j,5],OPEN[j,6],OPEN[j,7],j]])
            # Verifica se il nodo in esame è il target
            if (OPEN[j,1] == xTarget and OPEN[j,2] == yTarget):
                flag=1
                goal_index=j#Store the index of the goal node       
    #Get all nodes that are on the list open
    if flag == 1: # one of the successors is the goal node 
            i_min = goal_index
    #S the index of the smallest node
    if np.any(temp_array) :
        i = argmin(temp_array[1:shape(temp_array)[0],7])
        #while min(temp_array[:,7]) != temp_array[i,7]:
        #    i += 1  #Index of the smallest node in temp array
        i_min = int(temp_array[i+1,8])#Index of the smallest node in the OPEN array
    else:
        i_min = -1#The temp_array is empty i.e No more paths are available.
    return i_min