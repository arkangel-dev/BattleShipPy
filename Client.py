import random
import BattleShipPyClient
import supplement_functions as sf

ship = BattleShipPyClient.Client("Arkangel-" + str(random.randrange(100,999)), "localhost", 9999)
ship.Connect()
ship.StartRadar()

while 1:
    # ship.Fire(ship.x + random.randrange(-50, 50), ship.y + random.randrange(-50, 50)) # fire at random points within the firing range
    # ship.Fire(ship.x + random.randrange(-50, 50), ship.y + random.randrange(-50, 50))
    # print("Firing at : " + str(ship.x) + ":" + str(ship.y))
    # ship.Fire(ship.x, ship.y)
    # ship.Move(1, -1)
    # ship.Send("INIT Arkangel " + str(random.randrange(1000,)))
    # print("Coordiantes : " + str(ship.x) + ":" + str(ship.y))

    ship.MoveTowards((400, 400))
    if (len(ship.ShipList) > 1):
        ship.Fire(ship.ShipList[1]["x"], ship.ShipList[1]["y"]) 

    # ship.SelfDestruct()

    if (sf.CalculateDistance((ship.x, ship.y), (400, 400)) <= 50):
        if (len(ship.ShipList) > 1):
            if (sf.CalculateDistance((ship.x, ship.y), (ship.ShipList[1]["x"], ship.ShipList[1]["y"])) <= 130):
                ship.SelfDestruct()
    ship.CommitActions()


