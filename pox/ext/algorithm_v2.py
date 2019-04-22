from pox.core import core
import time as t
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
import normalize_feature
import pandas as pd
import numpy as np
import csv
from local_outlier_factor_v2 import local_outlier_factor
#import local_outlier_factor as lof
#import threading
# import minisom
# include as part of the betta branch
from pox.openflow.of_json import *
import time

lof = local_outlier_factor()


### Get data training
def read_training():
   global lof
   lof.get_data_list()
   lof.read_lrd()

def in_port(pre_sw,cur_sw):
   '''
   Use this function to take the logical port based on previous OvS and current OvS
   '''
   if(pre_sw == 1 and cur_sw == 4):
      return 1
   elif(pre_sw == 2 and cur_sw == 4):
      return 2
   elif(pre_sw == 3 and cur_sw == 5):
      return 1
   elif(pre_sw == 4 and cur_sw == 6):
      return 1
   elif(pre_sw == 5 and cur_sw == 6):
      return 2
   elif(pre_sw == 4 and cur_sw == 1):
      return 2
   elif(pre_sw == 4 and cur_sw == 2):
      return 2
   elif(pre_sw == 5 and cur_sw == 3):
      return 2
   elif(pre_sw == 6 and cur_sw == 4):
      return 3
   elif(pre_sw == 6 and cur_sw == 5):
      return 2
   else: 
      return -1


log = core.getLogger()
old_bytes = np.zeros((6,6)) # byte matrix of previous 5s
rate_matrix = np.zeros((6,6)) # rate matrix at this time
flow_count = np.zeros((6,6)) 
flow_count_temp = np.zeros((6,6))
switch = ['s1','s2','s3','s4','s5','s6']
stats_time = 5 # send request for statistics every 5s

#Read csv file and delete unneccesary column
data_normal_training = pd.read_csv('matrix_data.csv')
data_normal_training = data_normal_training.drop('Unnamed: 0', axis=1)

################### Handle event received from OvS ###################################
first_time = 0
def _handle_port_received(event):
   '''
   Handle the PortStatsReceived event
   '''
   global old_bytes, rate_matrix, first_time
   dpid = event.connection.dpid
   if(first_time < 7):
      for k in range(1,7):
      #print(k)
         if(in_port(k,dpid) != -1):
            for f in event.stats:
               #print (f.port_no)
               if(f.port_no == in_port(k,dpid)):
                  #print (in_port(k,dpid))
                  #print (f.port_no)
                  #rate_matrix[k-1][dpid-1] = (f.rx_bytes - old_bytes[k-1][dpid-1])*8/5
                  old_bytes[k-1][dpid-1] = f.rx_bytes
      first_time +=1
   else:
      for k in range(1,7):
         #print(k)
         if(in_port(k,dpid) != -1):
            for f in event.stats:
               #print (f.port_no)
               if(f.port_no == in_port(k,dpid)):
                  #print (in_port(k,dpid))
                  #print (f.port_no)
                  rate_matrix[k-1][dpid-1] = (f.rx_bytes - old_bytes[k-1][dpid-1])*8/5
                  old_bytes[k-1][dpid-1] = f.rx_bytes

def _handle_aggregate_received(event):
   '''
   Handle the AggregateFlowStatsReceived event
   '''
   if(event.connection.dpid == 1):
      print(event.stats.flow_count)

def _handle_packet_in(event):
   '''
   Handle the PacketIn event
   '''
   global flow_count
   #packet = event.parsed 
   dpid = event.dpid
   #print(event.__doc__)
   for k in range(1,7):
      if(in_port(k,dpid) != -1):
         if(in_port(k,dpid) == event.port):
            flow_count[k-1][dpid-1] += 1
            #print("packetIN")




############ Send request for statistics from controller to all OvSs ##################
def port_stats_request():
	for connection in core.openflow._connections.values():
		connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  	log.debug("Sent %i port stats request(s)", len(core.openflow._connections))

def aggregate_stats_request():
   for connection in core.openflow._connections.values():
      connection.send(of.ofp_stats_request(body=of.ofp_aggregate_stats_request()))
   log.debug("Sent %i aggregate stats request(s)", len(core.openflow._connections))

def flow_stats_request():
   for connection in core.openflow._connections.values():
      connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
   log.debug("Sent %i flow stats request(s)", len(core.openflow._connections))


