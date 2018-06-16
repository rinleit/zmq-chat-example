import zmq
import sys
import time
import thread
import configparser

__GOOD__ = '1'

class Message:
	"""docstring for Message"""
	def __init__(self, userid=None, targetid=None, content=None, name=None):
		self.userid = userid
		self.targetid = targetid
		self.name = name
		self.content = content
		self.sendtime = 0
	
	def settime(self, value):
		self.sendtime = value

	def list(self):
		return ['', self.userid, self.targetid, self.name, self.content, self.sendtime]


config = configparser.ConfigParser()
config.read('config.cfg')

ip_req = config['DEFAULT']['ipfront']
ip_pub = config['DEFAULT']['ippub']
port_req = config['DEFAULT']['port_req']
port_sub = config['DEFAULT']['port_pub']
timeout = int(config['DEFAULT']['timeout'])

if len(sys.argv) > 1:
	ip_req, port_req = sys.argv[1].split(":")
	ip_pub, port_pub =  sys.argv[2].split(":")

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://%s:%s" % (ip_req, port_req))

me = raw_input("Your Name: ").strip()
userid = str(hash(me) % 10**5)
friends = raw_input("FriendList Name: ").split(" ")
targetid = [str(hash(x) % 10**5) for x in friends if x != '']

def get_msg():
	context = zmq.Context()
	public = context.socket(zmq.SUB)
	public.connect("tcp://%s:%s" % (ip_pub, port_sub))
	public.setsockopt(zmq.SUBSCRIBE, '')
	
	while 1:
		msg_revc = public.recv_multipart()
		if msg_revc[6] == __GOOD__:
			if userid in msg_revc[2]:
				friendname = msg_revc[3]
				msg_content = msg_revc[4]
				sendtime = msg_revc[5]
				print("[%s %s] > %s" % (str(friendname).upper(), sendtime, msg_content))


poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
thread.start_new_thread(get_msg, ())

while 1:
	content = raw_input()
	msg = Message(userid=userid, targetid=str(targetid), name=me, content=content)
	msg.settime(time.strftime("%a, %d %b %Y %H:%M:%S"))
	socket.send_multipart(msg.list())
	del msg
	
	while 1:
		socks = dict(poller.poll(timeout=timeout * 1000))

		if socks.get(socket) == zmq.POLLIN:
			res =  socket.recv_multipart()
			if res[1] == __GOOD__:
				if res[0] == userid:
					break
		else:
			print("TimeOut")


			

		
		
				


		
		


	
















