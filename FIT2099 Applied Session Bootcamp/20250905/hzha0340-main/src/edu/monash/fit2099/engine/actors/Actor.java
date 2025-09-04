package edu.monash.fit2099.engine.actors;

import edu.monash.fit2099.engine.GameEntity;
import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.attributes.ActorAttribute;
import edu.monash.fit2099.engine.actors.attributes.ActorAttributeOperation;
import edu.monash.fit2099.engine.actors.attributes.BaseActorAttribute;
import edu.monash.fit2099.engine.actors.attributes.BaseAttributes;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.displays.Printable;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import java.util.*;

/**
 * The Actor class represents a {@link GameEntity} that can perform an
 * {@link Action}. It has a hit points attribute, which represents its health.
 * When this value reaches zero, the Actor is unconscious. Additionally, an
 * Actor has a collection of {@link Item}s it is carrying in its inventory.
 *
 * @author Riordan Alfredo
 * @author Adrian Kristanto
 */
public abstract class Actor extends GameEntity implements Printable {
    /**
     * A flexible and extensible attributes system that allows new stats to be
     * added, which enables more interesting game mechanics. For example, in
     * addition to hit points, another attribute that represents its stamina can
     * be added. If the actor runs out of stamina, it will be unable to perform
     * certain actions, such as attacking.
     */
    private final Map<Enum<?>, ActorAttribute<Integer>> attributes = new HashMap<>();

    /**
     * Actor's name
     */
    protected final String name;
    /**
     * A character that will be displayed on the terminal/console -- remain the
     * same to minimise mutability.
     */
    private final char displayChar;
    /**
     * A bag of items
     */
    private final List<Item> itemInventory = new ArrayList<>();

    /**
     * Natural/intrinsic weapon, like a punch
     */
    private IntrinsicWeapon intrinsicWeapon;

    /**
     * The constructor of the Actor class.
     *
     * @param name the name of the Actor
     * @param displayChar the character that will represent the Actor in the
     * display
     * @param hitPoints the Actor's starting hit points
     */
    public Actor(String name, char displayChar, int hitPoints) {
        this.name = name;
        this.displayChar = displayChar;
        this.addNewStatistic(BaseAttributes.HEALTH, new BaseActorAttribute(hitPoints));
    }

    /**
     * A method for checking whether this actor has a specific attribute
     *
     * @param name the name of the attribute, such as BaseActorStatistics.HEALTH
     * @return true if the actor has the queried attribute, false otherwise
     */
    public boolean hasStatistic(Enum<?> name) {
        return this.attributes.containsKey(name);
    }

    /**
     * A method for adding a attribute to the actor.
     *
     * @param name the name of the attribute to be added, which must be a value
     * of an enumeration, such as BaseActorattributes.STAMINA.
     * @param attribute an object that implements the {@link ActorAttribute}
     * interface.
     */
    public void addNewStatistic(Enum<?> name, ActorAttribute<Integer> attribute) {
        this.attributes.put(name, attribute);
    }

    /**
     * A method for modifying the value of an attribute . An alternative
     * implementation to this method is to create several smaller methods, such
     * as increaseAttribute(), decreaseAttribute(), and updateAttribute().
     * However, this results in the Actor class being bloated with boilerplate
     * methods. Another alternative is to simply return the attribute object and
     * let the client modify it directly. However, this results in privacy leak,
     * i.e. the client directly knows the underlying implementation of the
     * attribute, which could result in unwanted dependencies. Therefore, this
     * method is chosen as a compromise. It could be improved with the use of
     * higher-order functions, but since it is not relevant to object-oriented
     * programming, it is not implemented here.
     *
     * @param name the name of the attribute to be modified, which must be a
     * value of an enumeration, such as BaseActorAttributes.STAMINA.
     * @param operation the operation to be performed on the attribute, such as
     * INCREASE, DECREASE, or UPDATE.
     * @param value the value to be used in the operation.
     * @throws IllegalArgumentException if the operation is invalid.
     */
    public <E extends Enum<E>> void modifyAttribute(Enum<E> name, ActorAttributeOperation operation, int value) throws IllegalArgumentException {
        switch (operation) {
            case INCREASE:
                this.attributes.get(name).increase(value);
                break;
            case DECREASE:
                this.attributes.get(name).decrease(value);
                break;
            case UPDATE:
                this.attributes.get(name).update(value);
                break;
            default:
                throw new IllegalArgumentException("Invalid operation for modifying the value of actor's attribute.");
        }
    }

