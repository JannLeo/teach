public abstract class Item {
    protected final String name;
    protected final double weight;

    public Item(String name, double weight) {
        this.name = name;
        this.weight = weight;
    }

    public double getWeight() { return weight; }

    public String getSimpleName() { return getClass().getSimpleName(); }

    public Action getPackAction() {
        return new PackAction(this);
    }

    public Action getUnpackAction() {
        return new UnpackAction(this);
    }

    @Override
    public String toString() {
        return String.format("%s (%s) has weight of %.2f kg",
                getSimpleName(), name, weight);
    }
}