######################### Show everything here!! ######################################
def show_flow():
   global flow_count, flow_count_temp
   flow_df = pd.DataFrame(flow_count/5, columns=switch, index=switch)
   old_flow_count = np.zeros((6,6))
   flow_count_temp = flow_count
   flow_count = old_flow_count
   #print("--------------------- NewFlow/s-------------------")
   #print(flow_df)
   #print('\n')
   #print('\n')

def show_rate ():
   rate_df = pd.DataFrame(rate_matrix, columns=switch, index=switch)
   print("--------------------- bit/s-------------------")
   print(rate_df)
   print('\n')
   print('\n')

### Step 7.3: Collect matrix data (10 instead of 36 points)
### Each matrix will be changed to list (len = 10), including:
### [0]: 1-->4
### [1]: 2-->4
### [2]: 3-->5
### [3]: 4-->1
### [4]: 4-->2
### [5]: 4-->6
### [6]: 5-->3
### [7]: 5-->6
### [8]: 6-->4
### [9]: 6-->5
list_data = []
def collect_matrix_data():
   global flow_count_temp, rate_matrix, list_data
   matrix = []
   for i in range(6):
      for j in range(6):
         temp = []
         if(in_port(i+1,j+1) != -1):
            temp.append(rate_matrix[i][j])
            temp.append(flow_count_temp[i][j])
            temp = normalize_vector(temp)
         if(len(temp) != 0):
            matrix.append(temp)
   #list_data.append(matrix)
   #print(matrix)
   return matrix

def collect_data_training():
   '''Just collect data from OVS4 to OVs6'''
   global flow_count_temp,rate_matrix,list_data
   temp = [rate_matrix[3][5], flow_count_temp[3,5]]
   temp = normalize_vector(temp)
   list_data.append(temp)


def write_to_csv():
   data_df = pd.DataFrame(list_data,columns=['throughput','new_flow'])
   data_df.to_csv('normal_90.csv')
   #with open('normal_90m.csv','wb',) as myfile:
      #wr = csv.writer(myfile)
      #wr.writerow(list_data)
### Normal traffic capture
### TODO: Tao cac file pcap thuong de tan cong theo kich ban da dat ra!

###Step 6.1: Collect matrix data and normalize them before saving to csv file

feature = normalize_feature.max_min_feature
def normalize_vector(vector):
   #normalize throughput
   vector[0] = (vector[0]-feature.MIN_THROUGHPUT)/(feature.MAX_THROUGHPUT - feature.MIN_THROUGHPUT)
   #normalize newflow/s
   vector[1] = (vector[1]-feature.MIN_NEWFLOW)/(feature.MAX_NEWFLOW - feature.MIN_NEWFLOW)/stats_time
   return vector

def normalize_matrix(dataframe):
   for i in range(len(dataframe)):
      vector = [dataframe.at[i,'throughput'], dataframe.at[i,'new_flow']]
      temp = normalize_vector(vector)
      dataframe.at[i,'throughput'] = temp[0]
      dataframe.at[i,'new_flow'] = temp[1]


### Using LOF to detect anomally point
def do_lof():
   tx = time.time()
   matrix = collect_matrix_data()
   #print(matrix)
   lof_result = []
   for point in matrix:
      lof_result.append(lof.lof_predict(point)) 
   ty = time.time()
   print(ty-tx)
   print(lof_result)


### Main function to excute #####################################
def launch():

   read_training()
   #global rate
   #data_normal = pd.DataFrame(columns=['throughput (bps)','new_flow_rate (newflow/s'])
   core.openflow.addListenerByName("PortStatsReceived", _handle_port_received)
   #core.openflow.addListenerByName("AggregateFlowStatsReceived", _handle_aggregate_received)
   core.openflow.addListenerByName("PacketIn", _handle_packet_in)
   #core.openflow.addListenerByName("FlowStatsReceived", _handle_flow_received)

   #Try to normalize data and save it to data_normalization.csv
   #normalize_matrix(data_normal_training)
   #data_normal_training.to_csv('data_normalization.csv')

   Timer(stats_time,port_stats_request, recurring=True)
   Timer(stats_time,show_flow, recurring=True)

   ###### Data matrix is stored in rate_matrix and flow_count_temp

   Timer(stats_time,do_lof, recurring=True)

   #Timer(5,flow_stats_request, recurring=True)
   #Timer(stats_time,show_rate, recurring=True)


   #Run to collect data 
   #Timer(stats_time,collect_data_training,recurring=True)
   #Timer(5400,write_to_csv,recurring=False)
   #Timer(60,data_matrix_to_csv,recurring=False)
