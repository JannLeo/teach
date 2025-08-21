public class Bottle extends Item {
    public Bottle(String name, double weight) { super(name, weight); }

    @Override
    public String toString() {
        return super.toString() + " - to drink, with 1.0 liter left.";
    }
}