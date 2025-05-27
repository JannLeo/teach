from __future__ import annotations
from data_structures import *
from minecraft_block import MinecraftBlock


class MinecraftChecklist:
    def __init__(self, blocks: ArrayR[MinecraftBlock]) -> None:
        """
        Initializes the MinecraftChecklist instance with a list of blocks.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplementedError("Please implement the __init__ method")

    def __contains__(self, item: MinecraftBlock) -> bool:
        """
        Checks if the item is in the checklist.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplementedError("Please implement the __contains__ method")

    def __len__(self) -> int:
        """
        Returns the number of blocks in the checklist.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplementedError("Please implement the __len__ method")

    def add_block(self, block: MinecraftBlock) -> None:
        """
        Adds a block to the checklist.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplemented("Add block is not implemented yet.")

    def remove_block(self, block: MinecraftBlock) -> None:
        """
        Removes a block from the checklist.

        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplemented("Remove block is not implemented yet.")

    def get_sorted_blocks(self) -> ArrayR[MinecraftBlock]:
        """
        Returns the sorted blocks in the checklist.
        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplementedError("Please implement the get_sorted_blocks method")

    def get_optimal_blocks(self, block1: MinecraftBlock, block2: MinecraftBlock) -> ArrayR[MinecraftBlock]:
        """
        Returns the optimal blocks between two given blocks.
        Criteria 1:
            - Optimal blocks have a ratio of value to mining time more than the same ratio for block1.
        Criteria 2:
            - Optimal blocks have a ratio of value to mining time less than the same ratio for block2.
        Args:
            block1 (MinecraftBlock): The first block.
            block2 (MinecraftBlock): The second block.
        Returns:
            ArrayR: An array of optimal blocks between the two given blocks.
        Complexity:
            Best Case Complexity: TODO
            Worst Case Complexity: TODO
        Justification:
            TODO
        """
        raise NotImplementedError("Please implement the get_optimal_blocks method")
