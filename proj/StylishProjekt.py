'''@package docstring
'''

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

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


class ModernButton(tk.Canvas):
    """Custom gradient button"""
    def __init__(self, parent, text, command, color1, color2, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.text = text
        self.color1 = color1
        self.color2 = color2
        self.is_hover = False
        
        self.config(width=120, height=45, highlightthickness=0, bd=0)
        self.draw_button()
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def draw_button(self):
        self.delete("all")
        
        # Gradient effect
        if self.is_hover:
            self.create_rectangle(0, 0, 120, 45, fill=self.color2, outline="")
        else:
            self.create_rectangle(0, 0, 120, 45, fill=self.color1, outline="")
        
        # Rounded corners effect
        self.create_rectangle(2, 2, 118, 43, outline="#ffffff", width=2)
        
        # Text
        self.create_text(60, 22, text=self.text, fill="white", 
                        font=("Segoe UI", 11, "bold"))
    
    def on_click(self, event):
        self.command()
    
    def on_enter(self, event):
        self.is_hover = True
        self.draw_button()
    
    def on_leave(self, event):
        self.is_hover = False
        self.draw_button()


class CacheGUI:
    def __init__(self, master):
        self.master = master
        master.title("LRU Cache Simulator Pro")
        master.geometry("900x700")
        master.configure(bg="#1a1a2e")
        
        # Cache
        self.cache_size = 5
        self.cache = Cache(self.cache_size)
        self.history = []
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header = tk.Frame(master, bg="#16213e", height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(header, text="LRU CACHE SIMULATOR", 
                              font=("Segoe UI", 24, "bold"), 
                              fg="#00d4ff", bg="#16213e")
        title_label.pack(pady=25)
        
        # Main container
        main_frame = tk.Frame(master, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel
        left_panel = tk.Frame(main_frame, bg="#1a1a2e")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Size control
        size_frame = tk.Frame(left_panel, bg="#0f3460", relief=tk.RAISED, bd=3)
        size_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(size_frame, text="Cache Size", font=("Segoe UI", 12, "bold"), 
                fg="#00d4ff", bg="#0f3460").pack(pady=(10, 5))
        
        self.size_var = tk.IntVar(value=self.cache_size)
        self.size_scale = tk.Scale(size_frame, from_=1, to=20, orient=tk.HORIZONTAL,
                                   variable=self.size_var, command=self.on_size_change,
                                   bg="#0f3460", fg="white", highlightthickness=0,
                                   troughcolor="#1a1a2e", length=250, font=("Segoe UI", 10))
        self.size_scale.pack(pady=(0, 10))
        
        # Input frame
        input_frame = tk.Frame(left_panel, bg="#0f3460", relief=tk.RAISED, bd=3)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(input_frame, text="Enter Value", font=("Segoe UI", 12, "bold"),
                fg="#00d4ff", bg="#0f3460").pack(pady=(10, 5))
        
        self.entry = tk.Entry(input_frame, font=("Segoe UI", 14), justify=tk.CENTER,
                             bg="#16213e", fg="white", insertbackground="white",
                             relief=tk.FLAT, bd=0)
        self.entry.pack(pady=10, padx=20, ipady=8, fill=tk.X)
        self.entry.bind('<Return>', lambda e: self.write_value())
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg="#0f3460")
        btn_frame.pack(pady=(0, 15))
        
        ModernButton(btn_frame, "READ", self.read_value, "#2196F3", "#1976D2").pack(side=tk.LEFT, padx=5)
        ModernButton(btn_frame, "WRITE", self.write_value, "#9C27B0", "#7B1FA2").pack(side=tk.LEFT, padx=5)
        ModernButton(btn_frame, "RESET", self.reset_cache, "#f44336", "#d32f2f").pack(side=tk.LEFT, padx=5)
        
        # Result display
        self.result_frame = tk.Frame(left_panel, bg="#0f3460", height=60, relief=tk.RAISED, bd=3)
        self.result_frame.pack(fill=tk.X, pady=(0, 15))
        self.result_frame.pack_propagate(False)
        
        self.result_label = tk.Label(self.result_frame, text="Awaiting operation...", 
                                     font=("Segoe UI", 13, "bold"), fg="#ffffff", bg="#0f3460")
        self.result_label.pack(expand=True)
        
        # Cache visualization
        cache_frame = tk.Frame(left_panel, bg="#0f3460", relief=tk.RAISED, bd=3)
        cache_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(cache_frame, text="Cache State (LRU → MRU)", 
                font=("Segoe UI", 12, "bold"), fg="#00d4ff", bg="#0f3460").pack(pady=(10, 5))
        
        self.cache_canvas = tk.Canvas(cache_frame, bg="#16213e", highlightthickness=0)
        self.cache_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.capacity_label = tk.Label(cache_frame, text="Capacity: 0 / 5",
                                      font=("Segoe UI", 10), fg="#00d4ff", bg="#0f3460")
        self.capacity_label.pack(pady=(0, 10))
        
        # Right panel - Stats & History
        right_panel = tk.Frame(main_frame, bg="#1a1a2e", width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Stats
        stats_frame = tk.Frame(right_panel, bg="#0f3460", relief=tk.RAISED, bd=3)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(stats_frame, text="Statistics", font=("Segoe UI", 12, "bold"),
                fg="#00d4ff", bg="#0f3460").pack(pady=(10, 10))
        
        # Hits
        hits_card = tk.Frame(stats_frame, bg="#1b5e20", relief=tk.RAISED, bd=2)
        hits_card.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(hits_card, text="HITS", font=("Segoe UI", 9), 
                fg="#a5d6a7", bg="#1b5e20").pack(pady=(5, 0))
        self.hits_label = tk.Label(hits_card, text="0", font=("Segoe UI", 24, "bold"),
                                   fg="#ffffff", bg="#1b5e20")
        self.hits_label.pack(pady=(0, 5))
        
        # Misses
        miss_card = tk.Frame(stats_frame, bg="#b71c1c", relief=tk.RAISED, bd=2)
        miss_card.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(miss_card, text="MISSES", font=("Segoe UI", 9),
                fg="#ef9a9a", bg="#b71c1c").pack(pady=(5, 0))
        self.misses_label = tk.Label(miss_card, text="0", font=("Segoe UI", 24, "bold"),
                                     fg="#ffffff", bg="#b71c1c")
        self.misses_label.pack(pady=(0, 5))
        
        # Hit Rate
        rate_card = tk.Frame(stats_frame, bg="#01579b", relief=tk.RAISED, bd=2)
        rate_card.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(rate_card, text="HIT RATE", font=("Segoe UI", 9),
                fg="#81d4fa", bg="#01579b").pack(pady=(5, 0))
        self.rate_label = tk.Label(rate_card, text="0%", font=("Segoe UI", 24, "bold"),
                                   fg="#ffffff", bg="#01579b")
        self.rate_label.pack(pady=(0, 5))
        
        tk.Label(stats_frame, text="", bg="#0f3460").pack(pady=5)
        
        # History
        history_frame = tk.Frame(right_panel, bg="#0f3460", relief=tk.RAISED, bd=3)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(history_frame, text="Operation History", font=("Segoe UI", 12, "bold"),
                fg="#00d4ff", bg="#0f3460").pack(pady=(10, 5))
        
        # History listbox with scrollbar
        list_frame = tk.Frame(history_frame, bg="#16213e")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_list = tk.Listbox(list_frame, font=("Consolas", 9),
                                       bg="#16213e", fg="white",
                                       yscrollcommand=scrollbar.set,
                                       selectbackground="#0f3460",
                                       relief=tk.FLAT, bd=0)
        self.history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_list.yview)
        
        self.update_display()
    
    def on_size_change(self, value):
        new_size = int(value)
        if new_size != self.cache_size:
            self.cache_size = new_size
            self.cache = Cache(self.cache_size)
            self.history.clear()
            self.history_list.delete(0, tk.END)
            self.update_display()
    
    def read_value(self):
        value = self.entry.get().strip()
        if not value:
            return
        
        result = self.cache.read(value)
        self.show_result(f"READ '{value}'", result)
        self.add_history("READ", value, result)
        self.entry.delete(0, tk.END)
        self.update_display()
    
    def write_value(self):
        value = self.entry.get().strip()
        if not value:
            return
        
        result = self.cache.write(value)
        self.show_result(f"WRITE '{value}'", result)
        self.add_history("WRITE", value, result)
        self.entry.delete(0, tk.END)
        self.update_display()
    
    def reset_cache(self):
        self.cache.reset()
        self.history.clear()
        self.history_list.delete(0, tk.END)
        self.result_label.config(text="Cache reset!", fg="#ffffff")
        self.result_frame.config(bg="#0f3460")
        self.update_display()
    
    def show_result(self, text, is_hit):
        result_text = f"{text} → {'HIT' if is_hit else 'MISS'}"
        self.result_label.config(text=result_text)
        
        if is_hit:
            self.result_frame.config(bg="#1b5e20")
            self.result_label.config(bg="#1b5e20", fg="#a5d6a7")
        else:
            self.result_frame.config(bg="#b71c1c")
            self.result_label.config(bg="#b71c1c", fg="#ef9a9a")
    
    def add_history(self, operation, value, result):
        time = datetime.now().strftime("%H:%M:%S")
        entry = f"[{time}] {operation} '{value}' → {'HIT' if result else 'MISS'}"
        self.history_list.insert(0, entry)
    
    def update_display(self):
        # Update cache visualization
        elements = self.cache.get_elements()
        self.cache_canvas.delete("all")
        
        if not elements:
            self.cache_canvas.create_text(
                self.cache_canvas.winfo_width() // 2 or 150,
                self.cache_canvas.winfo_height() // 2 or 50,
                text="EMPTY CACHE", fill="#666666", font=("Segoe UI", 14, "bold")
            )
        else:
            x_start = 20
            y = 30
            box_width = 70
            box_height = 50
            gap = 15
            
            for i, elem in enumerate(elements):
                x = x_start + i * (box_width + gap)
                
                # Gradient color from old to new
                intensity = int(100 + (155 * i / max(len(elements) - 1, 1)))
                color = f"#{intensity:02x}{intensity//2:02x}{255:02x}"
                
                # Draw box
                self.cache_canvas.create_rectangle(x, y, x + box_width, y + box_height,
                                                  fill=color, outline="#ffffff", width=2)
                
                # Draw value
                self.cache_canvas.create_text(x + box_width // 2, y + box_height // 2,
                                             text=str(elem), fill="white",
                                             font=("Segoe UI", 14, "bold"))
                
                # Label
                label = "LRU" if i == 0 else "MRU" if i == len(elements) - 1 else ""
                if label:
                    self.cache_canvas.create_text(x + box_width // 2, y + box_height + 15,
                                                 text=label, fill="#00d4ff",
                                                 font=("Segoe UI", 8, "bold"))
        
        # Update labels
        self.capacity_label.config(text=f"Capacity: {len(elements)} / {self.cache_size}")
        self.hits_label.config(text=str(self.cache.hits))
        self.misses_label.config(text=str(self.cache.misses))
        
        # Update hit rate
        total = self.cache.hits + self.cache.misses
        if total > 0:
            rate = (self.cache.hits / total) * 100
            self.rate_label.config(text=f"{rate:.1f}%")
        else:
            self.rate_label.config(text="0%")


if __name__ == "__main__":
    root = tk.Tk()
    gui = CacheGUI(root)
    root.mainloop()