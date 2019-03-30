from pox.core import core
import time as t
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of
#import pickle
#import pandas as pd
#import numpy as np
#import threading
# import minisom
#####import mode
# include as part of the betta branch
from pox.openflow.of_json import *

log = core.getLogger()

def _handle_aggregate_received(event):
	stats = flow_stats_to_list(event.stats)
  	log.debug("FlowStatsReceived from %s: %s", dpidToStr(event.connection.dpid), stats)
  	#print(event.ofp)
  	global byte_count
  	#if (event.connection.dpid):
  		#print ("dpid =", event.connection.dpid)
  	flow_matrix = []
  	byte_count = 0
  	duration = 0
  	if(event.connection.dpid == 1):
	  	for f in event.stats:
	  		print(f.match.in_port)



  	#print (flowtable)


def _timer_func ():
	for connection in core.openflow._connections.values():
		connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
  	log.debug("Sent %i flow/port stats request(s)", len(core.openflow._connections))


def launch():
	core.openflow.addListenerByName("FlowStatsReceived", _handle_aggregate_received)
	Timer(5,_timer_func, recurring=True)
