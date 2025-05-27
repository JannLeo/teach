import ast
import inspect
from unittest import TestCase

from data_structures import ArrayR
from minecraft_block import MinecraftBlock, MinecraftItem
from minecraft_checklist import MinecraftChecklist
from miner import Miner
from tests.helper import CollectionsFinder


class TestTask2Setup(TestCase):
    def setUp(self) -> None:
        sample_minecraft_items = [
            MinecraftItem("Diamond", "A precious gem used for crafting.", 15),
            MinecraftItem("Iron Nugget", "A small piece of iron.", 3),
            MinecraftItem("Coal", "A common mineral used for crafting.", 2),
            MinecraftItem("Netherite", "A rare material used for crafting.", 20),
            MinecraftItem("Gold Nugget", "A small piece of gold.", 6),
        ]

        sample_minecraft_blocks = [
            MinecraftBlock("Netherite Ore", "A block containing netherite.", 5, sample_minecraft_items[3]),
            MinecraftBlock("Diamond Ore", "A block containing diamonds.", 5, sample_minecraft_items[0]),
            MinecraftBlock("Gold Ore", "A block containing gold.", 5, sample_minecraft_items[4]),
            MinecraftBlock("Iron Ore", "A block containing iron.", 4, sample_minecraft_items[1]),
            MinecraftBlock("Coal Ore", "A block containing coal.", 3, sample_minecraft_items[2]),
        ]

        self.SampleMinecraftItems = sample_minecraft_items
        self.SampleMinecraftBlocks = sample_minecraft_blocks


