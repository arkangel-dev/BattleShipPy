import BattleShipPy
environment = BattleShipPy.Server(
	dropConnectionOnBadRequest=True,
	enableColorDebug=True,
	maxPlayerCount=4
)
environment.Start()