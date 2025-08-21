public class UnpackAction extends Action {
    private final Item item;

    public UnpackAction(Item item) {
        this.item = item;
    }

    @Override
    public String execute(Camper camper, Campsite campsite) {
        if (camper == null || campsite == null) {
            return "Invalid context for unpacking.";
        }

        boolean removedFromBackpack = camper.getBackpack().remove(item);
        if (!removedFromBackpack) {
            return String.format("%s is not in the backpack.", item.getSimpleName());
        }

        campsite.addItem(item);
        return String.format("%s removed %s from the backpack",
                camper.toString(), item.getSimpleName());
    }

    @Override
    public String menuDescription(Camper camper) {
        return String.format("%s will unpack %s from the backpack",
                camper.toString(), item.getSimpleName());
    }
}

