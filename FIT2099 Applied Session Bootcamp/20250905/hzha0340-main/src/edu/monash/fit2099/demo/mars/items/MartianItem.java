package edu.monash.fit2099.demo.mars.items;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.Location;

public abstract class MartianItem extends Item {

    private Action martianAction;

    public MartianItem(String name, char displayChar, boolean portable) {
        super(name, displayChar, portable);
    }

    @Override
    public ActionList allowableActions(Location location) {
        ActionList actions = super.allowableActions(location);
        actions.add(martianAction);
        return actions;
    }

}
