from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(width, height, color, text=""):
    """Create a placeholder image with text"""
    img = Image.new('RGB', (width, height), color=color)
    
    if text:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Draw text in the center
        text_width, text_height = draw.textsize(text, font=font)
        position = ((width - text_width) // 2, (height - text_height) // 2)
        draw.text(position, text, fill=(255, 255, 255), font=font)
    
    return img

def resize_image(img, max_width, max_height):
    """Resize an image while maintaining aspect ratio"""
    width, height = img.size
    
    # Calculate the ratio
    ratio = min(max_width / width, max_height / height)
    
    # Calculate new dimensions
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    
    # Resize the image
    return img.resize((new_width, new_height), Image.LANCZOS)
