#!/usr/bin/env python

import json
import sys
import time

log_file = "./mavlink-log.txt"



def get_first_timestamp(log_file):
	with open(log_file) as f:
		for line in f:
			line_json = json.loads(line)
			return line_json["timestamp"]


start_time_importer = time.time()
start_time_file = get_first_timestamp(log_file)


with open(log_file) as f:
	for line in f:
		line_json = json.loads(line)

		importer_age = time.time() - start_time_importer
		line_age = line_json["timestamp"] - start_time_file

		sleep_time = abs(line_age - importer_age)

		print(sleep_time)
		time.sleep(sleep_time)