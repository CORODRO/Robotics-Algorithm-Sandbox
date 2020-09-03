# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 22:15:50 2020

@author: jasmi
"""

# first neural network with keras tutorial
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

# load the dataset
dataset = loadtxt('pima-indians-diabetes.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:,0:8]
y = dataset[:,8]


# define the keras model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu')) # 8 inputs + 12 nodes for first layer
model.add(Dense(8, activation='relu')) # 8 nodes for second layer
model.add(Dense(1, activation='sigmoid')) # 1 node for output

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# fit the keras model on the dataset
model.fit(X, y, epochs=150, batch_size=10)

# evaluate the keras model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))