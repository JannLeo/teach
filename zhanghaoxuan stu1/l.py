import csv 

class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = int(weight)
    
    def __str__(self):
        return f"{self.name} (weight: {self.weight})"

class Container:
    def __init__(self, name, emptyweight, capacity):
        self.name = name
        self.emptyweight = int(emptyweight)
        self.capacity = int(capacity)
        self.content = []

    def totalweight(self):
        return self.emptyweight + sum(item.weight for item in self.content)

    def capacity_now(self):
        return self.capacity - self.now()

    def now(self):
        return sum(item.weight for item in self.content)

    def item_add(self, item):
        if item.weight <= self.capacity_now():
            self.content.append(item)
            return True
        else:
            return False

    def __str__(self):
        return (f"{self.name} (total weight: {self.totalweight()},"  
                f" empty weight: {self.emptyweight}, capacity: {self.now()}/{self.capacity})")

def readitems(filename):
    items = []
    with open (filename, mode = 'r') as file:
        data = csv.DictReader(file)
        for row in data:
            row = {key.strip(): value for key, value in row.items()}
            items.append(Item(row['Name'], row['Weight']))
    return items

def readcontainers(filename):
    containers = []
    with open(filename, mode = 'r') as file:
        data = csv.DictReader(file)
        for row in data:
            row = {key.strip(): value for key, value in row.items()}
            containers.append(Container(row['Name'], row['Empty Weight'], row['Weight Capacity'].strip()))
    return containers

def main():
    items = readitems('items.csv')
    containers = readcontainers('containers.csv')

    total = len(items) + len(containers)
    containers_number = len(containers)

    print(f"Initialised {total} items including {containers_number} containers.\n")
    
    name = input("Enter the name of the container: ")
    container = next((c for c in containers if c.name == name), None)

    while container is None:
        print(f"'{name}' not found. Try again.")
        name = input("Enter the name of the container: ")
        container = next((c for c in containers if c.name == name), None)
    
    while True:
        print('==================================')
        print('Enter your choice:')
        print('1. Loot item.')
        print('2. List looted items.')
        print('0. Quit.')
        print('==================================')

        choice = input()
        if choice == "1":
            while True:
                name = input("Enter the name of the item: ")
                item = next((i for i in items if i.name == name), None)

                if item:
                    if container.item_add(item):
                        print(f'Success! Item "{item.name}" stored in container "{container.name}".')
                        break
                    else:
                        print(f'Failure! Item "{item.name}" NOT stored in container "{container.name}".')
                        break
            
                else:
                    print(f"'{name}' not found. Try again.")

        elif choice == '2':
            print(container)
            for item in container.content:
                print(f"   {item}")
                
        elif choice == '0':
            break


if __name__ == "__main__":
    main()
