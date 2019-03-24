import socket,sys

ip="127.0.0.1"
port=4444

class Listener:
	def __init__(self,ip,port):
		self.ip=ip
		self.port=port
		self.connection=self.connect(self.ip,self.port)
	def connect(self,ip,port):
		listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		listener.bind((ip,port))
		listener.listen(0)
		connection,self.address=listener.accept()
		print "[+] Connection established\n"
		return connection
	def __str__(self):
		print str(self.address)
	def send(self,data):
		self.connection.send(data);
		if(data=="exit"):
			sys.exit(0)
		return self.connection.recv(1024)
	def main(self):
		command = raw_input("$ ")
		_response = self.send(command)
		if _response=="":
			self.close()
			print "closed connection... Loooking for new ones"
			self.connect(self.ip,self.port)
			return
		print _response
	def close(self):
		self.connection.close()
	def check_connection(self):
		#TODO
		pass
	def packinput(self):
		#TODO
		pass
	def packoutput(self):
		#TODO
		pass



listnr=Listener(ip,port)
print listnr.address
while True:
	listnr.main()
