import socket
import json

def handleRequest(conn):
	print(conn)
	val = conn.recv(4096)
	config = getConfig(val)
	conn.send(json.dumps(config))
	print(config)
	fname = conn.recv(128)
	conn.settimeout(5)
	while fname:
		try:
			while fname == "12345678": fname = conn.recv(128)
			if fname == "Complete": break
			while fname[0:8] == "12345678": fname = fname[8:]
			print("sending file: {0}".format(fname))
			code = getCode(fname)
			sendFile(code,conn)
			fname = conn.recv(128)
		except IOError as e:
			print(e)
			fname = conn.recv(128)
		except Exception as e:
			print(e)
			break

def sendFile(val,conn):
	while len(val) > 120:
		payload = str(len(val))
		while len(payload)<8:payload = '0' + payload
		print(payload)
		payload += val[0:120]
		conn.send(payload)
		val = val[120:]
		conn.recv(8)
	payload = str(len(val))
	while len(payload)<8:payload = '0' + payload
	print(payload)
	payload += val
	conn.send(payload)

def getConfig(val):
	f = open("names.json",'r')
	names = json.loads(f.read())
	return names[val]

def getCode(name):
	return open(name,'r').read()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("192.168.0.17",41990))
s.listen(5)
while True:
	conn,addr = s.accept()
	print(addr)
	handleRequest(conn)
