package battleship;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.reflect.Type;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;

public class JaBattleship {
	public String client_name = "";
	public String ServerHost = "";
	public int ServerPort = 0;

	private Socket socket;
	private PrintWriter outgoing;
	private BufferedReader incoming;

	public Ship Me = new Ship(0, 0, 0, 0, 0);
	public JsonObject ActionList = new JsonObject();
	public List<Ship> ShipList;

	/**
	 * Clears the command cache
	 */
	public void ClearCommandCache() {
		ActionList = new JsonObject();
		ActionList.add("actions", new JsonArray());
	}

	public class Ship {
		public int x = 0;
		public int y = 0;
		public int score = 0;
		public int flag = 0;
		public int health = 0;

		public Ship(int x, int y, int score, int flag, int health) {
			this.x = x;
			this.y = y;
			this.score = score;
			this.flag = flag;
			this.health = health;
		}

		private double calculate_distance(int ax, int ay, int bx, int by){
			return Math.sqrt(
				Math.pow((bx-ax), 2) + 
				Math.pow((by-ay), 2)
			);
		}

		/**
		 * Calculate this ships distance from the co-ordinates passwed
		 * @param x 
		 * @param y
		 * @return
		 */
		public double CalculateDistanceFrom(int x, int y) {
			return calculate_distance(
				this.x, 
				this.y, 
				x, 
				y
			);
		}
	}

	/**
	 * Initilizes the client
	 */
	private void Init() {
		JsonObject moveCommand = new JsonObject();
		moveCommand.addProperty("Action", "INIT");
		moveCommand.addProperty("shipname", client_name);
		ActionList.get("actions").getAsJsonArray().add(moveCommand);
	}

	/**
	 * Constructor for the JaBattleship class
	 * 
	 * @param ShipName Name of the players ship
	 * @param Hostname Hostname of the hosting server
	 * @param Port     Port of the hosting server
	 * @throws UnknownHostException
	 * @throws IOException
	 */
	public JaBattleship(String ShipName, String Hostname, int Port) throws UnknownHostException, IOException {
		ServerHost = Hostname;
		ServerPort = Port;
		client_name = ShipName;
		socket = new Socket(Hostname, Port);
		outgoing = new PrintWriter(socket.getOutputStream(), true);
		incoming = new BufferedReader(new InputStreamReader(socket.getInputStream()));
		
		ClearCommandCache(); // initilize the CommandCache
		Init();
		Commit(); // Send the initilization command to the server
	}

	/**
	 * Reads data from the connection
	 */
	private String ReadData() {
		char[] buff = new char[500];
		try {
			incoming.read(buff, 0, 500);
		} catch (IOException e) {
			e.printStackTrace();
		}
		String content = String.valueOf(buff);
		return content;
	}

	/**
	 * Updates the client telemetry data. Call this function every iteration to make sure that all
	 * telemetry data stays up-to-date
	 */
	public void UpdateTelemetry() {
		JsonElement jsonTree = new JsonParser()
			.parse(ReadData())
			.getAsJsonObject();
		Type listType = new TypeToken<List<Ship>>(){}.getType();
		ShipList = new Gson()
			.fromJson(
				jsonTree.getAsJsonObject()
				.get("ships"),
				listType
			);
		this.Me = ShipList.get(0);
		
	}

	/**
	 * Moves the ship in a step-like fashion in the x and y axis
	 * @param x Defines how many steps to move in the x axis
	 * @param y Defines how many steps to move in the y axis
	 */
	public void Move(int x, int y){
		JsonObject moveCommand = new JsonObject();
		moveCommand.addProperty("Action", "MOVE");
		moveCommand.addProperty("x", Integer.toString(x));
		moveCommand.addProperty("y", Integer.toString(y));
		ActionList.get("actions")
			.getAsJsonArray()
			.add(moveCommand);		
	}

	/**
	 * Fires the canons at the passed co-ordinates
	 * @param x
	 * @param y
	 */
	public void Fire(int x, int y){
		JsonObject moveCommand = new JsonObject();
		moveCommand.addProperty("Action", "FIRE");
		moveCommand.addProperty("x", Integer.toString(x));
		moveCommand.addProperty("y", Integer.toString(y));
		ActionList.get("actions")
			.getAsJsonArray()
			.add(moveCommand);		
	}

	/**
	 * Detonates a bomb and damages all ships within a 126 unit radius.
	 * This will damage your ship as well and reduce your health level
	 * by 75 units. Your ship will take 10 seconds to repair.
	 */
	public void SelfDestruct(){
		JsonObject moveCommand = new JsonObject();
		moveCommand.addProperty("Action", "DESTRUCT");
		ActionList.get("actions")
			.getAsJsonArray()
			.add(moveCommand);		
	}

	/**
	 * Moves towards the specified co-dinates.
	 * @param x
	 * @param y
	 */	
	public void MoveTowards(int x, int y) {
        int mx = 0;
        int my = 0;
        if (Me.x > x){
			mx = -1;
		} else if (Me.x < x) {
			mx = 1;
		}
        if (Me.y > y) {
			my = -1;
		} else if (Me.y < y) {
			my = 1;
		}
        this.Move(mx, my);
	}

	/**
	 * Commits the pending actions and sends it to the server
	 */
	public void Commit() {
		String commandString = ActionList.toString();
		outgoing.println(commandString);
		ClearCommandCache();
	}


}

