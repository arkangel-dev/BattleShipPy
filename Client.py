import time
import random
import math
import ClientLib

ship = ClientLib.BattleBotClient("Arkangel-" + str(random.randrange(100,999)), "localhost", 9999)
ship.Connect()
ship.StartRadar()

def MoveTowards(coords):
    x = 0
    y = 0
    if (ship.x > coords[0]):
        x = -1
    elif (ship.x < coords[0]):
        x = 1

    if (ship.y > coords[1]):
        y = -1
    elif (ship.y < coords[1]):
        y = 1

    ship.Move(x, y)

def CalculateDistance(tuplea, tupleb):
    xdiff = tuplea[0] - tupleb[0]
    ydiff = tuplea[1] - tupleb[1]
    xdiff = xdiff * xdiff
    ydiff = ydiff * ydiff
    diff = xdiff + ydiff
    result = math.sqrt(diff)
    return result

while 1:
    # ship.Fire(ship.x + random.randrange(-50, 50), ship.y + random.randrange(-50, 50)) # fire at random points within the firing range
    # ship.Fire(ship.x + random.randrange(-50, 50), ship.y + random.randrange(-50, 50))
    # print("Firing at : " + str(ship.x) + ":" + str(ship.y))
    # ship.Fire(ship.x, ship.y)
    # ship.Move(1, -1)
    # ship.Send("INIT Arkangel " + str(random.randrange(1000,)))
    # print("Coordiantes : " + str(ship.x) + ":" + str(ship.y))

    MoveTowards((400, 400))
    if (len(ship.ShipList) > 1):
        ship.Fire(ship.ShipList[1]["x"], ship.ShipList[1]["y"]) 

    # ship.SelfDestruct()


    if (CalculateDistance((ship.x, ship.y), (400, 400)) <= 50):
        if (len(ship.ShipList) > 1):
            if (CalculateDistance((ship.x, ship.y), (ship.ShipList[1]["x"], ship.ShipList[1]["y"])) <= 130):
                ship.SelfDestruct()
    ship.CommitActions()


