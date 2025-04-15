import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import uuid
from utils.ai_utils import get_ai_greeting, enhance_image_with_ai, get_text_suggestions

class DraggableObject:
    """Class to handle draggable objects on the canvas"""
    def __init__(self, canvas, item, type="text"):
        self.canvas = canvas
        self.item = item
        self.type = type  # "text" or "image"
        
        # Bind events
        self.canvas.tag_bind(item, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(item, "<ButtonRelease-1>", self.on_release)
        
        self.start_x = 0
        self.start_y = 0
    
    def on_press(self, event):
        """Handle mouse press"""
        self.start_x = event.x
        self.start_y = event.y
        # Raise the item to the top
        self.canvas.tag_raise(self.item)
    
    def on_drag(self, event):
        """Handle mouse drag"""
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.item, dx, dy)
        self.start_x = event.x
        self.start_y = event.y
    
    def on_release(self, event):
        """Handle mouse release"""
        pass  # Could add snapping or other functionality here

class EditorView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        
        # Store draggable objects
        self.draggable_objects = []
        
        # Store text objects with their properties
        self.text_objects = []
        
        # Store image objects
        self.image_objects = []
        
        # Keep references to images to prevent garbage collection
        self.image_references = []
        
        # Current selected object
        self.selected_object = None
        
        # Create the layout
        self.create_layout()
    
    def create_layout(self):
        """Create the editor layout"""
        # Top toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=10)
        
        # Back button
        back_button = ttk.Button(toolbar, text="← Back to Gallery", 
                               command=lambda: self.controller.show_frame("gallery"))
        back_button.pack(side="left", padx=20)
        
        # Title
        title_label = ttk.Label(toolbar, text="Card Editor", 
                              font=("Arial", 18, "bold"), style="TLabel")
        title_label.pack(pady=5)
        
        # Main content area with canvas and tools
        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel for tools
        tools_panel = ttk.Frame(content, width=200)
        tools_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Tools header
        tools_header = ttk.Label(tools_panel, text="Tools", 
                               font=("Arial", 14, "bold"), style="TLabel")
        tools_header.pack(pady=10)
        
        # Add text button
        add_text_btn = ttk.Button(tools_panel, text="Add Text", 
                                command=self.add_text)
        add_text_btn.pack(fill="x", pady=5)
        
        # Add AI text button
        add_ai_text_btn = ttk.Button(tools_panel, text="Add AI Generated Text", 
                                   command=self.add_ai_text)
        add_ai_text_btn.pack(fill="x", pady=5)
        
        # Add image button
        add_image_btn = ttk.Button(tools_panel, text="Upload Image", 
                                 command=self.add_image)
        add_image_btn.pack(fill="x", pady=5)
        
        # Enhance image with AI button
        enhance_image_btn = ttk.Button(tools_panel, text="Enhance Image with AI", 
                                     command=self.enhance_selected_image)
        enhance_image_btn.pack(fill="x", pady=5)
        
        # Text properties frame
        self.text_properties = ttk.LabelFrame(tools_panel, text="Text Properties")
        self.text_properties.pack(fill="x", pady=10, padx=5)
        
        # Font family
        ttk.Label(self.text_properties, text="Font:").pack(anchor="w", padx=5, pady=2)
        self.font_var = tk.StringVar(value="Arial")
        font_combo = ttk.Combobox(self.text_properties, textvariable=self.font_var, 
                                state="readonly", values=["Arial", "Times New Roman", "Courier", "Verdana"])
        font_combo.pack(fill="x", padx=5, pady=2)
        font_combo.bind("<<ComboboxSelected>>", self.update_text_properties)
        
        # Font size
        ttk.Label(self.text_properties, text="Size:").pack(anchor="w", padx=5, pady=2)
        self.size_var = tk.IntVar(value=24)
        size_spin = ttk.Spinbox(self.text_properties, from_=8, to=72, textvariable=self.size_var, width=5)
        size_spin.pack(fill="x", padx=5, pady=2)
        size_spin.bind("<Return>", self.update_text_properties)
        size_spin.bind("<FocusOut>", self.update_text_properties)
        
        # Text color
        ttk.Label(self.text_properties, text="Color:").pack(anchor="w", padx=5, pady=2)
        self.color_var = tk.StringVar(value="#000000")
        color_frame = ttk.Frame(self.text_properties)
        color_frame.pack(fill="x", padx=5, pady=2)
        
        self.color_preview = tk.Label(color_frame, bg=self.color_var.get(), width=3, height=1)
        self.color_preview.pack(side="left")
        
        color_btn = ttk.Button(color_frame, text="Choose Color", 
                             command=self.choose_color)
        color_btn.pack(side="left", padx=5)
        
        # Edit text button
        edit_text_btn = ttk.Button(self.text_properties, text="Edit Text", 
                                 command=self.edit_text)
        edit_text_btn.pack(fill="x", padx=5, pady=5)
        
        # Disable text properties initially
        self.disable_text_properties()
        
        # Export button
        export_btn = ttk.Button(tools_panel, text="Export Card", 
                              command=self.export_card)
        export_btn.pack(fill="x", pady=20)
        
        # Canvas area for editing
        canvas_frame = ttk.Frame(content, style="TFrame")
        canvas_frame.pack(side="right", fill="both", expand=True)
        
        # Canvas for the greeting card
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=600, height=400, 
                              highlightthickness=1, highlightbackground="#cccccc")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas click event to deselect objects
        self.canvas.bind("<Button-1>", self.canvas_click)
    
    def update_view(self):
        """Update the view when shown"""
        if self.controller.current_template:
            self.load_template(self.controller.current_template)
    
    def load_template(self, template_path):
        """Load the selected template into the canvas"""
        # Clear canvas
        self.canvas.delete("all")
        self.draggable_objects = []
        self.text_objects = []
        self.image_objects = []
        self.image_references = []
        
        try:
            # Load the template image
            img = Image.open(template_path)
            
            # Resize to fit canvas if needed
            canvas_width = self.canvas.winfo_width() or 600
            canvas_height = self.canvas.winfo_height() or 400
            
            # Resize image to fit canvas while maintaining aspect ratio
            img_width, img_height = img.size
            ratio = min(canvas_width/img_width, canvas_height/img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage and keep a reference
            self.template_image = ImageTk.PhotoImage(img)
            self.image_references.append(self.template_image)
            
            # Create image on canvas
            self.template_id = self.canvas.create_image(
                canvas_width/2, canvas_height/2, 
                image=self.template_image, 
                tags="template"
            )
            
            # Store original image for export
            self.original_template = img
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load template: {str(e)}")
    
    def add_text(self):
        """Add text to the canvas"""
        # Create a dialog to get text input
        text_dialog = tk.Toplevel(self)
        text_dialog.title("Add Text")
        text_dialog.geometry("300x150")
        text_dialog.transient(self)  # Make dialog modal
        text_dialog.grab_set()
        
        ttk.Label(text_dialog, text="Enter your text:").pack(pady=10)
        
        text_var = tk.StringVar()
        text_entry = ttk.Entry(text_dialog, textvariable=text_var, width=30)
        text_entry.pack(pady=5)
        text_entry.focus_set()
        
        def add_text_to_canvas():
            text = text_var.get()
            if text:
                # Create text on canvas
                text_id = self.canvas.create_text(
                    300, 200,  # Center of canvas
                    text=text,
                    font=(self.font_var.get(), self.size_var.get()),
                    fill=self.color_var.get(),
                    tags=f"text_{len(self.text_objects)}"
                )
                
                # Make text draggable
                drag_obj = DraggableObject(self.canvas, text_id, "text")
                self.draggable_objects.append(drag_obj)
                
                # Store text object with properties
                text_obj = {
                    "id": text_id,
                    "text": text,
                    "font": self.font_var.get(),
                    "size": self.size_var.get(),
                    "color": self.color_var.get()
                }
                self.text_objects.append(text_obj)
                
                # Select the new text
                self.select_object(text_id, "text")
            
            text_dialog.destroy()
        
        # Add buttons
        button_frame = ttk.Frame(text_dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Cancel", 
                 command=text_dialog.destroy).pack(side="left", padx=10)
        
        ttk.Button(button_frame, text="Add", 
                 command=add_text_to_canvas).pack(side="left", padx=10)
        
        # Bind Enter key to add text
        text_dialog.bind("<Return>", lambda e: add_text_to_canvas())
    
    def add_ai_text(self):
        """Add AI-generated text to the canvas"""
        # Create a dialog to configure AI text
        ai_dialog = tk.Toplevel(self)
        ai_dialog.title("Add AI-Generated Text")
        ai_dialog.geometry("400x300")
        ai_dialog.transient(self)
        ai_dialog.grab_set()
        
        # Get current category
        category = self.controller.current_category or "Birthday"
        
        # Create form
        form_frame = ttk.Frame(ai_dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Recipient name
        ttk.Label(form_frame, text="Recipient Name (optional):").pack(anchor="w", pady=(10, 2))
        recipient_var = tk.StringVar()
        recipient_entry = ttk.Entry(form_frame, textvariable=recipient_var, width=30)
        recipient_entry.pack(fill="x", pady=(0, 10))
        
        # Sender name
        ttk.Label(form_frame, text="Sender Name (optional):").pack(anchor="w", pady=(10, 2))
        sender_var = tk.StringVar()
        sender_entry = ttk.Entry(form_frame, textvariable=sender_var, width=30)
        sender_entry.pack(fill="x", pady=(0, 10))
        
        # Style selection
        ttk.Label(form_frame, text="Style:").pack(anchor="w", pady=(10, 2))
        style_var = tk.StringVar(value="standard")
        style_frame = ttk.Frame(form_frame)
        style_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Radiobutton(style_frame, text="Standard", variable=style_var, 
                      value="standard").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(style_frame, text="Creative", variable=style_var, 
                      value="creative").pack(side="left")
        
        # Preview area
        preview_frame = ttk.LabelFrame(form_frame, text="Preview")
        preview_frame.pack(fill="both", expand=True, pady=10)
        
        preview_text = tk.Text(preview_frame, wrap="word", height=5, width=40)
        preview_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Generate initial preview
        def generate_preview():
            recipient = recipient_var.get()
            sender = sender_var.get()
            style = style_var.get()
            
            # Get AI-generated text
            greeting = get_ai_greeting(category, recipient, sender, style)
            
            # Update preview
            preview_text.delete(1.0, tk.END)
            preview_text.insert(tk.END, greeting)
        
        # Generate preview when form changes
        def update_preview(*args):
            generate_preview()
        
        recipient_var.trace_add("write", update_preview)
        sender_var.trace_add("write", update_preview)
        style_var.trace_add("write", update_preview)
        
        # Generate initial preview
        generate_preview()
        
        # Button frame
        button_frame = ttk.Frame(ai_dialog)
        button_frame.pack(fill="x", pady=10)
        
        # Regenerate button
        ttk.Button(button_frame, text="Regenerate", 
                 command=generate_preview).pack(side="left", padx=10)
        
        # Cancel button
        ttk.Button(button_frame, text="Cancel", 
                 command=ai_dialog.destroy).pack(side="right", padx=10)
        
        # Add button
        def add_ai_text_to_canvas():
            greeting = preview_text.get(1.0, tk.END).strip()
            if greeting:
                # Create text on canvas
                text_id = self.canvas.create_text(
                    300, 200,  # Center of canvas
                    text=greeting,
                    font=(self.font_var.get(), self.size_var.get()),
                    fill=self.color_var.get(),
                    width=400,  # Wrap text at 400 pixels
                    justify=tk.CENTER,
                    tags=f"text_{len(self.text_objects)}"
                )
                
                # Make text draggable
                drag_obj = DraggableObject(self.canvas, text_id, "text")
                self.draggable_objects.append(drag_obj)
                
                # Store text object with properties
                text_obj = {
                    "id": text_id,
                    "text": greeting,
                    "font": self.font_var.get(),
                    "size": self.size_var.get(),
                    "color": self.color_var.get()
                }
                self.text_objects.append(text_obj)
                
                # Select the new text
                self.select_object(text_id, "text")
                
                ai_dialog.destroy()
        
        ttk.Button(button_frame, text="Add to Card", 
                 command=add_ai_text_to_canvas).pack(side="right", padx=10)
    
    def edit_text(self):
        """Edit the selected text"""
        if not self.selected_object or self.selected_object["type"] != "text":
            return
        
        # Find the text object
        text_id = self.selected_object["id"]
        text_obj = None
        for obj in self.text_objects:
            if obj["id"] == text_id:
                text_obj = obj
                break
        
        if not text_obj:
            return
        
        # Create a dialog to edit text
        text_dialog = tk.Toplevel(self)
        text_dialog.title("Edit Text")
        text_dialog.geometry("400x250")
        text_dialog.transient(self)
        text_dialog.grab_set()
        
        ttk.Label(text_dialog, text="Edit your text:").pack(pady=10)
        
        # Text entry with suggestions
        text_frame = ttk.Frame(text_dialog)
        text_frame.pack(fill="x", pady=5)
        
        text_var = tk.StringVar(value=text_obj["text"])
        text_entry = ttk.Entry(text_frame, textvariable=text_var, width=40)
        text_entry.pack(fill="x", padx=5)
        text_entry.focus_set()
        text_entry.select_range(0, tk.END)
        
        # Suggestions frame
        suggestions_frame = ttk.LabelFrame(text_dialog, text="AI Suggestions")
        suggestions_frame.pack(fill="x", padx=20, pady=10)
        
        suggestion_buttons = []
        for i in range(3):
            btn = ttk.Button(suggestions_frame, text="", state="disabled")
            btn.pack(fill="x", pady=2)
            suggestion_buttons.append(btn)
        
        # Update suggestions as user types
        def update_suggestions(*args):
            current_text = text_var.get()
            category = self.controller.current_category or "Birthday"
            
            # Get suggestions
            suggestions = get_text_suggestions(current_text, category)
            
            # Update suggestion buttons
            for i, btn in enumerate(suggestion_buttons):
                if i < len(suggestions):
                    suggestion = suggestions[i]
                    btn.config(text=suggestion[:50] + "..." if len(suggestion) > 50 else suggestion, 
                              state="normal", command=lambda s=suggestion: apply_suggestion(s))
                else:
                    btn.config(text="", state="disabled")
        
        def apply_suggestion(suggestion):
            text_var.set(suggestion)
        
        # Bind text changes to update suggestions
        text_var.trace_add("write", update_suggestions)
        
        # Initial suggestions update
        update_suggestions()
        
        def update_text():
            new_text = text_var.get()
            if new_text:
                # Update canvas text
                self.canvas.itemconfig(text_id, text=new_text)
                
                # Update stored text
                text_obj["text"] = new_text
            
            text_dialog.destroy()
        
        # Add buttons
        button_frame = ttk.Frame(text_dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Cancel", 
                 command=text_dialog.destroy).pack(side="left", padx=10)
        
        ttk.Button(button_frame, text="Update", 
                 command=update_text).pack(side="left", padx=10)
        
        # Bind Enter key
        text_dialog.bind("<Return>", lambda e: update_text())
    
    def add_image(self):
        """Add an image to the canvas"""
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if not file_path:
            return
        
        try:
            # Load the image
            img = Image.open(file_path)
            
            # Resize if too large
            max_size = 300
            img_width, img_height = img.size
            if img_width > max_size or img_height > max_size:
                ratio = min(max_size/img_width, max_size/img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            self.image_references.append(photo)  # Keep reference
            
            # Create image on canvas
            img_id = self.canvas.create_image(
                300, 200,  # Center of canvas
                image=photo,
                tags=f"image_{len(self.image_objects)}"
            )
            
            # Make image draggable
            drag_obj = DraggableObject(self.canvas, img_id, "image")
            self.draggable_objects.append(drag_obj)
            
            # Store image object
            img_obj = {
                "id": img_id,
                "image": photo,
                "original": img,
                "path": file_path
            }
            self.image_objects.append(img_obj)
            
            # Select the new image
            self.select_object(img_id, "image")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def enhance_selected_image(self):
        """Enhance the selected image using AI"""
        if not self.selected_object or self.selected_object["type"] != "image":
            messagebox.showinfo("Info", "Please select an image to enhance")
            return
        
        # Find the image object
        img_id = self.selected_object["id"]
        img_obj = None
        for obj in self.image_objects:
            if obj["id"] == img_id:
                img_obj = obj
                break
        
        if not img_obj or not img_obj["path"]:
            messagebox.showinfo("Info", "Cannot enhance this image")
            return
        
        try:
            # Show loading cursor
            self.config(cursor="wait")
            self.update()
            
            # Enhance the image
            enhanced_img = enhance_image_with_ai(img_obj["path"])
            
            # Resize if needed
            max_size = 300
            img_width, img_height = enhanced_img.size
            if img_width > max_size or img_height > max_size:
                ratio = min(max_size/img_width, max_size/img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                enhanced_img = enhanced_img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(enhanced_img)
            self.image_references.append(photo)  # Keep reference
            
            # Update canvas image
            self.canvas.itemconfig(img_id, image=photo)
            
            # Update stored image
            img_obj["image"] = photo
            img_obj["original"] = enhanced_img
            
            # Reset cursor
            self.config(cursor="")
            
            messagebox.showinfo("Success", "Image enhanced successfully!")
            
        except Exception as e:
            # Reset cursor
            self.config(cursor="")
            messagebox.showerror("Error", f"Failed to enhance image: {str(e)}")
    
    def choose_color(self):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(initialcolor=self.color_var.get())
        if color[1]:  # If a color was selected
            self.color_var.set(color[1])
            self.color_preview.config(bg=color[1])
            self.update_text_properties()
    
    def update_text_properties(self, event=None):
        """Update the properties of the selected text"""
        if not self.selected_object or self.selected_object["type"] != "text":
            return
        
        # Find the text object
        text_id = self.selected_object["id"]
        text_obj = None
        for obj in self.text_objects:
            if obj["id"] == text_id:
                text_obj = obj
                break
        
        if not text_obj:
            return
        
        # Update font properties
        font = self.font_var.get()
        size = self.size_var.get()
        color = self.color_var.get()
        
        # Update canvas text
        self.canvas.itemconfig(text_id, font=(font, size), fill=color)
        
        # Update stored properties
        text_obj["font"] = font
        text_obj["size"] = size
        text_obj["color"] = color
    
    def canvas_click(self, event):
        """Handle canvas click to select/deselect objects"""
        # Find the object under the cursor
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        
        # Deselect current object
        self.deselect_current_object()
        
        # If clicked on an object, select it
        if items:
            # Get the topmost item (excluding the template)
            for item in reversed(items):
                tags = self.canvas.gettags(item)
                if "template" not in tags:
                    # Determine if it's a text or image
                    item_type = "text" if any("text_" in tag for tag in tags) else "image"
                    self.select_object(item, item_type)
                    break
    
    def select_object(self, item_id, item_type):
        """Select an object on the canvas"""
        # Deselect current object
        self.deselect_current_object()
        
        # Store selected object
        self.selected_object = {"id": item_id, "type": item_type}
        
        # Highlight the selected object
        if item_type == "text":
            # Create a bounding box around the text
            bbox = self.canvas.bbox(item_id)
            if bbox:
                # Add padding
                padding = 5
                x1, y1, x2, y2 = bbox
                x1 -= padding
                y1 -= padding
                x2 += padding
                y2 += padding
                
                # Create highlight rectangle
                highlight = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="blue", width=2,
                    tags="highlight"
                )
                
                # Enable text properties
                self.enable_text_properties()
                
                # Set current text properties
                for obj in self.text_objects:
                    if obj["id"] == item_id:
                        self.font_var.set(obj["font"])
                        self.size_var.set(obj["size"])
                        self.color_var.set(obj["color"])
                        self.color_preview.config(bg=obj["color"])
                        break
        else:
            # Create a bounding box around the image
            bbox = self.canvas.bbox(item_id)
            if bbox:
                # Create highlight rectangle
                highlight = self.canvas.create_rectangle(
                    bbox, outline="blue", width=2,
                    tags="highlight"
                )
                
                # Disable text properties
                self.disable_text_properties()
    
    def deselect_current_object(self):
        """Deselect the current object"""
        # Remove highlight
        self.canvas.delete("highlight")
        
        # Reset selected object
        self.selected_object = None
        
        # Disable text properties
        self.disable_text_properties()
    
    def enable_text_properties(self):
        """Enable text property controls"""
        for child in self.text_properties.winfo_children():
            try:
                child.configure(state="normal")
            except:
                pass
    
    def disable_text_properties(self):
        """Disable text property controls"""
        for child in self.text_properties.winfo_children():
            try:
                child.configure(state="disabled")
            except:
                pass
    
    def export_card(self):
        """Export the greeting card as an image"""
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            title="Save Greeting Card",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        
        if not file_path:
            return
        
        try:
            # Create a new image from the template
            if hasattr(self, 'original_template'):
                # Use the original template image
                card_img = self.original_template.copy()
                
                # Get canvas dimensions
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                # Calculate scaling factors
                img_width, img_height = card_img.size
                scale_x = img_width / canvas_width
                scale_y = img_height / canvas_height
                
                # Create a drawing context
                draw = ImageDraw.Draw(card_img)
                
                # Add text elements
                for text_obj in self.text_objects:
                    # Get text position on canvas
                    bbox = self.canvas.bbox(text_obj["id"])
                    if bbox:
                        # Calculate center position
                        cx = (bbox[0] + bbox[2]) / 2
                        cy = (bbox[1] + bbox[3]) / 2
                        
                        # Scale to image coordinates
                        img_x = cx * scale_x
                        img_y = cy * scale_y
                        
                        # Load font
                        try:
                            font = ImageFont.truetype(text_obj["font"], text_obj["size"])
                        except:
                            # Fallback to default font
                            font = ImageFont.load_default()
                        
                        # Draw text
                        draw.text(
                            (img_x, img_y),
                            text_obj["text"],
                            fill=text_obj["color"],
                            font=font,
                            anchor="mm"  # Center alignment
                        )
                
                # Add image elements
                for img_obj in self.image_objects:
                    # Get image position on canvas
                    bbox = self.canvas.bbox(img_obj["id"])
                    if bbox:
                        # Calculate center position
                        cx = (bbox[0] + bbox[2]) / 2
                        cy = (bbox[1] + bbox[3]) / 2
                        
                        # Scale to image coordinates
                        img_x = cx * scale_x
                        img_y = cy * scale_y
                        
                        # Get original image
                        user_img = img_obj["original"]
                        
                        # Calculate paste position
                        paste_x = int(img_x - user_img.width / 2)
                        paste_y = int(img_y - user_img.height / 2)
                        
                        # Paste the image
                        if user_img.mode == 'RGBA':
                            # Handle transparent images
                            card_img.paste(user_img, (paste_x, paste_y), user_img)
                        else:
                            card_img.paste(user_img, (paste_x, paste_y))
                
                # Save the image
                card_img.save(file_path)
                
                messagebox.showinfo("Success", f"Card saved successfully to {file_path}")
            else:
                messagebox.showerror("Error", "No template loaded")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export card: {str(e)}")
