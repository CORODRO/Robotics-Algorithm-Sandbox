# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 08:34:36 2020

@author: Jasmine Rimani

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import random
import os
# import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from mpl_toolkits.mplot3d import Axes3D 
import mpl_toolkits.mplot3d.art3d as art3d

# os.clear()
D = np.arange(0.05,3,0.01)
N = 0.013*D**-2.66 # the rock 
# N = 5.61*np.exp(-12.05*D)
rho = 0.0403*D**-0.66
# rho = 0.069*np.exp(-4.08*D)
A = 2000 # area
a = np.sqrt(A)
P_rho = np.zeros(len(D))
n = np.zeros(len(D))
x = []
y = []
area = []
h = []
for ii in range(0,len(D)):
    
    n[ii] = math.ceil(N[ii]*A)
    b = np.int(n[ii])
    for jj in range(0,b):
        x.append(random.random()*a)
        y.append(random.random()*a)
        area.append ((D[ii]**2)/4)
        h.append(0.506*D[ii]+0.008)
    # P_rho[ii] = (((rho[ii]*A)**n[ii])/math.factorial(n[ii]))*np.exp(-rho[ii]*A) 
    
# obstacles_x = []
# obstacles_y = []   
# Create obstacles for A*
# for jj in x:
#     obstacles_x.append(jj+0.1)
        
        

def my_circle_scatter(axes, x_array, y_array, radius=0.5, **kwargs):
    for x, y, R in zip(x_array, y_array, radius):
        circle = plt.Circle((x,y), radius=R, **kwargs)
        axes.add_patch(circle)
    return True

# def 3D_scatter(axes, x_array, y_array, radius=0.5, **kwargs):
#     for x, y, R in zip(x_array, y_array, radius):
#         circle = plt.Circle((x,y), radius=R, **kwargs)
#         axes.add_patch(circle)
#     return True

def my_square_scatter(axes, x_array, y_array, size=0.5, **kwargs):
    size = float(size)
    for x, y in zip(x_array, y_array):
        square = plt.Rectangle((x-size/2,y-size/2), size, size, **kwargs)
        axes.add_patch(square)
    return True

def my_polygon_scatter(axes, x_array, y_array, resolution=5, radius=0.5, **kwargs):
    ''' resolution is number of sides of polygon '''
    for x, y in zip(x_array, y_array):
        polygon = matplotlib.patches.CirclePolygon((x,y), radius=radius, resolution=resolution, **kwargs)
        axes.add_patch(polygon)
    return True

axes = plt.axes()
my_circle_scatter(axes, x, y, radius=D/2, alpha=.5, color='g')
plt.axis('scaled')
plt.show()

# plt.scatter(x,y,s=area)
# plt.show()

def MapGenerator(x_array,y_array,R_array):
    # set obstacle positions
    ox, oy = [], []
    
    for x,y,R in zip(x_array, y_array, R_array): 
        for jj in range(1,20):
            theta = 360/jj
            ox.append(R*np.cos(theta))
            ox.append(R*np.sin(theta))

        
    return ox,oy



# # DEM
# width = max(x)-min(x)
# length = max(y)-min(y)
# X = np.arange(min(x),max(x), 0.1)    
# Y = np.arange(min(y),max(y), 0.1)    
# X, Y = np.meshgrid(X, Y)
# H = np.ones((len(X),len(Y)))
# flag_out =  0

# for ii, jj, mm in zip(X,Y,H):
#     for i, k in zip(ii,jj):
#         for kk,pp,oo,hh in zip(x,y,D,h):
#             if ((i) <= (kk)+oo/2) and ((i) >= (kk)-oo/2) and flag_out == 0 and ((k) <= (pp)+oo/2) and ((k) >= (pp)-oo/2): 
#                 flag = 1
#                 flag_out = 1
#                 mm = random.random
#             else:
#                 flag = 0
#                 mm = 0
#         flag_out = 0

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi/2, 100)    
 
# x = 10 * np.outer(np.cos(u), np.sin(v))
# y = 10 * np.outer(np.sin(u), np.sin(v))
# z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

# x1 = 15+2* np.outer(np.cos(u), np.sin(v))
# y1 = 15+2* np.outer(np.sin(u), np.sin(v))
# z1 = 2 * np.outer(np.ones(np.size(u)), np.cos(v))



