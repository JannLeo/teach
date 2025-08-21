import java.util.*;

public class Campsite {
    private final ArrayList<Item> items = new ArrayList<>();

    public Campsite() {}

    public void addItem(Item item) { items.add(item); }
    public boolean removeItem(Item item) { return items.remove(item); }

    public List<Action> allowableActions() {
        List<Action> actions = new ArrayList<>();
        for (Item item : items) {
            actions.add(item.getPackAction());
        }
        return actions;
    }

    public void listOutItems() {
        System.out.println("Here are the items that we have on campsite:");
        if (!items.isEmpty()) {
            for (Item item : items) {
                System.out.println(item);
            }
        }
    }

    public void simulate(Camper camper) {
        while (true) {
            List<Action> actions = new ArrayList<>();
            actions.addAll(this.allowableActions());
            actions.addAll(camper.allowableActions());

            System.out.println("#########################################");
            camper.checkAllItems();
            System.out.println();
            this.listOutItems();
            System.out.println();
            System.out.println("#########################################");

            Action action = Menu.showMenu(actions, camper);
            if (action == null) {
                break;
            }
            System.out.println(action.execute(camper, this));
        }
    }
}