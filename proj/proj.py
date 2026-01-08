'''@package docstring
'''

''' 
write:
- sprawdza czy wartosc jest w cache
    - jesli tak to zwraca HIT i aktualizuje jej pozycje w kolejce LRU na najnowsza
    - jesli nie to sprawdza czy mamy miejsce w cache (jeśli nie ma to usuwa najstarsze w LRU) i zwraca MISS i dodaje wartosc do cache i kolejki LRU

'''

class Cache:
    """ Class implementing a simple LRU cache """
    
    class Node:
        """ Node for doubly linked list """
        def __init__(self, value):
            """ 
            Initialize node with given value; next and prev pointers to None 
            :param value: value to store in the node
            """
            self.value = value
            self.next = None
            self.prev = None


    class Queue:
        """ Doubly linked list implementation for LRU queue """
    
        def __init__(self):
            """ Initialize empty queue """
            self.head = None
            self.tail = None

        def append(self, value):
            """ 
            Append value to the tail of the queue 
            :param value: value to append
            :return: newly created node
            """

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

        def pop_head(self):
            """ 
            Remove and return value from head of the queue 
            :return: value of the removed node
            """

            if not self.head:
                return None

            node = self.head

            self.head = self.head.next

            if self.head:
                self.head.prev = None
            else:
                self.tail = None

            return node.value
        
        def pop(self, node):
            """
            Remove specific node from the queue
            :param node: node to remove
            :return: value of the removed node
            """

            if not node:
                return None

            # setting prev
            if node.prev:
                node.prev.next = node.next
            else:
                self.head = node.next

            # setting next
            if node.next:
                node.next.prev = node.prev
            else:
                self.tail = node.prev

            return node.value

    def __init__(self, size):
        """
        Initialize cache with given size; uses a dictionary for fast lookups and a doubly linked list for LRU tracking.
        :param size: maximum size of the cache
        """
        self.size = size
        self.cache = dict()
        self.queue = self.Queue()

    def write(self, value):
        """
        Write value to the cache
        :param value: value to write
        :return: True if HIT, False if MISS
        """
        
        if (value in self.cache):
            # HIT case, so we need to update its position in LRU queue to newest
            
            old_node = self.cache[value]
            self.queue.pop(old_node)

            new_node = self.queue.append(value)
            self.cache[value] = new_node

            return True 
        
        # MISS case

        if len(self.cache) >= self.size:
            # cache is full, need to remove oldest
            oldest = self.queue.pop_head()
            self.cache.pop(oldest)

        # putting new value to the newest position of queue
        new_node = self.queue.append(value)
        # putting new value to cache (with reference to its node in queue)
        self.cache[value] = new_node

        return False  # MISS

    # TODO
    def read(self, value):
        """
        Read value from the cache
        :param value: value to read
        :return: True if HIT, False if MISS
        """
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

