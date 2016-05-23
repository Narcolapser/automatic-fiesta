try:
	import usocket as socket
except:
	import socket

from machine import Pin
from rcswitch import RCswitch
import time
import machine

#CONTENT = b"""\
#HTTP/1.0 200 OK
#Hello #%d from MicroPython!
#"""

CONTENT = b"""HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>Success</title>
</head>
<body>
Boo! #%d
</body>
</html>
"""

def main(use_stream=False):
	s = socket.socket()

	# Binding to all interfaces - server will be accessible to other hosts!
	ai = socket.getaddrinfo("0.0.0.0", 8080)
	print("Bind address info:", ai)
	addr = ai[0][-1]

	#prepping LED pin
	p = Pin(2,Pin.OUT)
#	p.high()
#	time.sleep(1)
#	p.low()


	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(addr)
	s.listen(5)
	print("Listening, connect your browser to http://<this_host>:8080/")

	counter = 0
	while True:
		res = s.accept()
		client_s = res[0]
		client_addr = res[1]
		print("Client address:", client_addr)
		print("Client socket:", client_s)
		print("Request:")
		if use_stream:
			# MicroPython socket objects support stream (aka file) interface
			# directly.
			#print(client_s.read(4096))
			val = client_s.read(4096)
			print(val)
			client_s.write(CONTENT % counter)
		else:
			#print(client_s.recv(4096))
			val = client_s.recv(4096)
			print(val)
			client_s.send(CONTENT % counter)
		if "GET /toggle" in val:
			print("Toggling!")
			p.high()
			time.sleep(1)
			p.low()
			machine.reset()
		client_s.close()
		counter += 1
		print()


print('Hello my name is Fructose, you are getting this from the new server config.')
main()


