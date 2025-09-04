package edu.monash.fit2099.demo.mars.items;

import edu.monash.fit2099.demo.mars.DemoAbilities;
import edu.monash.fit2099.demo.mars.capabilities.SpaceTravelling;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.MoveActorAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.Location;

public class Rocket extends MartianItem {

    private final Location destination;

    public Rocket(Location destination) {
        super("Rocket", '^', false);
        this.destination = destination;
    }

    private boolean canAnyItemTravel(Actor actor) {
        if (actor == null || !actor.hasAbility(DemoAbilities.SPACETRAVELLING)) {
            return false;
        }

        //NOTE: if we have ability, we don't need to do this here.
//        for (Item item : actor.getItemInventory()) {
//            if (item.asCapability(SpaceTravelling.class)
//                    .map(SpaceTravelling::canTravel)
//                    .orElse(false)) {
//                return true;
//            }
//        }
//        return false
        return actor.hasAbility(DemoAbilities.SPACETRAVELLING);
    }

    @Override
    public ActionList allowableActions(Location location) {
        // location.map().trackStatusEffect(new Burnable(this));
        ActionList actions = super.allowableActions(location);
        if(canAnyItemTravel(location.getActor())){
            actions.add(new MoveActorAction(destination, "to Mars!"));
        }
        return actions;
    }


}
