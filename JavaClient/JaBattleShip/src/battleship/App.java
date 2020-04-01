package battleship;

public class App {
    public static void main(String[] args) throws Exception {

		JaBattleship Server = new JaBattleship(
			"Ark",
			"127.0.0.1",
			 9999
		); // Define the connection

		// while (true) {
		// 	Server.UpdateTelemetry(); // Update the telemetry
		// 	Server.Move(1, 1); // Move the ship
		// 	Server.Commit(); // Commit to the appended commands
		// 	Thread.sleep(250); // Sleep

		// 	System.out.println(
		// 		"X : " + Server.Me.x +
		// 		" | y " + Server.Me.y
		// 	); // Print the current position
		// }
		while (true) {
			Thread.sleep(1000);
			Server.SelfDestruct();
			Server.Commit();
		}
    }
}