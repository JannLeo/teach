package edu.monash.fit2099.demo.mars.grounds;

import edu.monash.fit2099.demo.mars.DemoAbilities;
import edu.monash.fit2099.demo.mars.capabilities.Burning;
import edu.monash.fit2099.demo.mars.capabilities.Flammable;
import edu.monash.fit2099.demo.mars.items.MartianItem;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
/**
 * Crater类表示火星地图中的陨石坑地形
 * 这是一种特殊的地面类型，具有年龄增长机制和对进入角色的特殊影响
 */
public class Crater extends Ground {

    private int age;

    public Crater() {
        super('o', "Crater");
        age = 0;
    }

    private Crater(int age, char displayChar) {
        super(displayChar, "Crater");
        this.age = age;
    }

    @Override
    public void tick(Location location) {
        age++;
        if (age == 10) {
            location.setGround(new Crater(age, '#'));
        } else if (age == 20) {
            location.setGround(new Crater(age, '$'));
        }
        // feature: burn the actor when they step on the crater.
        if (location.containsAnActor()) {
            Flammable flammable = location.getActorAs(Flammable.class);
            if(flammable != null){
                // 如果角色可以燃烧，则为其添加Burning状态
                location.getActor().addStatus(new Burning(flammable));
            }
        }
    }

    @Override
    public boolean canActorEnter(Actor actor) {
        // Only allow actors who can travel through space and are currently able to do so
      return actor.hasAbility(DemoAbilities.SPACETRAVELLING);
    }
}
