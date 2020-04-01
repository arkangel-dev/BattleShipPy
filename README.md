# BattleShipPy
This is a recreation of the Battle Ship game made by UWE written in python. I wrote this because the UWE version had limited control over how the server behaved, like speed of the server, spawning points, etc. Also, the client was written in C, so that was a nightmare to send string messages.

## Prerequisites
Pygame : `pip install pygame`


## Usage
### Start Server:
```python
import gameEnvironment
environment = gameEnvironment.BattleEnvironment()
environment.StartEnvironment()
```

### Connect Clients
### `Python`
Note : Each instruction for the ship to behave in the `BattleBotClient` class, only adds that instruction to a list an only by calling `CommitActions` method, will the client send the instruction list to the server, where they are executed.

```python
import random
import BattleShipPyClient

ship = BattleShipPyClient.Client("Arkangel", "localhost", 9999) # Define the connection
ship.Connect() # Connect
ship.StartRadar() # Start the 'radar' thread

while 1:
    ship.Move(1, 2) # Move 1 units to the right and 2 units down
    ship.Fire(4, 4) # Fire the co-ordiantes (4, 4)
    ship.SelfDestruct() # Detonate self destruct
    ship.CommitActions() # Send the actions to the server. This is required for the server to execute the previous actions
```

### `Java`

The java  client has more or less the same functionality as the its python counterpart. The only main difference is that the Java client runs on a single thread. But that will be soon updated to run multi-threaded as Python.

```java
package battleship;

public class App {
    public static void main(String[] args) throws Exception {
		
		JaBattleship Server = new JaBattleship(
			"Ark",
			"127.0.0.1",
			 9999
		); // Define the connection

		while (true) {
			Server.UpdateTelemetry(); // Update the telemetry
			Server.Move(1, 1); // Move the ship
			Server.Commit(); // Commit to the appended commands
			Thread.sleep(250); // Sleep

			System.out.println(
				"X : " + Server.Me.x +
				" | y : " + Server.Me.y
			); // Print the current position
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