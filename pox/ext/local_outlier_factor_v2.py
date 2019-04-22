import pandas as pd
import math as m
import time
import numpy as np
#count = 0
### Step 7.5: Write LOF
class local_outlier_factor():
	def __init__(self,k = 20,threshold = 3):
		self.k = k
		self.data = pd.DataFrame(columns=['throughput','new_flow_normalized'],index=range(49))
		self.threshold = threshold
		self.lrd_all = []
		self.data_list = []
		self.knn_set = []
		self.k_dist =[]
		#self.count_loop = 0
		#self.count = 0

	def read_data(self,filename):
		self.data = pd.read_csv(filename)
		self.data = self.data.drop('Unnamed: 0',axis=1) # Remove column named 'Unnamed: 0'
		self.data = self.data.drop('new_flow',axis=1) # Remove column named 'new_flow'. We just need new_flow_normalized
		#self.data = self.data.drop_duplicates(['throughput','new_flow_normalized'])
		#self.data = self.data.drop_duplicates(['new_flow_normalized'])
		#print(self.data)


	def calculate_distance(self,v1,v2):
		'''This function is used for calculating distance between 2 points'''
		dist = m.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)
		return dist


	### Get values from dataframe, change to list

	### get data_list
	def get_data_list(self):
		self.read_data('normal_90_v2.csv')
		for i in self.data.index:
			self.data_list.append([self.data['throughput'][i],self.data['new_flow_normalized'][i]])

		self.data_list = np.array(self.data_list)

	###Calculate distance of each point from data
	def k_distance(self,point):
		
		# point is a list
		dist_arr = []
		#knn_set = {}
		for i in self.data.index:
			point_i = self.data_list[i]
			dist = self.calculate_distance(point,point_i)
			dist_arr.append(dist)
		dist_arr.sort()
		return dist_arr[self.k-1]

	### Find the index of K nearest neighboors
	def find_all_knn(self):
		#k_distance = 0
		#knn_set =[]
		#flag = 0
		#count = 0
		#global count
		#count = count +1
		
		#tx = time.time()
		for j in range(len(self.data_list)):
			dist = []
			for i in range(len(self.data_list)):
				dist.append(self.calculate_distance(self.data_list[j],self.data_list[i]))
			dist_df = pd.DataFrame(dist)
			dist_df.sort_values(axis = 0, by = 0, inplace = True)
			k_distance = dist_df.at[self.k-1,0]
			temp = dist_df.index[:self.k]
			self.knn_set.append(temp)
			self.k_dist.append(k_distance)
		#ty=time.time()
		#print(ty-tx)


	### Calculate reachability distance of 2 points
	def reachability_distance(self,i,j):
		return max(self.k_dist[i],self.calculate_distance(self.data_list[i],self.data_list[j]))
	#cnt = 0
	### Calculate local reachability density (lrd)
	def lrd(self,index):
		global cnt
		knn_set = self.knn_set[index]
		sum_reach_dist = 0
		#cnt = 0
		for i in knn_set:
			point_i = self.data_list[i]
			sum_reach_dist += self.reachability_distance(index,i)
		if(sum_reach_dist == 0): return 100 # return positive infinity
		else: return 1/(sum_reach_dist/self.k)


	### Calculate lrd for all points of data
	def calculate_lrd_all(self):
		#lrd_all = []
		#tx= time.time()
		for i in range(len(self.data)):
			self.lrd_all.append(self.lrd(i))
		#return lrd_all
		#ty=time.time()
		#print(ty-tx)
		lrd_df = pd.DataFrame(self.lrd_all,columns=['lrd'],index = range(1074))
		lrd_df.to_csv('lrd_v1.csv')


	### lof ratio
	def LOF_ratio(self,index):
		knn_set = self.knn_set[index]
		sum_density = 0
		for i in knn_set:
			point_i = self.data_list[i]
			sum_density += self.lrd_all[i]
		avg_lrd = sum_density/self.k
		ratio = avg_lrd/self.lrd_all[index]
		return ratio


	### Training function
	def train(self):
		#t1 = time.time()
		print("LOF training has started!!!")
		#self.read_data('normal_90_v2.csv')
		#self.read_data('test4.csv')
		self.get_data_list()
		#self.find_all_knn()

		#t2 = time.time()
		#print(t2-t1)
		self.find_all_knn()
		self.calculate_lrd_all()

		#t3 = time.time()
		#print(t3-t2)


		#t4 = time.time()
		#print(t4-t3)
		score = []
		for i in range(len(self.data)):
			#print(len(self.data))
			#t6 = time.time()
			score.append(self.LOF_ratio(i))
			#print(i)
			#t7 = time.time()
			#print(t7-t6)

		#t5 = time.time()
		#print(t5-t4)
		#print(t5-t1)
		self.threshold = max(score)
		#print(score)
		#print(self.threshold)
		#print(count)


	def read_lrd(self):
		self.lrd_all = pd.read_csv('lrd_v1.csv')
		self.lrd_all = self.lrd_all.drop(axis=1,columns=['Unnamed: 0'])
		#print(self.lrd_all)

	def find_knn_predict(self,point):
		knn_set =[]

		#flag = 0
		#count = 0
		dist = []
		for i in range(len(self.data_list)):
			dist.append(self.calculate_distance(point,self.data_list[i]))
		dist_df = pd.DataFrame(dist)
		dist_df.sort_values(axis = 0, by = 0, inplace = True)
		k_distance = dist_df.at[self.k-1,0]
		knn_set = dist_df.index[:self.k]
		#knn_set.append(temp)
		return k_distance, knn_set

	### Calculate reachability distance of 2 points
	def reachability_distance_predict(self,point1,point2):
		return max(self.k_distance(point2),self.calculate_distance(point1,point2))
	#cnt = 0

	def lof_predict(self,point):
		#global cnt
		k_distance, knn_set = self.find_knn_predict(point)
		sum_reach_dist = 0
		#cnt = 0
		knn_set = list(knn_set)
		#print(knn_set)
		for i in knn_set:
			point_i = self.data_list[i]
			#if(i)
			#print(self.data_list[i])
			sum_reach_dist += self.reachability_distance_predict(point,point_i)
			#print(sum_reach_dist)
			#self.count_loop =+1
		if(sum_reach_dist == 0): lrd = 100 # return positive infinity
		else: lrd = 1/(sum_reach_dist/self.k)
		sum_lrd = 0
		for i in knn_set:
			sum_lrd += self.lrd_all.at[i,'lrd']
		score = sum_lrd/self.k/lrd

		if(score > self.threshold): return 1
		else: return 0





test = local_outlier_factor()
test.get_data_list()
test.read_lrd()
#print(test.data_list[70][1])
#t11 = time.time()
#test.train()
#test_point = np.ones((6,2))
#t11 = time.time()
print(test.lof_predict([0,4]))
#t22 = time.time()
#print(t22-t11)