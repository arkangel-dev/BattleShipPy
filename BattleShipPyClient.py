import socket
import threading
import json 
import time
import pygame

class Client:
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

    showWindow = False
    windowObejct = ""
    done = False

    def __init__ (self, client_name, server, port):
        self.server = server
        self.port = port
        self.client_name = client_name
        self.server_address = (self.server, self.port)


    clock = None
    screen = None

    def UpdateWindow(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                break

        self.screen.fill((0, 0, 0))



        pygame.draw.rect(
            self.screen, (0, 255, 0),
            pygame.Rect(self.x - 3, self.y - 3, 6, 6)
        )

        skip = False
        for ship in self.ShipList:
            if (skip):
                pygame.draw.rect(
                    self.screen, (255, 0, 0),
                    pygame.Rect(ship["x"] - 3, ship["y"] - 3, 6, 6)
                )
            else:
                skip = True


        pygame.display.flip()
        self.clock.tick(60)


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
        connthread = threading.Thread(target=self.CommitConnection())
        connthread.start()

        if (self.showWindow):
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((800, 800))

    def CommitConnection(self):
        self.sock.connect(self.server_address)
        Command = {
            "Action" : "INIT",
            "shipname" : self.client_name
        }
        self.action_list["actions"].append(Command)
        self.CommitActions()

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

    def MoveTowards(self, coords):
        x = 0
        y = 0
        if (self.x > coords[0]):
            x = -1
        elif (self.x < coords[0]):
            x = 1
        if (self.y > coords[1]):
            y = -1
        elif (self.y < coords[1]):
            y = 1
        self.Move(x, y)