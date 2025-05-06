from __future__ import annotations
from datetime import datetime
from data_structures.hash_table_linear_probing import LinearProbeTable


class HashyDateTable(LinearProbeTable[str]):
    """
    HashyDateTable assumed the keys are strings representing dates, and therefore tries to
    produce a balanced, uniform distribution of keys across the table.

    Conflicts are resolved using Linear Probing.
    
    All values will also be strings.
    """
    base_date = datetime(1970, 1, 1)  #give a base data

    def __init__(self) -> None:
        """
        Initialise the Hash Table with with increments of 366 as the table size.
        This means, initially we will have 366 slots, once they are full, we will have 4 * 366 slots, and so on.

        No complexity is required for this function.
        Do not make any changes to this function.
        """
        LinearProbeTable.__init__(self, (366, 4 * 366, 16 * 366))


    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        The key will always be exactly 10 characters long and can be any of these formats, but nothing else:
        - DD/MM/YYYY
        - DD-MM-YYYY
        - YYYY/MM/DD
        - YYYY-MM-DD

        The function assumes the dates will always be valid i.e. the input will never be something like 66/14/2020.
        
        Complexity:
        Best Case Complexity: O(1) first date format success
        Worst Case Complexity: O(1) need to try four date formats then success
        """
        date_str = key
        
        formats = ('%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d') #supported date formats

        for format in formats:   #try four sup date formats

            try:
                target_date = datetime.strptime(date_str, format) #chage string to date
                days = (target_date - self.base_date).days  #get the different day number of base day
                return days % self.table_size
            
            except ValueError: #current format not success try next
                continue
        
        raise NotImplementedError #all formats unsuccess
