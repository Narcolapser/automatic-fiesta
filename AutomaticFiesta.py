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

def main(use_stream=False):
	s = socket.socket()

	# Binding to all interfaces - server will be accessible to other hosts!
	ai = socket.getaddrinfo("0.0.0.0", 8080)
	print("Bind address info:", ai)
	addr = ai[0][-1]

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
			val = client_s.read(4096)
			print(val)
			client_s.write()
		else:
			val = client_s.recv(4096)
			print(val)
			client_s.send()
		client_s.close()
		if "GET /toggle" in val:
			print("Toggling!")
			r.send(3847937)
		counter += 1
		print()

main()
