from unittest import TestCase

from cave_system import CaveSystem, CaveNode
from minecraft_block import MinecraftBlock, MinecraftItem
from minecraft_checklist import MinecraftChecklist
from not_minecraft import NotMinecraft
from random_gen import RandomGen
from tests.helper import convert_inbuiltlist_to_arrayList, convert_inbuiltlist_to_arrayR


class TestTask3Setup(TestCase):
    def setUp(self):
        """
        Sets up the test environment for Task 3.
        This includes creating a small cave system, a large cave system, and a cave system with multiple neighbours.
        """
        self.setUpSmallCave()
        self.setUpLargeCave()
        self.setupMultipleNeighbourCaveSystem()

    def setUpSmallCave(self):
        # Sample Items
        sample_items = [
            MinecraftItem("Coal", "Common fuel source.", 2),
            MinecraftItem("Iron", "Useful for tools and armor.", 10),
            MinecraftItem("Gold", "Rare material for trading.", 15),
            MinecraftItem("Diamond", "Precious gem for strongest tools.", 50),
        ]

        # Sample Blocks
        sample_blocks = [
            MinecraftBlock("Coal Ore", "Contains coal.", 1, sample_items[0]),
            MinecraftBlock("Iron Ore", "Contains iron.", 3, sample_items[1]),
            MinecraftBlock("Gold Ore", "Contains gold.", 2, sample_items[2]),
            MinecraftBlock("Diamond Ore", "Contains diamond.", 4, sample_items[3]),
        ]

        # Sample CaveNodes
        node1 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[0], sample_blocks[1]]), name=f"Node 1")  # Coal Iron
        node2 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[1], sample_blocks[2], sample_blocks[3]]),
                         name=f"Node 2")  # Iron Gold Diamond
        node3 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[2]]), name=f"Node 3")  # Gold
        node4 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[3], sample_blocks[3]]), name=f"Node 4")  # Diamond Diamond

        # Connect CaveNodes
        node1.connect(node2)  # node1 - node2
        node2.connect(node3)  # node2 - node3
        node2.connect(node4)  # node2 - node4

        # Create CaveSystem
        self.small_cave_system_blocks = sample_blocks
        self.small_cave_system = CaveSystem(cave_node=node1, number_of_nodes=4)
        self.small_cave_system_nodes = [node1, node2, node3, node4]

    def setUpLargeCave(self):
        # Sample Items
        sample_items = [
            MinecraftItem("Coal", "Common fuel source.", 2),
            MinecraftItem("Iron", "Useful for tools and armor.", 10),
            MinecraftItem("Gold", "Rare material for trading.", 15),
            MinecraftItem("Diamond", "Precious gem for strongest tools.", 50),
            MinecraftItem("Redstone", "Useful for advanced machines.", 5),
            MinecraftItem("Lapis Lazuli", "Useful for enchanting.", 7),
            MinecraftItem("Emerald", "Rare for trading with villagers.", 30),
        ]

        # Sample Blocks
        sample_blocks = [
            MinecraftBlock("Coal Ore", "Contains coal.", 1, sample_items[0]),
            MinecraftBlock("Iron Ore", "Contains iron.", 3, sample_items[1]),
            MinecraftBlock("Gold Ore", "Contains gold.", 2, sample_items[2]),
            MinecraftBlock("Diamond Ore", "Contains diamond.", 4, sample_items[3]),
            MinecraftBlock("Redstone Ore", "Contains redstone.", 2, sample_items[4]),
            MinecraftBlock("Lapis Ore", "Contains lapis lazuli.", 2, sample_items[5]),
            MinecraftBlock("Emerald Ore", "Contains emerald.", 5, sample_items[6]),
        ]

        # Sample CaveNodes
        node1 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[0]]), name=f"Node 1")  # Coal
        node2 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[1], sample_blocks[0]]), name=f"Node 2")  # Iron Coal
        node3 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[2], sample_blocks[3], sample_blocks[0]]),
                         name=f"Node 3")  # Gold Diamond Coal
        node4 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[3]]), name=f"Node 4")  # Diamond
        node5 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[4]]), name=f"Node 5")  # Redstone
        node6 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[5]]), name=f"Node 6")  # Lapis
        node7 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks[6], sample_blocks[3]]), name=f"Node 7")  # Emerald Diamond

        # Connect CaveNodes
        node1.connect(node2)  # Coal <-> Iron
        node1.connect(node3)  # Coal <-> Gold
        node2.connect(node4)  # Iron <-> Diamond
        node2.connect(node5)  # Iron <-> Redstone
        node3.connect(node6)  # Gold <-> Lapis
        node4.connect(node7)  # Diamond <-> Emerald

        # Create CaveSystem
        self.large_cave_system_blocks = sample_blocks
        self.larger_cave_system = CaveSystem(cave_node=node1, number_of_nodes=7)
        self.large_cave_system_nodes = [node1, node2, node3, node4, node5, node6, node7]

    def setupMultipleNeighbourCaveSystem(self):
        # Sample Items (another set)
        sample_items_3 = [
            MinecraftItem("Ruby", "Extremely rare gem.", 18),
            MinecraftItem("Silver", "Shiny metal used for trade.", 9),
            MinecraftItem("Sapphire", "Blue precious stone.", 14),
            MinecraftItem("Topaz", "Golden-yellow gem.", 11),
            MinecraftItem("Onyx", "Dark gemstone.", 13),
            MinecraftItem("Granite", "Common rock.", 3),
        ]

        # Sample Blocks
        sample_blocks_3 = [
            MinecraftBlock("Ruby Ore", "Contains rubies.", 4, sample_items_3[0]),
            MinecraftBlock("Silver Ore", "Contains silver.", 3, sample_items_3[1]),
            MinecraftBlock("Sapphire Ore", "Contains sapphires.", 4, sample_items_3[2]),
            MinecraftBlock("Topaz Ore", "Contains topaz.", 3, sample_items_3[3]),
            MinecraftBlock("Onyx Ore", "Contains onyx.", 5, sample_items_3[4]),
            MinecraftBlock("Granite Block", "Common rock.", 2, sample_items_3[5]),
        ]

        # Sample CaveNodes
        hub = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks_3[0]]), name=f"Node 1")  # Ruby - main hub
        room2 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks_3[1]]), name=f"Node 2")  # Silver
        room3 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks_3[2]]), name=f"Node 3")  # Sapphire
        room4 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks_3[3]]), name=f"Node 4")  # Topaz
        room5 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks_3[4]]), name=f"Node 5")  # Onyx
        room6 = CaveNode(blocks=convert_inbuiltlist_to_arrayList([sample_blocks_3[5]]), name=f"Node 6")  # Granite

        # Connect the Hub Room to all others (hub structure!)
        hub.connect(room2)
        hub.connect(room3)
        hub.connect(room4)
        hub.connect(room5)
        hub.connect(room6)

        # Some extra random connections between side rooms
        room2.connect(room3)
        room4.connect(room5)
        room5.connect(room6)

        # Create CaveSystem
        self.multiple_neighbour_cave_system_blocks = sample_blocks_3
        self.hub_cave_system = CaveSystem(cave_node=hub, number_of_nodes=6)
        self.multiple_neighbour_cave_system_nodes = [hub, room2, room3, room4, room5, room6]


