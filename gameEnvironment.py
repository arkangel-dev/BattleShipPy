import socket
import threading
import io
import time
import math
import json
import pygame
import shipDefinitions
import weakref

class BattleEnvironment:
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 800))
    done = False
    clock = pygame.time.Clock()
    val = 0

    shipIdList = []
    craterList = []
    ShipList = weakref.WeakValueDictionary()

    bind_ip = '0.0.0.0'
    bind_port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    myfont = pygame.font.SysFont('Arial MS', 16)


    def remember(self, obj):
        oid = id(obj)
        self.ShipList[oid] = obj
        return oid

    def RecallShip(self, oid):
        return self.ShipList[oid]

    def StartEnvironment(self):
            network_handler = threading.Thread(target=self.StartListener)
            print("[+] Starting Network Handler...")
            network_handler.start()
            print("[+] Starting GUI Handler...")
            self.StartGUI()

            
    def StartListener(self):
        print('[+] Listening on ' + str(self.bind_ip) + ":" + str(self.bind_port))
        while True:
            client_sock, address = self.server.accept()
            print('[+] Accepted connection from {}:{}'.format(address[0], address[1]))
            client_handler = threading.Thread(
                target=self.newPlayer,
                args=(client_sock,) 
            )
            client_handler.start()

    def StartGUI(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.screen.fill((0, 0, 0))
            # Draw the elements...
            for shipid in self.shipIdList:
                ship = self.RecallShip(shipid)
                # Draw the ships...
                pygame.draw.rect(
                    self.screen, ship.color,
                    pygame.Rect(ship.x - 3, ship.y - 3, 6, 6)
                )
                # Draw the ranges...
                pygame.draw.circle(self.screen, (50, 0, 0), (ship.x, ship.y), 100, 1)
                pygame.draw.circle(self.screen, (0, 0, 50), (ship.x, ship.y), 200, 1)
                # Draw the ship names...
                textsurface = self.myfont.render(ship.name, True, (0, 156, 3))
                self.screen.blit(textsurface, (ship.x, ship.y + 9))
                # Draw ship flags...
                textsurface = self.myfont.render(ship.flag, True, (0, 156, 3))
                self.screen.blit(textsurface, (ship.x + 18, ship.y + 18))
                # Draw the ship co-ordinates...
                textsurface = self.myfont.render(str(ship.x) + ":" + str(ship.y), True, (0, 156, 3))
                self.screen.blit(textsurface, (ship.x - 18, ship.y - 18))
                
            # Draw the shots...
            for crater in self.craterList:
                # check if the crater is expired or not...
                if not (crater.lifetime <= 0):
                    pygame.draw.circle(self.screen, crater.color, (crater.x, crater.y), int(crater.size))
                    crater.Tick()
                else: # if it is expired, remove it from the list...
                    self.craterList.remove(crater)

            # print(self.shipIdList)

            pygame.display.flip()
            self.clock.tick(60)



    def newPlayer(self, client_socket): # add a new ship to the system...
        currentShip = shipDefinitions.BattleShip("???")
        newshipid = id(currentShip)
        print("[+] Generating Ship : " + str(newshipid))
        self.remember(currentShip)
        self.shipIdList.append(newshipid)
        self.handle_client_connection(client_socket, newshipid)


    def SendRadarData(self, client_socket, ship_id): # send the radar information to the client
        while True:
            Message = self.generateReport(ship_id)
            self.Send(client_socket, Message)
            time.sleep(0.5)

    
    def generateReport(self, ship_id): # generate a json report so SendRadarData() can send it to the client...
        ship = self.RecallShip(ship_id)

        template = {"ships" : []}
        shiptemplate = {"x" : "null", "y" : "null", "health" : "null", "flag" : "null"}

        # add local ship first...
        shiptemplate["x"] = ship.x
        shiptemplate["y"] = ship.y
        shiptemplate["health"] = ship.health
        shiptemplate["flag"] = ship.flag
        template["ships"].append(shiptemplate)

        for ship_par_id in self.shipIdList:
            ship_par = self.RecallShip(ship_par_id)
            if (ship_par.flag != ship.flag):
                shiptemplate["x"] = ship_par.x
                shiptemplate["y"] = ship_par.y
                shiptemplate["health"] = ship_par.health
                shiptemplate["flag"] = ship_par.flag
                template["ships"].append(shiptemplate)

        return json.dumps(template)
                
    def Send(self, socket, Command): # send the message...
        Command = Command.ljust(500, " ") # fill up the message with white space to make sure it is 500 bytes...
        socket.sendall(Command.encode('utf-8')) # encode and send it...


    def handle_client_connection(self, client_socket, ship_id):
        ship = self.RecallShip(ship_id)
        locked = True
        RadarThread = threading.Thread(target=self.SendRadarData, args=[client_socket, ship_id])
        RadarThread.start() # this is a new client... so create and start a thread for radar...
        while locked:
            request = client_socket.recv(100)
            if (not request):
                locked = False

            request = request.decode("utf-8")
            request_parts = request.split(" ")
            command = request_parts[0]

            if (command == "MOVE"):
                movementx = int(request_parts[1])
                movementy = int(request_parts[2])
                ship.Move(movementx, movementy)

            if (command == "INIT"):
                ship.name = request_parts[1]

            if (command == "FIRE"):
                if ((self.CalculateDistance(
                    (int(request_parts[1]), int (request_parts[2])),
                    (ship.x, ship.y))
                    ) < 100):
                    self.checkBlastingRadius(ship_id, int(request_parts[1]), int(request_parts[2]))
                    self.craterList.append(shipDefinitions.Shot(ship, int(request_parts[1]), int(request_parts[2])))
                else:
                    print("Invalid Range")

            if (command == "QUIT"):
                locked = False

            time.sleep(0.25)
        client_socket.close()

    def checkBlastingRadius(self, ship_id, x, y):
        ship = self.RecallShip(ship_id)
        for test_ship_id in self.shipIdList:
            test_ship = self.RecallShip(test_ship_id)
            if ((test_ship.x == x) & (test_ship.y == y)):
                test_ship.GetHit(ship, ship.firepower)
                ship.score += 1
                

    def CalculateDistance(self, tuplea, tupleb):
        xdiff = tuplea[0] - tupleb[0]
        ydiff = tuplea[1] - tupleb[1]
        xdiff = xdiff * xdiff
        ydiff = ydiff * ydiff
        diff = xdiff + ydiff
        result = math.sqrt(diff)
        return result
