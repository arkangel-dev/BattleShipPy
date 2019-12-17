import socket
import threading
import time
import json

class BattleBotClient:
    client_name = ""
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

    def __init__ (self, client_name, server, port):
        self.server = server
        self.port = port
        self.client_name = client_name
        self.server_address = (self.server, self.port)

    def StartRadar(self):
        radarThread = threading.Thread(target=self.RadarProcess)
        radarThread.start()

    def RadarProcess(self):
        while True:
            data = self.sock.recv(500)
            self.ProcessRadarData(data)

    def ProcessRadarData(self, data):
        jsonObj = data.decode('utf-8')
        jsonObj = json.loads(jsonObj)

        # print(jsonObj)

        self.ShipList.clear()
        self.ShipList = jsonObj["ships"]

        self.x = jsonObj["ships"][0]["x"]
        self.y = jsonObj["ships"][0]["y"]
        self.health = jsonObj["ships"][0]["health"]
        self.flag = jsonObj["ships"][0]["flag"]

    def Connect(self):
        self.sock.connect(self.server_address)
        Command = {
            "Action" : "INIT",
            "shipname" : self.client_name
        }
        self.action_list["actions"].append(Command)

    def Move(self, x, y):
        # Command = "MOVE " + str(x) + " " + str(y)
        Command = {
            "Action" : "MOVE",
            "x" : str(x),
            "y" : str(y)
        }
        self.action_list["actions"].append(Command)

    def Fire(self, x, y):
        # Command = "FIRE " + str(x) + " " + str(y)
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
        Data = json.dumps(self.action_list)
        Data = Data.ljust(50)
        self.sock.sendall(Data.encode('utf-8'))
        time.sleep(0.25)
        self.action_list["actions"].clear()

    