public class FlintAndSteel extends Item {
    public FlintAndSteel(String name, double weight) { super(name, weight); }

    @Override
    public String toString() {
        return super.toString() + " - to start a fire.";
    }
}