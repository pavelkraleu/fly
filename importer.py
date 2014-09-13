#!/usr/bin/env python

log_file = "./mavlink-log.txt"

def get_first_timestamp(log_file):
	with open(log_file) as f:
		for line in f:
			print line
			return

with open(log_file) as f:
	for line in f:
		print line