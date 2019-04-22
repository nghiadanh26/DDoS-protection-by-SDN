import pandas as pd
import numpy as np
import math
### Step 6.2: Create local_outlier_factor_matrix class for LOF algorithm




class local_outlier_factor_matrix(object):
	"""This class for local outlier factor but thr input is a matrix and output is anomally or not
	and which components of matrix are anomally
	"""
	def __init__(self, k = 3, column = 6, row = 6):

		#row is number of rows, column is number of columns
		self.k = k
		#self.data = data
		self.column = column
		self.row = row
		self.list_data = []
		self.matrix_size = column*row

	### Step 6.3: Write the function read_data to read data from csv file and convert them to 6x6 matrix
	def read_data(self, filename):
		data = pd.read_csv(filename)
		data = data.drop('Unnamed: 0',axis=1) # Remove column named 'Unnamed: 0'
		#list_data = []
		i = 0
		#print(len(data))
		matrix = np.zeros((self.row,self.column,2))
		while(i<len(data)):
			#matrix = np.zeros((self.row,self.column,2))
			temp = i%self.matrix_size
			row_index = int(temp/self.row)
			column_index = temp%self.row
			matrix[row_index][column_index][0] = data.at[i,'throughput']
			#matrix[row_index][column_index][0] = 1
			#print(data.at[111,'throughput'])
			#print(matrix[0][3][0])
			matrix[row_index][column_index][1] = data.at[i,'new_flow']
			#print(i)
			i +=1
			if(i%self.matrix_size == 0):
				self.list_data.append(matrix)
				print(matrix)

		return self.list_data

	### Step 6.4: Write the function to calculate matrix_distance
	### matrix_distance = avg(components_distance)

	### Distance between 2 points, 2 dimensions

	def calculate_distance(a,b):
		d = math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
		return d


	### Distance between 2 matrixes
	def calculate_matrix_distance(m1,m2):
		for i in range(len(m1)):
			for j in range(len(m1[i])):




#test = local_outlier_factor_matrix()
#data = test.read_data('data_normalization1.csv')
#print(data[0][5])









		