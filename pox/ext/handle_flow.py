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

def _handle_port_received(event):
  	#log.debug("PortStatsReceived from %s: %s", dpidToStr(event.connection.dpid), stats)

  	global byte_count
  	if(event.connection.dpid == 4):
	  	for f in event.stats:
	  		if(f.port_no == 1):
		  		#print(f.port_no)
		  		print(f.rx_bytes)
		  		print("\n")



  	#print (flowtable)


def _timer_func ():
	for connection in core.openflow._connections.values():
		connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  	log.debug("Sent %i flow/port stats request(s)", len(core.openflow._connections))


def launch():
	core.openflow.addListenerByName("PortStatsReceived", _handle_port_received)
	Timer(5,_timer_func, recurring=True)
