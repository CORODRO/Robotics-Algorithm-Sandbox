"""Helper that returns the array index of a node stored in the open list."""

def node_index(OPEN,xval,yval):
    #This function returns the index of the location of a node in the list OPEN
    i = 0
    while(OPEN[i,1] != xval or OPEN[i,2] != yval ):
        i += 1
    n_index = i
    return n_index
