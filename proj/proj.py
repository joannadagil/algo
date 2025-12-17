
class Cache:
    size: int
    cache: dict
    queue: list

    def __init__(self, size):
        self.size = size
        self.catche = dict()
        self.queue = list()

    def write(self, value):
        pass


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

