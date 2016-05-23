f = open("boot.py","w")
v = """
import time
import network
import socket
import esp
import ubinascii


wlan = network.WLAN()

failsafe = 0

while wlan.status() != network.STAT_GOT_IP:
	failsafe += 1
	if failsafe > 100:
		break
	time.sleep_ms(100)
	print("Nope!",wlan.status(),failsafe)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Connected! ",wlan.ifconfig()[0])

s.connect(("192.168.0.17",41990))
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
s.send(mac)

print("Getting script")
r = s.recv(128)
main_str = r
s.settimeout(2)
print("recieved {0} chars".format(len(r)))
while len(r) > 0:
	try:
		r = s.recv(128)
		print("recieved {0} chars".format(len(r)))
		main_str += r
	except OSError as OSE:
		print("Nothing left to get. Moving no.")
		break

print("Recived script.")

main_file = open("main.py","w")
main_file.write(main_str)
main_file.close()

print("Main has been writen.")
"""
f.write(v)
f.close()
