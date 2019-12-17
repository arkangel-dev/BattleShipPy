from random import randrange
import time
import threading

class BattleShip:
    x = 0
    y = 0
    health = 100
    flag = "0"
    name = ""
    endurace = 12
    color = (0, 255, 0)
    score = 0
    firepower = 10

    cannon_count = 2
    movement_count = 1

    status = ""

    locked = False
    lock_elapsed = 0
    lock_duration = 10

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
        if self.health < 0:
            self.health = 0
        self.CheckHealth()
        self.UpdateColor()
        self.lock_elapsed = self.lock_duration
        self.locked = True
        repairThread = threading.Thread(target=self.Repairs)
        repairThread.start()

    def CheckHealth(self):
        if self.health <= 0:
            self.Reset()

    def UpdateColor(self):
        red = (255 * ((100 - self.health) / 100))
        green = ((255 * (self.health / 100)))

        if (green < 0):
            green = 0
        
        if (red > 255):
            red = 255


        self.color = (
            red,
            green,
            0
            )

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
            if self.health < 0:
                self.health = 0
            self.UpdateColor()

            
    def Reset(self):
        self.health = 100
        self.x = randrange(0, 800)
        self.y = randrange(0, 800)
        self.color = (0, 255, 0)

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