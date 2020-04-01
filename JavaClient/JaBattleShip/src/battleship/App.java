package battleship;

public class App {
    public static void main(String[] args) throws Exception {
		JaBattleship Client = new JaBattleship("Ark", "127.0.0.1", 9999);
		while (true) {
			Client.UpdateTelemetry();
			// Insert battle logic here...
			Client.Commit();
			Thread.sleep(250);
		}
    }
}