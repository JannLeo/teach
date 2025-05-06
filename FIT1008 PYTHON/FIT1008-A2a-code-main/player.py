from __future__ import annotations
from enums import PlayerPosition
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining

# Do not change the import statement below
# If you need more modules and classes from datetime, do not use
# separate import statements. Use them from datetime like this:
# datetime.datetime, or datetime.date, etc.
import datetime


class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Complexity:
            Best Case Complexity: O(1) all sentence are constant-time operation
            Worst Case Complexity: O(1) all sentence are constant-time operation
        """
        self.name = name
        self.position = position
        self.goals = 0
        self.birth_year = datetime.datetime.now().year - age
        self.stats = HashTableSeparateChaining()

    def reset_stats(self) -> None:
        """
        Reset the stats of the player.
        
        This doesn't delete the existing stats, but resets them to 0.
        I.e. all stats that were previously set should still be available, with a value of 0.

        Complexity:
            Best Case Complexity: O(1) when stats table empty
            Worst Case Complexity: O(n) first call self.stats.keys() so need to traverse all the table
        """
 
        keys = self.stats.keys()
        for key in keys:
            self.stats[key] = 0

    def __setitem__(self, statistic: str, value: int) -> None:
        """
        Set the given value for the given statistic for the player.

        Args:
            statistic (string): The key of the stat
            value (int): The value of the stat

        Complexity:
            Best Case Complexity: O(1) key hashes to empty chain
            Worst Case Complexity: O(n) it must traverse all the chain
        """
        self.stats[statistic] = value

    def __getitem__(self, statistic: str) -> int:
        """
        Get the value of the player's stat based on the passed key.

        Args:
            statistic (str): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            Best Case Complexity: O(1) key is the first one
            Worst Case Complexity: O(n) it must traverse all the chain
        """
        return self.stats[statistic]

    def get_age(self) -> int:
        """
        Get the age of the player

        Returns:
            int: The age of the player

        Complexity:
            Best Case Complexity: O(1) both of two operation are constant time
            Worst Case Complexity: O(1) both of two operation are constant time
        """
        current_year = datetime.datetime.now().year
        return current_year - self.birth_year

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity Analysis not required.
        """
        return "Player(name={}, position={}, age={}, goals={})".format(self.name, self.position.name, self.get_age(), self.goals)    
    
    def __repr__(self) -> str:
        """ String representation of the Player object.
        Useful for debugging or when the Player is held in another data structure.
        """
        return str(self)
