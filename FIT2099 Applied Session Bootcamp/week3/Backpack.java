import java.util.*;

public class Backpack {
    private final ArrayList<Item> storage = new ArrayList<>();
    private final double limit;

    public Backpack(double limit) { this.limit = limit; }

    public boolean add(Item item) {
        double newTotal = totalWeight() + (item == null ? 0.0 : item.getWeight());
        if (item == null) return false;
        if (newTotal > limit) return false;
        return storage.add(item);
    }
    public boolean remove(Item item) { return storage.remove(item); }
    public boolean contains(Item item) { return storage.contains(item); }
    public double totalWeight() {
        double sum = 0.0;
        for (Item it : storage) {
            sum += it.getWeight();
        }
        return sum;
    }
    public double getLimit() { return limit; }

    public List<Action> allowableActions() {
        List<Action> actions = new ArrayList<>();
        for (Item item : storage) {
            actions.add(item.getUnpackAction());
        }
        return actions;
    }

    public void listOutItems() {
        System.out.printf("Here are the items that Cloudy has in the Backpack (%.2f / %.2fkg):%n", totalWeight(), limit);
        if (!storage.isEmpty()) {
            for (Item item : storage) {
                System.out.println(item);
            }
        }
    }

    public List<Item> getItems() { return Collections.unmodifiableList(storage); }
}