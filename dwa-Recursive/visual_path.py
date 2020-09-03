from numpy import shape

def visual_path(start,map,Optimal_path):
    # Denote the start position with number 3
    map[start[0],start[1]] = 3
    print('\nStarting Map')
    print(map)
    print('\nOptimal Path Nodes')
    length = shape(Optimal_path)[0]
    for i in range(length-1,-1,-1):
        # Denote a step with number 4
        map[int(Optimal_path[i,0]),int(Optimal_path[i,1])] = 4
        print(Optimal_path[i,:])
        # Uncomment this if you want to print step by step map
        #print('\n')
        #print (map)
    print ('\nOptimal Path Map')
    print(map)
