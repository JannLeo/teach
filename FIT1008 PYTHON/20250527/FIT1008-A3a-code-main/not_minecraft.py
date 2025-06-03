from __future__ import annotations
from cave_system import CaveSystem
from data_structures import ArrayList, ArraySet
from minecraft_block import MinecraftBlock
from minecraft_checklist import MinecraftChecklist
from random_gen import RandomGen
from miner import Miner
from algorithms.mergesort import mergesort


class NotMinecraft:
    """
    A class representing a NotMinecraft game.
    """
    LATS_INDEX = -1

    def __init__(self, cave_system: CaveSystem, checklist: MinecraftChecklist) -> None:
        """
        Initializes the NotMinecraft game.
        Args:
            cave_system (CaveSystem): The cave system for the game.
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        Justification:
            type check and attribute assignment all constant time operation
        """
        if not isinstance(cave_system, CaveSystem):
            raise TypeError(f"CaveSystem, got {type(cave_system).__name__}")
        
        if not isinstance(checklist, MinecraftChecklist):
            raise TypeError(f"MinecraftChecklist, got {type(checklist).__name__}")
        
        self.cave_system = cave_system
        self.checklist = checklist
        self.miner = Miner('Steve')      # initialise a miner object


    def dfs_explore_cave(self) -> ArrayList[MinecraftBlock]:
        """
        Performs a depth-first search (DFS) to explore the cave system and collect blocks.
        Returns:
            ArrayList[MinecraftBlock]: A list of collected blocks.
        Complexity:
            Not required
        """
        # ArraySet record the node that already visited
        visited = ArraySet(len(self.cave_system))    # return number of node
        collected = ArrayList()

        def dfs(node):
            visited.add(node)      # mark current node already visited

            for block in node.blocks:   # add every MinecraftBlock contained current node collected
                collected.append(block)

            for neighbour in node.neighbours:    #all neighbour nodes, continue dfs if not visited yet
                if neighbour not in visited:
                    dfs(neighbour)

        dfs(self.cave_system.entrance)
        return collected

    def objective_mining_filter(self, blocks: ArrayList[MinecraftBlock], block1: MinecraftBlock,
                                block2: MinecraftBlock) -> ArrayList:
        """
        Given a list of blocks, filter the blocks that should be considered according to scenario 1.
        Args:
            blocks (ArrayList[MinecraftBlock]): The list of blocks to mine.
            block1 (MinecraftBlock): Filtered blocks should have a ratio of value to mining time > block1.
            block2 (MinecraftBlock): Filtered blocks should have a ratio of value to mining time < block2.
        Complexity:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
        Justification:
            n = the number of elements in blocks
            for loop O(n) ratio calculate O(1), then check whether in the checklist(hash set) O(1) append O(1)

        """
        if not isinstance(blocks, ArrayList):
            raise TypeError(f"ArrayList[MinecraftBlock], got {type(blocks).__name__}")
        if not isinstance(block1, MinecraftBlock):
            raise TypeError(f"Block1 MinecraftBlock, got {type(block1).__name__}")
        if not isinstance(block2, MinecraftBlock):
            raise TypeError(f"Block2 MinecraftBlock, got {type(block2).__name__}")

        # calculate the value/hardness ratio of block1 and block2
        ratio1 = block1.item.value / block1.hardness
        ratio2 = block2.item.value / block2.hardness
        lower, upper = min(ratio1, ratio2), max(ratio1, ratio2)      # ensure that lower <= upper

        filtered = ArrayList()      # used to store blocks that meet requirements

        for block in blocks:      # traverse all the blocks

            if not isinstance(block, MinecraftBlock):
                raise TypeError(f"Found non-MinecraftBlock in blocks: {type(block).__name__}")
            
            ratio = block.item.value / block.hardness
            if block in self.checklist and lower < ratio < upper:    # if block meets both conditions
                filtered.append(block)    #append
        return filtered

    def objective_mining(self, blocks: ArrayList[MinecraftBlock]) -> None:
        """
        Mines the cave system to achieve the objective of collecting blocks.
        Complexity:
            Best Case Complexity: O(nlogn)
            Worst Case Complexity: O(nlogn)
        Justification:
            mergesort sort list of length n O(nlogn), traverse the sorted results in reverse order O(n)
            but O(nlogn) + O(n) = O(nlogn)
        """
        if not isinstance(blocks, ArrayList):
            raise TypeError(f"ArrayList[MinecraftBlock], got {type(blocks).__name__}")
        
        sorted_blocks = mergesort(blocks, key=lambda x: x.item.value / x.hardness)

        #traverse sorted_blocks reverse order and process downward start from highest ratio
        for i in range(len(sorted_blocks) + self.LATS_INDEX, self.LATS_INDEX, self.LATS_INDEX):
            self.miner.mine(sorted_blocks[i])


    def objective_mining_summary(self, blocks: ArrayList[MinecraftBlock], block1: MinecraftBlock,
                                 block2: MinecraftBlock) -> None:
        """
        Returns the summary of the objective mining.
        This is to explain how objective mining will be called and tested.
        Complexity:
            Not Required
        """
        filtered_blocks = self.objective_mining_filter(blocks, block1, block2)

        self.chicken_jockey_attack(filtered_blocks)

        self.objective_mining(filtered_blocks)

    def profit_mining(self, blocks: ArrayList[MinecraftBlock], time_in_seconds: int) -> None:
        """
        Mines the cave system casually.
        Args:
            blocks (ArrayList[MinecraftBlock]): The list of blocks to mine.
            time_in_seconds (int): The time in seconds to mine.
        Complexity:
            Best Case Complexity: O(nlogn)/O(1)
            Worst Case Complexity: O(nlogn)
        Justification:
        I feel that mergesort needs to be used to sort all the blocks by ratio. only in this way can test them one by one 
        from the highest ratio to the lowest ratio and automatically skip blocks hardness > remaining time O(nlogn) 
        but if time_in_seconds = 0, the time complexity can reach O(1)...
            
        """
        if not isinstance(blocks, ArrayList):
            raise TypeError(f"ArrayList[MinecraftBlock], got {type(blocks).__name__}")
        if not isinstance(time_in_seconds, int):
            raise TypeError(f"time_in_seconds to be int, got {type(time_in_seconds).__name__}")
        if time_in_seconds < 0:
            raise ValueError("time_in_seconds must be non-negative.")

        remaining = time_in_seconds
        sorted_blocks = mergesort(blocks, key=lambda x: x.item.value / x.hardness)    # sort in ascending of ratio

        # eeverse traversal, if hardness of current block time need is less or equal to remaining time then dig. otherwise, skip
        for index in range(len(sorted_blocks) + self.LATS_INDEX, self.LATS_INDEX, self.LATS_INDEX):
            block = sorted_blocks[index]
            if block.hardness <= remaining:
                self.miner.mine(block)
                remaining -= block.hardness
                # keep digg  until time out or the list traversal complet


    def chicken_jockey_attack(self, blocks: ArrayList[MinecraftBlock]) -> None:
        """
        Chicken Jockey Attack
        Args:
            blocks (ArrayList[MinecraftBlock]): The list of blocks to mine.
        Complexity:
            Not required
        """
        RandomGen.random_shuffle(blocks)

    def main(self, scenario: int, **criteriaArgs) -> None:
        """
        Main function to run the NotMinecraft game.
        Args:
            scenario (int): The scenario number to run.
            criteriaArgs (dict): Additional arguments for the scenario.
        Complexity:
            Not required
        Sample Usage:
            not_minecraft = NotMinecraft(cave_system, checklist)
            not_minecraft.main(1, block1=block1, block2=block2)
            not_minecraft.main(2, time_in_seconds=60)
        """
        if scenario == 1:
            blocks = self.dfs_explore_cave()
            self.objective_mining_summary(blocks, **criteriaArgs)
        elif scenario == 2:
            blocks = self.dfs_explore_cave()
            self.profit_mining(blocks, **criteriaArgs)
