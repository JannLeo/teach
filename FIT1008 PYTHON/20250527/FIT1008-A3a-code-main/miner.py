from __future__ import annotations
from typing import Iterable

from data_structures import *
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
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplementedError("Please implement the __init__ method")

    def mine(self, block: MinecraftBlock) -> None:
        """
        Mines a block and adds the item to the miner's bag.

        Args:
            block (MinecraftBlock): The block to be mined.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplementedError("Please implement the mine method")

    def clear_inventory(self) -> Iterable:
        """
        Clears the miner's inventory and returns what he had in the inventory before the clear.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplementedError("Please implement the clear_inventory method")


    def __str__(self) -> str:
        return f"Miner: {self.name}"
