#!/usr/bin/env python3

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
import asyncio
import time
import json
import numpy
import pprint
import zmq
import sys
import numpy as np
import base64
from classes.BroadcastServerFactory import BroadcastServerFactory
from classes.BroadcastServerProtocol import BroadcastServerProtocol
from classes.WebsocketClient import WebsocketClient

if len(sys.argv) < 3:
	print("Usage: "+sys.argv[0]+" server_type zmq_endpoint ws_port")
	sys.exit(1)

server_type = sys.argv[1]
zmq_endpoint = sys.argv[2]
listen_port = sys.argv[3]

allowed_types = ("telemetry","images")

if server_type not in allowed_types:
	print("server_type '"+server_type+"' is not allowed")
	sys.exit(-1)


listen_addr = "0.0.0.0"

factory = BroadcastServerFactory("ws://"+listen_addr+":"+str(listen_port), zmq_endpoint, server_type, debug = False)
factory.protocol = BroadcastServerProtocol

loop = asyncio.get_event_loop()


#loop.call_soon(factory.sendTick, loop)
loop.call_soon(factory.cleanClients, loop)
loop.call_soon(factory.pullData, loop)
loop.call_soon(factory.printStats, loop)


coro = loop.create_server(factory, listen_addr, listen_port)
server = loop.run_until_complete(coro)

loop.run_forever()
