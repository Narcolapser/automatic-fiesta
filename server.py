import socket
import json

def handleRequest(conn):
	print(conn)
	val = conn.recv(4096)
	config = getConfig(val)
	conn.send(json.dumps(config))
	print(config)
	

def sendFile(val,conn):
	while len(val) > 120:
		payload = len(val)
		print(payload)
		payload += val[0:120]
		conn.send(payload)
	payload = len(val)
	print(payload)
	payload += val

def getConfig(val):
	f = open("names.json",'r')
	names = json.loads(f.read())
	return names[val]

def getCode(name):
	codeFiles = []
	for i in name:
		with open(i,'r') as f:
			codeFiles.append((i,f.read))
	return codeFiles
	
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("192.168.0.17",41990))
s.listen(5)
while True:
	conn,addr = s.accept()
	print(addr)
	handleRequest(conn)
