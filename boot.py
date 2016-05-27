v = """
import time
import network
import socket
import esp
import ubinascii
import json
#from helpers import *

def parseFetch(val):
	remaining = val[0:8]
	payload = val[8:]
	print(val)
	return (remaining,payload)

def fetch(name,s):
	s.send(name)
	remaining,ret = parseFetch(s.recv(128))
	s.send("12345678")
	remaining = int(remaining)
	print("recieved {0} chars".format(len(ret)))
	while remaining > 120:
		try:
			remaining,payload = parseFetch(s.recv(128))
			s.send("12345678")
			remaining = int(remaining)
			ret += payload
			print("recieved {0} chars with {1} left to go.".format(len(payload),remaining))
		except OSError as OSE:
			print(ret)
			print("Nothing left to get. Moving no.")
			break
	print("Got all of {0} it had a total of {1} bytes".format(name,len(ret)))
	return ret

wlan = network.WLAN()

failsafe = 0

while wlan.status() != network.STAT_GOT_IP:
	failsafe += 1
	if failsafe > 500:
		break
	time.sleep_ms(100)
	print("Nope!",wlan.status(),failsafe)

print("Connected! ",wlan.ifconfig()[0])
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(("192.168.0.17",41990))
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
s.send(mac)
config = json.loads(s.recv(128))
s.settimeout(5)
print(config)
print(config["Main"])
print("Getting script")

main_str = fetch(config["Main"],s)
script_file = open("main.py","w")
script_file.write(main_str)
script_file.close()

print("Received main.")

print("There are {0} files to get next.".format(len(config["Files"])))
for script in config["Files"]:
	script_string = fetch(script,s)
	script_file = open(script,"w")
	script_file.write(script_string)
	script_file.close()

print("Main has been writen.")
"""
f = open("boot.py","w")
f.write(v)
f.close()
