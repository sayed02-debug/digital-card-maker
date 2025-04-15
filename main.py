import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import random  # Add this import for the random functions
from views.home_view import HomeView
from views.gallery_view import GalleryView
from views.editor_view import EditorView
from views.prompt_generator_view import PromptGeneratorView

# Create necessary directories for template organization
def create_template_directories():
    """Create organized directory structure for templates"""
    categories = ["birthday", "valentine", "eid", "puja", "newyear"]
    for category in categories:
        # Create main category directory
        category_dir = os.path.join("templates", category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Create style subdirectories based on category
        if category == "birthday":
            styles = ["elegant", "fun", "kids", "minimal"]
        elif category == "valentine":
            styles = ["romantic", "cute", "modern", "vintage"]
        elif category == "eid":
            styles = ["traditional", "modern", "festive", "cultural"]
        elif category == "puja":
            styles = ["diwali", "durga", "ganesh", "navratri"]
        elif category == "newyear":
            styles = ["fireworks", "elegant", "party", "minimal"]
        
        # We'll keep the templates in the main category directory
        # but we create the style directories for future organization
        for style in styles:
            style_dir = os.path.join(category_dir, style)
            os.makedirs(style_dir, exist_ok=True)

class GreetingCardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI-Powered Greeting Card Maker")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        
        # Create a container frame
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Current selected template and category
        self.current_template = None
        self.current_category = None
        
        # Initialize views
        self.setup_views()
        
        # Show home view initially
        self.show_frame("home")
    
    def setup_views(self):
        # Create and store each view
        home_view = HomeView(self.container, self)
        gallery_view = GalleryView(self.container, self)
        editor_view = EditorView(self.container, self)
        prompt_generator_view = PromptGeneratorView(self.container, self)
        
        self.frames["home"] = home_view
        self.frames["gallery"] = gallery_view
        self.frames["editor"] = editor_view
        self.frames["prompt_generator"] = prompt_generator_view
        
        # Place all frames in the same position
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, page_name):
        """Show the frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
        # Update the frame if it has an update method
        if hasattr(frame, "update_view"):
            frame.update_view()
    
    def select_category(self, category):
        """Set the current category and show the gallery view"""
        self.current_category = category
        self.show_frame("gallery")
    
    def select_template(self, template_path):
        """Set the current template and show the editor view"""
        self.current_template = template_path
        self.show_frame("editor")

if __name__ == "__main__":
    # Create directories if they don't exist
    os.makedirs("templates", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    create_template_directories()
    
    # Start the application
    app = GreetingCardApp()
    app.mainloop()
