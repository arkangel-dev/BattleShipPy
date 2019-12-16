from random import randrange

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

    def __init__(self, name):
        self.name = name
        self.x = randrange(0, 800)
        self.y = randrange(0, 800)
        self.flag = str(randrange(1000, 9999))

    def Move(self, movex, movey):
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

            red = (255 * ((100 - self.health) / 100))
            green = ((255 * (self.health / 100)))

            if (green < 0):
                green = 0
            
            if (red > 255):
                red = 255

            if self.health < 0:
                self.health = 0

            self.color = (
                red,
                green,
                0
                )
            hitter.score += 1

            
    def Reset(self):
        self.health = 100
        self.x = randrange(0, 800)
        self.y = randrange(0, 800)
        color = (0, 255, 0)

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