import time
import base64

class ProcessImages:

	def __init__(self):
		self.packet_count = 0
		self.packet_count_invalid = 0
		self.last_metric_exec = time.time()

	def processPacket(self,packet):
		self.packet_count+=1
		#print("Image !")
		new_packet = base64.b64encode(packet)

		return new_packet

	def processMetrics(self):
		metric_delay = time.time() - self.last_metric_exec 

		print("IMAGES image_count {}/sec image_count_invalid {}/sec".format(self.packet_count/metric_delay,self.packet_count_invalid/metric_delay))

		packet = {'packet_count':self.packet_count,'packet_count_invalid':self.packet_count_invalid}

		self.packet_count = 0
		self.packet_count_invalid = 0
		self.last_metric_exec = time.time()

		return packet
