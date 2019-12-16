import ClientLib
import time
import random

ship = ClientLib.BattleBotClient("Arkangel-" + str(random.randrange(100,999)), "localhost", 9999)
ship.Connect()
ship.StartRadar()

while 1:
    ship.Fire(ship.x + random.randrange(-50, 50), ship.y + random.randrange(-50, 50)) # fire at random points within the firing range
    # print("Firing at : " + str(ship.x) + ":" + str(ship.y))
    # ship.Fire(ship.x, ship.y)
    # ship.Move(1, -1)
    # ship.Send("INIT Arkangel " + str(random.randrange(1000,)))
