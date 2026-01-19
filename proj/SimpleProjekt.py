'''@package docstring
'''

import tkinter as tk
from tkinter import messagebox, simpledialog

class Cache:
    """ Class implementing a simple LRU cache """
    
    class Node:
        """ Node for doubly linked list """
        def __init__(self, value):
            self.value = value
            self.next = None
            self.prev = None

    class Queue:
        """ Doubly linked list implementation for LRU queue """
    
        def __init__(self):
            self.head = None
            self.tail = None

        def append(self, value):
            new_node = Cache.Node(value)
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
            return new_node

        def pop_head(self):
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
        
        def to_list(self):
            elements = []
            current = self.head
            while current:
                elements.append(current.value)
                current = current.next
            return elements

    def __init__(self, size):
        self.size = size
        self.cache = dict()
        self.queue = self.Queue()
        self.hits = 0
        self.misses = 0

    def write(self, value):
        if value in self.cache:
            self.hits += 1
            old_node = self.cache[value]
            self.queue.pop(old_node)
            new_node = self.queue.append(value)
            self.cache[value] = new_node
            return True 
        
        self.misses += 1
        if len(self.cache) >= self.size:
            oldest = self.queue.pop_head()
            self.cache.pop(oldest)
        
        new_node = self.queue.append(value)
        self.cache[value] = new_node
        return False

    def read(self, value):
        if value in self.cache:
            self.hits += 1
            old_node = self.cache[value]
            self.queue.pop(old_node)
            new_node = self.queue.append(value)
            self.cache[value] = new_node
            return True
        
        self.misses += 1
        return False

    def get_elements(self):
        return self.queue.to_list()

    def reset(self):
        self.cache = dict()
        self.queue = self.Queue()
        self.hits = 0
        self.misses = 0


class CacheGUI:
    def __init__(self, master):
        self.master = master
        master.title("LRU Cache Simulator")
        master.geometry("600x500")
        
        # Cache size
        self.cache_size = 5
        self.cache = Cache(self.cache_size)
        
        # Cache size frame
        size_frame = tk.Frame(master)
        size_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(size_frame, text="Rozmiar cache:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.size_label = tk.Label(size_frame, text=str(self.cache_size), font=("Arial", 10))
        self.size_label.pack(side=tk.LEFT, padx=5)
        tk.Button(size_frame, text="Zmień rozmiar", command=self.change_size).pack(side=tk.LEFT)
        
        # Input frame
        input_frame = tk.Frame(master)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(input_frame, text="Wartość:").pack(side=tk.LEFT)
        self.entry = tk.Entry(input_frame, width=20)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<Return>', lambda e: self.write_value())
        
        tk.Button(input_frame, text="READ", command=self.read_value, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(input_frame, text="WRITE", command=self.write_value, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(input_frame, text="RESET", command=self.reset_cache, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=2)
        
        # Result frame
        self.result_frame = tk.Frame(master, height=50)
        self.result_frame.pack(pady=10, padx=10, fill=tk.X)
        self.result_label = tk.Label(self.result_frame, text="", font=("Arial", 12, "bold"))
        self.result_label.pack()
        
        # Cache display frame
        cache_frame = tk.LabelFrame(master, text="Stan Cache (LRU → MRU)", font=("Arial", 10, "bold"))
        cache_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.cache_display = tk.Text(cache_frame, height=5, font=("Arial", 12), state=tk.DISABLED)
        self.cache_display.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        self.capacity_label = tk.Label(cache_frame, text="Pojemność: 0 / 5")
        self.capacity_label.pack()
        
        # Stats frame
        stats_frame = tk.LabelFrame(master, text="Statystyki", font=("Arial", 10, "bold"))
        stats_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.hits_label = tk.Label(stats_frame, text="HITS: 0", font=("Arial", 10))
        self.hits_label.pack()
        self.misses_label = tk.Label(stats_frame, text="MISSES: 0", font=("Arial", 10))
        self.misses_label.pack()
        
        self.update_display()
    
    def change_size(self):
        new_size = simpledialog.askinteger("Rozmiar cache", "Podaj nowy rozmiar (1-20):", 
                                           initialvalue=self.cache_size, minvalue=1, maxvalue=20)
        if new_size:
            self.cache_size = new_size
            self.cache = Cache(self.cache_size)
            self.size_label.config(text=str(self.cache_size))
            self.update_display()
    
    def read_value(self):
        value = self.entry.get().strip()
        if not value:
            return
        
        result = self.cache.read(value)
        self.show_result("HIT" if result else "MISS", result)
        self.entry.delete(0, tk.END)
        self.update_display()
    
    def write_value(self):
        value = self.entry.get().strip()
        if not value:
            return
        
        result = self.cache.write(value)
        self.show_result("HIT" if result else "MISS", result)
        self.entry.delete(0, tk.END)
        self.update_display()
    
    def reset_cache(self):
        self.cache.reset()
        self.result_label.config(text="")
        self.result_frame.config(bg=self.master.cget('bg'))
        self.update_display()
    
    def show_result(self, text, is_hit):
        self.result_label.config(text=f"Wynik: {text}")
        if is_hit:
            self.result_frame.config(bg="#d4edda")
            self.result_label.config(bg="#d4edda")
        else:
            self.result_frame.config(bg="#f8d7da")
            self.result_label.config(bg="#f8d7da")
    
    def update_display(self):
        elements = self.cache.get_elements()
        
        self.cache_display.config(state=tk.NORMAL)
        self.cache_display.delete(1.0, tk.END)
        
        if elements:
            self.cache_display.insert(1.0, " → ".join(elements))
        else:
            self.cache_display.insert(1.0, "PUSTY")
        
        self.cache_display.config(state=tk.DISABLED)
        
        self.capacity_label.config(text=f"Pojemność: {len(elements)} / {self.cache_size}")
        self.hits_label.config(text=f"HITS: {self.cache.hits}")
        self.misses_label.config(text=f"MISSES: {self.cache.misses}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = CacheGUI(root)
    root.mainloop()