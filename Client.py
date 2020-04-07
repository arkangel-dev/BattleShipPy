import random
import BattleShipPyClient

ship = BattleShipPyClient.Client("Arkangel-" + str(random.randrange(100,999)), "S"+str(random.randrange(100,999)) ,"localhost", 9999)
ship.Connect()

while ship.gameActive:
	
	ship.MoveTowards((400, 400))
	if (len(ship.ShipList) > 1):
		ship.Fire(ship.ShipList[1]["x"], ship.ShipList[1]["y"]) 


	# ship.SelfDestruct()

	if (ship.CalculateDistance((ship.x, ship.y), (400, 400)) <= 50):
		if (len(ship.ShipList) > 1):
			if (ship.CalculateDistance((ship.x, ship.y), (ship.ShipList[1]["x"], ship.ShipList[1]["y"])) <= 130):
				ship.SelfDestruct()
	

	# if not Fired:
	# ship.Fire(ship.x + random.randrange(-50, 50), ship.y + random.randrange(-50, 50)) # fire at random points within the firing range
	ship.CommitActions()
	# ship.UpdateWindow()