# X = []
# Y = []
# H = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
          
for ii, jj, dd in zip(x,y,D/2):
    X = (ii+dd*np.outer(np.cos(u), np.sin(v)))
    Y = (jj+dd*np.outer(np.sin(u), np.sin(v)))
    H = (((0.506*dd*2+0.008)/2)*np.outer(np.ones(np.size(u)), np.cos(v)))
    ax.plot_surface(X, Y, H, color='b')
ax.set_xlim3d(0,a)
ax.set_ylim3d(0,a)
ax.set_zlim3d(0,dd*7)
plt.show()
# Plot the surface

# ax.plot_surface(x1, y1, z1, color='b')



# for ii in X:
#     for jj in ii:
#         for kk,pp,oo,hh in zip(x,y,D,h):
#              if ((jj) <= (kk)+oo/2) and ((jj) >= (kk)-oo/2) and flag_out == 0:
#                  flag = 1
#                  dim = pp
#                  theta = np.arctan(abs(oo)/abs(hh))
#                  flag_out = 1
#              else:
#                  flag = 0
#                  dim = 0
#                  theta = 0
#         flag_out = 0
#         if flag == 1:
#             H.append(0.506*dim+0.008)
#         else:
#             H.append(0)
            
                    
    
    
    
    
# for ii in X:
#     for jj,kk,ll,oo in zip(x,y,D,h):
#         if ((ii) <= (jj)+ll/2) and ((ii) >= (jj)-ll/2):
#             flag = 1
#             dim = ll
#             theta = np.arctan(abs(oo)/abs(ll))
#             # H.append(np.tan(theta)*ll)
#         else:
#             flag = 0
#             dim = 0
#             theta = 0
#             # H.append(0)
#     if flag == 1:
#           H.append(np.tan(theta)*dim)
#     else:
#           H.append(0)
          
# for ii in X:
#     for jj in Y[]:
#         H.append(random.random)
        
        
# count = 0    
# for ii,jj in zip(X,Y):
#     for kk,ll,oo,hh in zip(x,y,D,h):
#         if abs(ii-kk)<= 0.5 and abs(jj-ll)<= 0.5:
#             flag = 1
#             dim = hh
#         else:
#             flag = 0
#     count = count+1   

#     if flag == 1:
#          H.append(dim)
#     else:
#          H.append(0)

# H_1 = np.reshape(H,(len(X),len(Y)))

# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x,y,zs =D/2)
# plt.show()
# X = np.reshape(x,(len(x),1))
# Y = np.reshape(y,(len(y),1))
# H = np.reshape(h,(len(h),1))

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_wireframe(X, Y, H)

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# plt.show()
# for ii,jj,kk,ll in zip(x,y,h,D):
#     X= np.arange(ii-ll/2,ii+ll/2)
#     Y = np.arange(jj-ll/2,jj+ll/2)
#     X, Y = np.meshgrid(X, Y)
#     R = np.sqrt(X**2 + Y**2)
#     Z = np.sin(R)
#     surf= ax.plot_surface(X, Y, Z)
#     ax.add_patch(surf)
# plt.show()
# ax.set_aspect("equal")

# fig = plt.figure()
# ax = fig.gca(projection='3d')


# # # Make data.
# # X = np.arange(-5, 5, 0.25)
# # xlen = len(X)
# # Y = np.arange(-5, 5, 0.25)
# # ylen = len(Y)
# # X, Y = np.meshgrid(x, y)
# # R = np.sqrt(X**2 + Y**2)
# # Z = np.sin(R)

# # Create an empty array of strings with the same shape as the meshgrid, and
# # populate it with two colors in a checkerboard pattern.
# # colortuple = ('y', 'b')
# # colors = np.empty(X.shape, dtype=str)
# # for y in range(ylen):
# #     for x in range(xlen):
# #         colors[x, y] = colortuple[(x + y) % len(colortuple)]

# # Plot the surface with face colors taken from the array we made.
# surf = ax.plot_surface(X, Y, Z)

# # Customize the z axis.
# ax.set_zlim(-1, 1)
# ax.w_zaxis.set_major_locator(LinearLocator(6))

# plt.show()
# Axes3D.plot_surface(x, y, height_rocks, *args, **kwargs)
# Axes3D.plot_wireframe(X, Y, Z, *args, **kwargs)
