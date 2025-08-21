public class PackAction extends Action {
    private final Item item;

    public PackAction(Item item) {
        this.item = item;
    }

    @Override
    public String execute(Camper camper, Campsite campsite) {
        if (camper == null || campsite == null) {
            return "Invalid context for packing.";
        }

        boolean removedFromCampsite = campsite.removeItem(item);
        if (!removedFromCampsite) {
            return String.format("%s is not at the campsite.", item.getSimpleName());
        }

        boolean addedToBackpack = camper.getBackpack().add(item);
        if (!addedToBackpack) {
            campsite.addItem(item);
            return String.format("%s can not be packed as it will exceed the backpack limit",
                    item.getSimpleName());
        }

        return String.format("%s packed %s to the backpack",
                camper.toString(), item.getSimpleName());
    }

    @Override
    public String menuDescription(Camper camper) {
        return String.format("%s will pack %s to the backpack",
                camper.toString(), item.getSimpleName());
    }
}

