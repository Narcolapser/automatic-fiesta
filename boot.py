import time
import network
import socket
import esp

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
#s.send("18:fe:34:de:25:f8")
s.send(str(esp.flash_id()))

print("Getting script")
r = s.recv(4096)
main_str = r

while len(r) == 4096:
	r = s.recv(4096)
	main_str += r

print("Recived script.")

main_file = open("main.py","w")
main_file.write(main_str)
main_file.close()

print("Main has been writen.")
