from autobahn.asyncio.websocket import  WebSocketServerFactory
import zmq
import numpy as np
import time
import json
from classes.WebsocketClient import WebsocketClient

class BroadcastServerFactory(WebSocketServerFactory):
	def __init__(self, url, zmq_endpoint,server_type, debug = False, debugCodePaths = False):
		WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
		self.tickcount = 0

		self.server_type = server_type

		self.cleanClientsTimeout = 5
		self.clientMaxTimeout = 30
		self.statsTimeout = 5

		self.clients = {}

		self.context = zmq.Context()
		self.recv_context = self.context.socket(zmq.PULL)
		self.recv_context.bind(zmq_endpoint)

		self.cycleTracker = [0]

		self.timeouts = []
		self.packetLoss = []

	def printStats(self,loop):
		print("STATS")
		print("Busy cycles {0:.2f}".format(np.mean(self.cycleTracker)))
		print("Num of clients {0}".format(len(self.clients)))
		if len(self.clients) > 0:
			print("Time Max {0:.2f}s Min {1:.2f}s Avg {2:.2f}s".format(max(self.timeouts),min(self.timeouts),np.mean(self.timeouts)))
			print("Loss Max {0} Min {1} Avg {2}".format(max(self.packetLoss),min(self.packetLoss),np.mean(self.packetLoss)))

		print()

		loop.call_later(self.statsTimeout, self.printStats, loop)

	def trackcycles(self,gotData):
		if gotData == True:
			self.cycleTracker.insert(0,100)
		else:
			self.cycleTracker.insert(0,0)

		del self.cycleTracker[100:]

	def pullData(self,loop):
		#print("pullData")
		try:
			if self.server_type == "telemetry":
				packet = self.recv_context.recv_json(flags=zmq.NOBLOCK)
			else:
				packet = self.recv_context.recv(flags=zmq.NOBLOCK)

			self.broadcast(packet)
			#print("data")
			#print(packet)
			#print(packet["type"]+" "+str(np.mean(cycleTracker)))
			self.trackcycles(True)
			#time.sleep(0.00001)
		except zmq.error.Again:
			#print("No data")
			self.trackcycles(False)


		loop.call_soon(self.pullData, loop)

	def sendTick(self, loop):
		print("sendTick")

	def cleanClients(self,loop):
		#print("cleanClients")

		toDelete = []
		self.timeouts = []
		self.packetLoss = []

		for ind in self.clients:
			timeout = time.time() - self.clients[ind].lastSeqTime
			self.timeouts.append(timeout)
			self.packetLoss.append(self.clients[ind].packetLoss)
			#print("{0} {1} {2}".format(ind,self.clients[ind].lastSeq,timeout))

			if timeout > self.clientMaxTimeout:
				print("Deleting {0} {1} {2}".format(ind,self.clients[ind].lastSeq,timeout))
				toDelete.append(ind)

		for delete in toDelete:
			del self.clients[delete]



		loop.call_later(self.cleanClientsTimeout, self.cleanClients, loop)

	def register(self, client):
		print("registered client {} {}".format(client.peer,client.path))

		newClient = WebsocketClient(client)
		self.clients[str(client.peer)] = newClient


		#help(client)


	def unregister(self, client):
		print("unregister")

	def broadcast(self, msg):
		#print("broadcast "+str(msg))
		
		#jpgnp = np.array(msg).tostring()
		if self.server_type == "images":
			#jpgb64 = base64.b64encode(msg)
			for ind in self.clients:
				self.clients[ind].clientObj.sendMessage(msg,isBinary = False)

		if self.server_type == "telemetry":
			for ind in self.clients:	
				print(json.dumps(msg))
				self.clients[ind].clientObj.sendMessage(json.dumps(msg).encode('utf-8'),isBinary = False)