    /**
     * A method for modifying the maximum value of a attribute. See the
     * rationale for
     * {@link Actor#modifyAttribute(Enum, ActorAttributeOperation, int)} for why
     * this method is implemented this way.
     *
     * @param name the name of the attribute to be modified, which must be a
     * value of an enumeration, such as BaseActorStatistics.STAMINA.
     * @param operation the operation to be performed on the attribute, such as
     * INCREASE, DECREASE, or UPDATE.
     * @param value the value to be used in the operation.
     * @throws IllegalArgumentException if the operation is invalid.
     */
    public <E extends Enum<E>>void modifyStatsMaximum(Enum<E> name, ActorAttributeOperation operation, int value) throws IllegalArgumentException {
        switch (operation) {
            case INCREASE:
                this.attributes.get(name).increaseMaximum(value);
                break;
            case DECREASE:
                this.attributes.get(name).decreaseMaximum(value);
                break;
            case UPDATE:
                this.attributes.get(name).updateMaximum(value);
                break;
            default:
                throw new IllegalArgumentException("Invalid operation for modifying the maximum value of actor's stats.");
        }
    }


    /**
     * A method for getting the value of an attribute.
     *
     * @param name the name of the attribute to be retrieved, which must be a
     * value of an enumeration, such as BaseActorattributes.STAMINA.
     * @return the value of the attribute.
     */
    public int getAttribute(Enum<?> name) {
        return this.attributes.get(name).get();
    }

    /**
     * A method for getting the maximum value of an attribute, such as the
     * maximum hit points of the current actor.
     *
     * @param name the name of the attribute to be retrieved, which must be a
     * value of an enumeration, such as BaseActorattributes.STAMINA.
     * @return the maximum value of the attribute.
     */
    public int getMaximumAttribute(Enum<?> name) {
        return this.attributes.get(name).getMaximum();
    }

    /**
     * Add an item to this Actor's inventory.
     *
     * @param item The Item to add.
     */
    public void addItemToInventory(Item item) {
        itemInventory.add(item);
    }

    /**
     * Remove an item from this Actor's inventory. Although it is possible to
     * return the itemInventory to be modified by the client directly, it is not
     * done so to prevent privacy leak.
     *
     * @param item The Item to remove.
     */
    public void removeItemFromInventory(Item item) {
        itemInventory.remove(item);
    }

    /**
     * Get a copy of this Actor's inventory list. Although it is possible to
     * return the itemInventory to be modified by the client directly, it is not
     * done so to prevent privacy leak.
     *
     * @return An unmodifiable wrapper of the inventory.
     */
    public List<Item> getItemInventory() {
        return Collections.unmodifiableList(itemInventory);
    }

    /**
     * Returns a list of all capabilities of the specified type that are present
     * in the item inventory. For each item, attempts to retrieve the capability
     * using {@code asCapability}. If the capability is present, it is included
     * in the returned list.
     *
     * @param <T> the type of capability to retrieve
     * @param capability the class object representing the capability type
     * @return a list containing all capabilities of the specified type found in the inventory;
     *         the list is empty if no items provide the capability
     */
    public <T> List<T> getItemInventoryAs(Class<T> capability) {
        List<T> result = new ArrayList<>();
        for (Item item : itemInventory) {
            if(item != null){
                item.asCapability(capability).ifPresent(result::add);
            }
        }
        return result;
    }


