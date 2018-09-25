#!/usr/bin/python
# -*- coding: utf8 -*-
import zmq
import sys
import configparser


config = configparser.ConfigParser()
config.read('config.cfg')

portfrontend = config['DEFAULT']['port_req']
portbackend = config['DEFAULT']['port_back']
timeout = int(config['DEFAULT']['timeout'])

if len(sys.argv) > 1:
    portfrontend = sys.argv[1]
    portbackend =  sys.argv[2]

# Prepare our context and sockets
context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)

frontend.bind("tcp://%s:%s" % ("*", portfrontend))
backend.bind("tcp://%s:%s" % ("*", portbackend))

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

print("Server Running...")
# Switch messages between sockets
while True:
    socks = dict(poller.poll(timeout=timeout * 1000))

    if socks.get(frontend) == zmq.POLLIN:
        message = frontend.recv_multipart()
        backend.send_multipart(message)

    if socks.get(backend) == zmq.POLLIN:
        message = backend.recv_multipart()
        frontend.send_multipart(message)
