import socket
import json

def handleRequest(conn):
	print(conn)
	val = conn.recv(4096)
	name = getName(val)
	conn.send(getCode(name))
	#if val == "5c:cf:7f:02:4f:a5":
		#conn.send("print('Hello my name is Glucose')")
	#elif val == "18:fe:34:de:25:f8":
		#conn.send("print('Hello my name is Fructose')")

def getName(val):
	f = open("names.json",'r')
	names = json.loads(f.read())
	return names[val]

def getCode(name):
	f = open(name,'r')
	return f.read()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(("192.168.0.17",41990))
s.listen(5)
while True:
	conn,addr = s.accept()
	print(addr)
	handleRequest(conn)

