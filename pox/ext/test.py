import math as m
import numpy as np

def calculate_distance(v1,v2):
		'''This function is used for calculating distance between 2 points'''
		dist = m.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)
		return dist

x = np.zeros((6,2))
a = x[0]
y = np.ones((6,2))
b = y[0]
print(calculate_distance(a,b))