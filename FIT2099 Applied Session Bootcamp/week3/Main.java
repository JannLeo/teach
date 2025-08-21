public class Main {
    public static void main(String[] args) {
        Backpack backpack = new Backpack(10.00);

        Camper cloudy = new Camper("Cloudy", backpack);

        backpack.add(new Bedroll("KAMUI", 7.00));
        backpack.add(new Bottle("Mountain Franklin", 1.00));
        backpack.add(new FlintAndSteel("Aurora", 0.50));

        Campsite campsite = new Campsite();
        campsite.addItem(new Bedroll("KAMUI V2", 7.00));
        campsite.simulate(cloudy);
    }
}

