from __future__ import annotations
from collections.abc import Callable
from typing import Tuple, TypeVar

from data_structures.bst import BinarySearchTree
from data_structures import ArrayList
from algorithms.mergesort import mergesort

K = TypeVar('K')
I = TypeVar('I')


class BetterBST(BinarySearchTree[K, I]):
    def __init__(self, elements: ArrayList[Tuple[K, I]]) -> None:
        """
        Initialiser for the BetterBST class.
        We assume that the all the elements that will be inserted
        into the tree are contained within the elements ArrayList.

        As such you can assume the length of elements to be non-zero.
        The elements ArrayList will contain tuples of key, item pairs.

        First sort the elements ArrayList and then build a balanced tree from the sorted elements
        using the corresponding methods below.

        Args:
            elements(ArrayList[tuple[K, I]]): The elements to be inserted into the tree.

        Complexity:
            Best Case Complexity: O(NlogN * comp(T))
            Worst Case Complexity: O(NlogN * comp(T))
        Justification:
            call __sort_elements for mergesort(O(NlogN * comp(T))), then insert
        """
        if elements is None or len(elements) == 0:
            raise ValueError
        
        super().__init__()
        new_elements: ArrayList[Tuple[K, I]] = self.__sort_elements(elements)
        self.__build_balanced_tree(new_elements)

    def __sort_elements(self, elements: ArrayList[Tuple[K, I]]) -> ArrayList[Tuple[K, I]]:
        """
        Recall one of the drawbacks to using a binary search tree is that it can become unbalanced.
        If we know the elements ahead of time, we can sort them and then build a balanced tree.
        This will help us maintain the O(log n) complexity for searching, inserting, and deleting elements.

        Args:
            elements (ArrayList[Tuple[K, I]]): The elements we wish to sort.

        Returns:
            ArrayList(Tuple[K, I]]) - elements after being sorted.

        Complexity:
            Best Case Complexity: O(nlogn)
            Worst Case Complexity: O(nlogn)

        Justification:
            where n is the length of the list just call mergesort here
        """
        return mergesort(elements, key=lambda x: x[0])


    def __build_balanced_tree(self, elements: ArrayList[Tuple[K, I]]) -> None:
        """
        This method will build a balanced binary search tree from the sorted elements.

        Args:
            elements (ArrayList[Tuple[K, I]]): The elements we wish to use to build our balanced tree.

        Returns:
            None

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(nlogn)
            Worst Case Complexity: O(nlogn)

        Justification:
            assist is call to insert element n times, when insert n times the height of tree is O(logn)
        """
        def assist(start, end):

            if start > end:      # no elements insert
                return
            
            mid = (start + end) // 2      # find middle index
            key, item = elements[mid]

            self[key] = item

            assist(start, mid - 1)       # recursively build left subtree
            assist(mid + 1, end)         # recursively build right subtree

        assist(0, len(elements) - 1)     # start the tree


    def filter_keys(self, filter_func1: Callable[[K], bool], filter_func2: Callable[[K], bool]) -> ArrayList[Tuple[K, I]]:
        """
        Filters the keys in the tree based on two criteria.

        Args:
            filter_func1 (callable): A function that takes a value and returns True if the key is more than criteria1.
            filter_func2 (callable): A function that takes a value and returns True if the key is less than criteria2.
        Returns:
            ArrayList[Tuple[K, I]]: An ArrayList of tuples containing Key,Item pairs that match the filter.

        Complexity:
            Best Case Complexity: O(logn(filter_func1+filter_func2))
            Worst Case Complexity: O(n(filter_func1+filter_func2))
        Justification:
            call two filters at each node first, 
            if filter_func1(key) == False, so now node and left subtree is not suit,
            skip left subtree and recursively right subtree, at most O(logn)
            if filter_func2(key) == False, so now node and right subtree is not suit,
            skip right subtree and recursively left subtree, at most O(logn)
            if two all suit inorder visit the left and right subtrees
            so best case is most of the branches cut off O(logn(filter_func1+filter_func2))
            worst case is need traverse n nodes in the tree O(n(filter_func1+filter_func2))


        """

        result = ArrayList()
        def dfs(node):
            if node is None:
                return
            key = node.key

            if not filter_func1(key):     # all the keys in the left subtree of this node have failed
                dfs(node.right)           # skip left subtree
                return

            if not filter_func2(key):     # all the keys in the right subtree of this node have failed
                dfs(node.left)            # skip right subtree
                return

            dfs(node.left)        # recurse left
            result.append((key, node.item))     # record the current
            dfs(node.right)       # recurse right
        
        dfs(self.root)  # start
        return result
