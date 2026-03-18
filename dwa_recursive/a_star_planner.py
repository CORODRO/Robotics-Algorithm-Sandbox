import numpy as np

from expand_array import expand_array
from insert_open import insert_open
from mapgenerator import mapgenerator
from min_fn import min_fn
from node_index import node_index
from visual_path import visual_path
#import DWA as dwa


def ast( start = np.array([0, 0]), target = np.array([9, 9]) ):
    # Define the dimension of the search field
    x_max = 10
    y_max = 10
    # Define start location
    # Start location [x y]
    # start = np.array([0, 0])
    # Define Target location
    # Target location [x y]
    #target = np.array([9, 9])
    # Define number of obstacles
    N = 20
    # Call the map generation function
    [map,obst] = mapgenerator(N, start[0], start[1], target[0], target[1], x_max, y_max)
    # Locate the target in to the map
    map[target[0], target[1]] = 2
    ## Preliminary procedures

    # CLOSED contains all the nodes that don't have to be evaluated
    # CLOSED ==> X val | Y val |
    # I've created the closed array and initialized it with the starting node because I don't know how to create an empty 1x2 array
    CLOSED = start
    # Put all obstacles on the Closed List
    for i in range(0,np.shape(obst)[1],1):
        CLOSED = np.vstack([CLOSED, [obst[0, i], obst[1, i]]]) # [[obst[0,i],obst[1,i]]
    # Update the dimension of the closed list whit the number of obstacles
    closed_count = i+1
    # Set the starting node as the firs node to expand
    xNode = start[0]
    yNode = start[1]
    # Assign a zero cost to the starting node (heuristic_function)
    path_cost = 0
    # Calculate starting distance to the target (cost_function)
    goal_distance = np.sqrt((target[0] - start[0])**2+(target[1] - start[1])**2)
    # OPEN list stores all the coordinates of all the nodes that have to be expanded, the coordinates of the # parent node and the 3 functions linked to that node: heuristic (distance from the start), cost (distance to the target), heuristic + cost.
    # OPEN ==> IS ON LIST 1/0 |X val |Y val |Parent X val |Parent Y val |h(n) |g(n)|f(n)|
    # Same as CLOSED
    OPEN = np.array([0,0,0,0,0,0,0,0])
    OPEN = np.vstack([OPEN,[0, xNode, yNode, xNode, yNode, path_cost, goal_distance, path_cost + goal_distance]])
    # Update the open list dimension with the first node added
    open_count = 2
    # Set the flag which tells us the impossibility to find a path    
    NoPath = 0
    new_node = []

    ## Main algorithm

    # Here there's the main loop which is iterated until the coordindates are
    # the same of the target node or is impossible to find a path
    while (xNode != target[0] or yNode!=target[1]) and NoPath == 0:
        # Expand the actual node exploring the adjacent nodes
        exp_node = expand_array(xNode, yNode, path_cost, target[0], target[1], CLOSED, x_max, y_max)
        # Counter which counts the number of allowed nodes created
        exp_count = np.shape(exp_node)[0]
        # In this loop we check if a node expanded is already present in the OPEN list and if the cost now calculated has decreased we update his cost.
        if np.any(exp_node):   
            for i in range(0,exp_count,1):
                new_node = 1
                for j in range(1,open_count,1):
                    #Check if the node is already present in the open list
                    if (exp_node[i,0] == OPEN[j,1] and exp_node[i,1] == OPEN[j,2]):
                        # If yes it match the cost values for the same node and take the minimum value
                        OPEN[j,7] = np.amin([OPEN[j,7],exp_node[i,4]])
                        new_node = 0
                        # If the cost has been updated (also if two costs are the same, the one already in OPEN e and the one found by the expansion then update all others parameter.
                        if OPEN[j, 7] == exp_node[i, 4]:
                            #UPDATE PARENTS,gn,hn
                            OPEN[j, 3] = xNode
                            OPEN[j, 4] = yNode
                            OPEN[j, 5] = exp_node[i, 2]
                            OPEN[j, 6] = exp_node[i, 3]
                        #End of minimum fn chec
                    #End of node check
                #End of j for
                # If the flag new_node is still 0 it means the node has never been explored before so it has to be added to the OPEN list
                if new_node == 1 :
                    OPEN = np.vstack([OPEN,[insert_open(exp_node[i,0],exp_node[i,1],xNode,yNode,exp_node[i,2],exp_node[i,3],exp_node[i,4])]])
                    open_count += 1
                #End of insert new element into the OPEN list
            #End of i for

        #Find out the node with the smallest fn
        index_min_node = min_fn(OPEN,open_count,target[0],target[1])
        # La funzione da -1 se non ci sono più nodi da espandere
        if (index_min_node != -1):
            #Set xNode and yNode to the node with minimum fn
            xNode = OPEN[index_min_node,1]
            yNode = OPEN[index_min_node,2]
            #Update the cost of reaching the parent node
            path_cost = OPEN[index_min_node,5]
            #Move the Node to list CLOSED
            CLOSED = np.vstack([CLOSED,[xNode,yNode]])
            closed_count += 1
            # Instead of remove the node from the OPEN list it is set unactive
            OPEN[index_min_node,0] = 0
        else:
            #No path exists to the Target!!
            NoPath = 1#Exits the loop!
        #End of index_min_node check
    #End of While Loop

    #Once algorithm has run The optimal path is generated by starting of at the
    #last node(if it is the target node) and then identifying its parent node
    #until it reaches the start node.This is the optimal path

    i = np.shape(CLOSED)[0]
    # Find the last node inserted in the closed list if everithing worked fine it should be the target node
    xval = CLOSED[i-1,0]
    yval = CLOSED[i-1,1]
    # Control if the last CLOSED node is the target one
    if ((xval == target[0] and yval == target[1])):
        #Traverse OPEN and determine the parent nodes
        parent_x = OPEN[node_index(OPEN,xval,yval),3]
        parent_y = OPEN[node_index(OPEN,xval,yval),4]

        Optimal_path = [parent_x, parent_y]
        
        while (parent_x != start[0] or parent_y != start[1]):
            Optimal_path = np.vstack([Optimal_path,[parent_x,parent_y]])
            inode = node_index(OPEN, parent_x, parent_y)
            parent_x = OPEN[inode,3]
            parent_y = OPEN[inode,4]     
        # Print a graphical output
        visual_path(start,map,Optimal_path[1:np.shape(Optimal_path)[0]+1])
        #dwa.main(target[0], target[1], np.transpose(obst), Optimal_path)
    else:
        print('\n Sorry, No path exists to the Target! \n')
        print(map)


ast()



