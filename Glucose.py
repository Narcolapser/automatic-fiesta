from TelnetFiesta import *
import time

def listdir(val,telServer=None):
	import os
	ret = " ".join(os.listdir())
	return ret + "\n"

server = TelnetServer(blocking=False)

server.registerFunction("ls",listdir) #closes the connection.

while True:
	server.run()
	print("Look ma! no blocking!")
	time.sleep(1)
