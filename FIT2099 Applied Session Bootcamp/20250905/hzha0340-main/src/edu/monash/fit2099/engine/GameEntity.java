package edu.monash.fit2099.engine;

import edu.monash.fit2099.engine.capabilities.Status;
import edu.monash.fit2099.engine.positions.Location;

import java.lang.reflect.Modifier;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Base class for all objects that can exist in the game.
 *
 * This version supports: - Multiple status effects of any type (e.g., multiple
 * poisons). - Static abilities via Enums.
 *
 * Example: An actor may have several status effects (burning, poisoned,
 * stunned, etc.) by implementing interfaces, abilities such as CAN_BE_BURNED.
 *
 * @author Riordan Alfredo
 */
public abstract class GameEntity {

    /**
     * List of all current status effects attached to this entity.
     */
    private final List<Status> statuses = new ArrayList<>();

    private final Set<Enum<?>> abilitySet = new HashSet<>();

    /**
     * Adds a status effect to this entity.
     *
     * @param status the status effect to add
     */
    public void addStatus(Status status) {
        statuses.add(status);
    }

    /**
     * Removes a status effect from this entity.
     *
     * @param status the status effect to remove
     * @return true if the status was present and removed, false otherwise
     */
    public boolean removeStatus(Status status) {
        return statuses.remove(status);
    }

    /**
     * Returns an unmodifiable list of all current statuses.
     *
     * @return a list of statuses, may be empty if none are present
     */
    public List<Status> statuses() {
        return Collections.unmodifiableList(statuses);
    }

    /**
     * Returns a list of all statuses of the specified type.
     *
     * @param type the class type of the status to retrieve
     * @param <T>  the type of the status
     * @return a list of statuses of the given type
     */
    public <T extends Status> List<T> statusesOf(Class<T> type) {
        return statuses.stream()
                .filter(type::isInstance)
                .map(type::cast)
                .collect(Collectors.toList());
    }

    /**
     * Checks whether this entity currently has at least one status of the
     * specified type.
     *
     * @param type the class type of the status to check for
     * @return true if at least one status of the given type is present, false
     * otherwise
     */
    public boolean hasStatus(Class<? extends Status> type) {
        return statuses.stream().anyMatch(type::isInstance);
    }

    /**
     * Ticks all status effects attached to this entity. For each status, calls
     * its tick() method. If a status is no longer active after ticking, it is
     * removed from the entity.
     */
    public void tickStatuses(Location location) {
        Iterator<Status> it = statuses.iterator();
        while (it.hasNext()) {
            Status status = it.next();
            status.tickStatus(this, location);
            if (!status.isStatusActive()) {
                it.remove();
            }
        }
    }

    /**
     * Check if this instance has ability
     *
     * @param ability enum
     * @return true if it has the ability, false otherwise
     */
    public boolean hasAbility(Enum<?> ability) {
        return abilitySet.contains(ability);
    }

    /**
     * Attach ability/status to the instance
     *
     * @param ability enum
     */
    public void enableAbility(Enum<?> ability) {
        if (!hasAbility(ability)) {
            abilitySet.add(ability);
        }
    }

    /**
     * Detach ability from the instance
     *
     * @param ability enum
     */
    public void disableAbility(Enum<?> ability) {
        if (hasAbility(ability)) {
            abilitySet.remove(ability);
        }
    }

    /**
     * Get unmodifiable capabilities list to avoid privacy leak
     *
     * @return unmodifiable list of capabilities
     */
    public List<Enum<?>> abilities() {
        return List.copyOf(abilitySet);
    }

    /**
     * Returns an Optional containing the capability if supported, or empty if
     * not.
     */
    public final <T> Optional<T> asCapability(Class<T> capability) {
        // Ensure that 'type' is an interface
        if (!capability.isInterface() && !Modifier.isAbstract(capability.getModifiers()) ) {
            throw new IllegalArgumentException("Capability must be a contract (abstract/interface): " + capability.getName());
        }
        if (capability.isInstance(this)) {
            return Optional.of(capability.cast(this));
        }
        return Optional.empty();
    }
}
