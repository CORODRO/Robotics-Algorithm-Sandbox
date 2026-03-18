"""Helper for generating simple obstacle maps used by the planner experiments."""

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