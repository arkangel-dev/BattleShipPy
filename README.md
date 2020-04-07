# BattleShipPy
This is a recreation of the Battle Ship game made by UWE written in python. I wrote this because the UWE version had limited control over how the server behaved, like speed of the server, spawning points, etc. Also, the client was written in C, so that was a nightmare to send string messages.

## Prerequisites
Pygame : `pip install pygame`


## Usage
### Start Server:
```python
import BattleShipPy
environment = BattleShipPy.Server(
	dropConnectionOnBadRequest=True,
	enableColorDebug=True,
	maxPlayerCount=4
)
environment.Start()
```

### Connect Clients
### `Python`
Note : Each instruction for the ship to behave in the `BattleBotClient` class, only adds that instruction to a list an only by calling `CommitActions` method, will the client send the instruction list to the server, where they are executed.

```python
import random
import BattleShipPyClient

ship = BattleShipPyClient.Client("Arkangel-" + str(random.randrange(100,999)), "S23", localhost", 9999)
ship.Connect()

while ship.gameActive:
	
	ship.MoveTowards((400, 400))
	if (len(ship.ShipList) > 1):
		ship.Fire(ship.ShipList[1]["x"], ship.ShipList[1]["y"]) 

	if (ship.CalculateDistance((ship.x, ship.y), (400, 400)) <= 50):
				ship.SelfDestruct()
	ship.CommitActions()
```

### `Java`

The java  client has more or less the same functionality as the its python counterpart. The radar thread on the Java client also now runs on its own thread.

```java
package battleship;

public class App {
    public static void main(String[] args) throws Exception {
		JaBattleship Client = new JaBattleship("Ark", "SEC435389", "127.0.0.1", 9999);
		while (true) {
			Client.MoveTowards(400, 400);
			Client.Commit();
		}
    }
}
```




## Advantages BattleShipPy Has Over The Old UWE version
- Its written in Python
- Its Open-Source
- Its supports multiples instances of the same instruction per tick
- Doesn't require the client to listen for a connection
- Ships have self-destruct methods
- Displays visible ranges and firing ranges
- Displays ship co-ordinates
- Displays ship flags
- Displays which ships are visible to each other
- Displays the distances between each ship