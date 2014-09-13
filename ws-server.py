#!/usr/bin/env python3

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
import asyncio
import time
import json
import numpy
import pprint
import zmq
import numpy as np
import base64
from classes.BroadcastServerFactory import BroadcastServerFactory
from classes.BroadcastServerProtocol import BroadcastServerProtocol
from classes.WebsocketClient import WebsocketClient


listen_addr = "0.0.0.0"
listen_port = 10000

zmq_connect_addr = "0.0.0.0"
zmq_connect_port = 5001

server_type = "telemetry"

factory = BroadcastServerFactory("ws://"+listen_addr+":"+str(listen_port), zmq_connect_addr, zmq_connect_port, server_type, debug = False)
factory.protocol = BroadcastServerProtocol

loop = asyncio.get_event_loop()


#loop.call_soon(factory.sendTick, loop)
loop.call_soon(factory.cleanClients, loop)
loop.call_soon(factory.pullData, loop)
loop.call_soon(factory.printStats, loop)


coro = loop.create_server(factory, listen_addr, listen_port)
server = loop.run_until_complete(coro)

loop.run_forever()
