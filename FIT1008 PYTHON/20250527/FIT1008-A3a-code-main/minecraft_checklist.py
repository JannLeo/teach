from __future__ import annotations
from data_structures import ArrayList, ArrayR, ArraySet
from minecraft_block import MinecraftBlock
from data_structures.bst import BSTInOrderIterator, BinarySearchTree
from betterbst import BetterBST

class MinecraftChecklist:
    def __init__(self, blocks: ArrayR[MinecraftBlock]) -> None:
        """
        Initializes the MinecraftChecklist instance with a list of blocks.

        Complexity:
            Best Case Complexity: O(nlogn)
            Worst Case Complexity: O(nlogn)
        Justification:
            traverse n elements O(n)
            build the balanced tree O(nlogn): BetterBST call internal __sort_elements(temp_list) the length of temp_list is 
            n, mergesort to sort n elements need O(nlogn). call __build_balanced_tree(new_elements) after the sorting is 
            completed, the time complexity also O(nlogn).
        """
        
        try:       # O(1)
            _ = iter(blocks)
        except TypeError:
            raise TypeError(f"MinecraftBlock, but got {type(blocks).__name__}")

        n = len(blocks)    # O(1)
        temp_list = ArrayList()    # used to store (ratio, block)

        capacity = max(1, 2 * n)    # the capacity of ArraySet at least 1 otherwise 2*n
        self.set = ArraySet(capacity)    # O(1)

        for index, block in enumerate(blocks):      # O(n)
            if not isinstance(block, MinecraftBlock):
                raise TypeError(f"Element at {index} not MinecraftBlock: got {type(block).__name__}")
            ratio = block.item.value / block.hardness
            temp_list.append((ratio, block))
            self.set.add(block)     # add the original block to set
 
        if len(temp_list) == 0:
            self.bst = BinarySearchTree()      # O(1) empty tree
        else:
            self.bst = BetterBST(temp_list)   # O(nlogn)
        
        
        '''
        if not isinstance(blocks, MinecraftBlock):
            raise TypeError

        self.blocks = ArrayList()
        for i in range(len(blocks)):
            self.blocks.append(blocks[i])
        '''

    def __contains__(self, item: MinecraftBlock) -> bool:
        """
        Checks if the item is in the checklist.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(n)
        Justification:
            hash distribution is uniform is best case O(1), the worst case, there are hash conflicts O(n)
        """
        if not isinstance(item, MinecraftBlock):    # O(1)
            return False
        return item in self.set    # check HashSet contains this block    


    def __len__(self) -> int:
        """
        Returns the number of blocks in the checklist.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        Justification:
            return the element count in ArraySet directly
        """
        return len(self.set)


    def add_block(self, block: MinecraftBlock) -> None:
        """
        Adds a block to the checklist.

        Complexity:
            Best Case Complexity: O(logn)
            Worst Case Complexity: O(logn)
        Justification:
            self.bst[ratio] = block: insert a new key need search the position in the tree O(logn)(height of the tree)
        """
        if not isinstance(block, MinecraftBlock):    # O(1)
            raise TypeError(f"only add MinecraftBlock, got {type(block).__name__}")

        if block in self.set:     # O(1)/O(n)
            return

        ratio = block.item.value / block.hardness
        self.bst[ratio] = block     # O(logn)
        self.set.add(block)   # O(1)/O(n) add block to HashSet


    def remove_block(self, block: MinecraftBlock) -> None:
        """
        Removes a block from the checklist.

        Complexity:
            Best Case Complexity: O(logn)
            Worst Case Complexity: O(logn)
        Justification:
            del self.bst[ratio]: find the key in the tree O(logn) then delet and rebalance O(logn)
        """
        if not isinstance(block, MinecraftBlock):    # O(1)
            raise TypeError(f"only remove MinecraftBlock, got {type(block).__name__}")

        try:
            self.set.remove(block)
        except KeyError:
            return

        ratio = block.item.value / block.hardness    # O(1)
        del self.bst[ratio]     # O(logn)   delete key from bst


    def get_sorted_blocks(self) -> ArrayR[MinecraftBlock]:
        """
        Returns the sorted blocks in the checklist.
        Complexity:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
        Justification:
            BSTInOrderIterator performs in-order traversal to visiting n nodes in the tree O(n)
            during the traversal process, n times node.item assign to result[idx] O(n)
        """

        n = len(self.bst)
        result = ArrayR(n)
        index = 0

        for node in BSTInOrderIterator(self.bst.root):      #in order traversal the tree
            result[index] = node.item
            index += 1

        return result
    


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
            Best Case Complexity: O(logn)
            Worst Case Complexity: O(n)
        Justification:
            1. calculate the ratio twice O(1)
            2. filter_keys pruning traversal best case  O(logn)    then collect m node
                                             worst case O(n)
            3. arrayR allocation O(m)
            4. copy m elements to arrayR O(m)
            so best = O(1) + O(logn) + O(m) + O(m) because m better approach to 0, no node is suit. so just O(logn)
            worst = O(1) + O(n) + O(n) + O(n) = O(n)
        """
        ratio1 = block1.item.value / block1.hardness
        ratio2 = block2.item.value / block2.hardness
        lower, upper = min(ratio1, ratio2), max(ratio1, ratio2)    # O(1)

        # two filter function
        def filter_func1(ratio):      # O(1)
            return ratio > lower

        def filter_func2(ratio):      # O(1)
            return ratio < upper

        filtered_pairs = self.bst.filter_keys(filter_func1, filter_func2)      # pruning

        m = len(filtered_pairs)    # put m blocks from filtered_pairs to ArrayR
        result = ArrayR(m)
        for index in range(m):
            _, block = filtered_pairs[index]
            result[index] = block

        return result       # return array of blocks in ascending by ratio
    

