"""Helper functions for expanding neighboring nodes in the grid-search open list."""

from numpy import vstack
from numpy import zeros
from numpy import shape
from numpy import sqrt
from numpy import all

def expand_array (node_x,node_y,hn,xTarget,yTarget,CLOSED,MAX_X,MAX_Y):
#This function takes a node and returns the expanded list
#of successors,with the calculated fn values.
#The criteria being none of the successors are on the CLOSED list.
#EXPANDED ARRAY FORMAT
#--------------------------------------
#| X val | Y val | h(n) | g(n) | f(n) |
#--------------------------------------
    exp_array = zeros(5)
    exp_count = 0
    #%Number of elements in CLOSED including the zeros 
    c2 = shape(CLOSED)[0] 
    # This two for loops (k,j) are used to check the nodes surrounding the current node
    for k in [1,0,-1]: 
        for j in [1,0,-1]:
            if (k!=j or k!=0):  
                s_x = node_x+k
                s_y = node_y+j
                if( (s_x >=0 and s_x <MAX_X) and (s_y >=0 and s_y <MAX_Y)): #node within array bound S-Nadim - > && to (and)
                    flag = 1  
                    # Check if the nodes are already in the closed list                  
                    for c1 in range(0,c2): 
                        if(s_x == CLOSED[c1,0] and s_y == CLOSED[c1,1]):
                            flag = 0
                    #End of for loop to check if a successor is on closed list.
                    if (flag == 1): 
                        exp_array = vstack([exp_array,[ s_x , s_y , hn + sqrt((node_x - s_x)**2 + (node_y - s_y)**2), sqrt((xTarget - s_x)**2 + (yTarget - s_y)**2) ,  hn + sqrt((node_x - s_x)**2 + (node_y - s_y)**2) + sqrt((xTarget - s_x)**2 + (yTarget - s_y)**2)]])
                        exp_count += 1
    
                    #Populate the exp_array list!!!
                #% End of node within array bound
            #%End of if node is not its own successor loop 
        #%End of j for loop
    #%End of k for loop 
    # This if condition has been created because if there is no nodes in promiximity the expanded array will be zeros(5) so the return with two index won't work
    if all(exp_array == 0):
        return[0,0,0,0,0]
    else:
        return exp_array[1:exp_count+1,:]
    
    
    