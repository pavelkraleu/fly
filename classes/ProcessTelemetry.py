
import time

class ProcessTelemetry:

	def __init__(self):
		self.packet_count = 0
		self.packet_count_invalid = 0
		self.last_metric_exec = time.time()

	def processMetrics(self):
		metric_delay = time.time() - self.last_metric_exec 

		print("TELEMETRY packet_count {}/sec packet_count_invalid {}/sec".format(self.packet_count/metric_delay,self.packet_count_invalid/metric_delay))

		packet = {'packet_count':self.packet_count,'packet_count_invalid':self.packet_count_invalid}

		self.packet_count = 0
		self.packet_count_invalid = 0
		self.last_metric_exec = time.time()

		return packet

	def processPacket(self,packet):
		try:
			if packet["type"] == "mavlink":
				self.packet_count+=1
				return self.processMAVlinkPacket(packet)
			if packet["type"] == "flightmode":
				self.packet_count+=1
				return self.processFlightmodePacket(packet)
		except KeyError:
			#print("Invalid packet type")
			self.packet_count_invalid+=1

	def processFlightmodePacket(self,packet):		
		new_packet = {'source':packet["source"],'type':'flightmode','content':{"flightmode":packet["content"]["mode"]}} 

		return new_packet


	def processMAVlinkPacket(self,packet):
		packet_type = packet["content"]["mavpackettype"]

		new_packet = None
		new_packet_skeleton = {'source':packet["source"],'content':{}} 

		if packet_type == "GPS_RAW_INT":
			new_packet = self.processMAVlinkPacketGPSRawInt(packet,new_packet_skeleton)
		elif packet_type == "SYS_STATUS":
			new_packet = self.processMAVlinkPacketSysStatus(packet,new_packet_skeleton)
		elif packet_type == "VFR_HUD":
			new_packet = self.processMAVlinkPacketVfrHud(packet,new_packet_skeleton)
		elif packet_type == "RC_CHANNELS_RAW":
			new_packet = self.processMAVlinkPacketRcChannelsRaw(packet,new_packet_skeleton)
		elif packet_type == "ATTITUDE":
			new_packet = self.processMAVlinkPacketAttitude(packet,new_packet_skeleton)

		#print(new_packet)
		return new_packet
		
	def processMAVlinkPacketAttitude(self,packet,new_packet):
		new_packet["type"] = "attitude"

		new_packet["content"]["pitchspeed"] = round(packet["content"]["pitchspeed"],2)
		new_packet["content"]["rollspeed"] = round(packet["content"]["rollspeed"],2)
		new_packet["content"]["yawspeed"] = round(packet["content"]["yawspeed"],2)

		return new_packet

		
	def processMAVlinkPacketGPSRawInt(self,packet,new_packet):
		new_packet["type"] = "gps"

		new_packet["content"]["satellites_visible"] = packet["content"]["satellites_visible"]
		new_packet["content"]["lon"] = float(packet["content"]["lon"]/10000000)
		new_packet["content"]["lat"] = float(packet["content"]["lat"]/10000000)

		return new_packet

	def processMAVlinkPacketSysStatus(self,packet,new_packet):
		new_packet["type"] = "sys_status"

		new_packet["content"]["battery_remaining"] = packet["content"]["battery_remaining"]
		new_packet["content"]["voltage_battery"] = round(packet["content"]["voltage_battery"]/1000,1)
		new_packet["content"]["current_battery"] = round(float(packet["content"]["current_battery"])/100,1)

		return new_packet

	def processMAVlinkPacketVfrHud(self,packet,new_packet):
		new_packet["type"] = "vfr_hud"

		new_packet["content"]["heading"] = packet["content"]["heading"]
		new_packet["content"]["climb"] = round(packet["content"]["climb"],2)
		new_packet["content"]["throttle"] = packet["content"]["throttle"]
		new_packet["content"]["alt"] = round(packet["content"]["alt"],1)

		return new_packet

	def processMAVlinkPacketRcChannelsRaw(self,packet,new_packet):
		new_packet["type"] = "rc_channels_raw"

		for i in range(1,5):
			value = packet["content"]["chan"+str(i)+"_raw"]
			new_packet["content"]["chan"+str(i)+"_raw"] = value
			
		return new_packet
