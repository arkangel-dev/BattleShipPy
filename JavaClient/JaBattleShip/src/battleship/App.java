package battleship;



public class App {
    public static void main(String[] args) throws Exception {
		JaBattleship Client = new JaBattleship("Ark", "SEC435389", "127.0.0.1", 9999);
		while (true) {
			// Client.UpdateTelemetry();
			// Insert battle logic here...
			Client.MoveTowards(400, 400);
			// System.out.println(Client.Me.x + " " + Client.Me.y);
			Client.Commit();
		}
    }
}