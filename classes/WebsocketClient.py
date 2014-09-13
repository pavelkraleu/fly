import time

class WebsocketClient:
	def __init__(self,client):

		self.clientObj = client
		self.lastSeq = 0
		self.packetLoss = 0
		self.lastSeqTime = time.time()

		print("Client "+str(client.peer)+" created")