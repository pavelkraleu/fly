from autobahn.asyncio.websocket import WebSocketServerProtocol
import json
import time

class BroadcastServerProtocol(WebSocketServerProtocol):
	def __init__(self):
		self.path = ""

	def onConnect(self, request):
		self.path = request.path

		#print(request.peer)
		#print(request.headers)
		#print(request.host)
		#print(request.path)
		#print(request.params)
		#print(request.version)
		#print(request.origin)
		#print(request.protocols)
		#print(request.extensions)

	def connectionLost(self, reason):
   		WebSocketServerProtocol.connectionLost(self, reason)
   		self.factory.unregister(self)
   		print("connectionLost")

	def onOpen(self):
		self.factory.register(self)
		print("open")

	def onMessage(self, payload, isBinary):
		#print("onMessage")

		msgJson = json.loads(payload.decode('utf8'))

		if msgJson['type'] == "tick_client":
			try:
				#if self.factory.clients[self.peer].lastSeq+1 != int(msgJson['seq']):
				#	self.factory.clients[self.peer].packetLoss+=1
				#self.factory.clients[self.peer].lastSeq = int(msgJson['seq'])
				self.factory.clients[self.peer].lastSeqTime = int(time.time())
			except KeyError:
				print("Unknown client {0}".format(self.factory.clients[self.peer].clientObj.peer))
