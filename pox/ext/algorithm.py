from pox.core import core
import time as t
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
import normalize_feature
import pandas as pd
import numpy as np
#import local_outlier_factor as lof
#import threading
# import minisom
#####import mode
# include as part of the betta branch
from pox.openflow.of_json import *

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
   print("--------------------- NewFlow/s-------------------")
   print(flow_df)
   print('\n')
   print('\n')

def show_rate ():
   rate_df = pd.DataFrame(rate_matrix, columns=switch, index=switch)
   print("--------------------- bit/s-------------------")
   print(rate_df)
   print('\n')
   print('\n')


######################## Collect new flow rate (new_flow/s) and rate (bps) version 0############

data_normal = pd.DataFrame(columns=['throughput','new_flow'])
def collect_normal_data():
   '''
   this function will measure newflow rate and rate from OvS1 to OvS4 (topo: 6sw_v2.py)
   '''
   cur_sw = 4
   pre_sw = 1
   in_port = 1
   global data_normal, rate_matrix, flow_count_temp
   data = [[rate_matrix[pre_sw-1][cur_sw - 1], flow_count_temp[pre_sw-1][cur_sw - 1]]]
   data_df = pd.DataFrame(data, columns=['throughput','new_flow'])
   #print(data_df)
   data_normal = data_normal.append(data_df)

def write_to_csv():
   #global data_normal
   data_normal.to_csv('normal.csv')


######################## Collect matrix data version 1 #########################################

data_matrix = pd.DataFrame(columns=['throughput','new_flow'])
def collect_data_matrix():
   '''

   '''

   global data_matrix, rate_matrix, flow_count_temp
   for i in range(1,7):
      for j in range(1,7):
         temp = [[rate_matrix[i-1][j-1],flow_count_temp[i-1][j-1]]]
         #print(temp)
         temp_df = pd.DataFrame(temp, columns=['throughput','new_flow'])
         data_matrix = data_matrix.append(temp_df)
   #set_index_data_matrix(36,5,60)

def set_index_data_matrix(size,stats_time,write_time):
   global data_matrix
   temp = int(write_time/stats_time)
   index = []
   for i in range(1,temp):
      for j in range(1,size+1):
         index.append([i])
   data_matrix = data_matrix.set_index(index)


def data_matrix_to_csv():
   data_matrix.to_csv('matrix_data.csv')

########################Step 6.1: Collect matrix data and normalize them before saving to csv file

feature = normalize_feature.max_min_feature
def normalize_vector(vector):
   #normalize throughput
   vector[0] = (vector[0]-feature.MIN_THROUGHPUT)/(feature.MAX_THROUGHPUT - feature.MIN_THROUGHPUT)
   #normalize newflow/s
   vector[1] = (vector[1]-feature.MIN_NEWFLOW)/(feature.MAX_NEWFLOW - feature.MIN_NEWFLOW)
   return vector

def normalize_matrix(dataframe):
   for i in range(len(dataframe)):
      vector = [dataframe.at[i,'throughput'], dataframe.at[i,'new_flow']]
      temp = normalize_vector(vector)
      dataframe.at[i,'throughput'] = temp[0]
      dataframe.at[i,'new_flow'] = temp[1]


######################## Main function to excute #####################################
def launch():
   #global rate
   #data_normal = pd.DataFrame(columns=['throughput (bps)','new_flow_rate (newflow/s'])
   core.openflow.addListenerByName("PortStatsReceived", _handle_port_received)
   core.openflow.addListenerByName("AggregateFlowStatsReceived", _handle_aggregate_received)
   core.openflow.addListenerByName("PacketIn", _handle_packet_in)
   #core.openflow.addListenerByName("FlowStatsReceived", _handle_flow_received)

   #Try to normalize data and save it to data_normalization.csv
   normalize_matrix(data_normal_training)
   data_normal_training.to_csv('data_normalization.csv')

   Timer(stats_time,port_stats_request, recurring=True)
   #Timer(stats_time,show_flow, recurring=True)
   #Timer(1,aggregate_stats_request, recurring=True)
   #Timer(5,flow_stats_request, recurring=True)
   Timer(stats_time,show_rate, recurring=True)

   #Run to collect normal data to training. Run it only once and result csv file in pox folder
   #Timer(stats_time,collect_normal_data,recurring=True)
   #Timer(600,write_to_csv,recurring=False)

   #Run to collect data 
   #Timer(stats_time,collect_data_matrix,recurring=True)
   #Timer(60,data_matrix_to_csv,recurring=False)
