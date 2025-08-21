import java.util.*;

public class Camper {
    private final String name;
    private int hydrationLevel = 20;
    private int coldnessLevel = 20;
    private final Backpack backpack;

    public Camper(String name, Backpack backpack) {
        this.name = name;
        this.backpack = backpack;
    }

    public Backpack getBackpack() { return backpack; }

    public List<Action> allowableActions() {
        List<Action> actions = new ArrayList<>();
        actions.addAll(backpack.allowableActions());
        return actions;
    }

    public void checkAllItems() {
        backpack.listOutItems();
    }

    @Override
    public String toString() {
        return String.format("%s (hydration level: %d, coldness level: %d)",
                name, hydrationLevel, coldnessLevel);
    }
}