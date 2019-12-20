from pygame.locals import *
import socket
import threading
import time
import math
import json
import pygame
import weakref
import gc
from random import randrange


class Server:
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 800))
    done = False
    clock = pygame.time.Clock()
    val = 0

    shipIdList = []
    craterList = []
    bombList = []
    ShipList = weakref.WeakValueDictionary()

    bind_ip = '0.0.0.0'
    bind_port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    myfont = pygame.font.SysFont('Arial MS', 16)
    max_users = 5
    user_count = 0


    # Visual Settings...
    showRanges = True
    showFlag = True
    showCoords = True
    showName = True
    showDistance = True
    showScore = True


    def remember(self, obj):
        oid = id(obj)
        self.ShipList[oid] = obj
        return oid

    def RecallShip(self, oid):
        for obj in gc.get_objects():
            if id(obj) == oid:
                return obj

    def Start(self):
        network_handler = threading.Thread(target=self.StartListener)
        print("[+] Starting Network Handler...")
        network_handler.start()
        print("[+] Starting GUI Handler...")
        self.StartGUI()

            
    def StartListener(self):
        print('[+] Listening on ' + str(self.bind_ip) + ":" + str(self.bind_port))
        while True:
            client_sock, address = self.server.accept()
            if (self.user_count < self.max_users):
                print('[+] Accepted connection from {}:{}'.format(address[0], address[1]))
                client_handler = threading.Thread(
                    target=self.newPlayer,
                    args=(client_sock,) 
                )
                client_handler.start()
            else:
                print("[+] Dropped connection from {}:{} due to max user capacity".format(address[0], address[1]))
                self.Send(client_sock, "Cannot Accept Connection : Reason : Server is at maximum capacity!")
                self.Send(client_sock, "")
                client_sock.close()
            print(str(self.user_count))

    def StartGUI(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.screen.fill((0, 0, 0))

            # Draw the bombs...
            for bomb in self.bombList:
                if not (bomb.lifetime <= 0):
                    pygame.draw.circle(self.screen, bomb.color, (bomb.x, bomb.y), int(bomb.size))
                    bomb.Tick()

                    for shipid in self.shipIdList: # check if there are any ships in the bomb radius and inflict damange on them
                        ship = self.RecallShip(shipid)
                        distance = self.CalculateDistance((ship.x, ship.y), (bomb.x, bomb.y))
                        if ((distance <= bomb.size) & (distance >= 5)):
                            ship.GetHit(bomb.shooter, 2.5)
                else:
                    self.bombList.remove(bomb)

            # Draw the elements...
            for shipid in self.shipIdList:
                ship = self.RecallShip(shipid)
                # Draw the ships...
                pygame.draw.rect(
                    self.screen, ship.color,
                    pygame.Rect(ship.x - 3, ship.y - 3, 6, 6)
                )

                textsurface = self.myfont.render(ship.status, True, (156, 0, 3))
                self.screen.blit(textsurface, (ship.x, ship.y + 45))

                if self.showRanges:
                    # Draw the ranges...
                    pygame.draw.circle(self.screen, (50, 0, 0), (ship.x, ship.y), 100, 1)
                    pygame.draw.circle(self.screen, (0, 0, 50), (ship.x, ship.y), 200, 1)
                
                if self.showName:
                    # Draw the ship names...
                    textsurface = self.myfont.render(ship.name, True, (0, 156, 3))
                    self.screen.blit(textsurface, (ship.x, ship.y + 9))
                
                if self.showFlag:
                    # Draw ship flags...
                    textsurface = self.myfont.render(ship.flag, True, (0, 156, 3))
                    self.screen.blit(textsurface, (ship.x, ship.y + 18))
                
                if self.showCoords:
                    # Draw the ship co-ordinates...
                    textsurface = self.myfont.render(str(ship.x) + ":" + str(ship.y), True, (0, 156, 3))
                    self.screen.blit(textsurface, (ship.x, ship.y + 27))

                if self.showScore:
                    # Draw the ship score...
                    textsurface = self.myfont.render(str(ship.score), True, (0, 156, 3))
                    self.screen.blit(textsurface, (ship.x, ship.y + 36))

                if self.showDistance:
                    # Draw a line between the ships...
                    for nearby_ships_id in self.shipIdList:
                        if (shipid != nearby_ships_id):
                            nearby_ship = self.RecallShip(nearby_ships_id)
                            distance = self.CalculateDistance((nearby_ship.x, nearby_ship.y), (ship.x, ship.y))
                            if (distance < 200):
                                # g_color = 255 * ((200 - distance) / 200)
                                pygame.draw.line(self.screen, (0, 100, 0), (ship.x, ship.y), (nearby_ship.x, nearby_ship.y), 1)
                                # midpoint = ((ship.x + nearby_ship.x) / 2 + 18, (ship.y + nearby_ship.y) / 2 + 18)
                                # textsurface = self.myfont.render(str(distance), True, (0, 156, 3))
                                # self.screen.blit(textsurface, (midpoint))
                
            # Draw the shots...
            for crater in self.craterList:
                # check if the crater is expired or not...
                if not (crater.lifetime <= 0):
                    pygame.draw.circle(self.screen, crater.color, (crater.x, crater.y), int(crater.size))
                    crater.Tick()
                else: # if it is expired, remove it from the list...
                    self.craterList.remove(crater)

            pygame.display.flip()
            self.clock.tick(30)



    def newPlayer(self, client_socket): # add a new ship to the system...
        currentShip = Ships.BattleShip("???")
        newshipid = id(currentShip)
        self.user_count += 1
        self.remember(currentShip)
        self.shipIdList.append(newshipid)
        self.handle_client_connection(client_socket, newshipid)
        


    def SendRadarData(self, client_socket, ship_id): # send the radar information to the client
        while True:
            try:
                Message = self.generateReport(ship_id)
                self.Send(client_socket, Message)
                time.sleep(0.25)
            except:
                break

    
    def generateReport(self, ship_id): # generate a json report so SendRadarData() can send it to the client...
        ship = self.RecallShip(ship_id)
        template = {"ships" : []}
        # add local ship first...
        template["ships"].append({
            'x' : ship.x,
            'y' : ship.y,
            'flag' : ship.flag,
            'health' : ship.health
        })

        for ship_par_id in self.shipIdList:
            ship_par = self.RecallShip(ship_par_id)
            if not (ship_par is ship):
                if (self.CalculateDistance((ship_par.x, ship_par.y), (ship.x, ship.y)) <= 200):
                    template["ships"].append({
                        'x' : ship_par.x,
                        'y' : ship_par.y,
                        'flag' : ship_par.flag,
                        'health' : ship_par.health
                    })

        return json.dumps(template)
                
    def Send(self, insock, Command): # send the message...
        Command = Command.ljust(500, " ") # fill up the message with white space to make sure it is 500 bytes...
        insock.sendall(Command.encode('utf-8')) # encode and send it...


    def RemovePlayer(self, shipid):
        self.user_count -= 1
        self.shipIdList.remove(shipid)
        

    def handle_client_connection(self, client_socket, ship_id):
        ship = self.RecallShip(ship_id)
        locked = True
        RadarThread = threading.Thread(target=self.SendRadarData, args=[client_socket, ship_id])
        RadarThread.start() # this is a new client... so create and start a thread for radar...
        while locked:
            try:
                manifest = client_socket.recv(2048)
            except:
                self.RemovePlayer(ship_id)
                print("[+] Player " + str(ship_id) + " has disconnected...")
                locked = False
                break
            # if (not manifest):
            #     locked = False

            manifest = manifest.decode("utf-8")
            try:
                manifest = json.loads(manifest)
            except:
                manifest = {"actions" : []}

            # print(manifest)

            cannon_limit = ship.cannon_count
            move_limit = ship.movement_count

            for request in manifest["actions"]:                
                command = request["Action"]

                if (command == "MOVE"):
                    if (move_limit != 0):
                        movementx = int(request["x"])
                        movementy = int(request["y"])
                        ship.Move(movementx, movementy)
                        move_limit -= 1

                if (command == "INIT"):
                    ship.name = request["shipname"]

                if (command == "FIRE"):
                    if not ship.locked:
                        if ((self.CalculateDistance(
                            (int(request["x"]), int (request["y"])),
                            (ship.x, ship.y))
                            ) < 100):
                            if (cannon_limit != 0):
                                self.checkBlastingRadius(ship_id, int(request["x"]), int(request["y"]))
                                self.craterList.append(Weapons.Shot(ship, int(request["x"]), int(request["y"])))
                                cannon_limit -= 1

                if (command == "DESTRUCT"):
                    if not (ship.locked):
                        ship.status = "Arming Bomb"
                        time.sleep(5)
                        if not (ship.locked):
                            self.bombList.append(Weapons.Bomb(ship, ship.x, ship.y))
                            ship.Destruct()

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




class Ships:
    class BattleShip:
        x = 0
        y = 0
        health = 100
        endurace = 12
        color = (0, 255, 0)
        score = 0
        firepower = 10
        cannon_count = 2
        movement_count = 1
        lock_elapsed = 0
        lock_duration = 10
        locked = False

        status = ""
        flag = "0"
        name = ""



        def Repairs(self):
            while self.lock_elapsed != 0:
                percent = ((self.lock_duration - self.lock_elapsed) / self.lock_duration) * 100
                self.status = "Repairing - " + str(percent) + "%"
                self.lock_elapsed -= 1
                time.sleep(1)
            self.status = ""
            self.locked = False

        def __init__(self, name):
            self.name = name
            self.x = randrange(0, 800)
            self.y = randrange(0, 800)
            self.flag = str(randrange(1000, 9999))
            healthCheckThread = threading.Thread(target=self.CheckHealth)
            healthCheckThread.start()

        def Destruct(self):
            self.health -= 75
            if self.health < 0: self.health = 0
            self.CheckHealth()
            self.UpdateColor()
            self.lock_elapsed = self.lock_duration
            self.locked = True
            repairThread = threading.Thread(target=self.Repairs)
            repairThread.start()

        def CheckHealth(self):
            if self.health <= 0: self.Reset()

        def UpdateColor(self):
            red = (255 * ((100 - self.health) / 100))
            green = ((255 * (self.health / 100)))
            if (green < 0): green = 0
            if (red > 255): red = 255
            self.color = (red, green, 0)

        def Move(self, movex, movey):
            if not self.locked:
                # set the x movement
                if (movex > 4):
                    self.x += 4
                else:
                    self.x += movex
                
                # set the y movement
                if (movey > 4):
                    self.y += 4
                else:
                    self.y += movey

        def GetHit(self, hitter, firepower):
            if (self.health <= 0):
                self.Reset()
            else:
                damage_rate = firepower - (firepower * (self.endurace / 100))
                self.health -= damage_rate
                hitter.score += 1
                self.score -= 1
                if self.health < 0:
                    self.health = 0
                self.UpdateColor()

                
        def Reset(self):
            self.health = 100
            self.x = randrange(0, 800)
            self.y = randrange(0, 800)
            self.color = (0, 255, 0)

class Weapons:
    class Shot:
        x = 0
        y = 0
        lifetime = 100
        size = 3
        decay = 5
        color = (255, 0, 0)
        shooter = ""

        def __init__(self, shooter, x, y):
            self.shooter = shooter
            self.x = x
            self.y = y

        def Tick(self):
            self.color = ((255 * (self.lifetime / 100)), 0, 0)
            self.size = (self.size * (self.lifetime / 100))
            self.lifetime -= self.decay

    class Bomb:
        x = 0
        y = 0
        lifetime = 100
        size = 126
        decay = 1
        color = (255, 0, 0)
        shooter = ""

        def __init__ (self, shooter, x, y):
            self.x = x
            self.y = y
            self.shooter = shooter

        def Tick(self):
            self.color = ((155 * (self.lifetime / 100)), 0, 0)
            self.size = (126 - (self.size * (self.lifetime / 100)))
            self.lifetime -= self.decay
