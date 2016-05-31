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
<title>Success</title>
</head>
<body>
You have accessed an Automatic Fiesta Node. It is named "{0}". and posseses the following functions:</br>
{1}
</body>
</html>
"""

class WebFiesta:
	def __init__(self,content=None,port=8080,blocking=True):
		self.PORT = port # the default port is 23, but you can change it if you like.
		self.blocking = blocking
		self.__bind()

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
			print("Binding error: ",msg)
		print('Socket bind complete')

	def run(self):
		if not self.blocking:
			self.sock.settimeout(5)
		else:
			self.sock.settimeout(None)


		try:
			#wait to accept a connection 
			self.conn, self.addr = self.sock.accept()
			print('Connected with ' + self.addr[0] + ':' + str(self.addr[1]))
		except OSError as e:
			print("OS Error in connecting: ",e)
			return

		recv = self.conn.recv(4096).decode("utf-8").split("\r\n")[0].split(" ")

		func,data = recv[1][1:],recv
		if func in self.functions.keys():
			reply = self.functions[data](data,self)
		else:
			reply = "Command not find.\n"

		if "GET /toggle" in val:
			print("Toggling!")
			r.send(3847937)
		counter += 1
		print()

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
		telServer.conn.sendall("Rebooting...\n\000")
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
