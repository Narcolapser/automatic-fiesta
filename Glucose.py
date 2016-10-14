from TelnetFiesta import *
import gc
import time

def listdir(val,telServer=None):
	import os
	ret = " ".join(os.listdir())
	return ret + "\n"

telserver = TelnetServer(blocking=False)
telserver.registerFunction("ls",listdir)
print("Telnet Server ready")
#while True:
#	telserver.run()
#	print("Look ma! no blocking!")
#	time.sleep(1)

from WebFiesta import *

webserver = WebFiesta(blocking=False)
webserver.registerFunction("ls",listdir)
print("Web Server ready")

#while True:
#	webserver.run()
#	print("Lap")
#	time.sleep(1)

while True:
	telserver.run()
	webserver.run()
	print("Both ran! Memory free:",gc.mem_free())
	time.sleep(1)