class TestTask2(TestTask2Setup):
    def test_miner_init(self):
        """
        #name(Test the mine method)
        #score(1)
        """
        steve = Miner("Steve")
        self.assertTrue(hasattr(steve, "name"))
        self.assertTrue(hasattr(steve, "inventory"))

        self.assertEqual(steve.name, "Steve", f"Expected name to be 'Steve' but got {steve.name}")
        self.assertEqual(len(steve.inventory), 0, f"Expected inventory to be empty but got {len(steve.inventory)}")

    def test_miner_mine(self):
        """
        #name(Test the mine method)
        #score(1)
        """
        steve = Miner("Steve")
        for block in self.SampleMinecraftBlocks:
            steve.mine(block)

        self.assertEqual(len(steve.inventory), len(self.SampleMinecraftBlocks),
                         f"Expected to have {len(self.SampleMinecraftBlocks)} items in inventory but got {len(steve.inventory)}")

    def test_miner_clear_inventory(self):
        """
        #name(Test the clear_inventory method)
        #score(1)
        """
        steve = Miner("Steve")
        for block in self.SampleMinecraftBlocks:
            steve.mine(block)

        items = steve.clear_inventory()

        index = 0
        for item in items:
            self.assertEqual(item, self.SampleMinecraftBlocks[index].item,
                             f"Expected {self.SampleMinecraftItems[index]} to be in the items returned by clear_inventory")
            index += 1

        self.assertEqual(index, len(self.SampleMinecraftItems), f"Expected to have {len(self.SampleMinecraftItems)} items but got {index}")

        self.assertEqual(len(steve.inventory), 0, f"Expected inventory to be empty but got {len(steve.inventory)}")

    def test_minecraft_checklist_init(self):
        """
        #name(Test the MinecraftBlock constructor)
        #score(1)
        """
        blocks = ArrayR(len(self.SampleMinecraftBlocks))
        for i in range(len(self.SampleMinecraftBlocks)):
            blocks[i] = self.SampleMinecraftBlocks[i]
        checklist = MinecraftChecklist(blocks)

        self.assertEqual(len(self.SampleMinecraftBlocks), len(checklist),
                         f"Expected to have {len(self.SampleMinecraftBlocks)} blocks but got {len(checklist)}")

        for i in range(len(self.SampleMinecraftBlocks)):
            self.assertIn(self.SampleMinecraftBlocks[i], checklist,
                          f"Expected {self.SampleMinecraftBlocks[i]} to be in the checklist")

    def test_add_block(self):
        """
        #name(Test the add_block method)
        #score(1)
        """
        blocks = ArrayR(len(self.SampleMinecraftBlocks))
        for i in range(len(self.SampleMinecraftBlocks)):
            blocks[i] = self.SampleMinecraftBlocks[i]
        checklist = MinecraftChecklist(blocks)
        new_item = MinecraftItem("New Item", "A new item.", 10)
        new_block = MinecraftBlock("New Block", "A new block.", 99, new_item)
        checklist.add_block(new_block)

        self.assertEqual(len(checklist), len(self.SampleMinecraftBlocks) + 1,
                         f"Expected to have {len(self.SampleMinecraftBlocks) + 1} blocks but got {len(checklist)}")
        self.assertIn(new_block, checklist, f"Expected {new_block} to be in the checklist")

    def test_remove_block(self):
        """
        #name(Test the remove_block method)
        #score(1)
        """
        blocks = ArrayR(len(self.SampleMinecraftBlocks))
        for i in range(len(self.SampleMinecraftBlocks)):
            blocks[i] = self.SampleMinecraftBlocks[i]
        checklist = MinecraftChecklist(blocks)

        block_to_remove = self.SampleMinecraftBlocks[0]
        checklist.remove_block(block_to_remove)

        self.assertEqual(len(checklist), len(self.SampleMinecraftBlocks) - 1,
                         f"Expected to have {len(self.SampleMinecraftBlocks) - 1} blocks but got {len(checklist)}")
        self.assertNotIn(block_to_remove, checklist, f"Expected {block_to_remove} to be removed from the checklist")


    def test_get_sorted_blocks(self):
        """
        #name(Test the get_sorted_blocks method)
        #score(1)
        """
        blocks = ArrayR(len(self.SampleMinecraftBlocks))
        for i in range(len(self.SampleMinecraftBlocks)):
            blocks[i] = self.SampleMinecraftBlocks[i]
        checklist = MinecraftChecklist(blocks)

        sorted_blocks = checklist.get_sorted_blocks()
        sorted_expected = [
            MinecraftBlock("Coal Ore", "A block containing coal.", 3, self.SampleMinecraftItems[2]),
            MinecraftBlock("Iron Ore", "A block containing iron.", 4, self.SampleMinecraftItems[1]),
            MinecraftBlock("Gold Ore", "A block containing gold.", 5, self.SampleMinecraftItems[4]),
            MinecraftBlock("Diamond Ore", "A block containing diamonds.", 5, self.SampleMinecraftItems[0]),
            MinecraftBlock("Netherite Ore", "A block containing netherite.", 5, self.SampleMinecraftItems[3]),
        ]

        self.assertEqual(len(sorted_expected), len(sorted_blocks),
                         f"Expected to have {len(sorted_expected)} blocks but got {len(sorted_blocks)}")

        for i in range(len(sorted_expected)):
            self.assertEqual(sorted_expected[i], sorted_blocks[i],
                             f"Expected the next block to be {sorted_expected[i]}")

    def test_get_optimal_blocks_unsorted(self):
        """
        #name(Test the get_optimal_blocks method)
        #score(1)
        """
        blocks = ArrayR(len(self.SampleMinecraftBlocks))
        for i in range(len(self.SampleMinecraftBlocks)):
            blocks[i] = self.SampleMinecraftBlocks[i]
        checklist = MinecraftChecklist(blocks)

        optimal_blocks = checklist.get_optimal_blocks(self.SampleMinecraftBlocks[len(self.SampleMinecraftBlocks) - 1],
                                                      self.SampleMinecraftBlocks[1])
        optimal_expected = [
            MinecraftBlock("Iron Ore", "A block containing iron.", 4, self.SampleMinecraftItems[1]),
            MinecraftBlock("Gold Ore", "A block containing gold.", 5, self.SampleMinecraftItems[4])
        ]

        self.assertEqual(len(optimal_expected), len(optimal_blocks),
                         f"Expected to have {len(optimal_expected)} blocks but got {len(optimal_blocks)}")

        for i in range(len(optimal_expected)):
            self.assertIn(optimal_expected[i], optimal_blocks, f"Expected to have {optimal_expected[i]}")

    def test_get_optimal_blocks_sorted(self):
        """
        #name(Test the get_optimal_blocks method)
        #score(1)
        """
        blocks = ArrayR(len(self.SampleMinecraftBlocks))
        for i in range(len(self.SampleMinecraftBlocks)):
            blocks[i] = self.SampleMinecraftBlocks[i]
        checklist = MinecraftChecklist(blocks)

        optimal_blocks = checklist.get_optimal_blocks(self.SampleMinecraftBlocks[len(self.SampleMinecraftBlocks) - 1],
                                                      self.SampleMinecraftBlocks[0])
        optimal_expected = [
            MinecraftBlock("Iron Ore", "A block containing iron.", 4, self.SampleMinecraftItems[1]),
            MinecraftBlock("Gold Ore", "A block containing gold.", 5, self.SampleMinecraftItems[4]),
            MinecraftBlock("Diamond Ore", "A block containing diamonds.", 5, self.SampleMinecraftItems[0]),
        ]

        self.assertEqual(len(optimal_expected), len(optimal_blocks),
                         f"Expected to have {len(optimal_expected)} blocks but got {len(optimal_blocks)}")

        for i in range(len(optimal_expected)):
            self.assertEqual(optimal_expected[i], optimal_blocks[i],
                             f"Expected the next block to be {optimal_expected[i]}")


class TestTask2Approach(TestTask2Setup):
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
