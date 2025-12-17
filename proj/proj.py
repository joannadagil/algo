''' 
write:
- sprawdza czy wartosc jest w cache
    - jesli tak to zwraca HIT i aktualizuje jej pozycje w kolejce LRU na najnowsza
    - jesli nie to sprawdza czy mamy miejsce w cache (jeśli nie ma to usuwa najstarsze w LRU) i zwraca MISS i dodaje wartosc do cache i kolejki LRU

'''

class Cache:
    
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None
            self.prev = None


    class Queue:
        # TODO

        def __init__(self):
            self.head = None
            self.tail = None

        def append(self, value):
            # adding to tail

            new_node = Cache.Node(value)

            if not self.head:
                # if queue is empty
                self.head = new_node
                self.tail = new_node
            else:
                # if queue is not empty
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
                
            return new_node

        def pop(self):
            # removing from head

            if not self.head:
                return None

            node_value = self.head.value

            self.head = self.head.next

            if self.head:
                self.head.prev = None
            else:
                self.tail = None

            return node_value
        
        def pop(self, node):
            # removing specific node

            if not node:
                return None
            if node.prev:
                node.prev.next = node.next
            else:
                self.head = node.next
            if node.next:
                node.next.prev = node.prev
            else:
                self.tail = node.prev
            return node.value

    

    def __init__(self, size):
        self.size = size
        self.cache = dict()
        self.queue = Queue()

    # TODO
    def write(self, value):
        
        if (value in self.cache):

            return True  # HIT
        
        if len(self.cache) >= self.size:
            oldest = self.queue.popleft()
            self.cache.remove(oldest)
        self.cache.add(value)
        self.queue.append(value)
        return False  # MISS

    # TODO
    def read(self, value):
        pass




if __name__ == "__main__":

    # Reading cache size from user
    size = 0
    while size <= 0:
        try:
            size = int(input("Enter size of the cache (positive integer): "))
            if size <= 0:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
            size = 0
    cache = Cache(size)
    print(f"Cache size set to {size}.")
    
    # Reading operations from user
    print("Enter commands: (READ <value> or WRITE <value> or EXIT):")
    print("     READ <value> or R <value> - to read a value from the cache,")
    print("     WRITE <value> or W <value> - to write a value to the cache,")
    print("     EXIT or E - to exit the program.")

    while True:
        command = input("> ").strip().split()

        if not command:
            continue

        if command[0].upper() == "EXIT" or command[0].upper() == "E":
            break

        if (command[0].upper() == "READ" or command[0].upper() == "R") and len(command) == 2:
            hit = cache.read(command[1])
            print("HIT" if hit else "MISS")

        elif (command[0].upper() == "WRITE" or command[0].upper() == "W") and len(command) == 2:
            hit = cache.write(command[1])
            print("HIT" if hit else "MISS")

        else:
            print("Invalid command.")

