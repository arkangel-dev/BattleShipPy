# Java Client for BattleShipPy

## `JaBattleShip.java`

### `ClearCommandCache()`

The Java client like its Python counterpart has a JSON list that contains all the commands that was called, and once the `Commit()` method is called, the list is sent to the server and the server executes all those commands. The command list is structured like below:

```json
{
    "actions" : []
}
```

### `Init()`

This command is called when the client first connects to the server. This method will add a new command to the command list. The command then will be used by the server to name the client, and maybe in a future update, define the type of ship it is. The command will be a JSON element structures like this :

```json
{
    "Action":"INIT",
    "shipname":"Arkangel"
}
```

### Move()

Will move the ship. The ship can only move 1 or 2 units on any axis at any time. You can call this method only once per commit. Will generate the following JSON if `Client.Move(2, 2)` is called:

```json
{
    "Action":"MOVE",
    "x":"2",
    "y":"2"
}
```



### `Fire()`

Fires the cannon at a specified co-ordinate. This method will also create a JSON element and append it to the command list JSON array. You can call this method twice per commit. The JSON element that was created to fire at `(5,5)` will look like this.

```json
{
    "Action":"FIRE",
    "x":"5",
    "y":"5"
}
```

### `Destruct()`

Detonates a bomb that will damage all ships in a 126 unit radius. The blast will damage your ship, but not as much as the nearby ships in the blast radius. The blast will deduct 75 from your ships health, which will render your ship unable to move and only able to fire at a limited range.  You can call this method once per commit. This command will also create a JSON object and append it to the command list. The JSON element will look like this :

```json
{
    "Action":"DESTRUCT"
}
```

### `UpdateTelemetry()`

This command will read the telemetry data from the TCP connection to the server by calling the `ReadData()` method, deserialize the data, and save it in the private variable `ShipList`. Note that in the current version you have to constantly call this method to keep the telemetry updated..The telemetry data will be structured like below

```json
{
    "ships": [
        {"x": 591, "y": 666, "flag": "4274", "health": 100}
    ]
}
```

### `ReadData()`

Reads the data from the TCP connection to the server and return it as a string. 

### `Commit()`

This command will send all pending commands to server and the server will execute them. You have to call this method after calling any other method. For example a the following code will generate the following command list:

```java
JaBattleship Client = new JaBattleship("Ark", "127.0.0.1", 9999); 
Client.Move(1,1);
Client.SelfDestruct();
```

```json
{
    "actions" : [
        {"Action":"INIT", "shipname":"Arkangel"},
        {"Action":"MOVE", "x":"2", "y":"2"},
        {"Action":"DESTRUCT"}
    ]
}
```

None of these commands will be run on the server. Not until you call the `commit()` method.

### `Me`

Me is an instance of the class `Ship`. This instance will contain the telemetry data of your ship. The `List<Ship>` instance that is returned by the method `GetShipList()` also has the telemetry data for your ships as well. Its always contained in the fist position of the list object.