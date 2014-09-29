#!/usr/bin/python2

import sys
import cv2
import cv2.cv as cv
import numpy
import zmq
import time


if len(sys.argv) != 2:
	print("Usage: "+sys.argv[0]+" tcp://10.8.0.1:2000")
	sys.exit(1)

images_endpoint = sys.argv[1]


zmq_context = zmq.Context()


frame_width = 320
frame_height = 240

print_debug = True

add_debug_text = False

resize_frame = False

jpeg_quality = 10

vc = cv2.VideoCapture(0)

vc.set(cv.CV_CAP_PROP_FRAME_WIDTH, frame_width)
vc.set(cv.CV_CAP_PROP_FRAME_HEIGHT, frame_height)


# Create images endpoint
images_context = zmq_context.socket(zmq.PUSH)

images_context.setsockopt(zmq.SNDBUF,50000)
images_context.setsockopt(zmq.RCVBUF,50000)
images_context.setsockopt(zmq.SNDHWM,20)

images_context.connect(images_endpoint)


encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),jpeg_quality]


def print_debug(text):
	if print_debug:
		print(text)


def process_frame():
	global frame
	if resize_frame:
		frame = cv2.resize(frame, (resize_frame_width, resize_frame_height)) 
		print_debug("Resizing frame to {}x{}".format(resize_frame_width,resize_frame_height))

def add_text():
	global frame
	height, width, depth = frame.shape
	txt = "{}x{} {}%".format(width,height,jpeg_quality)
	cv2.putText(frame,txt, (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

def send_frame():
	global frame,frame_count
	ret, jpg = cv2.imencode( '.jpg', frame,encode_param)
	images_context.send(jpg.tostring())
	#print "frame"


while True:
		
	rval, frame = vc.read()

	process_frame()

	if add_debug_text:
		#pass
		add_text()

	send_frame()


	

	





