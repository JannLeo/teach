public class Bedroll extends Item {
    public Bedroll(String name, double weight) { super(name, weight); }

    @Override
    public String toString() {
        return super.toString() + " - to rest.";
    }
}