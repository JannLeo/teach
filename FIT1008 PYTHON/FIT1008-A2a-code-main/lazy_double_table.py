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

    DELETED = object() #delete marked object

    FIRST_DELETE_NONE = -1  # the first insert can delete position

    def __init__(self, sizes = None) -> None:
        """
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes

        self.__size_index = 0
        self.__array: ArrayR[tuple[str, V]] = ArrayR(self.TABLE_SIZES[self.__size_index])
        self.__length = 0

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
        res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None:
                res[i] = self.__array[x][0]
                i += 1
        return res

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
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
        
    def __getitem__(self, key: str) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        
        position_item = self.__hashy_probe(key, False)
        item = self.__array[position_item]
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
            O(K) where K is the length of the key.
        """
        prime = 324528433123123   #big prime number reduce conflict
        value = 0
        multiplier = 999
        for char in key:
            value = (ord(char) + multiplier * value) % prime
            multiplier = multiplier * self.HASH_BASE % (prime - 1)
        
        number = prime - (value % prime)
        if number % 2 == 0:    # make sure number is odd
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
            Best Case Complexity: O(1) first time is success
            Worst Case Complexity: O(n) need to traverse all the table then success, n is the size of table
        """
        # Initial position
        initial_position = self.hash(key)
        current_position = initial_position
        number = self.hash2(key)

        for i in range(self.table_size):  #the biggest time is table_size
            item = self.__array[current_position]
            
            if item is None:
                if is_insert and self.FIRST_DELETE_NONE != -1:
                    return self.FIRST_DELETE_NONE  # when insert use delete position first
                return current_position  # find empty position
            
            elif item is self.DELETED:
                if self.FIRST_DELETE_NONE == -1:
                    self.FIRST_DELETE_NONE = current_position # get the first reuse position

            elif item[0] == key:
                return current_position   #find target key
              
            current_position = (current_position + number) % self.table_size  #doble hash

            if current_position == initial_position:
                break   #prevent runtimeerror
        
        if is_insert:
            self.__rehash()
            return self.__hashy_probe(key, True)  #after insert re-probe
        else:
            raise KeyError(key)
        

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set a (key, value) pair in our hash table.

        Remember! This is where you will need to call __rehash if the table is full!
        
        Complexity:
            Best Case Complexity: O(1) find empty position and overwrite by __hashy_probe
            Worst Case Complexity: O(n) when the length is > 2/3 then need __rehash, __rehash need O(n)
        """
        if self.__length >= self.table_size * 2 // 3:   #check if need rehash
            self.__rehash()

        position = self.__hashy_probe(key, True)

        if self.__array[position] is None or self.__array[position] is self.DELETED:  # when new key insert update
            self.__length += 1

        self.__array[position] = (key, data)


    def __delitem__(self, key: str) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Complexity:
            Best Case Complexity: O(1) though __hashy_probe the first is need delete
            Worst Case Complexity: O(n) need to traverse all the table then find the item need delete
        """
        position = self.__hashy_probe(key, False)
        if self.__array[position] is None or self.__array[position] is self.DELETED:
            raise KeyError(key)
        
        self.__array[position] = self.DELETED  #mark the position is deleted
        self.__length -= 1

    def __rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
            Best Case Complexity: O(n) necessary to traverse all items in the old table and reinsert the new table
            Worst Case Complexity: O(n) complete hashing and insertion operation need to performed on each item once
        """
        old_array = self.__array  #backup
        self.__size_index += 1

        if self.__size_index >= len(self.TABLE_SIZES):
            new_size = self.table_size * 2 + 1
        else:
            new_size = self.TABLE_SIZES[self.__size_index]

        self.__array = ArrayR(new_size)   # initialize the new array and reset the number
        self.__length = 0

        for item in old_array:     #insert valid items in the old table to new
            if item is not None and item is not self.DELETED:
                self[item[0]] = item[1]

