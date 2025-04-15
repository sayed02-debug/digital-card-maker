import tkinter as tk
from tkinter import ttk, Entry, StringVar
from PIL import Image, ImageTk
import os
import random

class HomeView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Background color constant
        self.bg_color = "#ffffff"  # White background like smilebox
        
        # Configure the frame background
        style = ttk.Style()
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color)
        
        # Create a canvas with scrollbar for the entire content
        self.canvas = tk.Canvas(self, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Configure the canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main container for all content
        self.main_container = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        
        # Configure the main container to expand to canvas width
        self.main_container.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Fixed width for content sections
        self.content_width = 900  # Fixed width for content
        
        # Header with navigation and search
        self.create_header(self.main_container)
        
        # Banner section
        self.create_banner(self.main_container)
        
        # Categories section
        self.create_categories_section(self.main_container)
        
        # Featured cards section
        self.create_featured_section(self.main_container)
        
        # Trending section
        self.create_trending_section(self.main_container)
    
    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """When the canvas resizes, resize the window within it"""
        # Update the width of the window to fill the canvas
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def create_header(self, parent):
        """Create the header with navigation and search"""
        header_frame = ttk.Frame(parent, style="TFrame")
        header_frame.pack(fill="x")
        
        # Content container with fixed width
        header_content = ttk.Frame(header_frame, style="TFrame", width=self.content_width)
        header_content.pack(pady=10)
        
        # Top navigation bar
        nav_frame = ttk.Frame(header_content, style="TFrame", width=self.content_width)
        nav_frame.pack(fill="x", pady=10)
        nav_frame.pack_propagate(False)  # Maintain fixed width
        
        # Logo
        logo_label = ttk.Label(nav_frame, text="Greeting Card Maker", 
                             font=("Helvetica", 18, "bold"), style="TLabel")
        logo_label.pack(side="left")
        
        # Search bar
        search_frame = ttk.Frame(nav_frame, style="TFrame")
        search_frame.pack(side="right")
        
        search_var = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side="left", padx=(0, 5))
        search_entry.insert(0, "Search cards...")
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, "end") 
                                              if search_entry.get() == "Search cards..." else None)
        search_entry.bind("<FocusOut>", lambda e: search_entry.insert(0, "Search cards...") 
                                               if search_entry.get() == "" else None)
        
        search_button = ttk.Button(search_frame, text="Search")
        search_button.pack(side="left")
        
        # Separator
        separator = ttk.Separator(header_frame, orient="horizontal")
        separator.pack(fill="x")
    
    def create_banner(self, parent):
        """Create the main banner"""
        banner_container = ttk.Frame(parent, style="TFrame")
        banner_container.pack(fill="x", pady=20)
        
        # Content container with fixed width
        banner_content = ttk.Frame(banner_container, style="TFrame", width=self.content_width)
        banner_content.pack()
        
        # Banner with light blue background
        banner_frame = tk.Frame(banner_content, bg="#F0F7FF", width=self.content_width, height=300)
        banner_frame.pack(fill="x")
        banner_frame.pack_propagate(False)  # Maintain fixed size
        
        # Left side content
        content_frame = tk.Frame(banner_frame, bg="#F0F7FF")
        content_frame.pack(side="left", padx=40, pady=40)
        
        # Banner title
        banner_title = tk.Label(content_frame, 
                              text="Create Beautiful\nGreeting Cards", 
                              font=("Helvetica", 28, "bold"), 
                              bg="#F0F7FF", fg="#333333",
                              justify="left")
        banner_title.pack(anchor="w")
        
        # Banner subtitle
        banner_subtitle = tk.Label(content_frame, 
                                 text="Design personalized cards with our AI-powered tools", 
                                 font=("Helvetica", 14), 
                                 bg="#F0F7FF", fg="#666666",
                                 justify="left")
        banner_subtitle.pack(anchor="w", pady=(10, 20))
        
        # Create button
        create_button = tk.Button(content_frame, text="Create a Card", 
                                font=("Helvetica", 14, "bold"),
                                bg="#4A7AFF", fg="white", 
                                padx=20, pady=10, bd=0,
                                command=lambda: self.controller.show_frame("prompt_generator"))
        create_button.pack(anchor="w")
        
        # Right side decorative image placeholder
        image_frame = tk.Frame(banner_frame, bg="#F0F7FF", width=400, height=220)
        image_frame.pack(side="right", padx=40, pady=40)
        
        # Add decorative elements
        canvas = tk.Canvas(image_frame, bg="#F0F7FF", width=400, height=220, highlightthickness=0)
        canvas.pack()
        
        # Draw some card-like shapes
        colors = ["#FF6B6B", "#4ECDC4", "#FFD166", "#118AB2", "#073B4C"]
        for i in range(5):
            x = 200 + i * 15
            y = 110 - i * 10
            width = 150
            height = 200
            canvas.create_rectangle(x, y, x+width, y+height, 
                                  fill=colors[i], outline="")
    
    def create_categories_section(self, parent):
        """Create the categories section"""
        # Container for the entire section
        section_container = ttk.Frame(parent, style="TFrame")
        section_container.pack(fill="x", pady=30)
        
        # Content container with fixed width
        section_content = ttk.Frame(section_container, style="TFrame", width=self.content_width)
        section_content.pack()
        
        # Section title
        title_label = ttk.Label(section_content, text="Browse by Category", 
                              font=("Helvetica", 20, "bold"), style="TLabel")
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Categories grid
        categories_frame = ttk.Frame(section_content, style="TFrame", width=self.content_width)
        categories_frame.pack(fill="x")
        categories_frame.pack_propagate(False)  # Maintain fixed width
        
        # Define categories with images and colors
        categories = [
            {"name": "Birthday", "icon": "🎂", "color": "#FFD166", "desc": "Celebrate special days"},
            {"name": "Valentine", "icon": "❤️", "color": "#EF476F", "desc": "Express your love"},
            {"name": "Eid", "icon": "🌙", "color": "#06D6A0", "desc": "Eid celebrations"},
            {"name": "Puja", "icon": "🪔", "color": "#118AB2", "desc": "Festival greetings"},
            {"name": "New Year", "icon": "🎉", "color": "#073B4C", "desc": "Welcome the new year"},
            {"name": "Thank You", "icon": "🙏", "color": "#9B5DE5", "desc": "Show appreciation"}
        ]
        
        # Calculate card width based on content width and number of columns
        num_columns = 3
        card_width = (self.content_width - (num_columns-1)*20) // num_columns
        
        # Create a grid of category cards
        for i, category in enumerate(categories):
            row = i // num_columns
            col = i % num_columns
            
            # Create category card
            card_frame = tk.Frame(categories_frame, bg="white", bd=1, relief="solid", 
                                width=card_width, height=200)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card_frame.grid_propagate(False)  # Maintain fixed size
            
            # Make the grid cells expandable
            categories_frame.grid_columnconfigure(col, weight=1)
            categories_frame.grid_rowconfigure(row, weight=1)
            
            # Category icon/image
            icon_frame = tk.Frame(card_frame, bg=category["color"], width=card_width, height=120)
            icon_frame.pack(fill="x")
            icon_frame.pack_propagate(False)
            
            icon_label = tk.Label(icon_frame, text=category["icon"], 
                                font=("Arial", 48), bg=category["color"], fg="white")
            icon_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Category name and description
            info_frame = tk.Frame(card_frame, bg="white", padx=10, pady=10)
            info_frame.pack(fill="both", expand=True)
            
            name_label = tk.Label(info_frame, text=category["name"], 
                                font=("Helvetica", 14, "bold"), bg="white")
            name_label.pack(anchor="w")
            
            desc_label = tk.Label(info_frame, text=category["desc"], 
                                font=("Helvetica", 12), bg="white", fg="#666666")
            desc_label.pack(anchor="w", pady=(5, 0))
            
            # Make the entire card clickable
            for widget in [card_frame, icon_frame, icon_label, info_frame, name_label, desc_label]:
                widget.bind("<Button-1>", lambda e, c=category["name"]: self.controller.select_category(c))
                widget.bind("<Enter>", lambda e, frame=card_frame: frame.config(bg="#f8f8f8"))
                widget.bind("<Leave>", lambda e, frame=card_frame: frame.config(bg="white"))
    
    def create_featured_section(self, parent):
        """Create the featured cards section"""
        # Container for the entire section
        section_container = ttk.Frame(parent, style="TFrame")
        section_container.pack(fill="x", pady=30)
        
        # Content container with fixed width
        section_content = ttk.Frame(section_container, style="TFrame", width=self.content_width)
        section_content.pack()
        
        # Section title
        title_label = ttk.Label(section_content, text="Featured Cards", 
                              font=("Helvetica", 20, "bold"), style="TLabel")
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Featured cards frame
        featured_frame = ttk.Frame(section_content, style="TFrame", width=self.content_width)
        featured_frame.pack(fill="x")
        featured_frame.pack_propagate(False)  # Maintain fixed width
        
        # Calculate card width based on content width and number of columns
        num_columns = 4
        card_width = (self.content_width - (num_columns-1)*20) // num_columns
        
        # Create a row of featured cards
        for i in range(num_columns):
            # Card frame
            card_frame = tk.Frame(featured_frame, bg="white", bd=1, relief="solid", 
                                width=card_width, height=280)
            card_frame.grid(row=0, column=i, padx=10, pady=10)
            card_frame.grid_propagate(False)  # Maintain fixed size
            
            # Make columns expandable
            featured_frame.grid_columnconfigure(i, weight=1)
            
            # Card image area
            image_color = random.choice(["#FFD166", "#EF476F", "#06D6A0", "#118AB2", "#073B4C"])
            image_frame = tk.Frame(card_frame, bg=image_color, width=card_width, height=180)
            image_frame.pack(fill="x")
            image_frame.pack_propagate(False)
            
            # Random emoji as placeholder
            emoji = random.choice(["🎂", "❤️", "🌙", "🪔", "🎉", "🎁", "🎊", "🌹"])
            emoji_label = tk.Label(image_frame, text=emoji, font=("Arial", 60), bg=image_color, fg="white")
            emoji_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Card title and description
            info_frame = tk.Frame(card_frame, bg="white", padx=10, pady=10)
            info_frame.pack(fill="both", expand=True)
            
            title_label = tk.Label(info_frame, text="Card Title", 
                                  font=("Helvetica", 14, "bold"), bg="white")
            title_label.pack(anchor="w")
            
            desc_label = tk.Label(info_frame, text="Short description of the card", 
                                 font=("Helvetica", 12), bg="white", fg="#666666")
            desc_label.pack(anchor="w", pady=(5, 0))
            
            # Add hover effect and click action
            for widget in [card_frame, image_frame, emoji_label, info_frame, title_label, desc_label]:
                widget.bind("<Enter>", lambda e, frame=card_frame: frame.config(bg="#f8f8f8"))
                widget.bind("<Leave>", lambda e, frame=card_frame: frame.config(bg="white"))
                # Add click action here if needed
    
    def create_trending_section(self, parent):
        """Create the trending cards section"""
        # Container for the entire section
        section_container = ttk.Frame(parent, style="TFrame")
        section_container.pack(fill="x", pady=30)
        
        # Content container with fixed width
        section_content = ttk.Frame(section_container, style="TFrame", width=self.content_width)
        section_content.pack()
        
        # Section title
        title_label = ttk.Label(section_content, text="Trending Now", 
                              font=("Helvetica", 20, "bold"), style="TLabel")
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Trending cards frame
        trending_frame = ttk.Frame(section_content, style="TFrame", width=self.content_width)
        trending_frame.pack(fill="x")
        trending_frame.pack_propagate(False)  # Maintain fixed width
        
        # Calculate card width based on content width and number of columns
        num_columns = 5
        card_width = (self.content_width - (num_columns-1)*20) // num_columns
        
        # Create a row of trending cards
        for i in range(num_columns):
            # Card frame
            card_frame = tk.Frame(trending_frame, bg="white", bd=1, relief="solid", 
                                width=card_width, height=250)
            card_frame.grid(row=0, column=i, padx=10, pady=10)
            card_frame.grid_propagate(False)  # Maintain fixed size
            
            # Make columns expandable
            trending_frame.grid_columnconfigure(i, weight=1)
            
            # Card image area
            image_color = random.choice(["#FF6B6B", "#4ECDC4", "#FFD166", "#118AB2", "#073B4C"])
            image_frame = tk.Frame(card_frame, bg=image_color, width=card_width, height=150)
            image_frame.pack(fill="x")
            image_frame.pack_propagate(False)
            
            # Random image placeholder
            # You would replace this with actual image loading logic
            emoji = random.choice(["🎂", "❤️", "🌙", "🪔", "🎉", "🎁", "🎊", "🌹"])
            emoji_label = tk.Label(image_frame, text=emoji, font=("Arial", 40), bg=image_color, fg="white")
            emoji_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Card title
            title_label = tk.Label(card_frame, text="Trending Card", 
                                  font=("Helvetica", 14, "bold"), bg="white")
            title_label.pack(pady=10)
            
            # Add hover effect
            card_frame.bind("<Enter>", lambda e: card_frame.config(bg="#f8f8f8"))
            card_frame.bind("<Leave>", lambda e: card_frame.config(bg="white"))
            
            # Add click action here if needed
