try:
	import usocket as socket
except:
	import socket

from machine import Pin
import time

CONTENT = b"""HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>{0}</title>
</head>
<body>
{1}
</body>
</html>
"""

class WebFiesta:
	def __init__(self,content=None,port=8080,host="0.0.0.0",blocking=True):
		self.PORT = port # the default port is 23, but you can change it if you like.
		self.HOST = host
		self.blocking = blocking
		self.__bind()
		
		if not content:
			self.content = CONTENT
		else:
			self.content = content

		#these are just some default functions.
		self.functions = {}
		self.registerFunction("time",getTime) #gets uptime.
		self.registerFunction("reboot",reboot) #reboots the device.
		self.registerFunction("exit",exit) #closes the connection.

	def __bind(self):
		'''
		Private function for binding and rebinding the socket as clients come and go.
		'''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.closed = True
		try:
			self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.sock.bind((self.HOST, self.PORT))
			self.sock.listen(10)
		except Exception as msg:
			print("Web Binding error: ",msg)
		print('Web Socket bind complete')

	def run(self):
		'''
		ME! CALL ME! This is the main function call for the AF Web Server. When this
		function is called it will do one of many things.
		
		
		'''
		if not self.blocking:
			self.sock.settimeout(5)
		else:
			self.sock.settimeout(None)


		try:
			#wait to accept a connection
			self.conn, self.addr = self.sock.accept()
			print('Web Connected with ' + self.addr[0] + ':' + str(self.addr[1]))
		except OSError as e:
			print("Web OS Error in connecting: ",e)
			return

		recv = self.conn.recv(1024).decode("utf-8").split("\r\n")[0].split(" ")

		func,data = recv[1][1:],recv
		print("What I got: ",func,data)
		if func in self.functions.keys():
			reply = self.functions[func](data,self)
		else:
			reply = "Command not find.\n"
		reply = self.content.format("Success",reply)
		print(reply)
		self.conn.send(reply)

	def registerFunction(self,name,func):
		'''
		Register a new function with the telnet server. the prototype for the function is:
		
			def functionName(stringFromClinet,telServer=None):
				return "response\n"
		
		Meaning, your function must accept one positional argument which will be the string
		sent in from the telnet client. And then a second argument, which will be the telnet
		server itself. For example:
		
			def getTime(val,telServer=None):
				return str(time.time()) + "\n"
		
		name -- the word that will invoke the call.
		func -- the function to call, as described above.
		'''
		self.functions[name] = func

def getTime(val,telServer=None):
	return str(time.time()) + "\n"

def reboot(val,telServer=None):
	if telServer:
		telServer.conn.sendall(telServer.content.format("Rebooting","Rebooting...\n\000"))
		telServer.conn.close()

	import machine
	machine.reset()

def exit(val,telServer=None):
	if telServer:
		telServer.closed=True
	return "Closing\n\000"

"""
Example Request:
GET /toggle HTTP/1.1
Host: 192.168.0.16:8080
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-GB,en-US;q=0.8,en;q=0.6
"""
