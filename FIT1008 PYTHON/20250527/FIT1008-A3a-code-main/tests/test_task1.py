from __future__ import annotations

import ast
import inspect
from typing import List, Tuple
from unittest import TestCase

from betterbst import BetterBST
from data_structures import ArrayList
from tests.helper import CollectionsFinder, convert_inbuiltlist_to_arrayList
from data_structures.bst import BinarySearchTree
from data_structures.node import TreeNode


class TestTask1Setup(TestCase):
    def setUp(self) -> None:
        """
        #name(Test Task 1 Setup)
        #score(0)
        """
        pass


class TestTask1(TestTask1Setup):
    def bst_is_balanced(self, bst: BinarySearchTree) -> bool:
        """
        Helper function to check if the BST is balanced.
        """
        height = self.bst_is_balanced_aux(bst.root) - 1 # Depth of a tree start from 0
        if height == -1:
            return False
        return True
    
    def bst_is_balanced_aux(self, node: TreeNode) -> int:
        """
        Helper function to check if the BST is balanced.
        """
        if node is None:
            return 0

        left_height = self.bst_is_balanced_aux(node.left)
        right_height = self.bst_is_balanced_aux(node.right)

        if left_height == -1 or right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return max(left_height, right_height) + 1

    def bst_get_depth(self, node: TreeNode) -> int:
        """
        Helper function to get the depth of the BST.
        """
        if node is None:
            return -1
        left_depth = self.bst_get_depth(node.left)
        right_depth = self.bst_get_depth(node.right)
        return max(left_depth, right_depth) + 1
    
    def test_bst_depth_small(self) -> None:
        """
        #name(Test the BetterBST constructor)
        #score(1)
        """
        numbers: List[tuple[int, str]] = [(x, str(x)) for x in range(1, 6)]
        better_bst: BetterBST = BetterBST(convert_inbuiltlist_to_arrayList(numbers))
        self.assertEqual(self.bst_get_depth(better_bst.root), 2,
                         f"Expected depth of 4 got {self.bst_get_depth(better_bst.root)}")

        numbers: List[int] = [1964, 586, 888]
        numbers: List[Tuple[int, str]] = [(x, str(x)) for x in numbers]
        better_bst = BetterBST(convert_inbuiltlist_to_arrayList(numbers))
        self.assertEqual(self.bst_get_depth(better_bst.root), 1,
                         f"Expected depth of 4 got {self.bst_get_depth(better_bst.root)}")
    
    def test_bst_depth_medium(self) -> None:
        """
        #name(Test the BetterBST constructor)
        #score(1)
        """
        numbers: List[tuple[int, str]] = [(x, str(x)) for x in range(1, 17)]
        better_bst: BetterBST = BetterBST(convert_inbuiltlist_to_arrayList(numbers))
        self.assertEqual(self.bst_get_depth(better_bst.root), 4,
                         f"Expected depth of 4 got {self.bst_get_depth(better_bst.root)}")

        numbers: List[int] = [1964, 586, 888, 416, 3088, 1736, 2690, 2502, 171, 767, 3053, 2156, 536,
                              486, 560, 601, 2140, 822, 1554, 2932, 505, 1245, 1639, 2179]
        numbers: List[Tuple[int, str]] = [(x, str(x)) for x in numbers]
        better_bst = BetterBST(convert_inbuiltlist_to_arrayList(numbers))
        self.assertEqual(self.bst_get_depth(better_bst.root), 4,
                         f"Expected depth of 5 got {self.bst_get_depth(better_bst.root)}")

    def test_better_bst_operations(self) -> None:
        """
        #name(Test the BetterBST constructor)
        #score(1)
        """
        numbers: List[tuple[int, str]] = [(x, str(x)) for x in range(1, 17)]
        better_bst: BetterBST = BetterBST(convert_inbuiltlist_to_arrayList(numbers))
        self.assertEqual(len(better_bst), 16, "There should be 16 elements in the bst")

        self.assertEqual(better_bst.get_minimal(better_bst.root).key, 1,
                         f"Expected 1 as the minimal key got {better_bst.get_minimal(better_bst.root)}")
        self.assertEqual(better_bst.get_maximal(better_bst.root).key, 16,
                         f"Expected 16 as the maximal key got {better_bst.get_maximal(better_bst.root)}")

        del better_bst[1]

        self.assertEqual(better_bst.get_minimal(better_bst.root).key, 2,
                         f"Expected 2 as the minimal key got {better_bst.get_minimal(better_bst.root)}")

    def test_bst_balance(self):
        """
        #name(Test the BetterBST constructor)
        #score(1)
        """
        numbers: List[tuple[int, str]] = [(x, str(x)) for x in range(1, 17)]
        better_bst: BetterBST = BetterBST(convert_inbuiltlist_to_arrayList(numbers))
        self.assertEqual(self.bst_is_balanced(better_bst), True, "The tree should be balanced")

        numbers: List[int] = [1964, 586, 888, 416, 3088, 1736, 2690, 2502, 171, 767, 3053, 2156, 536,
                              486, 560, 601, 2140, 822, 1554, 2932, 505, 1245, 1639, 2179, 1045, 1542, 179, 2639, 2961]
        numbers: List[Tuple[int, str]] = [(x, str(x)) for x in numbers]
        better_bst = BetterBST(convert_inbuiltlist_to_arrayList(numbers))
        self.assertEqual(self.bst_is_balanced(better_bst), True, "The tree should be balanced")

    def test_bst_balance_2(self):
        """
        #name(Test the BetterBST constructor)
        #score(1)
        """
        numbers: List[int] = [12482961, 28677579, 21589567, 29180361, 1465047, 20325086, 31013035, 10389326, 22283568,
                              28114676, 21715872, 36247, 30821720, 23565440, 25479803, 24206692, 19184335, 11410531,
                              6677957, 17108693, 9152417, 20235004,
                              27498797, 16228428, 13405296, 16604570, 24732332, 26675257, 18101333, 21295517, 15406486,
                              20504994, 5417150, 2550562, 19789429, 26821312, 14283105, 1523316, 815628, 22664586,
                              11186756, 2891723, 24207674, 23283113, 13113168]
        numbers: List[Tuple[int, str]] = [(x, str(x)) for x in numbers]
        better_bst = BetterBST(convert_inbuiltlist_to_arrayList(numbers))

        self.assertEqual(self.bst_is_balanced(better_bst), True, "The tree should be balanced")

    def test_bst_filter(self):
        """
        #name(Test the BetterBST constructor)
        #score(1)
        """
        numbers: List[int] = [12482962, 28677579, 21589567, 29180361, 1465047, 20325086, 31013035, 10389326, 22283568]
        numbers: List[Tuple[int, str]] = [(x, str(x)) for x in numbers]
        func1 = lambda x: x > 20000000
        func2 = lambda x: x < 30000000
        betterbst = BetterBST(convert_inbuiltlist_to_arrayList(numbers))

        result_inbuilt = [(28677579, '28677579'), (21589567, '21589567'), (29180361, '29180361'),
                          (20325086, '20325086'), (22283568, '22283568')]

        # Use ArrayList as the expected result type
        result = ArrayList(len(betterbst))
        for item in result_inbuilt:
            result.append(item)
        actual_result = betterbst.filter_keys(func1, func2)

        for i in range(len(result)):
            self.assertIn(result[i], actual_result, f"Expected {result[i]} not found in the given result")


class TestTask1Approach(TestTask1Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import betterbst
        modules = [betterbst]

        for f in modules:
            # Get the source code
            f_source = inspect.getsource(f)
            filename = f.__file__

            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)

            # Report any failures
            for failure in visitor.failures:
                self.fail(failure[3])
