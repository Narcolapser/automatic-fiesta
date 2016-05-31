from TelnetFiesta import *
import time

server = TelnetServer(blocking=False)
while True:
	server.run()
	print("Look ma! no blocking!")
	time.sleep(1)
