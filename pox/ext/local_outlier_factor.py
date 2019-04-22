import pandas as pd
import math as m
import time
count = 0
### Step 7.5: Write LOF
class local_outlier_factor():
	def __init__(self,k = 4):
		self.k = k
		self.data = pd.DataFrame(columns=['throughput','new_flow_normalized'],index=range(49))
		self.threshold = 2
		self.lrd_all = []
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
	def get_values(self, index):
		global count
		count = count +1 
		tx = time.time()
		point_i = [self.data['throughput'][index],self.data['new_flow_normalized'][index]]
		ty = time.time()
		#print(ty-tx)
		print(count)
		return point_i


	###Calculate distance of each point from data
	def k_distance(self,point):
		# point is a list
		dist_arr = []
		#knn_set = {}
		for i in self.data.index:
			point_i = self.get_values(i)
			dist = self.calculate_distance(point,point_i)
			dist_arr.append(dist)
		dist_arr.sort()
		return dist_arr[self.k-1]

	### Find the index of K nearest neighboors
	def find_knn(self,point):
		knn_set =[]
		#flag = 0
		#count = 0
		equal =[]
		for i in self.data.index:
			point_i = self.get_values(i)
			dist = self.calculate_distance(point,point_i)
			if(dist < self.k_distance(point)):
				knn_set.append(i)
				#count +=1			
			if(dist == self.k_distance(point)):
				equal.append(i)
		if(len(knn_set) < self.k):
			t = self.k - len(knn_set)
			for i in range(t):
				knn_set.append(equal[i])
		return knn_set

	### Calculate reachability distance of 2 points
	def reachability_distance(self,point1,point2):
		return max(self.k_distance(point2),self.calculate_distance(point1,point2))
	#cnt = 0
	### Calculate local reachability density (lrd)
	def lrd(self,point):
		global cnt
		knn_set = self.find_knn(point)
		sum_reach_dist = 0
		#cnt = 0
		for i in knn_set:
			point_i = self.get_values(i)
			sum_reach_dist += self.reachability_distance(point,point_i)
			#print(sum_reach_dist)
			#self.count_loop =+1
		if(sum_reach_dist == 0): return 100 # return positive infinity
		else: return 1/(sum_reach_dist/self.k)


	### Calculate lrd for all points of data
	def calculate_lrd_all(self):
		#lrd_all = []
		for i in range(len(self.data)):
			self.lrd_all.append(self.lrd(self.get_values(i)))
		#return lrd_all
		lrd_df = pd.DataFrame(self.lrd_all,columns=['lrd'],index=range(49))
		lrd_df.to_csv('lrd_v1.csv')

	### Calculate LOF score of a point
	def isOutlier(self,point):
		#knn_set = self.find_knn(point)
		#sum_density = 0
		#for i in knn_set:
			#point_i = self.get_values(i)
			#sum_density += self.lrd_all[i]
		#avg_lrd = sum_density/self.k
		ratio = self.LOF_ratio()
		if(ratio > self.threshold):
			return 1
		else:
			return 0


	### lof ratio
	def LOF_ratio(self,point):
		knn_set = self.find_knn(point)
		sum_density = 0
		for i in knn_set:
			point_i = self.get_values(i)
			sum_density += self.lrd_all[i]
		avg_lrd = sum_density/self.k
		ratio = avg_lrd/self.lrd(point)
		return ratio


	### Training function
	def train(self):
		t1 = time.time()
		print("LOF training has started!!!")
		#self.read_data('normal_90_v2.csv')
		self.read_data('test4.csv')

		t2 = time.time()
		#print(t2-t1)
		self.calculate_lrd_all()

		t3 = time.time()
		#print(t3-t2)
		#print(self.count_loop)
		#print(max(self.lrd_all))
		#print(self.lrd_all)

		t4 = time.time()
		#print(t4-t3)
		score = []
		for i in range(len(self.data)):
			#print(len(self.data))
			#t6 = time.time()
			score.append(self.LOF_ratio(self.get_values(i)))
			#print(i)
			#t7 = time.time()
			#print(t7-t6)

		t5 = time.time()
		#print(t5-t4)
		self.threshold = max(score)
		#print(score)
		#print(self.threshold)
		print(count)




#def launch():
	#cnt = 0
	#test = local_outlier_factor()
	#test.train()
	#print(test.data.index)

test = local_outlier_factor()
test.train()