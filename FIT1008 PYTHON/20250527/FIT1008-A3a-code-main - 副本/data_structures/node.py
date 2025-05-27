""" Implementation of a node in linked lists and binary search trees. """

from typing import Generic, TypeVar

I = TypeVar('I')
K = TypeVar('K')
T = TypeVar('T')

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev'
__docformat__ = 'reStructuredText'


class TreeNode(Generic[K, I]):
    """ Node class represent BST nodes. """

    def __init__(self, key: K, item: I = None, depth: int = 0) -> None:
        """
            Initialises the node with a key and optional item
            and sets the left and right pointers to None
            key: the key of the node
            item: the item of the node
            depth: the depth of the node in the tree
            The leaf of the largest subtree will have a
            depth equal to the height of the tree.

            :complexity: O(1)
        """
        self.key = key
        self.item = item
        self.left = None
        self.right = None
        self.depth = depth

    def __str__(self):
        """
            Returns the string representation of a node
            :complexity: O(N) where N is the size of the item
        """
        key = str(self.key) if type(self.key) != str else "'{0}'".format(self.key)
        item = str(self.item) if type(self.item) != str else "'{0}'".format(self.item)
        return '({0}, {1})'.format(key, item)

    def __repr__(self) -> str:
        return str(self)


class Node(Generic[T]):
    """ Simple linked node. It contains an item and has a reference to next node. """

    def __init__(self, item: T = None) -> None:
        """ Node initialiser. """
        self.item = item
        self.link = None
