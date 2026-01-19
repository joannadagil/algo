'''@package docstring
Ultra Advanced LRU Cache Simulator with insane visual effects
'''

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math
import random

class Cache:
    """ Class implementing a simple LRU cache """
    
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None
            self.prev = None

    class Queue:
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


class Particle:
    """Particle for background animation"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.size = random.randint(1, 3)
        self.color = random.choice(['#ff006e', '#fb5607', '#ffbe0b', '#8338ec', '#3a86ff'])
    
    def update(self, width, height):
        self.x += self.vx
        self.y += self.vy
        
        if self.x < 0 or self.x > width:
            self.vx *= -1
        if self.y < 0 or self.y > height:
            self.vy *= -1


class AnimatedButton(tk.Canvas):
    """Ultra animated button with glow effect"""
    def __init__(self, parent, text, command, gradient_colors, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.text = text
        self.colors = gradient_colors
        self.is_hover = False
        self.animation_frame = 0
        self.pulse_size = 0
        
        self.config(width=140, height=50, highlightthickness=0, bd=0, bg='#0a0e27')
        self.draw_button()
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.animate()
    
    def draw_button(self):
        self.delete("all")
        
        # Glow effect
        if self.is_hover:
            for i in range(5, 0, -1):
                alpha = i * 20
                self.create_rectangle(-i, -i, 140+i, 50+i, 
                                    outline=self.colors[1], width=2)
        
        # Main button with gradient simulation
        steps = 10
        for i in range(steps):
            y1 = i * (50 / steps)
            y2 = (i + 1) * (50 / steps)
            color = self.interpolate_color(self.colors[0], self.colors[1], i / steps)
            self.create_rectangle(0, y1, 140, y2, fill=color, outline="")
        
        # Border
        self.create_rectangle(2, 2, 138, 48, outline="#ffffff", width=2)
        
        # Pulse circle when hover
        if self.is_hover and self.pulse_size > 0:
            self.create_oval(70-self.pulse_size, 25-self.pulse_size,
                           70+self.pulse_size, 25+self.pulse_size,
                           outline=self.colors[1], width=2)
        
        # Text with shadow
        self.create_text(72, 27, text=self.text, fill="#333333", 
                        font=("Segoe UI", 12, "bold"))
        self.create_text(70, 25, text=self.text, fill="white", 
                        font=("Segoe UI", 12, "bold"))
    
    def interpolate_color(self, color1, color2, factor):
        c1 = [int(color1[i:i+2], 16) for i in (1, 3, 5)]
        c2 = [int(color2[i:i+2], 16) for i in (1, 3, 5)]
        c = [int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(3)]
        return f'#{c[0]:02x}{c[1]:02x}{c[2]:02x}'
    
    def animate(self):
        if self.is_hover:
            self.pulse_size = abs(math.sin(self.animation_frame * 0.1)) * 15
            self.draw_button()
            self.animation_frame += 1
        else:
            self.pulse_size = 0
        
        self.after(50, self.animate)
    
    def on_click(self, event):
        # Click animation
        self.create_oval(60, 15, 80, 35, fill="#ffffff", outline="")
        self.after(100, self.draw_button)
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
        master.title("⚡ ULTRA LRU CACHE SIMULATOR ⚡")
        master.geometry("1200x800")
        master.configure(bg="#0a0e27")
        
        # Cache
        self.cache_size = 8
        self.cache = Cache(self.cache_size)
        self.history = []
        
        # Animation
        self.particles = []
        self.init_particles()
        self.animation_active = True
        
        # Create animated background
        self.bg_canvas = tk.Canvas(master, bg="#0a0e27", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main container (on top of background)
        main_container = tk.Frame(master, bg="#0a0e27")
        main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.95, relheight=0.95)
        
        # Epic Header with animations
        header = tk.Frame(main_container, bg="#0a0e27", height=100)
        header.pack(fill=tk.X, pady=(0, 20))
        
        self.title_canvas = tk.Canvas(header, bg="#0a0e27", height=100, highlightthickness=0)
        self.title_canvas.pack(fill=tk.X)
        
        self.title_frame = 0
        self.animate_title()
        
        # Content frame
        content = tk.Frame(main_container, bg="#0a0e27")
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left mega panel
        left_panel = tk.Frame(content, bg="#0a0e27")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Control panel with neon border
        control_frame = tk.Canvas(left_panel, bg="#0a0e27", height=180, highlightthickness=0)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Draw neon frame
        self.draw_neon_frame(control_frame, 0, 0, 750, 180, "#ff006e")
        
        # Size control with cyberpunk style
        size_label = tk.Label(control_frame, text="CACHE SIZE MATRIX", 
                             font=("Consolas", 14, "bold"), fg="#00ff41", bg="#0a0e27")
        control_frame.create_window(375, 25, window=size_label)
        
        self.size_var = tk.IntVar(value=self.cache_size)
        
        # Custom scale with glow
        scale_frame = tk.Frame(control_frame, bg="#0a0e27")
        control_frame.create_window(375, 60, window=scale_frame)
        
        self.size_scale = tk.Scale(scale_frame, from_=1, to=20, orient=tk.HORIZONTAL,
                                   variable=self.size_var, command=self.on_size_change,
                                   bg="#1a1a3e", fg="#00ff41", highlightthickness=0,
                                   troughcolor="#0a0e27", length=300, 
                                   font=("Consolas", 12, "bold"), width=20,
                                   sliderlength=40)
        self.size_scale.pack()
        
        # Input section
        input_container = tk.Frame(control_frame, bg="#0a0e27")
        control_frame.create_window(375, 125, window=input_container)
        
        self.entry = tk.Entry(input_container, font=("Consolas", 16, "bold"), 
                             justify=tk.CENTER, bg="#1a1a3e", fg="#00ff41",
                             insertbackground="#00ff41", relief=tk.FLAT, bd=0, width=15)
        self.entry.pack(side=tk.LEFT, ipady=10, padx=(0, 10))
        self.entry.bind('<Return>', lambda e: self.write_value())
        
        # Mega buttons
        AnimatedButton(input_container, "READ", self.read_value, 
                      ["#667eea", "#764ba2"]).pack(side=tk.LEFT, padx=3)
        AnimatedButton(input_container, "WRITE", self.write_value,
                      ["#f093fb", "#f5576c"]).pack(side=tk.LEFT, padx=3)
        AnimatedButton(input_container, "RESET", self.reset_cache,
                      ["#fa709a", "#fee140"]).pack(side=tk.LEFT, padx=3)
        
        # Result display with hologram effect
        self.result_canvas = tk.Canvas(left_panel, bg="#0a0e27", height=80, highlightthickness=0)
        self.result_canvas.pack(fill=tk.X, pady=(0, 20))
        self.result_text = "SYSTEM READY"
        self.result_color = "#00ff41"
        
        # Cache visualization - THE MAIN SHOW
        viz_frame = tk.Canvas(left_panel, bg="#0a0e27", highlightthickness=0)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        self.draw_neon_frame(viz_frame, 10, 10, 730, 340, "#3a86ff")
        
        viz_label = tk.Label(viz_frame, text="⚡ CACHE QUANTUM STATE ⚡",
                            font=("Consolas", 16, "bold"), fg="#3a86ff", bg="#0a0e27")
        viz_frame.create_window(375, 30, window=viz_label)
        
        self.cache_canvas = tk.Canvas(viz_frame, bg="#0f1419", highlightthickness=0)
        viz_frame.create_window(375, 195, window=self.cache_canvas, width=700, height=280)
        
        # Right panel - STATS EXPLOSION
        right_panel = tk.Frame(content, bg="#0a0e27", width=380)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_panel.pack_propagate(False)
        
        # Stats cards with animations
        stats_container = tk.Frame(right_panel, bg="#0a0e27")
        stats_container.pack(fill=tk.X, pady=(0, 20))
        
        # Create animated stat cards
        self.create_stat_card(stats_container, "HITS", "#4ecca3", "hits")
        self.create_stat_card(stats_container, "MISSES", "#ee6055", "misses")
        self.create_stat_card(stats_container, "HIT RATE", "#ffd97d", "rate")
        
        # History terminal
        history_canvas = tk.Canvas(right_panel, bg="#0a0e27", highlightthickness=0)
        history_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.draw_neon_frame(history_canvas, 5, 5, 370, 450, "#8338ec")
        
        term_label = tk.Label(history_canvas, text="▸ OPERATION LOG",
                             font=("Consolas", 12, "bold"), fg="#8338ec", bg="#0a0e27")
        history_canvas.create_window(190, 25, window=term_label)
        
        # Scrollable terminal
        terminal_frame = tk.Frame(history_canvas, bg="#0a0e27")
        history_canvas.create_window(190, 240, window=terminal_frame, width=350, height=400)
        
        scrollbar = tk.Scrollbar(terminal_frame, bg="#1a1a3e")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_list = tk.Listbox(terminal_frame, font=("Consolas", 9),
                                       bg="#0f1419", fg="#00ff41",
                                       yscrollcommand=scrollbar.set,
                                       selectbackground="#1a1a3e",
                                       relief=tk.FLAT, bd=0,
                                       selectforeground="#00ff41")
        self.history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_list.yview)
        
        # Start animations
        self.animate_background()
        self.animate_result()
        
        self.update_display()
    
    def init_particles(self):
        for _ in range(50):
            self.particles.append(Particle(
                random.randint(0, 1200),
                random.randint(0, 800)
            ))
    
    def draw_neon_frame(self, canvas, x1, y1, x2, y2, color):
        """Draw glowing neon frame"""
        for i in range(3, 0, -1):
            canvas.create_rectangle(x1-i, y1-i, x2+i, y2+i, 
                                   outline=color, width=i)
    
    def animate_title(self):
        """Animate header title"""
        self.title_canvas.delete("all")
        
        text = "⚡ ULTRA LRU CACHE SIMULATOR ⚡"
        colors = ['#ff006e', '#fb5607', '#ffbe0b', '#8338ec', '#3a86ff']
        
        x = 600
        for i, char in enumerate(text):
            offset = math.sin((self.title_frame + i) * 0.2) * 5
            color = colors[(self.title_frame // 10 + i) % len(colors)]
            
            # Shadow
            self.title_canvas.create_text(x + i * 20 + 2, 52 + offset, 
                                         text=char, fill="#000000",
                                         font=("Consolas", 24, "bold"))
            # Main text
            self.title_canvas.create_text(x + i * 20, 50 + offset,
                                         text=char, fill=color,
                                         font=("Consolas", 24, "bold"))
        
        self.title_frame += 1
        self.master.after(50, self.animate_title)
    
    def animate_background(self):
        """Animate particle background"""
        self.bg_canvas.delete("all")
        
        width = self.bg_canvas.winfo_width() or 1200
        height = self.bg_canvas.winfo_height() or 800
        
        # Update and draw particles
        for particle in self.particles:
            particle.update(width, height)
            self.bg_canvas.create_oval(
                particle.x - particle.size, particle.y - particle.size,
                particle.x + particle.size, particle.y + particle.size,
                fill=particle.color, outline=""
            )
        
        # Draw connections
        for i, p1 in enumerate(self.particles[:20]):
            for p2 in self.particles[i+1:i+4]:
                dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
                if dist < 100:
                    alpha = int((1 - dist/100) * 50)
                    self.bg_canvas.create_line(p1.x, p1.y, p2.x, p2.y,
                                              fill=p1.color, width=1)
        
        if self.animation_active:
            self.master.after(50, self.animate_background)
    
    def animate_result(self):
        """Animate result display"""
        self.result_canvas.delete("all")
        
        # Glowing background
        for i in range(5, 0, -1):
            self.result_canvas.create_rectangle(10-i, 10-i, 740+i, 70+i,
                                               outline=self.result_color, width=2)
        
        self.result_canvas.create_rectangle(10, 10, 740, 70, 
                                           fill="#0f1419", outline="")
        
        # Animated text
        glow = abs(math.sin(self.title_frame * 0.1)) * 3
        self.result_canvas.create_text(375+glow, 40+glow, text=self.result_text,
                                      fill="#333333", font=("Consolas", 20, "bold"))
        self.result_canvas.create_text(375, 40, text=self.result_text,
                                      fill=self.result_color, font=("Consolas", 20, "bold"))
        
        self.master.after(50, self.animate_result)
    
    def create_stat_card(self, parent, title, color, var_name):
        """Create animated stat card"""
        card = tk.Canvas(parent, bg="#0a0e27", height=100, highlightthickness=0)
        card.pack(fill=tk.X, pady=5)
        
        # Neon border
        for i in range(3, 0, -1):
            card.create_rectangle(5-i, 5-i, 375+i, 95+i, outline=color, width=i)
        
        card.create_rectangle(5, 5, 375, 95, fill="#0f1419", outline="")
        
        card.create_text(190, 25, text=title, fill=color, 
                        font=("Consolas", 11, "bold"))
        
        value_label = tk.Label(card, text="0", font=("Consolas", 32, "bold"),
                              fg=color, bg="#0f1419")
        card.create_window(190, 60, window=value_label)
        
        setattr(self, f"{var_name}_label", value_label)
    
    def on_size_change(self, value):
        new_size = int(value)
        if new_size != self.cache_size:
            self.cache_size = new_size
            self.cache = Cache(self.cache_size)
            self.history.clear()
            self.history_list.delete(0, tk.END)
            self.result_text = f"CACHE RESIZED TO {new_size}"
            self.result_color = "#00ff41"
            self.update_display()
    
    def read_value(self):
        value = self.entry.get().strip()
        if not value:
            return
        
        result = self.cache.read(value)
        self.result_text = f"READ [{value}] → {'HIT' if result else 'MISS'}"
        self.result_color = "#4ecca3" if result else "#ee6055"
        self.add_history("READ", value, result)
        self.entry.delete(0, tk.END)
        self.update_display()
    
    def write_value(self):
        value = self.entry.get().strip()
        if not value:
            return
        
        result = self.cache.write(value)
        self.result_text = f"WRITE [{value}] → {'HIT' if result else 'MISS'}"
        self.result_color = "#4ecca3" if result else "#ee6055"
        self.add_history("WRITE", value, result)
        self.entry.delete(0, tk.END)
        self.update_display()
    
    def reset_cache(self):
        self.cache.reset()
        self.history.clear()
        self.history_list.delete(0, tk.END)
        self.result_text = "⚡ CACHE PURGED ⚡"
        self.result_color = "#ffd97d"
        self.update_display()
    
    def add_history(self, operation, value, result):
        time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        symbol = "✓" if result else "✗"
        entry = f"[{time}] {symbol} {operation} '{value}'"
        self.history_list.insert(0, entry)
        
        # Color code
        if result:
            self.history_list.itemconfig(0, fg="#4ecca3")
        else:
            self.history_list.itemconfig(0, fg="#ee6055")
    
    def update_display(self):
        """Update all displays with EPIC visuals"""
        elements = self.cache.get_elements()
        self.cache_canvas.delete("all")
        
        width = 700
        height = 280
        
        if not elements:
            # Epic "EMPTY" display
            for i in range(5):
                offset = math.sin(self.title_frame * 0.1 + i) * 3
                self.cache_canvas.create_text(350 + offset, 140 + offset,
                                             text="[ EMPTY CACHE ]",
                                             fill="#333333",
                                             font=("Consolas", 24, "bold"))
            self.cache_canvas.create_text(350, 140, text="[ EMPTY CACHE ]",
                                         fill="#666666",
                                         font=("Consolas", 24, "bold"))
        else:
            # Calculate layout
            n = len(elements)
            cols = min(n, 4)
            rows = (n + cols - 1) // cols
            
            box_width = 140
            box_height = 80
            gap_x = 30
            gap_y = 30
            
            start_x = (width - (cols * box_width + (cols - 1) * gap_x)) // 2
            start_y = (height - (rows * box_height + (rows - 1) * gap_y)) // 2
            
            for idx, elem in enumerate(elements):
                row = idx // cols
                col = idx % cols
                
                x = start_x + col * (box_width + gap_x)
                y = start_y + row * (box_height + gap_y)
                
                # Age-based color (rainbow gradient)
                hue = (idx / max(n - 1, 1)) * 300  # 0 to 300 degrees
                color = self.hsv_to_rgb(hue, 0.8, 0.9)
                
                # Glow effect
                for i in range(5, 0, -1):
                    self.cache_canvas.create_rectangle(
                        x - i, y - i, x + box_width + i, y + box_height + i,
                        outline=color, width=2
                    )
                
                # Main box
                self.cache_canvas.create_rectangle(x, y, x + box_width, y + box_height,
                                                  fill=color, outline="#ffffff", width=3)
                
                # Value with shadow
                self.cache_canvas.create_text(x + box_width//2 + 2, y + box_height//2 + 2,
                                             text=str(elem), fill="#000000",
                                             font=("Consolas", 20, "bold"))
                self.cache_canvas.create_text(x + box_width//2, y + box_height//2,
                                             text=str(elem), fill="#ffffff",
                                             font=("Consolas", 20, "bold"))
                
                # Labels
                if idx == 0:
                    self.cache_canvas.create_text(x + box_width//2, y - 10,
                                                 text="◀ LRU", fill="#ee6055",
                                                 font=("Consolas", 10, "bold"))
                elif idx == n - 1:
                    self.cache_canvas.create_text(x + box_width//2, y + box_height + 15,
                                                 text="MRU ▶", fill="#4ecca3",
                                                 font=("Consolas", 10, "bold"))
        
        # Update stats
        self.hits_label.config(text=str(self.cache.hits))
        self.misses_label.config(text=str(self.cache.misses))
        
        total = self.cache.hits + self.cache.misses
        if total > 0:
            rate = (self.cache.hits / total) * 100
            self.rate_label.config(text=f"{rate:.1f}%")
        else:
            self.rate_label.config(text="0%")
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB hex"""
        h = h / 60.0
        c = v * s
        x = c * (1 - abs(h % 2 - 1))
        m = v - c
        
        if 0 <= h < 1:
            r, g, b = c, x, 0
        elif 1 <= h < 2:
            r, g, b = x, c, 0
        elif 2 <= h < 3:
            r, g, b = 0, c, x
        elif 3 <= h < 4:
            r, g, b = 0, x, c
        elif 4 <= h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        r, g, b = int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
        return f'#{r:02x}{g:02x}{b:02x}'


if __name__ == "__main__":
    root = tk.Tk()
    gui = CacheGUI(root)
    root.mainloop()