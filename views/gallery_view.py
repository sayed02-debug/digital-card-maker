import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import random

class GalleryView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        
        # Header frame
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=10)
        
        # Back button
        back_button = ttk.Button(header_frame, text="← Back", 
                               command=lambda: controller.show_frame("home"))
        back_button.pack(side="left", padx=20)
        
        # Title
        self.title_label = ttk.Label(header_frame, text="Select a Template", 
                                   font=("Arial", 18, "bold"), style="TLabel")
        self.title_label.pack(pady=10)
        
        # Create scrollable frame for templates
        self.canvas = tk.Canvas(self, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.template_frame = ttk.Frame(self.canvas, style="TFrame")
        self.template_frame.bind("<Configure>", 
                               lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.template_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Placeholder for template images
        self.template_images = []  # Keep references to prevent garbage collection
        
        # Sample templates for each category with more options and better organization
        self.templates = {
            "Birthday": [
                {"path": "templates/birthday/elegant_1.jpg", "name": "Elegant Birthday", "style": "Elegant"},
                {"path": "templates/birthday/elegant_2.jpg", "name": "Golden Celebration", "style": "Elegant"},
                {"path": "templates/birthday/fun_1.jpg", "name": "Party Balloons", "style": "Fun"},
                {"path": "templates/birthday/fun_2.jpg", "name": "Confetti Explosion", "style": "Fun"},
                {"path": "templates/birthday/kids_1.jpg", "name": "Kids Birthday", "style": "Kids"},
                {"path": "templates/birthday/kids_2.jpg", "name": "Cartoon Cake", "style": "Kids"},
                {"path": "templates/birthday/minimal_1.jpg", "name": "Minimal White", "style": "Minimal"},
                {"path": "templates/birthday/minimal_2.jpg", "name": "Simple Elegance", "style": "Minimal"}
            ],
            "Valentine": [
                {"path": "templates/valentine/romantic_1.jpg", "name": "Red Roses", "style": "Romantic"},
                {"path": "templates/valentine/romantic_2.jpg", "name": "Heart Bokeh", "style": "Romantic"},
                {"path": "templates/valentine/cute_1.jpg", "name": "Cute Hearts", "style": "Cute"},
                {"path": "templates/valentine/cute_2.jpg", "name": "Love Birds", "style": "Cute"},
                {"path": "templates/valentine/modern_1.jpg", "name": "Modern Love", "style": "Modern"},
                {"path": "templates/valentine/modern_2.jpg", "name": "Geometric Hearts", "style": "Modern"},
                {"path": "templates/valentine/vintage_1.jpg", "name": "Vintage Romance", "style": "Vintage"},
                {"path": "templates/valentine/vintage_2.jpg", "name": "Classic Love Letter", "style": "Vintage"}
            ],
            "Eid": [
                {"path": "templates/eid/traditional_1.jpg", "name": "Traditional Lanterns", "style": "Traditional"},
                {"path": "templates/eid/traditional_2.jpg", "name": "Mosque Silhouette", "style": "Traditional"},
                {"path": "templates/eid/modern_1.jpg", "name": "Modern Geometric", "style": "Modern"},
                {"path": "templates/eid/modern_2.jpg", "name": "Minimalist Moon", "style": "Modern"},
                {"path": "templates/eid/festive_1.jpg", "name": "Festive Lights", "style": "Festive"},
                {"path": "templates/eid/festive_2.jpg", "name": "Celebration Gold", "style": "Festive"},
                {"path": "templates/eid/cultural_1.jpg", "name": "Cultural Patterns", "style": "Cultural"},
                {"path": "templates/eid/cultural_2.jpg", "name": "Heritage Design", "style": "Cultural"}
            ],
            "Puja": [
                {"path": "templates/puja/diwali_1.jpg", "name": "Diwali Lamps", "style": "Diwali"},
                {"path": "templates/puja/diwali_2.jpg", "name": "Rangoli Design", "style": "Diwali"},
                {"path": "templates/puja/durga_1.jpg", "name": "Durga Puja", "style": "Durga"},
                {"path": "templates/puja/durga_2.jpg", "name": "Goddess Durga", "style": "Durga"},
                {"path": "templates/puja/ganesh_1.jpg", "name": "Ganesh Chaturthi", "style": "Ganesh"},
                {"path": "templates/puja/ganesh_2.jpg", "name": "Lord Ganesha", "style": "Ganesh"},
                {"path": "templates/puja/navratri_1.jpg", "name": "Navratri Colors", "style": "Navratri"},
                {"path": "templates/puja/navratri_2.jpg", "name": "Garba Celebration", "style": "Navratri"}
            ],
            "New Year": [
                {"path": "templates/newyear/fireworks_1.jpg", "name": "Midnight Fireworks", "style": "Fireworks"},
                {"path": "templates/newyear/fireworks_2.jpg", "name": "Celebration Sky", "style": "Fireworks"},
                {"path": "templates/newyear/elegant_1.jpg", "name": "Elegant Countdown", "style": "Elegant"},
                {"path": "templates/newyear/elegant_2.jpg", "name": "Golden New Year", "style": "Elegant"},
                {"path": "templates/newyear/party_1.jpg", "name": "Party Confetti", "style": "Party"},
                {"path": "templates/newyear/party_2.jpg", "name": "Champagne Toast", "style": "Party"},
                {"path": "templates/newyear/minimal_1.jpg", "name": "Minimal Calendar", "style": "Minimal"},
                {"path": "templates/newyear/minimal_2.jpg", "name": "Clean Slate", "style": "Minimal"}
            ]
        }
        
        # For demo purposes, we'll create placeholder images
        self.create_placeholder_templates()
    
    def update_view(self):
        """Update the view when shown"""
        if self.controller.current_category:
            self.title_label.config(text=f"Select a {self.controller.current_category} Template")
            self.display_templates(self.controller.current_category)
    
    def display_templates(self, category):
        """Display templates for the selected category with style filtering"""
        # Clear previous templates
        for widget in self.template_frame.winfo_children():
            widget.destroy()
        
        self.template_images = []  # Clear image references
        
        # Get templates for the category
        templates = self.templates.get(category, [])
        
        # Create style filter at the top
        filter_frame = ttk.Frame(self.template_frame)
        filter_frame.pack(fill="x", pady=10)
        
        ttk.Label(filter_frame, text="Filter by style:", style="TLabel").pack(side="left", padx=10)
        
        # Get unique styles for this category
        styles = sorted(list(set(t["style"] for t in templates)))
        styles.insert(0, "All Styles")  # Add "All" option
        
        # Style variable
        self.style_var = tk.StringVar(value="All Styles")
        style_combo = ttk.Combobox(filter_frame, textvariable=self.style_var, 
                                  values=styles, width=15, state="readonly")
        style_combo.pack(side="left", padx=5)
        style_combo.bind("<<ComboboxSelected>>", 
                        lambda e: self.filter_templates_by_style(category))
        
        # Create a grid of templates
        self.templates_container = ttk.Frame(self.template_frame)
        self.templates_container.pack(fill="both", expand=True)
        
        # Display all templates initially
        self.show_filtered_templates(templates)
    
    def filter_templates_by_style(self, category):
        """Filter templates by the selected style"""
        selected_style = self.style_var.get()
        templates = self.templates.get(category, [])
        
        if selected_style == "All Styles":
            filtered_templates = templates
        else:
            filtered_templates = [t for t in templates if t["style"] == selected_style]
        
        # Clear and redisplay templates
        for widget in self.templates_container.winfo_children():
            widget.destroy()
        
        self.show_filtered_templates(filtered_templates)
    
    def show_filtered_templates(self, templates):
        """Display the filtered templates in a grid"""
        self.template_images = []  # Clear image references
        
        # Create a grid of templates
        row, col = 0, 0
        for template in templates:
            self.create_template_card(self.templates_container, template, row, col)
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
        
        # If no templates match the filter
        if not templates:
            no_results = ttk.Label(self.templates_container, 
                                 text="No templates match the selected filter",
                                 font=("Arial", 14), style="TLabel")
            no_results.pack(pady=50)
    
    def create_template_card(self, parent, template, row, col):
        """Create a card for each template with style label"""
        # Create a frame for the template
        card = tk.Frame(parent, bg="white", bd=1, relief="solid", 
                      padx=10, pady=10, width=350, height=320)
        card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        card.grid_propagate(False)  # Maintain fixed size
        
        # Make the card clickable
        card.bind("<Button-1>", lambda e, t=template["path"]: self.controller.select_template(t))
        
        try:
            # Try to open the image
            img = Image.open(template["path"])
            img = img.resize((300, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.template_images.append(photo)  # Keep a reference
            
            img_label = tk.Label(card, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(pady=5)
        except Exception as e:
            # If image can't be loaded, show placeholder
            placeholder = tk.Label(card, text="Template Preview", bg="#e0e0e0", 
                                 width=40, height=10)
            placeholder.pack(pady=5)
        
        # Template name
        name_label = tk.Label(card, text=template["name"], font=("Arial", 12, "bold"), bg="white")
        name_label.pack(pady=2)
        
        # Style label
        style_label = tk.Label(card, text=f"Style: {template['style']}", 
                             font=("Arial", 10), bg="white", fg="#666666")
        style_label.pack(pady=2)
        
        # Select button
        select_btn = ttk.Button(card, text="Select Template", 
                              command=lambda t=template["path"]: self.controller.select_template(t))
        select_btn.pack(pady=5)
    
    def create_placeholder_templates(self):
        """Create aesthetically pleasing placeholder template images for demo purposes"""
        # Create directories for each category
        for category, templates in self.templates.items():
            for template in templates:
                template_dir = os.path.dirname(template["path"])
                os.makedirs(template_dir, exist_ok=True)
                
                if not os.path.exists(template["path"]):
                    # Create a styled image based on category and style
                    img = self.create_styled_template(category, template["style"], template["name"])
                    img.save(template["path"])
    
    def create_styled_template(self, category, style, name):
        """Create a styled template image based on category and style"""
        width, height = 600, 400
        
        # Base colors for different categories
        base_colors = {
            "Birthday": {
                "Elegant": (245, 223, 77),  # Gold
                "Fun": (255, 105, 180),     # Hot Pink
                "Kids": (64, 224, 208),     # Turquoise
                "Minimal": (240, 240, 240)  # Light Gray
            },
            "Valentine": {
                "Romantic": (220, 20, 60),   # Crimson
                "Cute": (255, 182, 193),     # Light Pink
                "Modern": (219, 112, 147),   # Pale Violet Red
                "Vintage": (188, 143, 143)   # Rosy Brown
            },
            "Eid": {
                "Traditional": (0, 100, 0),   # Dark Green
                "Modern": (32, 178, 170),     # Light Sea Green
                "Festive": (218, 165, 32),    # Goldenrod
                "Cultural": (72, 61, 139)     # Dark Slate Blue
            },
            "Puja": {
                "Diwali": (255, 140, 0),      # Dark Orange
                "Durga": (178, 34, 34),       # Firebrick
                "Ganesh": (255, 215, 0),      # Gold
                "Navratri": (186, 85, 211)    # Medium Orchid
            },
            "New Year": {
                "Fireworks": (25, 25, 112),   # Midnight Blue
                "Elegant": (47, 79, 79),      # Dark Slate Gray
                "Party": (138, 43, 226),      # Blue Violet
                "Minimal": (211, 211, 211)    # Light Gray
            }
        }
        
        # Get the base color for this category and style
        color = base_colors.get(category, {}).get(style, (200, 200, 200))
        
        # Create a new image with the base color
        img = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        
        # Add decorative elements based on style
        if style in ["Elegant", "Traditional"]:
            # Add elegant border
            border_width = 20
            draw.rectangle(
                [(border_width, border_width), (width-border_width, height-border_width)],
                outline=(255, 255, 255), width=2
            )
            
            # Add corner decorations
            corner_size = 40
            for x, y in [(border_width, border_width), (width-border_width, border_width), 
                         (border_width, height-border_width), (width-border_width, height-border_width)]:
                draw.rectangle(
                    [(x-corner_size//2, y-corner_size//2), (x+corner_size//2, y+corner_size//2)],
                    fill=(255, 255, 255, 128), outline=(255, 255, 255), width=1
                )
        
        elif style in ["Fun", "Party"]:
            # Add confetti or dots
            for _ in range(100):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(5, 15)
                r = random.randint(150, 255)
                g = random.randint(150, 255)
                b = random.randint(150, 255)
                draw.ellipse([(x, y), (x+size, y+size)], fill=(r, g, b))
        
        elif style in ["Modern", "Minimal"]:
            # Add geometric elements
            for _ in range(5):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(50, 150)
                opacity = random.randint(30, 100)
                shape_color = (255, 255, 255, opacity)
                
                # Randomly choose between rectangle, circle, or line
                shape_type = random.choice(["rect", "circle", "line"])
                if shape_type == "rect":
                    draw.rectangle([(x, y), (x+size, y+size)], fill=shape_color)
                elif shape_type == "circle":
                    draw.ellipse([(x, y), (x+size, y+size)], fill=shape_color)
                else:
                    draw.line([(x, y), (x+size, y+size)], fill=shape_color, width=5)
        
        # Add a placeholder for text
        text_box_height = 100
        draw.rectangle(
            [(width//4, height//2 - text_box_height//2), 
             (width*3//4, height//2 + text_box_height//2)],
            fill=(255, 255, 255, 128)
        )
        
        # Add template name as watermark
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        watermark_text = f"{category} - {style}"
        # Get text size
        text_width, text_height = 100, 20  # Default fallback size
        try:
            # For newer Pillow versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            # For older Pillow versions
            elif hasattr(draw, 'textsize'):
                text_width, text_height = draw.textsize(watermark_text, font=font)
        except Exception:
            # Keep the fallback values if any error occurs
            pass
        
        position = (width - text_width - 10, height - text_height - 10)
        draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)
        
        return img
    
    def get_color_for_category(self, category):
        """Get a color for each category"""
        colors = {
            "Birthday": (255, 215, 0),  # Gold
            "Valentine": (255, 105, 180),  # Hot Pink
            "Eid": (144, 238, 144),  # Light Green
            "Puja": (255, 165, 0),  # Orange
            "New Year": (135, 206, 235)  # Sky Blue
        }
        return colors.get(category, (200, 200, 200))  # Default gray
    
    def add_text_to_image(self, img, text):
        """Add text to an image (simplified version)"""
        # In a real app, you would use PIL's ImageDraw to add text
        # For this demo, we'll just create the image
        pass
