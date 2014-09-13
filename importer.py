#!/usr/bin/env python3

import json
import sys
import time
import zmq

log_file = "./mavlink-log.txt"

zmq_context = zmq.Context()

connect_to = sys.argv[1]
send_socket = zmq_context.socket(zmq.PUSH)
send_socket.connect(connect_to)

def get_first_timestamp(log_file):
	with open(log_file) as f:
		for line in f:
			line_json = json.loads(line)
			return line_json["timestamp"]



start_time_file = get_first_timestamp(log_file)
start_time_importer = time.time()

with open(log_file) as f:
	for line in f:
		line_json = json.loads(line)

		importer_age = time.time() - start_time_importer
		line_age = line_json["timestamp"] - start_time_file

		sleep_time = line_age - importer_age

		if sleep_time > 0:
			#print(str(line_age)+" - "+str(importer_age))
			#print(sleep_time)
			time.sleep(sleep_time)


		print(line_json)
		send_socket.send_json(line_json)
