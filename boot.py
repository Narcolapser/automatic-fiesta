f = open("boot.py","w")
v = """
import time
import network
import socket
import esp
import ubinascii
import json

def parseFetch(val):
	remaining = val[0:8]
	payload = val[8:]
	return (remaining,payload)

def fetch(name,s):
	s.send(name)
	remaining,ret = praseFetch(s.recv(128))
	remaining = int(remaining)
	print("recieved {0} chars".format(len(r)))
	while remaining > 120:
		try:
			remaining,payload = parseFetch(s.recv(128))
			remaining = int(remaining)
			ret += payload
			print("recieved {0} chars with {1} left to go.".format(len(payload),remaining))
		except OSError as OSE:
			print("Nothing left to get. Moving no.")
			break
	print("Got all of {0} it had a total of {1} bytes".format(name,len(ret)))
	return ret

wlan = network.WLAN()

failsafe = 0

while wlan.status() != network.STAT_GOT_IP:
	failsafe += 1
	if failsafe > 100:
		break
	time.sleep_ms(100)
	print("Nope!",wlan.status(),failsafe)

print("Connected! ",wlan.ifconfig()[0])
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(("192.168.0.17",41990))
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
s.send(mac)

s.settimeout(2)

print("Getting script")

main_str = fetch("Fructose",s)

print("Received script(s).")

for script,code in json.loads(main_str):
	script_file = open("main.py","w")
	script_file.write(main_str)
	script_file.close()

print("Main has been writen.")
"""
f.write(v)
f.close()
