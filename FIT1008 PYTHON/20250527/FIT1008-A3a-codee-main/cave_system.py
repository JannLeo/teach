from __future__ import annotations

from data_structures import List, ArrayList
from minecraft_block import MinecraftBlock


class CaveNode:
    """
    A node in the cave system representing a cave node.
    """

    def __init__(self, blocks: ArrayList[MinecraftBlock] = None, name: str = None) -> None:
        """
        Initializes a CaveNode instance with a list of blocks.

        Args:
            blocks (list): A list of blocks (ores) in the cave node.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            The complexity is constant because the initialization of the node and its attributes does not depend on the size of the input.
        """
        self.name = name
        # Each node can have multiple blocks (ores)
        self.blocks = blocks if blocks else ArrayList()
        # Connected neighboring nodes
        self.neighbours = ArrayList()

    def connect(self, other_node: 'CaveNode') -> None:
        """
        Connects this cave node to another cave node.
        Args:
            other_node (CaveNode): The other node to connect to.
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N) where N is the number of neighbours.
        Justification:
            The complexity is constant because adding a neighbor to the list does not depend on the size of the input.
            The worst case complexity is O(N) because the neighbours list will resize.
        """
        # Undirected connection between nodes
        self.neighbours.append(other_node)
        other_node.neighbours.append(self)

    def __str__(self) -> str:
        """
        Returns a string representation of the CaveNode.

        Returns:
            str: A string representation of the CaveNode.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)

        Justification:
            The complexity is constant because the string representation does not depend on the size of the input.
        """
        return f"CaveNode(name={self.name}, blocks={self.blocks}, neighbours={len(self.neighbours)})"


class CaveSystem:
    """
    A class to represent a cave system.
    """
    def __init__(self, cave_node: CaveNode, number_of_nodes: int) -> None:
        self.entrance = cave_node
        self.number_of_nodes = number_of_nodes

    def __len__(self) -> int:
        """
        Returns the number of nodes in the cave system.

        Returns:
            int: The number of nodes in the cave system.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.number_of_nodes

    def __str__(self) -> str:
        """
        Returns a string representation of the cave system.

        Returns:
            str: A string representation of the cave system.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return f"CaveSystem(entrance={self.entrance}, number_of_nodes={self.number_of_nodes})"
