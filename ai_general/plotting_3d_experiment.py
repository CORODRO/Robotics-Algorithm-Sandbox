# -*- coding: utf-8 -*-
"""Small 3D plotting sandbox used to visualize terrain-style datasets."""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math 
import random

D = np.arange(0.05,1,0.01)
N = 0.013*D**-2.66 # the rock 
# N = 5.61*np.exp(-12.05*D)
rho = 0.0403*D**-0.66
# rho = 0.069*np.exp(-4.08*D)
A = 100 # area
a = np.sqrt(A)
P_rho = np.zeros(len(D))
n = np.zeros(len(D))
x = []
y = []
area = []
height_rocks = []
for ii in range(0,len(D)):
    
    n[ii] = math.ceil(N[ii]*A)
    b = np.int(n[ii])
    for jj in range(0,b):
        x.append(random.random()*a)
        y.append(random.random()*a)
        area.append ((D[ii]**2)/4)
        height_rocks.append(0.506*D[ii]+0.008)
        
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = np.asarray(x)
y = np.asarray(y)
# x = np.linspace(-50,50,100)
# y = np.arange(25)
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from mpl_toolkits.mplot3d import Axes3D 
import mpl_toolkits.mplot3d.art3d as art3d


fig = plt.figure()
ax=fig.gca(projection='3d')

for i in ["x","y","z"]:
    circle = Circle((0, 0), 1)
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0, zdir=i)


ax.set_xlim3d(-2, 2)
ax.set_ylim3d(-2, 2)
ax.set_zlim3d(-2, 2)

plt.show()