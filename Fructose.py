try:
	import usocket as socket
except:
	import socket

from machine import Pin
from rcswitch import RCswitch
from WebFiesta import *

def toggle(val,server=None):
	from machien import Pin
	from rcswitch import RCswitch
	p = Pin(2,Pin.OUT)
	r = RCswitch(p)
	r.send(3847937)

webserver = WebFiesta(blocking=False)
webserver.registerFunction("toggle",toggle)


while True:
	try:
		webserver.run()
	except:
		print("oopsies!")
