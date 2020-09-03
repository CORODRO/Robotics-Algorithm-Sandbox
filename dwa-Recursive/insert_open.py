def insert_open(xNode,yNode,xPar,yPar,h,g,f):
#This function is used to add a node to the OPEN list.
#The OPEN list is structured as follows:
#OPEN ARRAY FORMAT
#------------------------------------------------------------------------------
#|IS ON LIST: 1/0 |X val |Y val |Parent X val |Parent Y val |h(n) |g(n) |f(n) |
#------------------------------------------------------------------------------
    add_node = [1,xNode, yNode, xPar, yPar, h, g, f]
    return add_node
