import zmq
import sys
import configparser


config = configparser.ConfigParser()
config.read('config.cfg')

ip_back = config['DEFAULT']['ipback']
ip_pub = config['DEFAULT']['ippub']
port_back = config['DEFAULT']['port_back']
port_pub = config['DEFAULT']['port_pub']
timeout = int(config['DEFAULT']['timeout'])

if len(sys.argv) > 1:
    ip_back, port_back = sys.argv[1].split(":")
    ip_pub, port_pub =  sys.argv[2].split(":")

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://%s:%s"% (ip_back, port_back))


poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

context2 = zmq.Context()
socketp = context2.socket(zmq.PUB)
socketp.bind("tcp://%s:%s" % (ip_back, port_pub))

print("Worker Running...")
while True:
    socks = dict(poller.poll(timeout=timeout * 1000))

    if socks.get(socket) == zmq.POLLIN:
        msg = socket.recv_multipart()
        userid = msg[1]
        # accept
        socket.send_multipart([userid, b'1'])
        msg.append('1')
        msg.append('response code')
        # do some work
        # sent to client
        socketp.send_multipart(msg)
        
        

        



    
    


