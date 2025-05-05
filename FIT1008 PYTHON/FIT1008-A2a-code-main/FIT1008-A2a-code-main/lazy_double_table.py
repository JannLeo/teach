from __future__ import annotations

from data_structures.referential_array import ArrayR
from data_structures.abstract_hash_table import HashTable
from typing import TypeVar


V = TypeVar('V')


class LazyDoubleTable(HashTable[str, V]):
    """
    Lazy Double Table uses double hashing to resolve collisions, and implements lazy deletion.

    Feel free to check out the implementation of the LinearProbeTable class if you need to remind
    yourself how to implement the methods of this class.

    Type Arguments:
        - V: Value Type.
    """
    
    # No test case should exceed 1 million entries.
    TABLE_SIZES = (5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869)
    HASH_BASE = 31
    DELETED = object()
    FIRST_DELETE_NONE = -1

    def __init__(self, sizes = None) -> None:
        """
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes

        self.size_index = 0
        self.array = ArrayR(self.TABLE_SIZES[self.__size_index])
        self.length = 0
    
    @property
    def table_size(self) -> int:
        return len(self.__array)

    def __len__(self) -> int:
        """
        Returns the number of elements in the hash table
        """
        return self.__length

    def keys(self) -> ArrayR[str]:
        """
        Returns all keys in the hash table.
        
        If you need to use this function, you will probably need to update its
        implementation according to how you implemented the lazy deletion.

        :complexity: O(N + S) where N is the number of items in the table and S is the table size.
        """
        key_res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None:
                key_res[i] = self.__array[x][0]
                i += 1
        return key_res

    def values(self) -> ArrayR[V]:
        """
        Returns all values in the hash table.

        If you need to use this function, you will probably need to update its
        implementation according to how you implemented the lazy deletion.

        :complexity: O(N + S) where N is the number of items in the table and S is the table size.
        """
        res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None:
                res[i] = self.__array[x][1]
                i += 1
        return res

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See __getitem__.
        """
        for i in range(self.table_size):
            item = self.__array[i]
            if item is not None and item is not self.__deleted:
                if item[0] == key:
                    return True
        # try:
        #     _ = self[key]
        # except KeyError:
        #     return False
        # else:
        #     return True

    def __getitem__(self, key: str) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self.__hashy_probe(key, False)
        item = self.__array[position]
        if item is None or item is self.DELETED:
            raise KeyError(key)
        return item[1]
    
    def is_empty(self) -> bool:
        return self.__length == 0
    
    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        """
        result = ""
        for item in self.__array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result

    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        :complexity: O(K) where K is the length of the key.
        """
        value = 0

        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: str) -> int:
        """
        Used to determine the step size for our hash table.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        prime = 109345121
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % prime
            a = a * self.HASH_BASE % (prime - 1)
        
        number = prime - (value % prime)
        if number % 2 == 0:
            number += 1
        return number

        #raise NotImplementedError

    def __hashy_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using hashy probing.

        Raises:
            KeyError: When the key is not in the table, but is_insert is False.
            RuntimeError: When a table is full and cannot be inserted.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        # Initial position
        initial_position = self.hash(key)
        current_position = initial_position
        number = self.hash2(key)
        first_deleted = self.FIRST_DELETE_NONE

        for i in range(self.table_size):
            item = self.__array[current_position]
            
            if item is None:
                if is_insert and first_deleted != self.FIRST_DELETE_NONE:
                    return first_deleted
                return current_position
            
            elif item is self.DELETED:
                if first_deleted == self.FIRST_DELETE_NONE:
                    first_deleted = current_position

            elif item[0] == key:
                return current_position
            
            current_position = (current_position + number) % self.table_size

            if current_position == initial_position:
                break
        
        if is_insert:
            self.__rehash()
            return self.__hashy_probe(key, True)
        else:
            raise KeyError(key)
        

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set a (key, value) pair in our hash table.

        Remember! This is where you will need to call __rehash if the table is full!
        
        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        if self.__length >= self.table_size * 2 // 3:
            self.__rehash()

        position = self.__hashy_probe(key, True)

        if self.__array[position] is None or self.__array[position] is self.DELETED:
            self.__length += 1

        self.__array[position] = (key, data)


    def __delitem__(self, key: str) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        position = self.__hashy_probe(key, False)
        if self.__array[position] is None or self.__array[position] is self.DELETED:
            raise KeyError(key)
        
        self.__array[position] = self.DELETED
        self.__length -= 1

    def __rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        old_array = self.__array
        self.__size_index += 1

        if self.__size_index >= len(self.TABLE_SIZES):
            new_size = self.table_size * 2 + 1
        else:
            new_size = self.TABLE_SIZES[self.__size_index]

        self.__array = ArrayR(new_size)
        self.__length = 0

        for item in old_array:
            if item is not None and item is not self.DELETED:
                self[item[0]] = item[1]