    /**
     * Select and return an action to perform on the current turn.
     *
     * @param actions collection of possible Actions for this Actor
     * @param lastAction The Action this Actor took last turn. Can do
     * interesting things in conjunction with Action.getNextAction()
     * @param map the map containing the Actor
     * @param display the I/O object to which messages may be written
     * @return the Action to be performed
     */
    public abstract Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display);

    /**
     * Returns a new collection of the Actions that the otherActor can do to the
     * current Actor.
     *
     * @param otherActor the Actor that might be performing attack
     * @param direction String representing the direction of the other Actor
     * @param map current GameMap
     * @return A collection of Actions.
     */
    public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {
        return new ActionList();
    }

    /**
     * Is this Actor conscious? Returns true if the current Actor has positive
     * hit points. Actors on zero hit points are deemed to be unconscious.
     * Depending on the game client, this status may be interpreted as either
     * unconsciousness or death, or inflict some other kind of status.
     *
     * @return true if and only if hitPoints is positive.
     */
    public boolean isConscious() {
        return this.getAttribute(BaseAttributes.HEALTH) > 0;
    }

    /**
     * Method that can be executed when the actor is unconscious due to the
     * action of another actor
     *
     * @param otherActor the perpetrator
     * @param map where the actor fell unconscious
     * @return a string describing what happened when the actor is unconscious
     */
    public String unconscious(Actor otherActor, GameMap map) {
        map.removeActor(this);
        return this + " met their demise in the hand of " + otherActor;
    }

    /**
     * Method that can be executed when the actor is unconscious due to natural
     * causes or accident For example, the actor is unconscious due to them
     * falling into a deep well.
     *
     * @param map where the actor fell unconscious
     * @return a string describing what happened when the actor is unconscious
     */
    public String unconscious(GameMap map) {
        map.removeActor(this);
        return this + " ceased to exist.";
    }

    /**
     * Hurt the current actor with the given damage points.
     *
     * @param damage the damage points that the actor receives
     */
    public void hurt(int damage) {
        this.modifyAttribute(BaseAttributes.HEALTH, ActorAttributeOperation.DECREASE, damage);
    }

    /**
     * Heal the current actor with the given health points.
     *
     * @param points the health points that the actor receives
     */
    public void heal(int points) {
        this.modifyAttribute(BaseAttributes.HEALTH, ActorAttributeOperation.INCREASE, points);
    }

    /**
     * Intrinsic weapon can be injected. This allows for more flexibility.
     *
     * @param intrinsicWeapon the intrinsic weapon of an actor, e.g. claw, bare
     * fist, etc.
     */
    protected void setIntrinsicWeapon(IntrinsicWeapon intrinsicWeapon) {
        this.intrinsicWeapon = intrinsicWeapon;
    }

    /**
     * Get intrinsic weapon.
     *
     * @return the intrinsic weapon of the current actor
     */
    public IntrinsicWeapon getIntrinsicWeapon() {
        return intrinsicWeapon;
    }

    /**
     * Returns true if and only if the current Actor has the required capability.
     * It will also return true if any of the items that the actor is carrying has the required capability.
     *
     * @param ability the ability required
     * @return true if and only if the current Actor has the required capability
     */
    @Override
    public final boolean hasAbility(Enum<?> ability) {
        for (Item item : itemInventory) {
            if (item.hasAbility(ability)) {
                return true;
            }
        }
        return super.hasAbility(ability);
    }

    /**
     * Returns the Actor's display character, so that it can be displayed in the
     * UI.
     *
     * @return the Actor's display character
     */
    @Override
    public char getDisplayChar() {
        return displayChar;
    }

    /**
     * A method for returning the string representation of an actor. It displays
     * the actor's name and its current hit points, along with its maximum
     * health hit points.
     */
    @Override
    public String toString() {
        return name + " ("
                + this.getAttribute(BaseAttributes.HEALTH) + "/"
                + this.getMaximumAttribute(BaseAttributes.HEALTH)
                + ")";
    }

}
