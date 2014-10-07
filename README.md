Startup
=======


* ./ws-server.py telemetry tcp://0.0.0.0:5001 1001
* ./ws-server.py images tcp://0.0.0.0:5002 1002
* ./zmq-bridge.py telemetry tcp://0.0.0.0:4001 tcp://127.0.0.1:5001
* ./zmq-bridge.py images tcp://0.0.0.0:4002 tcp://127.0.0.1:5002

* ./push-images.py tcp://10.8.0.6:4002