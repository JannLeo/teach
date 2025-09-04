package edu.monash.fit2099.demo.mars.items;


import edu.monash.fit2099.demo.mars.DemoAbilities;
import edu.monash.fit2099.demo.mars.capabilities.SpaceTravelling;

public class SpaceSuit extends MartianItem implements SpaceTravelling {

    private final int oxygenLevel;

    public SpaceSuit(int oxygenLevel) {
        super("Space suit", '[', true);
        this.oxygenLevel = oxygenLevel;
        this.enableAbility(DemoAbilities.SPACETRAVELLING);
    }

    @Override
    public void canTravel() {

    }
}
