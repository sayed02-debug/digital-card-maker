import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import random
import re
import uuid
from utils.ai_utils import get_ai_greeting, enhance_image_with_ai

class PromptGeneratorView(ttk.Frame):
    """View for generating cards from text prompts and images"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        
        # Store uploaded image path
        self.uploaded_image_path = None
        self.uploaded_image_preview = None
        
        # Create the layout
        self.create_layout()
    
    def create_layout(self):
        """Create the prompt generator layout"""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=10)
        
        # Back button
        back_button = ttk.Button(header_frame, text="← Back to Home", 
                               command=lambda: self.controller.show_frame("home"))
        back_button.pack(side="left", padx=20)
        
        # Title
        title_label = ttk.Label(header_frame, text="AI Card Generator", 
                              font=("Arial", 18, "bold"), style="TLabel")
        title_label.pack(pady=5)
        
        # Main content
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Left panel - Input
        input_frame = ttk.LabelFrame(content_frame, text="Card Details")
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        
        # Prompt input
        prompt_frame = ttk.Frame(input_frame)
        prompt_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(prompt_frame, text="Describe your greeting card:").pack(anchor="w")
        
        self.prompt_text = tk.Text(prompt_frame, height=5, width=40, wrap="word")
        self.prompt_text.pack(fill="x", pady=5)
        self.prompt_text.insert("1.0", "Example: Create a birthday card for my mom with flowers and warm colors")
        self.prompt_text.bind("<FocusIn>", self.clear_example_text)
        
        # Example prompts
        examples_frame = ttk.LabelFrame(input_frame, text="Example Prompts")
        examples_frame.pack(fill="x", padx=10, pady=10)
        
        example_prompts = [
            "A romantic Valentine's card with hearts and roses",
            "A funny birthday card for my brother who loves gaming",
            "An elegant Eid greeting with traditional patterns",
            "A colorful Diwali card with lamps and fireworks",
            "A minimalist New Year card with fireworks"
        ]
        
        for prompt in example_prompts:
            prompt_btn = ttk.Button(examples_frame, text=prompt, 
                                  command=lambda p=prompt: self.use_example_prompt(p))
            prompt_btn.pack(fill="x", padx=5, pady=2)
        
        # Image upload
        image_frame = ttk.Frame(input_frame)
        image_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(image_frame, text="Upload an image (optional):").pack(anchor="w")
        
        upload_btn = ttk.Button(image_frame, text="Upload Image", 
                              command=self.upload_image)
        upload_btn.pack(side="left", pady=5)
        
        self.image_label = ttk.Label(image_frame, text="No image selected")
        self.image_label.pack(side="left", padx=10)
        
        # Image preview frame
        self.preview_frame = ttk.Frame(input_frame)
        self.preview_frame.pack(fill="x", padx=10, pady=10)
        
        # Generate button
        generate_btn = ttk.Button(input_frame, text="Generate Card", 
                                command=self.generate_card)
        generate_btn.pack(fill="x", padx=10, pady=20)
        
        # Right panel - Preview
        preview_frame = ttk.LabelFrame(content_frame, text="Card Preview")
        preview_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)
        
        # Preview placeholder
        self.preview_placeholder = ttk.Label(preview_frame, 
                                          text="Your card preview will appear here")
        self.preview_placeholder.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Preview canvas (hidden initially)
        self.preview_canvas = tk.Canvas(preview_frame, bg="white", width=400, height=300,
                                      highlightthickness=1, highlightbackground="#cccccc")
        
        # Action buttons frame
        self.action_buttons = ttk.Frame(preview_frame)
        self.action_buttons.pack(side="bottom", fill="x", padx=20, pady=10)
        
        # Download button
        self.download_btn = ttk.Button(self.action_buttons, text="Download Card", 
                                     command=self.download_card,
                                     state="disabled")
        self.download_btn.pack(side="left", padx=(0, 5), fill="x", expand=True)
        
        # Edit button
        self.edit_btn = ttk.Button(self.action_buttons, text="Edit in Designer", 
                                 command=self.use_generated_card,
                                 state="disabled")
        self.edit_btn.pack(side="right", padx=(5, 0), fill="x", expand=True)
    
    def clear_example_text(self, event):
        """Clear example text when user focuses on the prompt field"""
        if self.prompt_text.get("1.0", "end-1c") == "Example: Create a birthday card for my mom with flowers and warm colors":
            self.prompt_text.delete("1.0", tk.END)
    
    def use_example_prompt(self, prompt):
        """Use an example prompt"""
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", prompt)
    
    def upload_image(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if not file_path:
            return
        
        try:
            # Store the image path
            self.uploaded_image_path = file_path
            
            # Update label
            filename = os.path.basename(file_path)
            self.image_label.config(text=f"Selected: {filename}")
            
            # Show preview
            img = Image.open(file_path)
            
            # Resize for preview
            img.thumbnail((150, 150))
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Create or update preview label
            if hasattr(self, 'image_preview_label'):
                self.image_preview_label.config(image=photo)
                self.image_preview_label.image = photo
            else:
                self.image_preview_label = tk.Label(self.preview_frame, image=photo)
                self.image_preview_label.image = photo
                self.image_preview_label.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def generate_card(self):
        """Generate a card based on the prompt and image"""
        # Get the prompt text
        prompt = self.prompt_text.get("1.0", "end-1c").strip()
        
        if not prompt or prompt == "Example: Create a birthday card for my mom with flowers and warm colors":
            messagebox.showinfo("Info", "Please enter a description for your card")
            return
        
        # Show loading cursor
        self.config(cursor="wait")
        self.update()
        
        try:
            # Analyze the prompt to determine category and style
            category, style, recipient, sender = self.analyze_prompt(prompt)
            
            # Select an appropriate template
            template_path = self.select_template(category, style)
            
            # Generate the card
            self.generate_preview(template_path, category, style, recipient, sender)
            
            # Reset cursor
            self.config(cursor="")
            
        except Exception as e:
            # Reset cursor
            self.config(cursor="")
            messagebox.showerror("Error", f"Failed to generate card: {str(e)}")
    
    def analyze_prompt(self, prompt):
        """Analyze the prompt to extract information"""
        prompt = prompt.lower()
        
        # Determine category
        categories = {
            "birthday": ["birthday", "bday", "born", "age", "year older"],
            "valentine": ["valentine", "love", "romantic", "heart", "romance"],
            "eid": ["eid", "ramadan", "mubarak", "islamic", "muslim"],
            "puja": ["puja", "diwali", "durga", "ganesh", "hindu", "festival"],
            "new year": ["new year", "year", "nye", "january", "resolution"]
        }
        
        category = "Birthday"  # Default
        for cat, keywords in categories.items():
            if any(keyword in prompt for keyword in keywords):
                category = cat.title()
                break
        
        # Determine style
        styles = {
            "elegant": ["elegant", "sophisticated", "classy", "formal", "luxury"],
            "fun": ["fun", "funny", "humorous", "joke", "laugh", "playful"],
            "minimal": ["minimal", "simple", "clean", "modern", "sleek"],
            "traditional": ["traditional", "classic", "cultural", "heritage"],
            "romantic": ["romantic", "love", "passion", "intimate"],
            "cute": ["cute", "adorable", "sweet", "lovely"],
            "festive": ["festive", "celebration", "party", "colorful"]
        }
        
        style = None
        for s, keywords in styles.items():
            if any(keyword in prompt for keyword in keywords):
                style = s
                break
        
        # If no style found, use default for the category
        if not style:
            if category == "Birthday":
                style = random.choice(["elegant", "fun", "minimal"])
            elif category == "Valentine":
                style = random.choice(["romantic", "cute"])
            elif category == "Eid":
                style = random.choice(["traditional", "elegant"])
            elif category == "Puja":
                style = random.choice(["traditional", "festive"])
            elif category == "New Year":
                style = random.choice(["elegant", "festive"])
        
        # Extract recipient and sender
        recipient = None
        sender = None
        
        # Look for recipient
        recipient_patterns = [
            r"for my (\w+)",
            r"for (\w+)",
            r"to my (\w+)",
            r"to (\w+)"
        ]
        
        for pattern in recipient_patterns:
            match = re.search(pattern, prompt)
            if match:
                recipient = match.group(1).capitalize()
                break
        
        # Look for sender
        sender_patterns = [
            r"from (\w+)",
            r"by (\w+)",
            r"signed (\w+)"
        ]
        
        for pattern in sender_patterns:
            match = re.search(pattern, prompt)
            if match:
                sender = match.group(1).capitalize()
                break
        
        return category, style, recipient, sender
    
    def select_template(self, category, style):
        """Select an appropriate template based on category and style"""
        # Convert category to directory name format
        category_dir = category.lower().replace(" ", "")
        
        # Look for templates in the specific style
        style_dir = os.path.join("templates", category_dir, style)
        templates = []
        
        if os.path.exists(style_dir):
            templates = [os.path.join(style_dir, f) for f in os.listdir(style_dir) 
                       if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        # If no templates in style dir, look in category dir
        if not templates:
            category_path = os.path.join("templates", category_dir)
            if os.path.exists(category_path):
                templates = [os.path.join(category_path, f) for f in os.listdir(category_path) 
                           if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        # If still no templates, use a default template
        if not templates:
            # Create a default template path
            template_path = os.path.join("templates", category_dir, f"{style}_1.jpg")
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(template_path), exist_ok=True)
            
            # Create a default template if it doesn't exist
            if not os.path.exists(template_path):
                from utils.template_designer import TemplateDesigner
                designer = TemplateDesigner()
                
                # Create template based on category and style
                if category == "Birthday":
                    img = designer.create_birthday_template(style)
                elif category == "Valentine":
                    img = designer.create_valentine_template(style)
                elif category == "Eid":
                    img = designer.create_eid_template(style)
                elif category == "Puja":
                    img = designer.create_puja_template(style)
                elif category == "New Year":
                    img = designer.create_newyear_template(style)
                else:
                    img = designer._create_default_template(category)
                
                # Save the template
                img.save(template_path)
            
            return template_path
        
        # Return a random template from the available ones
        return random.choice(templates)
    
    def generate_preview(self, template_path, category, style, recipient, sender):
        """Generate a preview of the card"""
        try:
            # Load the template
            img = Image.open(template_path)
            
            # Resize to fit preview
            preview_width = 400
            preview_height = 300
            
            # Resize image to fit preview while maintaining aspect ratio
            img_width, img_height = img.size
            ratio = min(preview_width/img_width, preview_height/img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Store original size for export
            self.original_width = img_width
            self.original_height = img_height
            
            # If there's an uploaded image, add it to the card
            if self.uploaded_image_path:
                try:
                    # Load and enhance the uploaded image
                    user_img = enhance_image_with_ai(self.uploaded_image_path)
                    
                    # Resize to fit on the card (max 40% of card width)
                    max_width = int(new_width * 0.4)
                    max_height = int(new_height * 0.4)
                    
                    user_img_width, user_img_height = user_img.size
                    ratio = min(max_width/user_img_width, max_height/user_img_height)
                    user_img = user_img.resize(
                        (int(user_img_width * ratio), int(user_img_height * ratio)), 
                        Image.LANCZOS
                    )
                    
                    # Position the image on the card (top right)
                    paste_x = new_width - user_img.width - 20
                    paste_y = 20
                    
                    # Paste the image
                    if user_img.mode == 'RGBA':
                        img.paste(user_img, (paste_x, paste_y), user_img)
                    else:
                        img.paste(user_img, (paste_x, paste_y))
                    
                    # Store for later use
                    self.uploaded_image_preview = user_img
                    
                except Exception as e:
                    print(f"Error adding image to card: {str(e)}")
            
            # Generate AI text for the card
            greeting = get_ai_greeting(category, recipient, sender, 
                                     "creative" if style in ["fun", "creative"] else "standard")
            
            # Store the generated text
            self.generated_text = greeting
            
            # Create a copy for drawing text
            img_with_text = img.copy()
            draw = ImageDraw.Draw(img_with_text)
            
            # Add text to image
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position and wrap
            text_width = new_width * 0.7
            text_x = new_width / 2
            text_y = new_height / 2
            
            # Draw multiline text
            lines = []
            words = greeting.split()
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                # Get text size
                text_size = None
                try:
                    # For newer Pillow versions
                    if hasattr(draw, 'textbbox'):
                        bbox = draw.textbbox((0, 0), test_line, font=font)
                        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
                    # For older Pillow versions
                    elif hasattr(draw, 'textsize'):
                        text_size = draw.textsize(test_line, font=font)
                except Exception:
                    # Fallback
                    text_size = (len(test_line) * 7, 15)  # Rough estimate
                
                if text_size and text_size[0] <= text_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line)
            
            # Draw each line
            y_offset = text_y - (len(lines) * 20) / 2
            for line in lines:
                # Get text size for centering
                text_size = None
                try:
                    # For newer Pillow versions
                    if hasattr(draw, 'textbbox'):
                        bbox = draw.textbbox((0, 0), line, font=font)
                        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
                    # For older Pillow versions
                    elif hasattr(draw, 'textsize'):
                        text_size = draw.textsize(line, font=font)
                except Exception:
                    # Fallback
                    text_size = (len(line) * 7, 15)  # Rough estimate
                
                x_position = text_x - text_size[0] / 2 if text_size else text_x
                
                draw.text((x_position, y_offset), line, fill="black", font=font)
                y_offset += 20
            
            # Store the final image for export
            self.final_card_image = img_with_text
            
            # Convert to PhotoImage for preview
            photo = ImageTk.PhotoImage(img_with_text)
            
            # Hide placeholder and show canvas
            self.preview_placeholder.pack_forget()
            self.preview_canvas.pack(expand=True, fill="both", padx=20, pady=20)
            
            # Clear canvas and set new size
            self.preview_canvas.delete("all")
            self.preview_canvas.config(width=new_width, height=new_height)
            
            # Add image to canvas
            self.preview_canvas.create_image(new_width/2, new_height/2, image=photo)
            self.preview_canvas.image = photo  # Keep a reference
            
            # Store template path for later use
            self.generated_template_path = template_path
            
            # Enable the action buttons
            self.download_btn.config(state="normal")
            self.edit_btn.config(state="normal")
            
        except Exception as e:
            raise Exception(f"Failed to generate preview: {str(e)}")
    
    def download_card(self):
        """Download the generated card as an image file"""
        if not hasattr(self, 'final_card_image'):
            messagebox.showinfo("Info", "Please generate a card first")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            title="Save Greeting Card",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        
        if not file_path:
            return
        
        try:
            # Save the image
            self.final_card_image.save(file_path)
            messagebox.showinfo("Success", f"Card saved successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save card: {str(e)}")
    
    def use_generated_card(self):
        """Use the generated card in the editor"""
        if hasattr(self, 'generated_template_path'):
            # Set the template in the controller
            self.controller.current_template = self.generated_template_path
            
            # Set the category if it can be determined from the path
            category_match = re.search(r'templates/(\w+)/', self.generated_template_path)
            if category_match:
                category = category_match.group(1)
                if category == "birthday":
                    self.controller.current_category = "Birthday"
                elif category == "valentine":
                    self.controller.current_category = "Valentine"
                elif category == "eid":
                    self.controller.current_category = "Eid"
                elif category == "puja":
                    self.controller.current_category = "Puja"
                elif category == "newyear":
                    self.controller.current_category = "New Year"
            
            # Show the editor view
            self.controller.show_frame("editor")
            
            # Get the editor view
            editor = self.controller.frames["editor"]
            
            # Add the generated text to the card
            if hasattr(self, 'generated_text'):
                # Create text on canvas
                text_id = editor.canvas.create_text(
                    300, 200,  # Center of canvas
                    text=self.generated_text,
                    font=("Arial", 14),
                    fill="#000000",
                    width=400,  # Wrap text at 400 pixels
                    justify=tk.CENTER,
                    tags=f"text_{len(editor.text_objects)}"
                )
                
                # Make text draggable
                drag_obj = editor.DraggableObject(editor.canvas, text_id, "text")
                editor.draggable_objects.append(drag_obj)
                
                # Store text object with properties
                text_obj = {
                    "id": text_id,
                    "text": self.generated_text,
                    "font": "Arial",
                    "size": 14,
                    "color": "#000000"
                }
                editor.text_objects.append(text_obj)
            
            # Add the uploaded image to the card if available
            if hasattr(self, 'uploaded_image_path') and self.uploaded_image_path:
                try:
                    # Use the enhanced image if available
                    if hasattr(self, 'uploaded_image_preview'):
                        img = self.uploaded_image_preview
                    else:
                        img = Image.open(self.uploaded_image_path)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    editor.image_references.append(photo)  # Keep reference
                    
                    # Create image on canvas
                    img_id = editor.canvas.create_image(
                        450, 150,  # Top right area
                        image=photo,
                        tags=f"image_{len(editor.image_objects)}"
                    )
                    
                    # Make image draggable
                    drag_obj = editor.DraggableObject(editor.canvas, img_id, "image")
                    editor.draggable_objects.append(drag_obj)
                    
                    # Store image object
                    img_obj = {
                        "id": img_id,
                        "image": photo,
                        "original": img,
                        "path": self.uploaded_image_path
                    }
                    editor.image_objects.append(img_obj)
                    
                except Exception as e:
                    print(f"Error adding image to editor: {str(e)}")
