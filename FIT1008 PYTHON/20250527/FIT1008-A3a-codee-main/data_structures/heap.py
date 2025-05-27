"""Max Heap implemented using an array"""
from __future__ import annotations

__author__ = "Brendon Taylor, modified by Jackson Goerner"
__docformat__ = 'reStructuredText'

from typing import Generic

from data_structures import ArrayList
from data_structures.abstract_list import List
from data_structures.referential_array import ArrayR, T


class MaxHeap(Generic[T]):
    MIN_CAPACITY = 1

    def __init__(self, max_size: int) -> None:
        """
        Args:
            max_size(int): The capacity of the heap

        Complexity:
            Best case complexity: O(n) where n is the size of the heap.
            Worst case complexity: O(n) where n is the size of the heap.
        """
        self.length: int = 0
        self.the_array: ArrayR[T] = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)

    def __len__(self) -> int:
        return self.length

    def is_full(self) -> bool:
        return self.length + 1 == len(self.the_array)

    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position

        Pre-condition:
            1 <= k <= self.length

        Complexity:
            Best case complexity: O(1) - Rising the root element
            Worst case complexity: O(logn) - Rising a leaf element
            n is the number of elements currently in the heap
        """
        item: T = self.the_array[k]
        while k > 1 and item > self.the_array[k // 2]:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        self.the_array[k] = item

    def add(self, element: T) -> None:
        """
        Swaps elements while rising

        Complexity:
            Best case complexity: O(1) - No rising required
            Worst case complexity: O(logn) - New largest element (rises to the root)
            n is the number of elements currently in the heap
        """
        if self.is_full():
            raise IndexError

        self.length += 1
        self.the_array[self.length] = element
        self.rise(self.length)

    def largest_child(self, k: int) -> int:
        """
        Returns the index of k's child with greatest value.

        Pre-condition:
            1 <= k <= self.length // 2

        Complexity:
            O(comp) where comp is the cost of comparing two elements in the heap
        """
        if 2 * k == self.length or \
                self.the_array[2 * k] > self.the_array[2 * k + 1]:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """
        Make the element at index k sink to the correct position.

        Pre-condition:
            1 <= k <= self.length

        Complexity:
            Best case complexity: O(1) - No sinking required
            Worst case complexity: O(logn) - Sinking the root node to the bottom
            n is the number of elements currently in the heap
        """
        item: T = self.the_array[k]

        while 2 * k <= self.length:
            max_child: int = self.largest_child(k)
            if self.the_array[max_child] <= item:
                break
            self.the_array[k] = self.the_array[max_child]
            k = max_child

        self.the_array[k] = item

    def get_max(self) -> T:
        """
            Remove (and return) the maximum element from the heap.

            Complexity:
                Best case complexity: O(logn)
                Worst case complexity: O(logn)
                n is the number of elements currently in the heap
        """
        if self.length == 0:
            raise IndexError

        max_elt = self.the_array[1]
        self.length -= 1
        if self.length > 0:
            self.the_array[1] = self.the_array[self.length + 1]
            self.sink(1)
        return max_elt

    @staticmethod
    def heapify(points: ArrayR[T] | ArrayList[T], overwrite_size: int = 0) -> MaxHeap[T]:
        """
        Complexity:
            Best case complexity: O(n)
            Worst case complexity: O(n)
            n is the number of elements inside points.
        """
        new_heap = MaxHeap(overwrite_size or (2 * len(points) + 2))
        new_heap.length = len(points)
        for i in range(len(points)):
            new_heap.the_array[i + 1] = points[i]
        for k in range(len(points), 0, -1):
            new_heap.sink(k)
        return new_heap


if __name__ == '__main__':
    items = [int(x) for x in input('Enter a list of numbers: ').strip().split()]
    heap = MaxHeap(len(items))

    for item in items:
        heap.add(item)

    while len(heap) > 0:
        print(heap.get_max())
