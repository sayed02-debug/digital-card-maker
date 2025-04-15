from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import math
import os

class TemplateDesigner:
    """Class to create aesthetically pleasing greeting card templates"""
    
    def __init__(self, width=600, height=400):
        self.width = width
        self.height = height
    
    def create_birthday_template(self, style):
        """Create a birthday themed template"""
        if style == "elegant":
            return self._create_elegant_birthday()
        elif style == "fun":
            return self._create_fun_birthday()
        elif style == "kids":
            return self._create_kids_birthday()
        elif style == "minimal":
            return self._create_minimal_birthday()
        else:
            return self._create_default_template("Birthday")
    
    def create_valentine_template(self, style):
        """Create a valentine themed template"""
        if style == "romantic":
            return self._create_romantic_valentine()
        elif style == "cute":
            return self._create_cute_valentine()
        elif style == "modern":
            return self._create_modern_valentine()
        elif style == "vintage":
            return self._create_vintage_valentine()
        else:
            return self._create_default_template("Valentine")
    
    def create_eid_template(self, style):
        """Create an Eid themed template"""
        if style == "traditional":
            return self._create_traditional_eid()
        elif style == "modern":
            return self._create_modern_eid()
        elif style == "festive":
            return self._create_festive_eid()
        elif style == "cultural":
            return self._create_cultural_eid()
        else:
            return self._create_default_template("Eid")
    
    def create_puja_template(self, style):
        """Create a Puja themed template"""
        if style == "diwali":
            return self._create_diwali_template()
        elif style == "durga":
            return self._create_durga_template()
        elif style == "ganesh":
            return self._create_ganesh_template()
        elif style == "navratri":
            return self._create_navratri_template()
        else:
            return self._create_default_template("Puja")
    
    def create_newyear_template(self, style):
        """Create a New Year themed template"""
        if style == "fireworks":
            return self._create_fireworks_newyear()
        elif style == "elegant":
            return self._create_elegant_newyear()
        elif style == "party":
            return self._create_party_newyear()
        elif style == "minimal":
            return self._create_minimal_newyear()
        else:
            return self._create_default_template("New Year")
    
    # Birthday Templates
    def _create_elegant_birthday(self):
        """Create an elegant birthday template with professional aesthetics"""
        # Create soft gradient background
        img = self._create_gradient_background((255, 250, 240), (255, 240, 220))
        draw = ImageDraw.Draw(img)
        
        # Add decorative border with golden color
        border_width = 15
        inner_padding = 10
        gold_color = (212, 175, 55)
        
        # Outer border
        draw.rectangle(
            [(border_width, border_width), 
             (self.width-border_width, self.height-border_width)],
            outline=gold_color, width=3
        )
        
        # Inner border with drop shadow effect
        for i in range(3):
            draw.rectangle(
                [(border_width+inner_padding+i, border_width+inner_padding+i), 
                 (self.width-border_width-inner_padding-i, self.height-border_width-inner_padding-i)],
                outline=(gold_color[0], gold_color[1], gold_color[2], 100-i*30), width=1
            )
        
        # Add elegant corner flourishes
        corner_size = 40
        corners = [
            (border_width+inner_padding, border_width+inner_padding),  # Top-left
            (self.width-border_width-inner_padding, border_width+inner_padding),  # Top-right
            (border_width+inner_padding, self.height-border_width-inner_padding),  # Bottom-left
            (self.width-border_width-inner_padding, self.height-border_width-inner_padding)  # Bottom-right
        ]
        
        for x, y in corners:
            # Draw curved flourish
            for i in range(5):
                angle = i * 18
                radius = corner_size - i * 5
                draw.arc(
                    [(x-radius, y-radius), (x+radius, y+radius)],
                    angle, angle+90, fill=gold_color, width=2
                )
        
        # Add ribbon banner at the top
        banner_y = self.height // 4
        banner_height = 60
        banner_color = (150, 120, 20)
        
        # Banner body
        draw.rectangle(
            [(50, banner_y), (self.width-50, banner_y+banner_height)],
            fill=banner_color, outline=None
        )
        
        # Banner ends (triangular)
        left_fold = [
            (50, banner_y),
            (30, banner_y+banner_height//2),
            (50, banner_y+banner_height)
        ]
        right_fold = [
            (self.width-50, banner_y),
            (self.width-30, banner_y+banner_height//2),
            (self.width-50, banner_y+banner_height)
        ]
        draw.polygon(left_fold, fill=banner_color)
        draw.polygon(right_fold, fill=banner_color)
        
        # Add text to banner
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        banner_text = "Happy Birthday"
        # Get text size for centering
        text_width, text_height = 100, 20  # Default fallback size
        try:
            # For newer Pillow versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), banner_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            # For older Pillow versions
            elif hasattr(draw, 'textsize'):
                text_width, text_height = draw.textsize(banner_text, font=font)
        except Exception:
            # Keep the fallback values if any error occurs
            pass
        
        draw.text(
            (self.width//2 - text_width//2, banner_y + banner_height//2 - text_height//2),
            banner_text, fill=(255, 255, 220), font=font
        )
        
        # Add decorative elements
        # Golden stars
        for _ in range(10):
            x = random.randint(border_width*2, self.width-border_width*2)
            y = random.randint(banner_y+banner_height+20, self.height-border_width*2)
            size = random.randint(5, 15)
            self._draw_star(draw, x, y, size, gold_color)
        
        # Add cake with a realistic design
        self._add_elegant_cake(draw, gold_color)
        
        # Add text area with a subtle shadow
        self._add_text_area_with_shadow(draw)
        
        # Add subtle confetti
        for _ in range(50):
            x = random.randint(border_width*2, self.width-border_width*2)
            y = random.randint(border_width*2, self.height-border_width*2)
            size = random.randint(2, 5)
            opacity = random.randint(30, 100)
            draw.ellipse(
                [(x-size, y-size), (x+size, y+size)],
                fill=(gold_color[0], gold_color[1], gold_color[2], opacity)
            )
        
        # Add watermark
        self._add_watermark_text(draw, "Elegant Birthday")
        
        return img
    
    def _create_fun_birthday(self):
        """Create a fun birthday template with modern, vibrant aesthetics"""
        # Create base image with bright color gradient
        img = self._create_gradient_background((255, 105, 180), (255, 180, 220))
        draw = ImageDraw.Draw(img)
        
        # Add a circular pattern background 
        for i in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(20, 100)
            opacity = random.randint(20, 60)
            circle_color = (255, 255, 255, opacity)
            draw.ellipse(
                [(x-size, y-size), (x+size, y+size)],
                fill=circle_color
            )
        
        # Add modern zigzag border
        steps = 40
        step_size = self.width / steps
        margin = 30
        zigzag_color = (255, 255, 255, 180)
        
        # Top zigzag
        points = []
        for i in range(steps + 1):
            x = i * step_size
            y = margin if i % 2 == 0 else margin + 15
            points.append((x, y))
        draw.line(points, fill=zigzag_color, width=3)
        
        # Bottom zigzag
        points = []
        for i in range(steps + 1):
            x = i * step_size
            y = self.height - margin if i % 2 == 0 else self.height - margin - 15
            points.append((x, y))
        draw.line(points, fill=zigzag_color, width=3)
        
        # Add party elements
        # Balloons
        self._add_modern_balloons(draw, 8)
        
        # Add gift box
        self._add_gift_box(draw, self.width//4, self.height*2//3)
        
        # Add confetti
        for _ in range(150):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 8)
            
            # Random bright colors
            r = random.randint(200, 255)
            g = random.randint(200, 255)
            b = random.randint(200, 255)
            
            # Randomly choose between circle, square, or triangle
            shape_type = random.choice(["circle", "square", "triangle"])
            
            if shape_type == "circle":
                draw.ellipse([(x, y), (x+size, y+size)], fill=(r, g, b, 180))
            elif shape_type == "square":
                draw.rectangle([(x, y), (x+size, y+size)], fill=(r, g, b, 180))
            else:  # triangle
                draw.polygon([(x, y), (x+size, y+size), (x-size, y+size)], fill=(r, g, b, 180))
        
        # Add a ribbon banner with text
        banner_y = self.height//6
        self._add_ribbon_banner(draw, "Happy Birthday", banner_y, (255, 255, 255))
        
        # Add text area
        self._add_text_area_with_border(draw)
        
        # Add watermark
        self._add_watermark_text(draw, "Fun Birthday")
        
        return img
    
    def _create_kids_birthday(self):
        """Create a kids birthday template with cartoon elements"""
        # Create base image with bright color
        img = Image.new('RGB', (self.width, self.height), color=(64, 224, 208))
        draw = ImageDraw.Draw(img)
        
        # Add polka dots
        self._add_polka_dots(draw, 30, (255, 255, 255, 100))
        
        # Add cartoon cake
        self._add_cartoon_cake(draw)
        
        # Add text area
        self._add_text_area(draw)
        
        # Add watermark
        self._add_watermark_text(draw, "Kids Birthday")
        
        return img
    
    def _create_minimal_birthday(self):
        """Create a minimal birthday template"""
        # Create base image with light color
        img = Image.new('RGB', (self.width, self.height), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Add subtle geometric shapes
        self._add_geometric_elements(draw, 10, (200, 200, 200, 50))
        
        # Add minimal cake icon
        self._add_minimal_cake(draw, (100, 100, 100))
        
        # Add text area
        self._add_text_area(draw, opacity=50)
        
        # Add watermark
        self._add_watermark_text(draw, "Minimal Birthday")
        
        return img
    
    # Valentine Templates
    def _create_romantic_valentine(self):
        """Create a romantic valentine template with roses and hearts"""
        # Create base image with gradient
        img = self._create_gradient_background((220, 20, 60), (255, 200, 200))
        draw = ImageDraw.Draw(img)
        
        # Add heart pattern
        self._add_heart_pattern(draw, 20, (255, 255, 255, 50))
        
        # Add rose silhouette
        self._add_rose_silhouette(draw)
        
        # Add text area
        self._add_text_area(draw)
        
        # Add watermark
        self._add_watermark_text(draw, "Romantic Valentine")
        
        return img
    
    def _create_cute_valentine(self):
        """Create a cute valentine template with cartoon hearts"""
        # Create base image
        img = Image.new('RGB', (self.width, self.height), color=(255, 182, 193))
        draw = ImageDraw.Draw(img)
        
        # Add cute hearts
        self._add_cute_hearts(draw, 25)
        
        # Add text area
        self._add_text_area(draw)
        
        # Add watermark
        self._add_watermark_text(draw, "Cute Valentine")
        
        return img
    
    def _create_modern_valentine(self):
        """Create a modern valentine template with geometric hearts"""
        # Create base image
        img = Image.new('RGB', (self.width, self.height), color=(219, 112, 147))
        draw = ImageDraw.Draw(img)
        
        # Add geometric pattern
        self._add_geometric_pattern(draw)
        
        # Add geometric heart
        self._add_geometric_heart(draw)
        
        # Add text area
        self._add_text_area(draw)
        
        # Add watermark
        self._add_watermark_text(draw, "Modern Valentine")
        
        return img
    
    def _create_vintage_valentine(self):
        """Create a vintage valentine template"""
        # Create base image with vintage color
        img = Image.new('RGB', (self.width, self.height), color=(188, 143, 143))
        
        # Add texture
        img = self._add_vintage_texture(img)
        draw = ImageDraw.Draw(img)
        
        # Add vintage frame
        self._add_vintage_frame(draw)
        
        # Add text area
        self._add_text_area(draw, opacity=70)
        
        # Add watermark
        self._add_watermark_text(draw, "Vintage Valentine")
        
        return img
    
    # Helper methods for creating template elements
    def _create_gradient_background(self, color1, color2, direction="vertical"):
        """Create a gradient background"""
        if direction == "vertical":
            # Create a vertical gradient
            gradient = Image.new('RGB', (self.width, self.height), color=color1)
            draw = ImageDraw.Draw(gradient)
            
            for y in range(self.height):
                r = int(color1[0] + (color2[0] - color1[0]) * y / self.height)
                g = int(color1[1] + (color2[1] - color1[1]) * y / self.height)
                b = int(color1[2] + (color2[2] - color1[2]) * y / self.height)
                draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        else:
            # Create a horizontal gradient
            gradient = Image.new('RGB', (self.width, self.height), color=color1)
            draw = ImageDraw.Draw(gradient)
            
            for x in range(self.width):
                r = int(color1[0] + (color2[0] - color1[0]) * x / self.width)
                g = int(color1[1] + (color2[1] - color1[1]) * x / self.width)
                b = int(color1[2] + (color2[2] - color1[2]) * x / self.width)
                draw.line([(x, 0), (x, self.height)], fill=(r, g, b))
        
        return gradient
    
    def _add_corner_decorations(self, draw, color):
        """Add decorative corners to the template"""
        corner_size = 40
        corners = [
            (corner_size, corner_size),  # Top-left
            (self.width - corner_size, corner_size),  # Top-right
            (corner_size, self.height - corner_size),  # Bottom-left
            (self.width - corner_size, self.height - corner_size)  # Bottom-right
        ]
        
        for x, y in corners:
            # Draw diagonal lines
            draw.line([(x-20, y), (x, y-20)], fill=color, width=2)
            draw.line([(x-20, y), (x, y+20)], fill=color, width=2)
            draw.line([(x+20, y), (x, y-20)], fill=color, width=2)
            draw.line([(x+20, y), (x, y+20)], fill=color, width=2)
    
    def _add_confetti(self, draw, count):
        """Add confetti to the template"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(3, 10)
            r = random.randint(150, 255)
            g = random.randint(150, 255)
            b = random.randint(150, 255)
            
            # Randomly choose between circle, square, or triangle
            shape_type = random.choice(["circle", "square", "triangle"])
            
            if shape_type == "circle":
                draw.ellipse([(x, y), (x+size, y+size)], fill=(r, g, b))
            elif shape_type == "square":
                draw.rectangle([(x, y), (x+size, y+size)], fill=(r, g, b))
            else:  # triangle
                draw.polygon([(x, y), (x+size, y+size), (x-size, y+size)], fill=(r, g, b))
    
    def _add_balloons(self, draw, count):
        """Add balloon shapes to the template"""
        for _ in range(count):
            x = random.randint(50, self.width-50)
            y = random.randint(50, self.height-50)
            size = random.randint(20, 40)
            r = random.randint(150, 255)
            g = random.randint(150, 255)
            b = random.randint(150, 255)
            
            # Draw balloon
            draw.ellipse([(x-size, y-size*1.2), (x+size, y+size*0.8)], fill=(r, g, b))
            
            # Draw string
            string_length = random.randint(30, 60)
            draw.line([(x, y+size*0.8), (x+random.randint(-10, 10), y+size*0.8+string_length)], 
                     fill=(255, 255, 255), width=1)
    
    def _add_cake_silhouette(self, draw, color):
        """Add a cake silhouette to the template"""
        # Base coordinates for the cake
        center_x = self.width // 4
        bottom_y = self.height * 3 // 4
        
        # Cake base
        cake_width = 100
        cake_height = 60
        draw.rectangle(
            [(center_x - cake_width//2, bottom_y - cake_height), 
             (center_x + cake_width//2, bottom_y)],
            fill=color
        )
        
        # Cake top layer
        top_width = 70
        top_height = 30
        draw.rectangle(
            [(center_x - top_width//2, bottom_y - cake_height - top_height), 
             (center_x + top_width//2, bottom_y - cake_height)],
            fill=color
        )
        
        # Candles
        candle_positions = [center_x - 25, center_x, center_x + 25]
        for x in candle_positions:
            # Candle
            draw.rectangle(
                [(x-3, bottom_y - cake_height - top_height - 20), 
                 (x+3, bottom_y - cake_height - top_height)],
                fill=color
            )
            
            # Flame
            draw.ellipse(
                [(x-5, bottom_y - cake_height - top_height - 30), 
                 (x+5, bottom_y - cake_height - top_height - 20)],
                fill=(255, 200, 0, 200)
            )
    
    def _add_text_area(self, draw, opacity=80):
        """Add a semi-transparent text area to the template"""
        text_box_height = 100
        text_box_width = self.width // 2
        
        draw.rectangle(
            [(self.width//2 - text_box_width//2, self.height//2 - text_box_height//2), 
             (self.width//2 + text_box_width//2, self.height//2 + text_box_height//2)],
            fill=(255, 255, 255, opacity)
        )
    
    def _add_watermark_text(self, draw, text):
        """Add watermark text to the template"""
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        text_width, text_height = 100, 20  # Default fallback size
        try:
            # For newer Pillow versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            # For older Pillow versions
            elif hasattr(draw, 'textsize'):
                text_width, text_height = draw.textsize(text, font=font)
        except Exception:
            # Keep the fallback values if any error occurs
            pass
        
        position = (self.width - text_width - 10, self.height - text_height - 10)
        draw.text(position, text, fill=(255, 255, 255, 128), font=font)
    
    def _add_polka_dots(self, draw, count, color):
        """Add polka dots pattern"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(10, 30)
            draw.ellipse([(x-size//2, y-size//2), (x+size//2, y+size//2)], fill=color)
    
    def _add_cartoon_cake(self, draw):
        """Add a colorful cartoon cake"""
        # Base coordinates for the cake
        center_x = self.width // 4
        bottom_y = self.height * 3 // 4
        
        # Cake plate
        plate_width = 120
        draw.ellipse(
            [(center_x - plate_width//2, bottom_y - 10), 
             (center_x + plate_width//2, bottom_y + 10)],
            fill=(200, 200, 200)
        )
        
        # Cake base - first layer
        cake_width = 100
        cake_height = 30
        draw.rectangle(
            [(center_x - cake_width//2, bottom_y - cake_height), 
             (center_x + cake_width//2, bottom_y)],
            fill=(255, 200, 200)  # Pink
        )
        
        # Second layer
        layer2_width = 80
        draw.rectangle(
            [(center_x - layer2_width//2, bottom_y - cake_height*2), 
             (center_x + layer2_width//2, bottom_y - cake_height)],
            fill=(200, 255, 200)  # Light green
        )
        
        # Third layer
        layer3_width = 60
        draw.rectangle(
            [(center_x - layer3_width//2, bottom_y - cake_height*3), 
             (center_x + layer3_width//2, bottom_y - cake_height*2)],
            fill=(200, 200, 255)  # Light blue
        )
        
        # Frosting
        for i in range(10):
            x = center_x - cake_width//2 + i * cake_width//10
            draw.ellipse(
                [(x-5, bottom_y - cake_height - 5), (x+5, bottom_y - cake_height + 5)],
                fill=(255, 255, 255)
            )
        
        # Candles
        candle_positions = [center_x - 20, center_x, center_x + 20]
        candle_colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
        
        for i, x in enumerate(candle_positions):
            # Candle
            draw.rectangle(
                [(x-3, bottom_y - cake_height*3 - 20), 
                 (x+3, bottom_y - cake_height*3)],
                fill=candle_colors[i % len(candle_colors)]
            )
            
            # Flame
            draw.ellipse(
                [(x-5, bottom_y - cake_height*3 - 30), 
                 (x+5, bottom_y - cake_height*3 - 20)],
                fill=(255, 200, 0)
            )
    
    def _add_minimal_cake(self, draw, color):
        """Add a minimal cake icon"""
        # Base coordinates
        center_x = self.width // 4
        center_y = self.height // 2
        
        # Simple cake outline
        cake_width = 80
        cake_height = 50
        
        # Cake base
        draw.rectangle(
            [(center_x - cake_width//2, center_y - cake_height//2), 
             (center_x + cake_width//2, center_y + cake_height//2)],
            outline=color, width=2
        )
        
        # Single candle
        draw.line(
            [(center_x, center_y - cake_height//2), (center_x, center_y - cake_height//2 - 20)],
            fill=color, width=2
        )
        
        # Flame
        draw.ellipse(
            [(center_x-3, center_y - cake_height//2 - 25), 
             (center_x+3, center_y - cake_height//2 - 19)],
            fill=color
        )
    
    def _add_heart_pattern(self, draw, count, color):
        """Add a pattern of hearts"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(10, 30)
            self._draw_heart(draw, x, y, size, color)
    
    def _draw_heart(self, draw, x, y, size, color):
        """Draw a heart shape"""
        # Create heart shape using bezier curves
        # This is a simplified version using a polygon
        points = []
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            heart_x = size * 16 * math.sin(rad) ** 3
            heart_y = -size * (13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad))
            points.append((x + heart_x, y + heart_y))
        
        draw.polygon(points, fill=color)
    
    def _add_rose_silhouette(self, draw):
        """Add a rose silhouette"""
        # Base coordinates
        center_x = self.width // 4
        center_y = self.height // 2
        
        # Rose head
        rose_size = 50
        draw.ellipse(
            [(center_x - rose_size, center_y - rose_size), 
             (center_x + rose_size, center_y + rose_size)],
            fill=(150, 0, 0, 150)
        )
        
        # Stem
        draw.line(
            [(center_x, center_y + rose_size), (center_x, center_y + rose_size + 100)],
            fill=(0, 100, 0, 150), width=5
        )
        
        # Leaf
        leaf_points = [
            (center_x, center_y + rose_size + 50),
            (center_x + 30, center_y + rose_size + 30),
            (center_x + 40, center_y + rose_size + 60),
            (center_x, center_y + rose_size + 70)
        ]
        draw.polygon(leaf_points, fill=(0, 100, 0, 150))
    
    def _add_cute_hearts(self, draw, count):
        """Add cute cartoon hearts"""
        heart_colors = [(255, 0, 0, 200), (255, 100, 100, 200), (255, 150, 150, 200)]
        
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(15, 40)
            color = random.choice(heart_colors)
            
            # Draw heart
            self._draw_heart(draw, x, y, size, color)
            
            # Add cute face to some hearts
            if random.random() > 0.7:
                # Eyes
                eye_size = size // 8
                draw.ellipse(
                    [(x - size//3 - eye_size, y - eye_size), 
                     (x - size//3 + eye_size, y + eye_size)],
                    fill=(0, 0, 0)
                )
                draw.ellipse(
                    [(x + size//3 - eye_size, y - eye_size), 
                     (x + size//3 + eye_size, y + eye_size)],
                    fill=(0, 0, 0)
                )
                
                # Smile
                draw.arc(
                    [(x - size//3, y + size//4), (x + size//3, y + size//2)],
                    0, 180, fill=(0, 0, 0), width=2
                )
    
    def _add_geometric_pattern(self, draw):
        """Add a geometric pattern"""
        # Create a grid of shapes
        grid_size = 50
        for x in range(0, self.width, grid_size):
            for y in range(0, self.height, grid_size):
                if (x // grid_size + y // grid_size) % 2 == 0:
                    draw.rectangle(
                        [(x, y), (x + grid_size, y + grid_size)],
                        fill=(255, 255, 255, 30)
                    )
    
    def _add_geometric_heart(self, draw):
        """Add a geometric heart"""
        # Base coordinates
        center_x = self.width // 4
        center_y = self.height // 2
        size = 80
        
        # Create a geometric heart using simple shapes
        # Two squares rotated
        square1_points = [
            (center_x - size//2, center_y - size//2),
            (center_x + size//2, center_y - size//2),
            (center_x + size//2, center_y + size//2),
            (center_x - size//2, center_y + size//2)
        ]
        
        square2_points = [
            (center_x, center_y - size//2 - size//4),
            (center_x + size//2 + size//4, center_y),
            (center_x, center_y + size//2 + size//4),
            (center_x - size//2 - size//4, center_y)
        ]
        
        draw.polygon(square1_points, fill=(255, 255, 255, 100))
        draw.polygon(square2_points, fill=(255, 255, 255, 100))
    
    def _add_vintage_texture(self, img):
        """Add a vintage texture to the image"""
        # Create a noise texture
        noise = Image.new('L', (self.width, self.height))
        noise_draw = ImageDraw.Draw(noise)
        
        # Add random noise
        for x in range(0, self.width, 2):
            for y in range(0, self.height, 2):
                noise_value = random.randint(200, 255)
                noise_draw.point((x, y), fill=noise_value)
        
        # Blur the noise
        noise = noise.filter(ImageFilter.GaussianBlur(1))
        
        # Apply the noise as a texture
        img = Image.blend(img, noise.convert('RGB'), 0.1)
        
        # Reduce saturation
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.8)
        
        return img
    
    def _add_vintage_frame(self, draw):
        """Add a vintage decorative frame"""
        # Outer border
        border_width = 20
        draw.rectangle(
            [(border_width, border_width), 
             (self.width - border_width, self.height - border_width)],
            outline=(255, 255, 255, 150), width=2
        )
        
        # Corner decorations
        corner_size = 40
        corners = [
            (border_width, border_width),  # Top-left
            (self.width - border_width, border_width),  # Top-right
            (border_width, self.height - border_width),  # Bottom-left
            (self.width - border_width, self.height - border_width)  # Bottom-right
        ]
        
        for x, y in corners:
            # Draw ornate corner
            draw.arc(
                [(x - corner_size, y - corner_size), 
                 (x + corner_size, y + corner_size)],
                0, 90, fill=(255, 255, 255, 150), width=2
            )
            
            # Add small flourish
            draw.arc(
                [(x - corner_size//2, y - corner_size//2), 
                 (x + corner_size//2, y + corner_size//2)],
                0, 180, fill=(255, 255, 255, 150), width=2
            )
    
    def _create_default_template(self, category):
        """Create a default template for any category"""
        # Create base image
        img = Image.new('RGB', (self.width, self.height), color=(100, 100, 100))
        draw = ImageDraw.Draw(img)
        
        # Add simple decoration
        border_width = 20
        draw.rectangle(
            [(border_width, border_width), 
             (self.width - border_width, self.height - border_width)],
            outline=(255, 255, 255), width=2
        )
        
        # Add text area
        self._add_text_area(draw)
        
        # Add watermark
        self._add_watermark_text(draw, f"Default {category}")
        
        return img
    
    # Additional helper methods for other categories can be added here
    # For example, methods for Eid, Puja, and New Year templates
    
    def _create_traditional_eid(self):
        """Create a traditional Eid template with professional aesthetics"""
        # Create base image with gradient from dark green to lighter green
        img = self._create_gradient_background((0, 60, 30), (0, 100, 50))
        draw = ImageDraw.Draw(img)
        
        # Add Islamic pattern background
        pattern_color = (255, 255, 255, 30)  # Subtle white
        self._add_islamic_pattern(draw, pattern_color)
        
        # Add ornate frame with gold color
        border_width = 20
        gold_color = (218, 165, 32)
        
        # Outer frame
        draw.rectangle(
            [(border_width, border_width), 
             (self.width-border_width, self.height-border_width)],
            outline=gold_color, width=3
        )
        
        # Inner frame with decorative corners
        inner_padding = 10
        draw.rectangle(
            [(border_width+inner_padding, border_width+inner_padding), 
             (self.width-border_width-inner_padding, self.height-border_width-inner_padding)],
            outline=gold_color, width=1
        )
        
        # Add decorative corners
        corner_size = 40
        for x, y in [
            (border_width+inner_padding, border_width+inner_padding),
            (self.width-border_width-inner_padding, border_width+inner_padding),
            (border_width+inner_padding, self.height-border_width-inner_padding),
            (self.width-border_width-inner_padding, self.height-border_width-inner_padding)
        ]:
            self._add_islamic_corner_decoration(draw, x, y, corner_size, gold_color)
        
        # Add crescent moon and star
        moon_x = self.width // 2
        moon_y = self.height // 3
        self._add_realistic_crescent_and_star(draw, moon_x, moon_y, gold_color)
        
        # Add mosque silhouette
        self._add_detailed_mosque(draw, self.width//2, self.height*2//3, gold_color)
        
        # Add a decorative arch at the top with "Eid Mubarak" text
        arch_y = self.height // 6
        self._add_decorative_arch(draw, "Eid Mubarak", arch_y, gold_color)
        
        # Add text area
        self._add_eid_text_area(draw)
        
        # Add subtle lantern decorations
        for i in range(5):
            x_pos = self.width / 6 * (i + 1)
            y_pos = self.height // 4 * 3
            size = random.randint(15, 25)
            self._add_lantern(draw, x_pos, y_pos, size, gold_color)
        
        # Add watermark
        self._add_watermark_text(draw, "Traditional Eid")
        
        return img
    
    def _add_islamic_pattern(self, draw, color):
        """Add Islamic geometric pattern"""
        cell_size = 50
        for x in range(0, self.width, cell_size):
            for y in range(0, self.height, cell_size):
                if (x//cell_size + y//cell_size) % 2 == 0:
                    # Draw 8-point star
                    center_x = x + cell_size // 2
                    center_y = y + cell_size // 2
                    size = cell_size // 2
                    
                    # Create star points
                    points = []
                    for i in range(8):
                        angle = i * math.pi / 4
                        # Outer points
                        x1 = center_x + size * math.cos(angle)
                        y1 = center_y + size * math.sin(angle)
                        points.append((x1, y1))
                        
                        # Inner points
                        x2 = center_x + size * 0.4 * math.cos(angle + math.pi/8)
                        y2 = center_y + size * 0.4 * math.sin(angle + math.pi/8)
                        points.append((x2, y2))
                    
                    # Alternate points to create star pattern
                    draw.polygon(points, fill=color)
    
    def _add_islamic_corner_decoration(self, draw, x, y, size, color):
        """Add Islamic corner decoration pattern"""
        # Main arch
        draw.arc([(x-size, y-size), (x+size, y+size)], 0, 90, fill=color, width=2)
        
        # Inner arches
        for i in range(3):
            inner_size = size - (i+1) * 8
            if inner_size > 0:
                draw.arc([(x-inner_size, y-inner_size), (x+inner_size, y+inner_size)], 
                       0, 90, fill=color, width=1)
        
        # Decorative dots
        for i in range(5):
            dot_x = x + (i * size // 5) if x < self.width // 2 else x - (i * size // 5)
            dot_y = y + (i * size // 5) if y < self.height // 2 else y - (i * size // 5)
            
            dot_size = 2
            draw.ellipse([(dot_x-dot_size, dot_y-dot_size), (dot_x+dot_size, dot_y+dot_size)], 
                       fill=color)
    
    def _add_realistic_crescent_and_star(self, draw, x, y, color):
        """Add a realistic crescent moon and star"""
        # Outer circle (full moon)
        moon_radius = 50
        draw.ellipse(
            [(x-moon_radius, y-moon_radius), (x+moon_radius, y+moon_radius)],
            fill=(255, 255, 220)
        )
        
        # Inner circle (to create crescent)
        inner_radius = 45
        offset = 25
        draw.ellipse(
            [(x-inner_radius+offset, y-inner_radius), (x+inner_radius+offset, y+inner_radius)],
            fill=(0, 60, 30)  # Same as background
        )
        
        # Add star
        star_distance = 80
        star_size = 15
        star_x = x
        star_y = y - star_distance
        
        # Draw a 5-pointed star
        star_points = []
        for i in range(5):
            # Outer points
            angle = math.pi/2 + i * 2*math.pi/5
            star_points.append((star_x + star_size * math.cos(angle), 
                              star_y + star_size * math.sin(angle)))
            # Inner points
            angle += math.pi/5
            star_points.append((star_x + star_size/2 * math.cos(angle), 
                              star_y + star_size/2 * math.sin(angle)))
        
        draw.polygon(star_points, fill=color)
        
        # Add glow around star
        for i in range(3):
            glow_size = star_size + i*3
            glow_points = []
            for j in range(5):
                # Outer points
                angle = math.pi/2 + j * 2*math.pi/5
                glow_points.append((star_x + glow_size * math.cos(angle), 
                                  star_y + glow_size * math.sin(angle)))
                # Inner points
                angle += math.pi/5
                glow_points.append((star_x + glow_size/2 * math.cos(angle), 
                                  star_y + glow_size/2 * math.sin(angle)))
            
            draw.polygon(glow_points, outline=(color[0], color[1], color[2], 100-i*30), width=1)
    
    def _add_detailed_mosque(self, draw, x, y, color):
        """Add a detailed mosque silhouette"""
        # Base width and height
        base_width = 200
        base_height = 80
        
        # Ground/base
        draw.rectangle(
            [(x-base_width//2, y), (x+base_width//2, y+20)],
            fill=(0, 40, 20), outline=color, width=1
        )
        
        # Main structure
        structure_height = 100
        draw.rectangle(
            [(x-base_width//2, y-structure_height), (x+base_width//2, y)],
            fill=(0, 50, 25), outline=color, width=1
        )
        
        # Create doorway arch
        door_width = 40
        door_height = 60
        
        # Door
        draw.rectangle(
            [(x-door_width//2, y-door_height), (x+door_width//2, y)],
            fill=(50, 30, 10)
        )
        
        # Door arch
        draw.arc(
            [(x-door_width//2, y-door_height-door_width//2), (x+door_width//2, y-door_height+door_width//2)],
            180, 0, fill=color, width=2
        )
        
        # Windows (small arched windows along the structure)
        window_width = 15
        window_height = 25
        window_count = 5
        window_spacing = base_width // window_count
        
        for i in range(window_count):
            window_x = x - base_width//2 + window_spacing//2 + i*window_spacing
            window_y = y - structure_height//2
            
            # Skip middle for the door
            if i == window_count // 2:
                continue
                
            # Window rectangle
            draw.rectangle(
                [(window_x-window_width//2, window_y-window_height//2), 
                 (window_x+window_width//2, window_y+window_height//2)],
                fill=(200, 180, 50)
            )
            
            # Window arch
            draw.arc(
                [(window_x-window_width//2, window_y-window_height//2-window_width//2), 
                 (window_x+window_width//2, window_y-window_height//2+window_width//2)],
                180, 0, fill=color, width=1
            )
        
        # Main dome
        dome_radius = 50
        dome_center_y = y - structure_height - dome_radius//2
        
        # Draw dome
        draw.arc(
            [(x-dome_radius, dome_center_y-dome_radius), (x+dome_radius, dome_center_y+dome_radius)],
            180, 0, fill=color, width=2
        )
        
        # Dome top (finial)
        finial_height = 20
        finial_width = 5
        draw.rectangle(
            [(x-finial_width//2, dome_center_y-dome_radius-finial_height), 
             (x+finial_width//2, dome_center_y-dome_radius)],
            fill=color
        )
        draw.ellipse(
            [(x-finial_width, dome_center_y-dome_radius-finial_height-finial_width), 
             (x+finial_width, dome_center_y-dome_radius-finial_height+finial_width)],
            fill=color
        )
        
        # Minarets
        minaret_width = 10
        minaret_height = 150
        minaret_spacing = base_width * 3 // 4
        
        for side in [-1, 1]:
            minaret_x = x + side * minaret_spacing // 2
            
            # Minaret body
            draw.rectangle(
                [(minaret_x-minaret_width//2, y-minaret_height), 
                 (minaret_x+minaret_width//2, y)],
                fill=(0, 50, 25), outline=color, width=1
            )
            
            # Minaret top (dome)
            minaret_dome_radius = minaret_width
            draw.ellipse(
                [(minaret_x-minaret_dome_radius, y-minaret_height-minaret_dome_radius), 
                 (minaret_x+minaret_dome_radius, y-minaret_height+minaret_dome_radius)],
                fill=color
            )
            
            # Minaret windows (small decorative elements)
            for i in range(3):
                window_y = y - minaret_height//4 * (i+1)
                draw.rectangle(
                    [(minaret_x-minaret_width//2-1, window_y-3), 
                     (minaret_x+minaret_width//2+1, window_y+3)],
                    fill=(200, 180, 50)
                )
    
    def _add_decorative_arch(self, draw, text, y_position, color):
        """Add a decorative arch with text"""
        center_x = self.width // 2
        arch_width = self.width // 2
        arch_height = 80
        
        # Draw the main arch
        draw.arc(
            [(center_x - arch_width//2, y_position), 
             (center_x + arch_width//2, y_position + arch_height*2)],
            180, 0, fill=color, width=3
        )
        
        # Draw inner arch
        inner_padding = 5
        draw.arc(
            [(center_x - arch_width//2 + inner_padding, y_position + inner_padding), 
             (center_x + arch_width//2 - inner_padding, y_position + arch_height*2 - inner_padding)],
            180, 0, fill=color, width=1
        )
        
        # Add decorative elements along the arch
        for i in range(10):
            angle = math.pi * i / 10
            x = center_x + (arch_width//2 - 10) * math.cos(angle)
            y = y_position + arch_height + arch_height * math.sin(angle)
            
            # Small decorative circle
            draw.ellipse(
                [(x-3, y-3), (x+3, y+3)],
                fill=color
            )
        
        # Add text below the arch
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        # Get text size for centering
        text_width, text_height = 100, 20  # Default fallback size
        try:
            # For newer Pillow versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            # For older Pillow versions
            elif hasattr(draw, 'textsize'):
                text_width, text_height = draw.textsize(text, font=font)
        except Exception:
            # Keep the fallback values if any error occurs
            pass
        
        # Draw text with decorative flourish
        draw.text(
            (center_x - text_width//2, y_position + arch_height//2 - text_height//2),
            text, fill=color, font=font
        )
    
    def _add_eid_text_area(self, draw, opacity=70):
        """Add a text area for Eid cards with Islamic style borders"""
        text_box_height = 120
        text_box_width = self.width // 2 + 50
        
        # Center coordinates
        center_x = self.width//2
        center_y = self.height//2 + 40
        
        # Create a rounded rectangle with Islamic pattern border
        # Main area with slight transparency
        draw.rectangle(
            [(center_x - text_box_width//2, center_y - text_box_height//2), 
             (center_x + text_box_width//2, center_y + text_box_height//2)],
            fill=(255, 255, 255, opacity)
        )
        
        # Add a subtle pattern inside the text area
        pattern_opacity = 20
        for i in range(0, text_box_width, 20):
            for j in range(0, text_box_height, 20):
                if (i//20 + j//20) % 2 == 0:
                    draw.rectangle(
                        [(center_x - text_box_width//2 + i, center_y - text_box_height//2 + j),
                         (center_x - text_box_width//2 + i + 10, center_y - text_box_height//2 + j + 10)],
                        fill=(200, 180, 50, pattern_opacity)
                    )
    
    def _add_lantern(self, draw, x, y, size, color):
        """Add a decorative Ramadan lantern"""
        # Lantern body
        body_width = size
        body_height = size * 2
        
        # Top dome
        dome_radius = size // 2
        draw.arc(
            [(x-dome_radius, y-body_height-dome_radius), (x+dome_radius, y-body_height+dome_radius)],
            180, 0, fill=color, width=2
        )
        
        # Top connector
        connector_height = size // 4
        draw.rectangle(
            [(x-size//6, y-body_height-connector_height), (x+size//6, y-body_height)],
            outline=color, width=1
        )
        
        # Main body with tapered shape
        # Calculate points for a hexagonal shape
        points = [
            (x-body_width//2, y-body_height+body_height//6),  # Top left
            (x+body_width//2, y-body_height+body_height//6),  # Top right
            (x+body_width//2+body_width//6, y-body_height//2),  # Middle right
            (x+body_width//2, y-body_height//6),  # Bottom right
            (x-body_width//2, y-body_height//6),  # Bottom left
            (x-body_width//2-body_width//6, y-body_height//2),  # Middle left
        ]
        
        draw.polygon(points, outline=color, width=2)
        
        # Inner details - decorative patterns
        inner_points = []
        for px, py in points:
            # Calculate a point closer to the center
            inner_x = x + (px - x) * 0.7
            inner_y = y-body_height//2 + (py - (y-body_height//2)) * 0.7
            inner_points.append((inner_x, inner_y))
        
        draw.polygon(inner_points, outline=color, width=1)
        
        # Bottom base
        base_width = body_width // 2
        base_height = size // 4
        draw.rectangle(
            [(x-base_width//2, y-base_height), (x+base_width//2, y)],
            outline=color, width=1
        )
        
        # Add a small light in the center (glowing effect)
        glow_radius = size // 3
        for i in range(3):
            opacity = 100 - i * 30
            radius = glow_radius - i * 2
            draw.ellipse(
                [(x-radius, y-body_height//2-radius), (x+radius, y-body_height//2+radius)],
                fill=(255, 255, 200, opacity), outline=(255, 255, 150, opacity)
            )
    
    def _create_diwali_template(self):
        """Create a professionally designed Diwali template"""
        # Create a rich gradient background from deep purple to dark red
        img = self._create_gradient_background((75, 0, 130), (150, 0, 50))
        draw = ImageDraw.Draw(img)
        
        # Add subtle mandala pattern to background
        self._add_mandala_pattern(draw, self.width//2, self.height//2, 200, (255, 255, 255, 20))
        
        # Add gold border
        border_width = 20
        gold_color = (255, 215, 0)
        
        # Outer border
        draw.rectangle(
            [(border_width, border_width), (self.width-border_width, self.height-border_width)],
            outline=gold_color, width=3
        )
        
        # Inner border with traditional pattern
        inner_padding = 10
        self._add_rangoli_border(
            draw, 
            [(border_width+inner_padding, border_width+inner_padding), 
             (self.width-border_width-inner_padding, self.height-border_width-inner_padding)],
            gold_color
        )
        
        # Add diyas (oil lamps) along the bottom
        diya_count = 5
        y_position = self.height * 3 // 4
        spacing = self.width // (diya_count + 1)
        
        for i in range(diya_count):
            x_position = spacing * (i + 1)
            self._add_realistic_diya(draw, x_position, y_position, 30, gold_color)
        
        # Add decorative Diwali title
        self._add_decorative_title(draw, "Happy Diwali", self.height // 4, gold_color)
        
        # Add lotus design
        lotus_x = self.width // 4
        lotus_y = self.height // 2
        self._add_lotus_design(draw, lotus_x, lotus_y, 60, gold_color)
        
        # Add text area
        self._add_diwali_text_area(draw)
        
        # Add small rangoli designs in corners
        corner_size = 50
        for x, y in [
            (border_width+inner_padding+corner_size, border_width+inner_padding+corner_size),
            (self.width-border_width-inner_padding-corner_size, border_width+inner_padding+corner_size),
            (border_width+inner_padding+corner_size, self.height-border_width-inner_padding-corner_size),
            (self.width-border_width-inner_padding-corner_size, self.height-border_width-inner_padding-corner_size)
        ]:
            self._add_small_rangoli(draw, x, y, corner_size//2, gold_color)
        
        # Add watermark
        self._add_watermark_text(draw, "Diwali Celebration")
        
        return img
    
    def _add_mandala_pattern(self, draw, center_x, center_y, size, color):
        """Add a mandala-like pattern"""
        num_circles = 4
        num_points = 16
        
        for circle_idx in range(num_circles):
            radius = size // 2 - circle_idx * (size // 8)
            
            # Draw circle
            draw.ellipse(
                [(center_x - radius, center_y - radius), 
                 (center_x + radius, center_y + radius)],
                outline=color, width=1
            )
            
            # Draw geometric pattern
            for i in range(num_points):
                angle = i * 2 * math.pi / num_points
                x1 = center_x + radius * math.cos(angle)
                y1 = center_y + radius * math.sin(angle)
                
                # Lines to center
                if circle_idx % 2 == 0:
                    draw.line([(center_x, center_y), (x1, y1)], fill=color, width=1)
                
                # Connect points along the circle
                if i % 2 == 0:
                    next_angle = (i + 1) * 2 * math.pi / num_points
                    x2 = center_x + radius * math.cos(next_angle)
                    y2 = center_y + radius * math.sin(next_angle)
                    draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
    
    def _add_rangoli_border(self, draw, rect, color):
        """Add a traditional rangoli pattern border"""
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        width = x2 - x1
        height = y2 - y1
        
        # Draw the basic rectangle
        draw.rectangle(rect, outline=color, width=1)
        
        # Add pattern elements along the border
        # Top and bottom edges
        num_elements = width // 20
        for i in range(num_elements):
            # Position along the edge
            x = x1 + i * width / num_elements + width / (2 * num_elements)
            
            # Top edge element
            self._draw_small_flower(draw, x, y1, 5, color)
            
            # Bottom edge element
            self._draw_small_flower(draw, x, y2, 5, color)
        
        # Left and right edges
        num_elements = height // 20
        for i in range(num_elements):
            # Position along the edge
            y = y1 + i * height / num_elements + height / (2 * num_elements)
            
            # Left edge element
            self._draw_small_flower(draw, x1, y, 5, color)
            
            # Right edge element
            self._draw_small_flower(draw, x2, y, 5, color)
    
    def _draw_small_flower(self, draw, x, y, size, color):
        """Draw a small stylized flower"""
        # Central dot
        draw.ellipse(
            [(x-size//3, y-size//3), (x+size//3, y+size//3)],
            fill=color
        )
        
        # Petals
        for i in range(6):
            angle = i * math.pi / 3
            petal_x = x + size * math.cos(angle)
            petal_y = y + size * math.sin(angle)
            
            draw.ellipse(
                [(petal_x-size//3, petal_y-size//3), 
                 (petal_x+size//3, petal_y+size//3)],
                fill=color
            )
    
    def _add_realistic_diya(self, draw, x, y, size, color):
        """Add a realistic diya (oil lamp)"""
        # Diya base - clay lamp shape
        clay_color = (150, 75, 0)  # Brown
        
        # Create base shape (semi-ellipse)
        base_width = size * 1.5
        base_height = size * 0.8
        
        # Draw the base
        base_points = []
        for angle in range(180, 360):
            rad_angle = math.radians(angle)
            base_x = x + base_width/2 * math.cos(rad_angle)
            base_y = y + base_height/2 * math.sin(rad_angle)
            base_points.append((base_x, base_y))
        
        # Add top points to close the shape
        base_points.append((x + base_width/2, y))
        base_points.append((x - base_width/2, y))
        
        # Draw the clay lamp
        draw.polygon(base_points, fill=clay_color, outline=(100, 50, 0))
        
        # Add a texture effect to the clay
        for i in range(5):
            texture_y = y + i * base_height / 10
            texture_width = base_width * (0.8 - i * 0.1)
            if texture_width > 0:
                draw.line(
                    [(x - texture_width/2, texture_y), (x + texture_width/2, texture_y)],
                    fill=(100, 50, 0), width=1
                )
        
        # Oil in the diya
        oil_level = y - base_height * 0.2
        oil_width = base_width * 0.7
        draw.ellipse(
            [(x - oil_width/2, oil_level - base_height*0.1), 
             (x + oil_width/2, oil_level + base_height*0.1)],
            fill=(200, 180, 50)  # Golden oil color
        )
        
        # Add flame
        flame_height = size * 0.8
        flame_width = size * 0.3
        
        # Main flame - create a teardrop shape
        flame_points = []
        for angle in range(0, 180):
            rad_angle = math.radians(angle)
            flame_x = x + flame_width/2 * math.cos(rad_angle)
            flame_y = oil_level - flame_height * (1 - math.sin(rad_angle))
            flame_points.append((flame_x, flame_y))
        
        # Bottom points to close the shape
        flame_points.append((x + flame_width/2, oil_level))
        flame_points.append((x - flame_width/2, oil_level))
        
        # Draw the flame
        draw.polygon(flame_points, fill=(255, 200, 0))  # Yellow flame
        
        # Inner brighter flame
        inner_flame_points = []
        inner_flame_width = flame_width * 0.6
        inner_flame_height = flame_height * 0.7
        
        for angle in range(0, 180):
            rad_angle = math.radians(angle)
            flame_x = x + inner_flame_width/2 * math.cos(rad_angle)
            flame_y = oil_level - inner_flame_height * (1 - math.sin(rad_angle))
            inner_flame_points.append((flame_x, flame_y))
        
        # Bottom points to close the shape
        inner_flame_points.append((x + inner_flame_width/2, oil_level))
        inner_flame_points.append((x - inner_flame_width/2, oil_level))
        
        # Draw the inner flame
        draw.polygon(inner_flame_points, fill=(255, 255, 200))  # Brighter yellow
        
        # Add glow effect around flame
        for i in range(3):
            glow_radius = flame_width/2 + i * flame_width/4
            opacity = 150 - i * 50
            if opacity > 0:
                draw.ellipse(
                    [(x - glow_radius, oil_level - flame_height/2 - glow_radius),
                     (x + glow_radius, oil_level - flame_height/2 + glow_radius)],
                    fill=(255, 200, 0, opacity), outline=(255, 200, 0, opacity//2)
                )
    
    def _add_decorative_title(self, draw, text, y_position, color):
        """Add decorative title with ornate styling"""
        center_x = self.width // 2
        
        # Try to use a decorative font
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Get text size for centering
        text_width, text_height = 200, 40  # Default fallback size
        try:
            # For newer Pillow versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            # For older Pillow versions
            elif hasattr(draw, 'textsize'):
                text_width, text_height = draw.textsize(text, font=font)
        except Exception:
            # Keep the fallback values if any error occurs
            pass
        
        # Add a decorative background behind the text
        padding = 20
        bg_rect = [
            (center_x - text_width/2 - padding, y_position - text_height/2 - padding),
            (center_x + text_width/2 + padding, y_position + text_height/2 + padding)
        ]
        
        # Draw a rectangle with slight transparency
        bg_color = (100, 0, 50, 150)  # Semi-transparent deep red
        draw.rectangle(bg_rect, fill=bg_color)
        
        # Add decorative corners
        corner_size = 10
        for (x, y) in [
            (bg_rect[0][0], bg_rect[0][1]),  # Top-left
            (bg_rect[1][0], bg_rect[0][1]),  # Top-right
            (bg_rect[0][0], bg_rect[1][1]),  # Bottom-left
            (bg_rect[1][0], bg_rect[1][1]),  # Bottom-right
        ]:
            # Draw corner decoration
            if x == bg_rect[0][0]:  # Left corners
                draw.line([(x, y-corner_size), (x, y), (x+corner_size, y)], fill=color, width=2)
            else:  # Right corners
                draw.line([(x, y-corner_size), (x, y), (x-corner_size, y)], fill=color, width=2)
        
        # Draw the text with shadow effect
        shadow_offset = 2
        draw.text(
            (center_x - text_width/2 + shadow_offset, y_position - text_height/2 + shadow_offset),
            text, fill=(0, 0, 0, 150), font=font
        )
        
        draw.text(
            (center_x - text_width/2, y_position - text_height/2),
            text, fill=color, font=font
        )
        
        # Add decorative lines on either side of text
        line_length = 100
        line_spacing = 30
        
        # Left decorative line
        draw.line(
            [(center_x - text_width/2 - line_spacing - line_length, y_position),
             (center_x - text_width/2 - line_spacing, y_position)],
            fill=color, width=2
        )
        
        # Right decorative line
        draw.line(
            [(center_x + text_width/2 + line_spacing, y_position),
             (center_x + text_width/2 + line_spacing + line_length, y_position)],
            fill=color, width=2
        )
        
        # Add ornaments at the ends of lines
        ornament_size = 5
        for x in [center_x - text_width/2 - line_spacing - line_length, 
                center_x - text_width/2 - line_spacing,
                center_x + text_width/2 + line_spacing,
                center_x + text_width/2 + line_spacing + line_length]:
            
            draw.ellipse(
                [(x - ornament_size, y_position - ornament_size),
                 (x + ornament_size, y_position + ornament_size)],
                fill=color
            )
    
    def _add_lotus_design(self, draw, x, y, size, color):
        """Add a lotus flower design"""
        # Center circle
        center_size = size // 4
        draw.ellipse(
            [(x - center_size, y - center_size),
             (x + center_size, y + center_size)],
            fill=(255, 200, 100), outline=color
        )
        
        # Petals
        petal_count = 8
        for i in range(petal_count):
            angle = i * 2 * math.pi / petal_count
            
            # Calculate control points for a curved petal
            # Petal tip
            tip_x = x + size * math.cos(angle)
            tip_y = y + size * math.sin(angle)
            
            # First control point (closer to center)
            ctrl1_x = x + center_size * 2 * math.cos(angle)
            ctrl1_y = y + center_size * 2 * math.sin(angle)
            
            # Second control points (on either side)
            side_angle1 = angle - math.pi/16
            side_angle2 = angle + math.pi/16
            
            side1_x = x + size * 0.7 * math.cos(side_angle1)
            side1_y = y + size * 0.7 * math.sin(side_angle1)
            
            side2_x = x + size * 0.7 * math.cos(side_angle2)
            side2_y = y + size * 0.7 * math.sin(side_angle2)
            
            # Draw the petal as a polygon
            petal_points = [
                (x, y),
                (ctrl1_x, ctrl1_y),
                (side1_x, side1_y),
                (tip_x, tip_y),
                (side2_x, side2_y),
                (ctrl1_x, ctrl1_y)
            ]
            
            # Alternate petal colors
            if i % 2 == 0:
                petal_fill = (255, 200, 100, 200)  # Light gold
            else:
                petal_fill = (255, 220, 180, 200)  # Lighter gold
                
            draw.polygon(petal_points, fill=petal_fill, outline=color)
            
        # Add inner details
        for i in range(petal_count):
            angle = i * 2 * math.pi / petal_count
            inner_x = x + center_size * 1.5 * math.cos(angle)
            inner_y = y + center_size * 1.5 * math.sin(angle)
            
            draw.ellipse(
                [(inner_x - 3, inner_y - 3),
                 (inner_x + 3, inner_y + 3)],
                fill=color
            )
    
    def _add_diwali_text_area(self, draw, opacity=80):
        """Add a text area with Diwali-themed decorations"""
        text_box_height = 120
        text_box_width = self.width // 2 + 50
        
        # Center coordinates
        center_x = self.width//2
        center_y = self.height//2 + 40
        
        # Draw decorative text area with rounded corners
        draw.rectangle(
            [(center_x - text_box_width//2, center_y - text_box_height//2), 
             (center_x + text_box_width//2, center_y + text_box_height//2)],
            fill=(255, 255, 255, opacity), outline=(255, 215, 0), width=2
        )
        
        # Add decorative elements in corners of text area
        corner_size = 15
        for corner_x, corner_y in [
            (center_x - text_box_width//2 + corner_size, center_y - text_box_height//2 + corner_size),
            (center_x + text_box_width//2 - corner_size, center_y - text_box_height//2 + corner_size),
            (center_x - text_box_width//2 + corner_size, center_y + text_box_height//2 - corner_size),
            (center_x + text_box_width//2 - corner_size, center_y + text_box_height//2 - corner_size),
        ]:
            self._draw_small_flower(draw, corner_x, corner_y, corner_size//2, (255, 215, 0))
    
    def _add_small_rangoli(self, draw, x, y, size, color):
        """Add a small rangoli design at the specified position"""
        # Center dot
        draw.ellipse(
            [(x - size//4, y - size//4), (x + size//4, y + size//4)],
            fill=color
        )
        
        # Concentric circles
        for i in range(2):
            radius = size//2 + i * size//4
            draw.ellipse(
                [(x - radius, y - radius), (x + radius, y + radius)],
                outline=color, width=1
            )
        
        # Radial lines
        for i in range(8):
            angle = i * math.pi / 4
            end_x = x + size * math.cos(angle)
            end_y = y + size * math.sin(angle)
            draw.line([(x, y), (end_x, end_y)], fill=color, width=1)
            
            # Small dots at the ends of lines
            dot_size = 2
            draw.ellipse(
                [(end_x - dot_size, end_y - dot_size), 
                 (end_x + dot_size, end_y + dot_size)],
                fill=color
            )
    
    def _create_fireworks_newyear(self):
        """Create a New Year template with fireworks"""
        # Create dark blue background
        img = Image.new('RGB', (self.width, self.height), color=(25, 25, 112))
        draw = ImageDraw.Draw(img)
        
        # Add city skyline silhouette
        self._add_city_skyline(draw)
        
        # Add fireworks
        self._add_fireworks(draw, 8)
        
        # Add text area
        self._add_text_area(draw)
        
        # Add watermark
        self._add_watermark_text(draw, "New Year Fireworks")
        
        return img
    
    def _add_city_skyline(self, draw):
        """Add a city skyline silhouette"""
        # Base coordinates
        base_y = self.height * 3 // 4
        
        # Create random buildings
        building_count = 15
        building_width = self.width // building_count
        
        for i in range(building_count):
            x = i * building_width
            height = random.randint(30, 100)
            
            # Draw building
            draw.rectangle(
                [(x, base_y - height), (x + building_width, base_y)],
                fill=(0, 0, 0)
            )
            
            # Add windows
            window_size = 5
            for wy in range(base_y - height + 10, base_y - 10, 15):
                for wx in range(x + 5, x + building_width - 5, 15):
                    if random.random() > 0.3:  # Some windows are lit
                        draw.rectangle(
                            [(wx, wy), (wx + window_size, wy + window_size)],
                            fill=(255, 255, 200)
                        )
    
    def _add_fireworks(self, draw, count):
        """Add fireworks to the template"""
        for _ in range(count):
            # Random position for firework
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height // 2)
            
            # Random color
            r = random.randint(150, 255)
            g = random.randint(150, 255)
            b = random.randint(150, 255)
            color = (r, g, b, 200)
            
            # Random size
            size = random.randint(30, 80)
            
            # Draw firework rays
            ray_count = random.randint(20, 40)
            for i in range(ray_count):
                angle = i * 2 * math.pi / ray_count
                end_x = x + size * math.cos(angle)
                end_y = y + size * math.sin(angle)
                
                # Draw ray with fading effect
                for t in range(10):
                    t_ratio = t / 10
                    point_x = x + (end_x - x) * t_ratio
                    point_y = y + (end_y - y) * t_ratio
                    point_size = 3 - 2 * t_ratio  # Decreasing size
                    alpha = int(200 - 150 * t_ratio)  # Decreasing alpha
                    
                    draw.ellipse(
                        [(point_x - point_size, point_y - point_size), 
                         (point_x + point_size, point_y + point_size)],
                        fill=(r, g, b, alpha)
                    )
    
    def _draw_star(self, draw, x, y, size, color):
        """Draw a star shape"""
        points = []
        for i in range(5):
            # Outer point
            angle_outer = i * 2 * math.pi / 5
            x_outer = x + size * math.cos(angle_outer - math.pi/2)
            y_outer = y + size * math.sin(angle_outer - math.pi/2)
            points.append((x_outer, y_outer))
            
            # Inner point
            angle_inner = angle_outer + math.pi / 5
            x_inner = x + size/2 * math.cos(angle_inner - math.pi/2)
            y_inner = y + size/2 * math.sin(angle_inner - math.pi/2)
            points.append((x_inner, y_inner))
        
        draw.polygon(points, fill=color)
    
    def _add_elegant_cake(self, draw, gold_color):
        """Add an elegant birthday cake"""
        # Base coordinates
        center_x = self.width // 3
        bottom_y = self.height * 2 // 3
        
        # Cake base color
        cake_color = (255, 245, 235)
        frosting_color = (255, 255, 255)
        
        # Cake plate
        plate_width = 140
        draw.ellipse(
            [(center_x - plate_width//2, bottom_y - 5), 
             (center_x + plate_width//2, bottom_y + 15)],
            fill=(230, 230, 230), outline=(200, 200, 200)
        )
        
        # Cake layers
        layer_heights = [40, 30, 25]
        layer_widths = [120, 100, 80]
        
        current_y = bottom_y
        for i, (height, width) in enumerate(zip(layer_heights, layer_widths)):
            # Cake layer
            draw.rectangle(
                [(center_x - width//2, current_y - height), 
                 (center_x + width//2, current_y)],
                fill=cake_color, outline=(220, 220, 220)
            )
            
            # Layer frosting
            draw.rectangle(
                [(center_x - width//2, current_y - height - 5), 
                 (center_x + width//2, current_y - height)],
                fill=frosting_color
            )
            
            # Add texture to frosting
            for j in range(width):
                if j % 10 < 5:  # Create a pattern
                    draw.ellipse(
                        [(center_x - width//2 + j, current_y - height - 8),
                         (center_x - width//2 + j + 5, current_y - height - 3)],
                        fill=frosting_color
                    )
            
            current_y -= height
        
        # Candles
        candle_positions = [center_x - 25, center_x, center_x + 25]
        candle_colors = [(255, 200, 200), (200, 255, 200), (200, 200, 255)]
        
        for i, x in enumerate(candle_positions):
            # Candle
            candle_color = candle_colors[i % len(candle_colors)]
            
            # Candle base
            draw.rectangle(
                [(x-3, current_y - 30), (x+3, current_y)],
                fill=candle_color
            )
            
            # Candle stripes
            for j in range(current_y - 30, current_y, 6):
                draw.line(
                    [(x-3, j), (x+3, j)],
                    fill=(255, 255, 255), width=1
                )
            
            # Flame
            flame_points = [
                (x, current_y - 40),
                (x-4, current_y - 32),
                (x+4, current_y - 32)
            ]
            draw.polygon(flame_points, fill=(255, 200, 0))
            
            # Flame glow
            for radius in range(3, 8, 2):
                draw.ellipse(
                    [(x-radius, current_y - 40 - radius), 
                     (x+radius, current_y - 40 + radius)],
                    outline=(255, 200, 0, 150 - radius * 20), width=1
                )
    
    def _add_text_area_with_shadow(self, draw, opacity=80):
        """Add a semi-transparent text area with shadow effect"""
        text_box_height = 120
        text_box_width = self.width // 2 + 50
        
        # Center coordinates
        center_x = self.width//2
        center_y = self.height//2 + 30
        
        # Shadow first
        shadow_offset = 5
        draw.rectangle(
            [(center_x - text_box_width//2 + shadow_offset, center_y - text_box_height//2 + shadow_offset), 
             (center_x + text_box_width//2 + shadow_offset, center_y + text_box_height//2 + shadow_offset)],
            fill=(100, 100, 100, 40)
        )
        
        # Text area with slightly rounded corners
        draw.rectangle(
            [(center_x - text_box_width//2, center_y - text_box_height//2), 
             (center_x + text_box_width//2, center_y + text_box_height//2)],
            fill=(255, 255, 255, opacity)
        )
        
        # Add a subtle inner border
        draw.rectangle(
            [(center_x - text_box_width//2 + 3, center_y - text_box_height//2 + 3), 
             (center_x + text_box_width//2 - 3, center_y + text_box_height//2 - 3)],
            outline=(220, 220, 220, 150), width=1
        )
    
    def _add_modern_balloons(self, draw, count):
        """Add modern, glossy balloons"""
        balloon_colors = [
            (255, 105, 180),  # Hot Pink
            (255, 215, 0),    # Gold
            (0, 191, 255),    # Deep Sky Blue
            (50, 205, 50),    # Lime Green
            (255, 69, 0),     # Orange Red
            (138, 43, 226)    # Blue Violet
        ]
        
        for _ in range(count):
            x = random.randint(50, self.width-50)
            y = random.randint(100, self.height//2)
            size = random.randint(30, 50)
            
            # Select color
            color = random.choice(balloon_colors)
            
            # Draw balloon body
            draw.ellipse(
                [(x-size, y-size*1.2), (x+size, y+size*0.8)],
                fill=color
            )
            
            # Add glossy highlight
            highlight_size = size // 2
            offset = size // 4
            draw.ellipse(
                [(x-highlight_size+offset, y-highlight_size), 
                 (x+highlight_size//2, y-highlight_size//2)],
                fill=(255, 255, 255, 100)
            )
            
            # Draw string with slight curve
            string_points = []
            string_length = random.randint(100, 200)
            curve_amplitude = random.randint(5, 15) * (1 if random.random() > 0.5 else -1)
            
            for i in range(string_length):
                t = i / string_length
                curve = curve_amplitude * math.sin(t * math.pi)
                string_points.append((
                    x + curve,
                    y + size*0.8 + i
                ))
            
            for i in range(len(string_points)-1):
                draw.line([string_points[i], string_points[i+1]], fill=(255, 255, 255), width=2)
            
            # Add balloon tie
            draw.ellipse(
                [(x-3, y+size*0.8-3), (x+3, y+size*0.8+3)],
                fill=(255, 255, 255)
            )
    
    def _add_gift_box(self, draw, x, y):
        """Add a colorful gift box"""
        # Box dimensions
        width = 80
        height = 60
        
        # Box base - bright colorful box
        box_color = (50, 205, 50)  # Green
        draw.rectangle(
            [(x-width//2, y-height), (x+width//2, y)],
            fill=box_color, outline=(30, 180, 30)
        )
        
        # Box top
        top_height = 20
        draw.rectangle(
            [(x-width//2, y-height-top_height), (x+width//2, y-height)],
            fill=box_color, outline=(30, 180, 30)
        )
        
        # Ribbon vertical
        ribbon_width = 10
        ribbon_color = (255, 50, 50)  # Red
        draw.rectangle(
            [(x-ribbon_width//2, y-height-top_height), (x+ribbon_width//2, y)],
            fill=ribbon_color
        )
        
        # Ribbon horizontal
        draw.rectangle(
            [(x-width//2, y-height-top_height//2-ribbon_width//2), 
             (x+width//2, y-height-top_height//2+ribbon_width//2)],
            fill=ribbon_color
        )
        
        # Ribbon bow
        bow_size = 20
        left_loop = [
            (x-ribbon_width//2, y-height-top_height-5),
            (x-bow_size, y-height-top_height-bow_size),
            (x-bow_size, y-height-top_height-bow_size//2),
            (x-ribbon_width//2, y-height-top_height+5)
        ]
        
        right_loop = [
            (x+ribbon_width//2, y-height-top_height-5),
            (x+bow_size, y-height-top_height-bow_size),
            (x+bow_size, y-height-top_height-bow_size//2),
            (x+ribbon_width//2, y-height-top_height+5)
        ]
        
        draw.polygon(left_loop, fill=ribbon_color)
        draw.polygon(right_loop, fill=ribbon_color)
        
        # Knot in the middle
        draw.ellipse(
            [(x-ribbon_width, y-height-top_height-ribbon_width), 
             (x+ribbon_width, y-height-top_height+ribbon_width)],
            fill=(220, 50, 50)
        )
        
        # Add shine/highlight to box
        for i in range(3):
            highlight_y = y - height//2 - i*10
            highlight_size = width//3 - i*5
            opacity = 120 - i*30
            
            draw.ellipse(
                [(x-highlight_size, highlight_y-2), (x+highlight_size, highlight_y+2)],
                fill=(255, 255, 255, opacity)
            )
    
    def _add_ribbon_banner(self, draw, text, y_position, text_color, angle=0):
        """Add a ribbon banner with text"""
        banner_width = self.width - 100
        banner_height = 60
        banner_x = self.width // 2
        banner_y = y_position
        
        # Banner color with gradient effect
        banner_color1 = (255, 100, 150)
        banner_color2 = (255, 50, 100)
        
        # Draw banner body
        draw.rectangle(
            [(banner_x - banner_width//2, banner_y), 
             (banner_x + banner_width//2, banner_y + banner_height)],
            fill=banner_color1
        )
        
        # Add gradient effect
        for i in range(banner_height//2):
            y = banner_y + i
            opacity = 150 - i * 5 if i < 20 else 0
            draw.line(
                [(banner_x - banner_width//2, y), (banner_x + banner_width//2, y)],
                fill=(255, 255, 255, opacity)
            )
        
        # Banner left tail
        left_tail = [
            (banner_x - banner_width//2, banner_y),
            (banner_x - banner_width//2 - 20, banner_y + banner_height//2),
            (banner_x - banner_width//2, banner_y + banner_height)
        ]
        draw.polygon(left_tail, fill=banner_color2)
        
        # Banner right tail
        right_tail = [
            (banner_x + banner_width//2, banner_y),
            (banner_x + banner_width//2 + 20, banner_y + banner_height//2),
            (banner_x + banner_width//2, banner_y + banner_height)
        ]
        draw.polygon(right_tail, fill=banner_color2)
        
        # Add text to banner
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        # Get text size for centering
        text_width, text_height = 100, 20  # Default fallback size
        try:
            # For newer Pillow versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            # For older Pillow versions
            elif hasattr(draw, 'textsize'):
                text_width, text_height = draw.textsize(text, font=font)
        except Exception:
            # Keep the fallback values if any error occurs
            pass
        
        # Draw text with subtle shadow for depth
        shadow_offset = 2
        draw.text(
            (banner_x - text_width//2 + shadow_offset, banner_y + banner_height//2 - text_height//2 + shadow_offset),
            text, fill=(100, 50, 50), font=font
        )
        
        draw.text(
            (banner_x - text_width//2, banner_y + banner_height//2 - text_height//2),
            text, fill=text_color, font=font
        )
    
    def _add_text_area_with_border(self, draw, opacity=80):
        """Add a text area with decorative border"""
        text_box_height = 120
        text_box_width = self.width // 2 + 50
        
        # Center coordinates
        center_x = self.width//2
        center_y = self.height//2 + 50
        
        # Create a rounded rectangle with dotted border
        # Main area
        draw.rectangle(
            [(center_x - text_box_width//2, center_y - text_box_height//2), 
             (center_x + text_box_width//2, center_y + text_box_height//2)],
            fill=(255, 255, 255, opacity)
        )
        
        # Dotted border
        dots = 40
        dot_size = 4
        
        # Top edge
        for i in range(dots):
            x = center_x - text_box_width//2 + i * text_box_width // dots
            y = center_y - text_box_height//2
            if i % 2 == 0:  # Skip every other dot for dotted effect
                draw.ellipse(
                    [(x-dot_size, y-dot_size), (x+dot_size, y+dot_size)],
                    fill=(255, 100, 150)
                )
        
        # Bottom edge
        for i in range(dots):
            x = center_x - text_box_width//2 + i * text_box_width // dots
            y = center_y + text_box_height//2
            if i % 2 == 0:
                draw.ellipse(
                    [(x-dot_size, y-dot_size), (x+dot_size, y+dot_size)],
                    fill=(255, 100, 150)
                )
        
        # Left edge
        for i in range(dots):
            x = center_x - text_box_width//2
            y = center_y - text_box_height//2 + i * text_box_height // dots
            if i % 2 == 0:
                draw.ellipse(
                    [(x-dot_size, y-dot_size), (x+dot_size, y+dot_size)],
                    fill=(255, 100, 150)
                )
        
        # Right edge
        for i in range(dots):
            x = center_x + text_box_width//2
            y = center_y - text_box_height//2 + i * text_box_height // dots
            if i % 2 == 0:
                draw.ellipse(
                    [(x-dot_size, y-dot_size), (x+dot_size, y+dot_size)],
                    fill=(255, 100, 150)
                )

    def _create_fireworks_newyear(self):
        """Create a New Year template with realistic fireworks against a night sky"""
        # Create dark blue to black gradient for night sky
        img = self._create_gradient_background((0, 10, 30), (0, 0, 10))
        draw = ImageDraw.Draw(img)
        
        # Add stars to the night sky
        self._add_twinkling_stars(draw, 100)
        
        # Add city skyline silhouette
        self._add_modern_city_skyline(draw)
        
        # Add realistic fireworks
        firework_positions = [
            (self.width // 4, self.height // 4),
            (self.width // 2, self.height // 6),
            (self.width * 3 // 4, self.height // 3),
            (self.width // 6, self.height // 3),
            (self.width * 5 // 6, self.height // 5)
        ]
        
        # Use different colors for each firework
        firework_colors = [
            (255, 50, 50),    # Red
            (50, 255, 100),   # Green
            (50, 150, 255),   # Blue
            (255, 200, 50),   # Gold
            (255, 100, 255)   # Pink
        ]
        
        for i, (x, y) in enumerate(firework_positions):
            color = firework_colors[i % len(firework_colors)]
            size = random.randint(50, 100)
            self._draw_realistic_firework(draw, x, y, size, color)
        
        # Add "Happy New Year" banner
        self._add_new_year_banner(draw)
        
        # Add text area with reflective styling
        self._add_new_year_text_area(draw)
        
        # Add the year number
        year_text = "2024"  # Can be updated programmatically
        self._add_year_text(draw, year_text)
        
        # Add watermark
        self._add_watermark_text(draw, "New Year Fireworks")
        
        return img

    def _add_twinkling_stars(self, draw, count):
        """Add twinkling stars to the night sky"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height // 2)  # Stars only in top half
            size = random.randint(1, 3)
            
            # Randomize brightness
            brightness = random.randint(150, 255)
            
            # Draw the star
            draw.ellipse(
                [(x - size, y - size), (x + size, y + size)],
                fill=(brightness, brightness, brightness)
            )
            
            # Add glow to some stars
            if random.random() < 0.2:  # 20% of stars get a glow
                glow_size = size + 2
                draw.ellipse(
                    [(x - glow_size, y - glow_size), (x + glow_size, y + glow_size)],
                    fill=(brightness, brightness, brightness, 50)
                )
    
    def _add_modern_city_skyline(self, draw):
        """Add a modern city skyline silhouette"""
        # Base coordinates
        base_y = self.height * 2 // 3
        
        # Create random buildings
        building_count = 25
        building_width_range = (self.width // 60, self.width // 30)
        building_min_height = 50
        building_max_height = 180
        
        # List to store building dimensions
        buildings = []
        
        # Generate random buildings with increasing height towards the center
        x = 0
        while x < self.width:
            # Determine position-dependent height factor (higher near center)
            center_factor = 1 - abs(x - self.width/2) / (self.width/2)
            height_factor = 0.5 + center_factor * 0.5
            
            # Calculate building width and height
            width = random.randint(building_width_range[0], building_width_range[1])
            max_height = building_min_height + (building_max_height - building_min_height) * height_factor
            height = random.randint(building_min_height, int(max_height))
            
            # Store building
            buildings.append((x, width, height))
            x += width
        
        # Draw buildings
        for x, width, height in buildings:
            # Main building shape
            draw.rectangle(
                [(x, base_y - height), (x + width, base_y)],
                fill=(0, 0, 0)  # Black silhouette
            )
            
            # Add windows
            window_size = 2
            window_spacing = 5
            
            # Calculate number of windows per row and column
            windows_per_row = (width - 4) // window_spacing
            if windows_per_row < 1:
                windows_per_row = 1
                
            windows_per_column = (height - 10) // window_spacing
            if windows_per_column < 1:
                windows_per_column = 1
            
            # Draw windows
            for row in range(windows_per_column):
                for col in range(windows_per_row):
                    # Only some windows are lit
                    if random.random() < 0.6:  # 60% of windows are lit
                        window_color = (255, 255, 200)  # Warm light
                    else:
                        window_color = (0, 0, 0)  # Dark window
                    
                    window_x = x + 4 + col * window_spacing
                    window_y = base_y - height + 5 + row * window_spacing
                    
                    draw.rectangle(
                        [(window_x, window_y), 
                         (window_x + window_size, window_y + window_size)],
                        fill=window_color
                    )
            
            # Add different roof shapes for variety
            roof_type = random.choice(["flat", "pointed", "antenna"])
            
            if roof_type == "pointed":
                # Pointed roof
                draw.polygon(
                    [(x, base_y - height), 
                     (x + width//2, base_y - height - 10),
                     (x + width, base_y - height)],
                    fill=(0, 0, 0)
                )
            elif roof_type == "antenna":
                # Building with antenna
                antenna_width = 1
                antenna_height = random.randint(5, 15)
                
                draw.rectangle(
                    [(x + width//2 - antenna_width, base_y - height - antenna_height),
                     (x + width//2 + antenna_width, base_y - height)],
                    fill=(0, 0, 0)
                )
    
    def _draw_realistic_firework(self, draw, x, y, size, color):
        """Draw a realistic firework explosion"""
        # Create rays with gradient effect
        ray_count = random.randint(20, 40)
        
        # Draw outer glow
        for radius in range(3):
            glow_size = size + radius * 10
            opacity = 50 - radius * 15
            if opacity > 0:
                draw.ellipse(
                    [(x - glow_size, y - glow_size), (x + glow_size, y + glow_size)],
                    fill=(color[0], color[1], color[2], opacity)
                )
        
        # Draw the main explosion rays
        for i in range(ray_count):
            angle = i * 2 * math.pi / ray_count
            ray_length = random.uniform(0.7, 1.0) * size
            
            end_x = x + ray_length * math.cos(angle)
            end_y = y + ray_length * math.sin(angle)
            
            # Draw ray with gradient
            points = []
            for t in range(10):
                t_ratio = t / 10
                point_x = x + (end_x - x) * t_ratio
                point_y = y + (end_y - y) * t_ratio
                
                # Calculate opacity based on distance from center
                opacity = int(230 * (1 - t_ratio))
                
                # Draw point with decreasing size
                point_size = 3 - 2 * t_ratio  # Decreasing size
                if point_size > 0:
                    draw.ellipse(
                        [(point_x - point_size, point_y - point_size), 
                         (point_x + point_size, point_y + point_size)],
                        fill=(color[0], color[1], color[2], opacity)
                    )
        
        # Add secondary smaller explosions for some fireworks
        if random.random() < 0.5:  # 50% chance
            secondary_count = random.randint(3, 8)
            for _ in range(secondary_count):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0.5, 0.8) * size
                
                sec_x = x + distance * math.cos(angle)
                sec_y = y + distance * math.sin(angle)
                
                # Smaller secondary explosion
                sec_size = size // 3
                sec_ray_count = ray_count // 2
                
                for i in range(sec_ray_count):
                    sec_angle = i * 2 * math.pi / sec_ray_count
                    sec_ray_length = random.uniform(0.7, 1.0) * sec_size
                    
                    sec_end_x = sec_x + sec_ray_length * math.cos(sec_angle)
                    sec_end_y = sec_y + sec_ray_length * math.sin(sec_angle)
                    
                    # Draw a simple line for secondary explosion
                    draw.line(
                        [(sec_x, sec_y), (sec_end_x, sec_end_y)],
                        fill=(color[0], color[1], color[2], 150),
                        width=1
                    )
    
    def _add_new_year_banner(self, draw):
        """Add a 'Happy New Year' banner"""
        banner_y = self.height // 5
        banner_text = "Happy New Year"
        
        # Try to use a decorative font
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Get text size for centering
        text_width, text_height = 300, 40  # Default fallback size
        try:
            # For newer Pillow versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), banner_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            # For older Pillow versions
            elif hasattr(draw, 'textsize'):
                text_width, text_height = draw.textsize(banner_text, font=font)
        except Exception:
            # Keep the fallback values if any error occurs
            pass
        
        # Center position
        center_x = self.width // 2
        
        # Draw text with glow effect
        for offset in range(5, 0, -1):
            opacity = 50 - offset * 10
            if opacity > 0:
                draw.text(
                    (center_x - text_width//2, banner_y - text_height//2),
                    banner_text, 
                    fill=(255, 255, 255, opacity), 
                    font=font
                )
        
        # Main text
        draw.text(
            (center_x - text_width//2, banner_y - text_height//2),
            banner_text, 
            fill=(255, 255, 255), 
            font=font
        )
        
        # Add decorative sparkle elements around the text
        sparkle_count = 15
        for _ in range(sparkle_count):
            # Position around the text
            sparkle_x = center_x - text_width//2 - 20 + random.randint(0, text_width + 40)
            sparkle_y = banner_y - text_height//2 - 20 + random.randint(0, text_height + 40)
            
            # Skip positions that would overlap with the text
            if (center_x - text_width//2 <= sparkle_x <= center_x + text_width//2 and
                banner_y - text_height//2 <= sparkle_y <= banner_y + text_height//2):
                continue
            
            # Draw a small star/sparkle
            self._draw_sparkle(draw, sparkle_x, sparkle_y, random.randint(3, 7))
    
    def _draw_sparkle(self, draw, x, y, size):
        """Draw a decorative sparkle/star"""
        # Choose a sparkly color
        colors = [
            (255, 255, 200),  # Pale yellow
            (255, 200, 200),  # Pale pink
            (200, 255, 255),  # Pale cyan
            (255, 255, 255)   # White
        ]
        color = random.choice(colors)
        
        # Draw main rays
        for i in range(4):
            angle = i * math.pi / 4
            end_x1 = x + size * math.cos(angle)
            end_y1 = y + size * math.sin(angle)
            
            draw.line([(x, y), (end_x1, end_y1)], fill=color, width=1)
        
        # Draw secondary rays (shorter)
        for i in range(4):
            angle = i * math.pi / 4 + math.pi / 8
            end_x2 = x + size * 0.5 * math.cos(angle)
            end_y2 = y + size * 0.5 * math.sin(angle)
            
            draw.line([(x, y), (end_x2, end_y2)], fill=color, width=1)
        
        # Add center dot
        draw.ellipse([(x-1, y-1), (x+1, y+1)], fill=color)
    
    def _add_new_year_text_area(self, draw, opacity=70):
        """Add a text area with reflective styling"""
        text_box_height = 120
        text_box_width = self.width // 2 + 50
        
        # Center coordinates
        center_x = self.width//2
        center_y = self.height//2 + 60
        
        # Draw main text area with gradient effect
        for i in range(text_box_height):
            y = center_y - text_box_height//2 + i
            # Calculate opacity based on position (more transparent at top)
            rect_opacity = opacity - (text_box_height//2 - i) * 0.5 if i < text_box_height//2 else opacity
            
            if rect_opacity > 0:
                draw.line(
                    [(center_x - text_box_width//2, y), 
                     (center_x + text_box_width//2, y)],
                    fill=(255, 255, 255, int(rect_opacity))
                )
        
        # Add border
        draw.rectangle(
            [(center_x - text_box_width//2, center_y - text_box_height//2),
             (center_x + text_box_width//2, center_y + text_box_height//2)],
            outline=(200, 200, 255), width=1
        )
        
        # Add reflective highlight at the top
        highlight_height = 10
        for i in range(highlight_height):
            y = center_y - text_box_height//2 + i
            highlight_opacity = 100 - i * 10
            
            if highlight_opacity > 0:
                draw.line(
                    [(center_x - text_box_width//2 + 5, y), 
                     (center_x + text_box_width//2 - 5, y)],
                    fill=(255, 255, 255, highlight_opacity)
                )
    
    def _add_year_text(self, draw, year_text):
        """Add large year text (e.g., '2024')"""
        # Position at the bottom section
        year_y = self.height * 3 // 4
        
        # Try to use a bold font
        try:
            font = ImageFont.truetype("arial.ttf", 72)
        except:
            font = ImageFont.load_default()
        
        # Get text size for centering
        text_width, text_height = 150, 70  # Default fallback size
        try:
            # For newer Pillow versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), year_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            # For older Pillow versions
            elif hasattr(draw, 'textsize'):
                text_width, text_height = draw.textsize(year_text, font=font)
        except Exception:
            # Keep the fallback values if any error occurs
            pass
        
        # Center position
        center_x = self.width // 2
        
        # Add metallic/reflective effect
        for i in range(text_height):
            y_pos = year_y - text_height//2 + i
            # Calculate brightness based on position
            brightness = 150 + int(100 * math.sin(i * math.pi / text_height))
            
            # Draw a horizontal segment of the text with varying brightness
            segment_text = year_text
            shadow_color = (brightness, brightness, brightness)
            
            draw.text(
                (center_x - text_width//2, year_y - text_height//2),
                segment_text, 
                fill=shadow_color, 
                font=font
            )
        
        # Add a thin outline
        outline_color = (200, 200, 255)
        for offset_x, offset_y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            draw.text(
                (center_x - text_width//2 + offset_x, year_y - text_height//2 + offset_y),
                year_text, 
                fill=outline_color, 
                font=font
            )
        
        # Main text
        draw.text(
            (center_x - text_width//2, year_y - text_height//2),
            year_text, 
            fill=(255, 255, 255), 
            font=font
        )
