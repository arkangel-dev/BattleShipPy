import socket
import threading
import json 
import time
import math

class Client:
	client_name = ""
	client_token = ""
	server = ""
	port = 0
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (server, port)

	x = 0
	y = 0
	health = 0
	flag = 0

	ShipList = []
	action_list = {"actions" : []}
	showWindow = False
	windowObejct = ""
	done = False
	radarThread = None
	gameActive = True

	def __init__ (self, client_name, secret_token, server, port):
		self.server = server
		self.port = port
		self.client_name = client_name
		self.client_token = secret_token
		self.server_address = (self.server, self.port)

	def StartRadar(self):
		self.radarThread = threading.Thread(target=self.RadarProcess)
		self.radarThread.start()

	def RadarProcess(self):
		while self.gameActive:
			try:
				data = self.sock.recv(500)
				self.ProcessRadarData(data)
			except (ConnectionAbortedError):
				print("[+] Disconnected from server...")

	def ProcessRadarData(self, data):
		jsonObj = data.decode('utf-8')

		if (jsonObj.split()[0].__eq__("[406]")):
			self.gameActive = False
			print("[!] Server has disconnected from client forcibly")
			print("[!] Reason :")
			print("\t {}".format(jsonObj.rstrip()))
			return

		jsonObj = json.loads(jsonObj)

		self.ShipList.clear()
		self.ShipList = jsonObj["ships"]
		self.x = jsonObj["ships"][0]["x"]
		self.y = jsonObj["ships"][0]["y"]
		self.health = jsonObj["ships"][0]["health"]
		self.flag = jsonObj["ships"][0]["flag"]

	def Connect(self):
		connthread = threading.Thread(target=self.CommitConnection)
		self.radarThread = threading.Thread(target=self.RadarProcess)
		self.CommitConnection()
		self.radarThread.start()
		
	def CommitConnection(self):
		self.sock.connect(self.server_address)
		Command = {
			"Action" : "INIT",
			"secret" : self.client_token,
			"shipname" : self.client_name
		}
		self.action_list["actions"].append(Command)
		self.CommitActions()

	def Move(self, x, y):
		Command = {
			"Action" : "MOVE",
			"x" : str(x),
			"y" : str(y)
		}
		self.action_list["actions"].append(Command)

	def SetCourse(self, x, y):
		Command = {
			"Action" : "SETCOURSE",
			"x" : str(x),
			"y" : str(y)
		}
		self.action_list["actions"].append(Command)

	def Fire(self, x, y):
		Command = {
			"Action" : "FIRE",
			"x" : str(x),
			"y" : str(y)
		}
		self.action_list["actions"].append(Command)

	def SelfDestruct(self):
		Command = {
			"Action" : "DESTRUCT",
		}
		self.action_list["actions"].append(Command)

	def CommitActions(self):
		if self.gameActive:
			try:
				Data = json.dumps(self.action_list)
				Data = Data.ljust(50)
				self.sock.sendall(Data.encode('utf-8'))
				time.sleep(0.08)
				self.action_list["actions"].clear()
			except (ConnectionAbortedError, KeyboardInterrupt):
				print("[+] Lost Connection to Server")
				self.gameActive = False
				self.sock.close()
		else:
			print("Game no longer active")

	def MoveTowards(self, coords):
		x = 0
		y = 0
		if (self.x > coords[0]): x = -1
		elif (self.x < coords[0]): x = 1
		if (self.y > coords[1]): y = -1
		elif (self.y < coords[1]): y = 1
		self.Move(x, y)

	def CalculateDistance(self, tuplea, tupleb):
		xdiff = tuplea[0] - tupleb[0]
		ydiff = tuplea[1] - tupleb[1]
		xdiff = math.pow(xdiff, 2)
		ydiff = math.pow(ydiff, 2)
		diff = xdiff + ydiff
		result = math.sqrt(diff)
		return result