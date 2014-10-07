#!/usr/bin/env python3

from optparse import OptionParser
import sys
import zmq
import time
from classes.ProcessTelemetry import ProcessTelemetry
from classes.ProcessImages import ProcessImages

if len(sys.argv) < 4:
	print("Usage: "+sys.argv[0]+" bridge_type listen_endpoint connect_to")
	sys.exit(1)

bridge_type = sys.argv[1]
listen_endpoint = sys.argv[2]
ws_endpoint = sys.argv[3]

metric_period = 1
last_metric_exec = time.time()

allowed_types = ("telemetry","images")

if bridge_type not in allowed_types:
	print("bridge_type '"+bridge_type+"' is not allowed")
	sys.exit(-1)

parser = OptionParser()
parser.add_option("-a", "--archive", dest="archive_data", help="Archive data")



zmq_context = zmq.Context()


listen_socket = zmq_context.socket(zmq.PULL)
send_socket = zmq_context.socket(zmq.PUSH)

if bridge_type == "telemetry":
	processor = ProcessTelemetry()

if bridge_type == "images":
	processor = ProcessImages()

listen_socket.bind(listen_endpoint)
send_socket.connect(ws_endpoint)
#print(ws_endpoint)

while True:
	if bridge_type == "images":
		packet = listen_socket.recv()
	else:
		packet = listen_socket.recv_json()
	#print(packet)
	new_packet = processor.processPacket(packet)
	if new_packet is not None:
		if bridge_type == "images":
			send_socket.send(new_packet)
		else:
			send_socket.send_json(new_packet)

	if time.time() >= (last_metric_exec + metric_period):
		metric_packet = processor.processMetrics()
		last_metric_exec = time.time()
