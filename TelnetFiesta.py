try:
	import usocket as socket
except:
	import socket
import time

class TelnetServer:
	'''
	Automatic Fiesta Telnet server!
	
	A simple, yet extendable, telnet server for automatic fiesta. This gives you even greater 
	control over you AF nodes out in the field. Most noteably because one of the default
	functions is "Reboot", which can make a node in the field pull down new code. 
	
	If you want to add commands to the telnet server just call server.registerFunction with the
	word used to invoke the command and the function name you want to register it to. The
	function must accept one positional argument which will be the string sent in from the
	telnet client. And then a second argument, which will be the telnet server itself. See the
	functions below (getTime,reboot,exit) to get an idea. 
	'''
	def __init__(self,blocking=True,port=23):
		'''
		create a new telnet server. This init function accepts optional two arguments. 
		
		blocking -- Whether or not you want the server to be blocking.
		port -- what port you want the server to be listening on.
		'''
		self.HOST = '' # Symbolic name, meaning all available interfaces
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
			print("Telnet Binding error: ",msg)
		print('Telnet Socket bind complete')

	def run(self):
		'''
		ME! CALL ME! This is the main function call for the AF Telnet Server. When this
		function is called it will do one of many things.
		
		If there is no active connection and the server is set to none blocking it will try
		to accept a incoming connection, waiting up to 5 seconds. If no connection is made,
		then it will return.
		
		If the server is blocking then it will wait here till a connection is made.
		
		When a connection is made or if there is already an active connection, then we move
		on to interacting with the client. 
		
		And again with the clinet, if the server is none blocking then it will wait 5
		seconds for a command before it returns. If the server is blocking then it will wait
		indefinately for a command.
		
		When a string has finally been recieved then it will procede to try and execute it
		returning the result. 
		'''
		if not self.blocking:
			self.sock.settimeout(5)
		else:
			self.sock.settimeout(None)

		if self.closed:
			try:
				#wait to accept a connection 
				self.conn, self.addr = self.sock.accept()
				print('Connected with ' + self.addr[0] + ':' + str(self.addr[1]))
				self.conn.recv(1024).decode("utf-8")
				self.closed = False
			except OSError as e:
				print("Telnet OS Error in connecting: ",e)
				return
		recv = ""

		while not self.closed:
			#Receiving from client
			try:
				recv += self.conn.recv(1024).decode("utf-8")
			except OSError as e:
				print("Telnet OS Error receiving: ", e)
				return None

			if recv[-1:] == '\n':
				data = recv
				recv = ""
				print(data)
			elif len(recv) == 0:
				data = ""
			
			#if a partial line has been recieved, we need to loop around and
			#try to get the rest of it.
			else:
				print((recv,))
				continue

			#this is where the functions are actually called.
			try:
				data = data.replace("\r","")
				data = data.replace("\n","")
				print((data,))
				if data in self.functions.keys():
					reply = self.functions[data](data,self)
				else:
					reply = "Telnet Command not find.\n"
		
			except Exception as e:
				data = "Error: " + str(e) + "\n"

			#reply = 'OK...' + str(data) + '\n'
			if not data:
				break
			data = ""
			print((reply,))
			self.conn.sendall(reply)
		print("Telnet Connection closed")

		if self.closed:
			self.sock.close()
			self.__bind()

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
