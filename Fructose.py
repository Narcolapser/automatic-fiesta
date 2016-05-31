try:
	import usocket as socket
except:
	import socket

from machine import Pin
from rcswitch import RCswitch
import time
import machine
import gc

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
#	shh = Pin(3,Pin.OUT)
#	shh.low()
	s = socket.socket()

	# Binding to all interfaces - server will be accessible to other hosts!
	ai = socket.getaddrinfo("0.0.0.0", 8080)
	print("Bind address info:", ai)
	addr = ai[0][-1]

	#prepping LED pin
	p = Pin(2,Pin.OUT)
	p.high()
	time.sleep(1)
	p.low()
	
	r = RCswitch(p)


	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(addr)
	s.listen(5)

	print("Listening, connect your browser to http://<this_host>:8080/")

	counter = 0
	while True:
		s.settimeout(None)
		res = s.accept()
		s.settimeout(1)
		client_s = res[0]
		client_addr = res[1]
		print("Client address:", client_addr)
		print("Client socket:", client_s)
		try:
			print("Getting content")
			val = client_s.recv(4096)
			print("Content:", val)
		except:
			print("nm, to slow")
			break
		client_s.send(CONTENT % counter)
		client_s.close()
		if "GET /toggle" in val:
			p.high()
			time.sleep(2)
			p.low()
			print("Toggling!")
			r.send(3847937)
		counter += 1
		gc.collect()


print('Hello my name is Fructose, you are getting this from the new server config.')
main()