class TestTask3(TestTask3Setup):
    def test_attributes(self):
        """
        #name(Test the attributes of NotMinecraft class.)
        #score(1)
        """
        checklist = MinecraftChecklist(convert_inbuiltlist_to_arrayR(self.small_cave_system_blocks))
        not_minecraft = NotMinecraft(self.small_cave_system, checklist)
        self.assertTrue(hasattr(not_minecraft, "cave_system"), "NotMinecraft should have a cave_system attribute.")
        self.assertTrue(hasattr(not_minecraft, "checklist"), "NotMinecraft should have a checklist attribute.")
        self.assertTrue(hasattr(not_minecraft, "miner"), "NotMinecraft should have a miner attribute.")

        self.assertEqual(not_minecraft.miner.name, "Steve", "Miner's name should be 'Steve'.")
        self.assertEqual(not_minecraft.cave_system, self.small_cave_system,
                         "Cave system should be the same as the one passed in.")
        self.assertEqual(not_minecraft.checklist, checklist,
                         "Checklist should be the same as the one passed in.")

    def test_dfs_small_cave_system(self):
        """
        #name(Test the DFS exploration of a small cave system.)
        #score(1)
        """
        not_minecraft = NotMinecraft(self.small_cave_system, MinecraftChecklist(convert_inbuiltlist_to_arrayR([])))
        blocks = not_minecraft.dfs_explore_cave()
        expect_blocks = [item for node in self.small_cave_system_nodes for item in node.blocks]
        self.assertEqual(len(expect_blocks), len(blocks),
                         f"Expected {len(expect_blocks)} blocks, but got {len(blocks)}.")

        for i in range(len(blocks)):
            self.assertEqual(expect_blocks[i], blocks[i],
                             f"Expected block {expect_blocks[i]} at index {i}, but got {blocks[i]}.")

    def test_dfs_large_cave_system(self):
        """
        #name(Test the DFS exploration of a large cave system.)
        #score(1)
        """
        not_minecraft = NotMinecraft(self.larger_cave_system, MinecraftChecklist(convert_inbuiltlist_to_arrayR([])))
        blocks = not_minecraft.dfs_explore_cave()
        expect_blocks = [item for node in self.large_cave_system_nodes for item in node.blocks]
        self.assertEqual(len(expect_blocks), len(blocks),
                         f"Expected {len(expect_blocks)} blocks, but got {len(blocks)}.")

        dfs_order = [
            self.large_cave_system_nodes[0],
            self.large_cave_system_nodes[1],
            self.large_cave_system_nodes[3],
            self.large_cave_system_nodes[6],
            self.large_cave_system_nodes[4],
            self.large_cave_system_nodes[2],
            self.large_cave_system_nodes[5]
        ]
        expect_blocks = [item for node in dfs_order for item in node.blocks]

        for i in range(len(blocks)):
            self.assertEqual(expect_blocks[i], blocks[i],
                             f"Expected block {expect_blocks[i]} at index {i}, but got {blocks[i]}.")

    def test_dfs_multiple_neighbour_cave_system(self):
        """
        #name(Test the DFS exploration of a cave system with multiple neighbours.)
        #score(1)
        """
        not_minecraft = NotMinecraft(self.hub_cave_system, MinecraftChecklist(convert_inbuiltlist_to_arrayR([])))
        blocks = not_minecraft.dfs_explore_cave()
        expect_blocks = [item for node in self.multiple_neighbour_cave_system_nodes for item in node.blocks]
        self.assertEqual(len(expect_blocks), len(blocks),
                         f"Expected {len(expect_blocks)} blocks, but got {len(blocks)}.")

        dfs_order = [
            self.multiple_neighbour_cave_system_nodes[0],
            self.multiple_neighbour_cave_system_nodes[1],
            self.multiple_neighbour_cave_system_nodes[2],
            self.multiple_neighbour_cave_system_nodes[3],
            self.multiple_neighbour_cave_system_nodes[4],
            self.multiple_neighbour_cave_system_nodes[5]
        ]
        expect_blocks = [item for node in dfs_order for item in node.blocks]

        for i in range(len(blocks)):
            self.assertEqual(expect_blocks[i], blocks[i],
                             f"Expected block {expect_blocks[i]} at index {i}, but got {blocks[i]}.")

    def test_small_cave_system_objective_mining(self):
        """
        #name(Test the objective mining functionality for small cave system.)
        #score(1)
        """
        checklist = MinecraftChecklist(convert_inbuiltlist_to_arrayR(self.small_cave_system_blocks))
        not_minecraft = NotMinecraft(self.small_cave_system, checklist)
        blocks = not_minecraft.dfs_explore_cave()
        custom_item_1 = MinecraftItem("Custom Item 1", "Custom item 1 description.", 5)
        custom_item_2 = MinecraftItem("Custom Item 2", "Custom item 2 description.", 200)
        block1 = MinecraftBlock("Custom Block 1", "Custom block 1 description.", 2, custom_item_1)
        block2 = MinecraftBlock("Custom Block 2", "Custom block 2 description.", 3, custom_item_2)

        RandomGen.set_seed(123)
        not_minecraft.objective_mining_summary(blocks, block1, block2)

        expected_mined_blocks = [
            self.small_cave_system_blocks[3],
            self.small_cave_system_blocks[3],
            self.small_cave_system_blocks[3],
            self.small_cave_system_blocks[2],
            self.small_cave_system_blocks[2],
            self.small_cave_system_blocks[1],
            self.small_cave_system_blocks[1]
        ]

        self.assertEqual(len(expected_mined_blocks), len(not_minecraft.miner.inventory),
                         f"Expected {len(expected_mined_blocks)} blocks, but got {len(not_minecraft.miner.inventory)}.")

        for i in range(len(not_minecraft.miner.inventory)):
            self.assertEqual(expected_mined_blocks[i].item, not_minecraft.miner.inventory[i],
                             f"Expected block {expected_mined_blocks[i].item} at index {i}, but got {not_minecraft.miner.inventory[i]}.")

    def test_large_cave_system_objective_mining(self):
        """
        #name(Test the objective mining functionality for large cave system.)
        #score(1)
        """
        checklist = MinecraftChecklist(convert_inbuiltlist_to_arrayR(self.large_cave_system_blocks))
        not_minecraft = NotMinecraft(self.larger_cave_system, checklist)
        blocks = not_minecraft.dfs_explore_cave()
        custom_item_1 = MinecraftItem("Custom Item 1", "Custom item 1 description.", 5)
        custom_item_2 = MinecraftItem("Custom Item 2", "Custom item 2 description.", 100)
        block1 = MinecraftBlock("Custom Block 1", "Custom block 1 description.", 2, custom_item_1)
        block2 = MinecraftBlock("Custom Block 2", "Custom block 2 description.", 3, custom_item_2)

        RandomGen.set_seed(124)
        not_minecraft.objective_mining_summary(blocks, block1, block2)
        expected_mined_blocks = [
            self.large_cave_system_blocks[3],
            self.large_cave_system_blocks[3],
            self.large_cave_system_blocks[3],
            self.large_cave_system_blocks[2],
            self.large_cave_system_blocks[6],
            self.large_cave_system_blocks[5],
            self.large_cave_system_blocks[1]
        ]

        self.assertEqual(len(expected_mined_blocks), len(not_minecraft.miner.inventory),
                         f"Expected {len(expected_mined_blocks)} blocks, but got {len(not_minecraft.miner.inventory)}.")

        for i in range(len(not_minecraft.miner.inventory)):
            self.assertEqual(expected_mined_blocks[i].item, not_minecraft.miner.inventory[i],
                             f"Expected block {expected_mined_blocks[i].item} at index {i}, but got {not_minecraft.miner.inventory[i]}.")

    def test_multiple_neighbour_cave_system_objective_mining(self):
        """
        #name(Test the objective mining functionality for multiple neighbour cave system.)
        #score(1)
        """
        checklist = MinecraftChecklist(convert_inbuiltlist_to_arrayR(self.multiple_neighbour_cave_system_blocks))
        not_minecraft = NotMinecraft(self.hub_cave_system, checklist)
        blocks = not_minecraft.dfs_explore_cave()
        custom_item_1 = MinecraftItem("Custom Item 1", "Custom item 1 description.", 5)
        custom_item_2 = MinecraftItem("Custom Item 2", "Custom item 2 description.", 200)
        block1 = MinecraftBlock("Custom Block 1", "Custom block 1 description.", 2, custom_item_1)
        block2 = MinecraftBlock("Custom Block 2", "Custom block 2 description.", 3, custom_item_2)

        RandomGen.set_seed(125)
        not_minecraft.objective_mining_summary(blocks, block1, block2)

        expected_mined_blocks = [
            self.multiple_neighbour_cave_system_blocks[0],
            self.multiple_neighbour_cave_system_blocks[3],
            self.multiple_neighbour_cave_system_blocks[2],
            self.multiple_neighbour_cave_system_blocks[1],
            self.multiple_neighbour_cave_system_blocks[4],
        ]

        self.assertEqual(len(expected_mined_blocks), len(not_minecraft.miner.inventory),
                         f"Expected {len(expected_mined_blocks)} blocks, but got {len(not_minecraft.miner.inventory)}.")

        for i in range(len(not_minecraft.miner.inventory)):
            self.assertEqual(expected_mined_blocks[i].item, not_minecraft.miner.inventory[i],
                             f"Expected block {expected_mined_blocks[i].item} at index {i}, but got {not_minecraft.miner.inventory[i]}.")

    def test_small_cave_system_profit_mining(self):
        """
        #name(Test the profit mining functionality for small cave system.)
        #score(1)
        """
        checklist = MinecraftChecklist(convert_inbuiltlist_to_arrayR(self.small_cave_system_blocks))
        not_minecraft = NotMinecraft(self.small_cave_system, checklist)
        blocks = not_minecraft.dfs_explore_cave()
        unexpected_item = MinecraftItem("Unexpected Item", "Unexpected item description.", 100)
        unexpected_block = MinecraftBlock("Unexpected Block", "Unexpected block description.", 1, unexpected_item)
        blocks.append(unexpected_block)

        RandomGen.set_seed(126)
        not_minecraft.profit_mining(blocks, 10)

        expected_mined_blocks = [
            unexpected_block,
            self.small_cave_system_blocks[3],
            self.small_cave_system_blocks[3],
            self.small_cave_system_blocks[0]
        ]

        self.assertEqual(len(expected_mined_blocks), len(not_minecraft.miner.inventory),
                         f"Expected {len(expected_mined_blocks)} blocks, but got {len(not_minecraft.miner.inventory)}.")

        for i in range(len(not_minecraft.miner.inventory)):
            self.assertEqual(expected_mined_blocks[i].item, not_minecraft.miner.inventory[i],
                             f"Expected block {expected_mined_blocks[i].item} at index {i}, but got {not_minecraft.miner.inventory[i]}.")

    def test_large_cave_system_profit_mining(self):
        """
        #name(Test the profit mining functionality for large cave.)
        #score(1)
        """
        checklist = MinecraftChecklist(convert_inbuiltlist_to_arrayR(self.large_cave_system_blocks))
        not_minecraft = NotMinecraft(self.larger_cave_system, checklist)
        blocks = not_minecraft.dfs_explore_cave()
        unexpected_item = MinecraftItem("Unexpected Item", "Unexpected item description.", 100)
        unexpected_block = MinecraftBlock("Unexpected Block", "Unexpected block description.", 7, unexpected_item)
        blocks.append(unexpected_block)

        RandomGen.set_seed(127)
        not_minecraft.profit_mining(blocks, 19)

        expected_mined_blocks = [
            unexpected_block,
            self.large_cave_system_blocks[3],
            self.large_cave_system_blocks[3],
            self.large_cave_system_blocks[3],
        ]

        self.assertEqual(len(expected_mined_blocks), len(not_minecraft.miner.inventory),
                         f"Expected {len(expected_mined_blocks)} blocks, but got {len(not_minecraft.miner.inventory)}.")

        for i in range(len(not_minecraft.miner.inventory)):
            self.assertEqual(expected_mined_blocks[i].item, not_minecraft.miner.inventory[i],
                             f"Expected block {expected_mined_blocks[i].item} at index {i}, but got {not_minecraft.miner.inventory[i]}.")

    def test_multiple_neighbour_cave_system_profit_mining(self):
        """
        #name(Test the profit mining functionality for multiple neighbour cave system.)
        #score(1)
        """
        checklist = MinecraftChecklist(convert_inbuiltlist_to_arrayR(self.multiple_neighbour_cave_system_blocks))
        not_minecraft = NotMinecraft(self.hub_cave_system, checklist)
        blocks = not_minecraft.dfs_explore_cave()
        unexpected_item = MinecraftItem("Unexpected Item", "Unexpected item description.", 100)
        unexpected_block = MinecraftBlock("Unexpected Block", "Unexpected block description.", 24, unexpected_item)
        blocks.append(unexpected_block)

        RandomGen.set_seed(128)
        not_minecraft.profit_mining(blocks, 32)

        expected_mined_blocks = [
            self.multiple_neighbour_cave_system_blocks[0],
            unexpected_block,
            self.multiple_neighbour_cave_system_blocks[3],
        ]

        self.assertEqual(len(expected_mined_blocks), len(not_minecraft.miner.inventory),
                         f"Expected {len(expected_mined_blocks)} blocks, but got {len(not_minecraft.miner.inventory)}.")

        for i in range(len(not_minecraft.miner.inventory)):
            self.assertEqual(expected_mined_blocks[i].item, not_minecraft.miner.inventory[i],
                             f"Expected block {expected_mined_blocks[i].item} at index {i}, but got {not_minecraft.miner.inventory[i]}.")

    def test_clear_inventory_profit(self):
        """
        #name(Test the clear_inventory method after profit mining.)
        #score(1)
        """
        checklist = MinecraftChecklist(convert_inbuiltlist_to_arrayR(self.multiple_neighbour_cave_system_blocks))
        not_minecraft = NotMinecraft(self.hub_cave_system, checklist)
        blocks = not_minecraft.dfs_explore_cave()
        unexpected_item = MinecraftItem("Unexpected Item", "Unexpected item description.", 100)
        unexpected_block = MinecraftBlock("Unexpected Block", "Unexpected block description.", 24, unexpected_item)
        blocks.append(unexpected_block)

        RandomGen.set_seed(128)
        not_minecraft.profit_mining(blocks, 32)

        expected_mined_blocks = [
            self.multiple_neighbour_cave_system_blocks[0],
            unexpected_block,
            self.multiple_neighbour_cave_system_blocks[3],
        ]
        actual_mined_blocks = not_minecraft.miner.clear_inventory()

        index = 0
        for i in actual_mined_blocks:
            self.assertEqual(expected_mined_blocks[index].item, i,
                             f"Expected block {expected_mined_blocks[index].item} at index {index}, but got {i}.")
            index += 1

        self.assertEqual(index, len(expected_mined_blocks),
                         f"Expected {len(expected_mined_blocks)} blocks, but got {index}.")

        self.assertEqual(len(not_minecraft.miner.inventory), 0,
                         f"Miner's Inventory should be empty after clear_inventory().")
