from __future__ import annotations


class MinecraftItem:
    """
    A class representing an item with a name, description, and rarity.
    """

    def __init__(self, name: str, description: str, value: int) -> None:
        """
        Initializes an Item instance with a name, description, and rarity.

        Args:
            name (str): The name of the item.
            description (str): A description of the item.
            value (int): The value of the item.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.name = name
        self.description = description
        self.value = value

    def __eq__(self, other: 'MinecraftItem') -> bool:
        """
        Checks if two items are equal based on their name.

        Args:
            other (MinecraftItem): The other item to compare.

        Returns:
            bool: True if the items are equal, False otherwise.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.name == other.name

    def __str__(self) -> str:
        """
        Returns a string representation of the item.

        Returns:
            str: A string representation of the item.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return f"Item(name={self.name}, description={self.description}, value={self.value})"

    def __repr__(self) -> str:
        """
        Returns a string representation of the item for debugging.

        Returns:
            str: A string representation of the item.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return str(self)


class MinecraftBlock:
    """
    A class representing a block in Minecraft containing an item.
    """

    def __init__(self, name: str, description: str, hardness: int, item: MinecraftItem) -> None:
        """
        Initializes a MinecraftBlock instance with a name, description, hardness, int.

        Args:
            name (str): The name of the block.
            description (str): A description of the block.
            hardness (int): The hardness of the block.
            item (MinecraftItem): The item contained in the block.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.name = name
        self.description = description
        self.hardness = hardness
        self.item = item

    def __eq__(self, other: 'MinecraftBlock') -> bool:
        """
        Compares two MinecraftBlock instances.

        Args:
            other (MinecraftBlock): The other block to compare with.

        Returns:
            bool: True if this block is equal to the other block, False otherwise.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            The comparison is based on the hardness of the blocks.
            This is a constant time operation as it involves simple arithmetic and comparison.
        """

        return self.name == other.name

    def __str__(self) -> str:
        """
        Returns a string representation of the block.

        Returns:
            str: A string representation of the block.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return f"Block(name={self.name}, description={self.description}, hardness={self.hardness}, item={self.item})"

    def __repr__(self) -> str:
        return str(self)
