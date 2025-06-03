from __future__ import annotations
from typing import Iterable

from data_structures import ArrayList
from minecraft_block import MinecraftBlock


class Miner:
    """
    A class representing a miner in a mining simulation.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the miner with a name and an empty inventory.
        Args:
            name (str): The name of the miner.
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        Justification:
            two assignment operation, a constant time complexity
        """
        if name is None or len(name) == 0:
            raise ValueError

        self.name = name
        self.inventory = ArrayList()      # initialise ArrayList as backpack

    def mine(self, block: MinecraftBlock) -> None:
        """
        Mines a block and adds the item to the miner's bag.

        Args:
            block (MinecraftBlock): The block to be mined.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        Justification:
            the time complexity of append is O(1)
        """
        if not isinstance(block, MinecraftBlock):
            raise TypeError

        self.inventory.append(block.item)       # save item of this square in backpack    

    def clear_inventory(self) -> Iterable:
        """
        Clears the miner's inventory and returns what he had in the inventory before the clear.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        Justification:
            two assignment operation one return, constant time complexity
        """

        old_inventory = self.inventory     # keep
        self.inventory = ArrayList()       # create empty ArrayList as new backpack
        return old_inventory               # return old


    def __str__(self) -> str:
        return f"Miner: {self.name}"
