import random
# Make numpy optional
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
from PIL import Image, ImageEnhance, ImageFilter
import os

# Import optional libraries if available
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import wordnet
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

class AIGreetingHelper:
    """Class to provide AI-powered features for greeting cards"""
    
    def __init__(self):
        """Initialize the AI helper"""
        self.templates = {
            "Birthday": [
                "Wishing you a day filled with happiness and a year filled with joy!",
                "Happy Birthday! May your day be as special as you are!",
                "Another year older, another year wiser. Happy Birthday!",
                "Count your life by smiles, not tears. Count your age by friends, not years. Happy Birthday!",
                "May your birthday be the start of a year filled with good luck, good health, and much happiness."
            ],
            "Valentine": [
                "You're my everything. Happy Valentine's Day!",
                "Every day with you is a wonderful addition to my life's journey. Happy Valentine's Day!",
                "You are the reason my heart beats. I love you today and always.",
                "In a world full of people, my heart chose you.",
                "You make my heart smile. Happy Valentine's Day!"
            ],
            "Eid": [
                "May Allah bless you with peace, happiness, and prosperity. Eid Mubarak!",
                "Wishing you a joyous Eid filled with blessings and love.",
                "May this Eid bring joy, health, and wealth to you and your family.",
                "Eid Mubarak! May Allah accept your good deeds and sacrifices.",
                "May the divine blessings of Allah fill your home and heart with happiness and peace."
            ],
            "Puja": [
                "May the divine blessings of the goddess bring peace and prosperity to your life.",
                "Wishing you a joyous celebration filled with divine blessings.",
                "May this sacred occasion bring you happiness, prosperity, and success.",
                "May the divine light guide you towards peace and prosperity.",
                "Wishing you a blessed Puja celebration with your loved ones."
            ],
            "New Year": [
                "Cheers to a new year and another chance for us to get it right!",
                "May the new year bring you happiness, peace, and prosperity.",
                "New year, new beginnings, and new blessings. Happy New Year!",
                "Wishing you 12 months of success, 52 weeks of laughter, and 365 days of happiness.",
                "May the coming year be full of grand adventures and opportunities."
            ]
        }
        
        # Initialize NLTK if available
        if NLTK_AVAILABLE:
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                try:
                    nltk.download('punkt', quiet=True)
                    nltk.download('wordnet', quiet=True)
                except:
                    pass
    
    def generate_greeting(self, category, recipient=None, sender=None, style="standard"):
        """Generate an AI-powered greeting message"""
        if category not in self.templates:
            category = random.choice(list(self.templates.keys()))
        
        # Get base template
        base_templates = self.templates[category]
        greeting = random.choice(base_templates)
        
        # Personalize if recipient/sender provided
        if recipient:
            # Add recipient name to greeting
            if "!" in greeting:
                greeting = greeting.replace("!", f", {recipient}!")
            else:
                greeting = f"{greeting} {recipient}!"
        
        if sender:
            # Add sender name at the end
            greeting = f"{greeting}\n\nWith love,\n{sender}"
        
        # Apply style variations if NLTK is available
        if NLTK_AVAILABLE and style == "creative":
            greeting = self._enhance_text_with_synonyms(greeting)
        
        return greeting
    
    def _enhance_text_with_synonyms(self, text):
        """Use NLTK to enhance text with synonyms for some words"""
        if not NLTK_AVAILABLE:
            return text
            
        try:
            words = word_tokenize(text)
            result = []
            
            for word in words:
                # Only replace some adjectives and adverbs (30% chance)
                if len(word) > 4 and word.isalpha() and random.random() < 0.3:
                    synonyms = []
                    for syn in wordnet.synsets(word):
                        for lemma in syn.lemmas():
                            synonyms.append(lemma.name())
                    
                    if synonyms and len(synonyms) > 1:
                        # Filter out the original word and duplicates
                        synonyms = [s for s in set(synonyms) if s != word]
                        if synonyms:
                            replacement = random.choice(synonyms).replace('_', ' ')
                            result.append(replacement)
                            continue
                
                result.append(word)
            
            # Reconstruct the text with proper spacing
            enhanced_text = ""
            for i, word in enumerate(result):
                if i > 0 and word not in ".,!?;:":
                    enhanced_text += " "
                enhanced_text += word
            
            return enhanced_text
        except:
            # Fallback to original text if any error occurs
            return text
    
    def enhance_image(self, image_path):
        """Enhance an image using AI-powered techniques"""
        try:
            # Try using OpenCV if available for advanced enhancement
            if CV2_AVAILABLE:
                return self._enhance_with_opencv(image_path)
            else:
                # Fallback to PIL for basic enhancement
                return self._enhance_with_pil(image_path)
        except Exception as e:
            print(f"Image enhancement error: {str(e)}")
            # Return original image if enhancement fails
            return Image.open(image_path)
    
    def _enhance_with_pil(self, image_path):
        """Enhance image using PIL"""
        img = Image.open(image_path)
        
        # Auto-enhance color
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)
        
        # Increase contrast slightly
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        # Increase brightness slightly
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
        # Sharpen the image
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)
        
        return img
    
    def _enhance_with_opencv(self, image_path):
        """Enhance image using OpenCV for more advanced processing"""
        if not NUMPY_AVAILABLE:
            # Fallback to PIL if numpy is not available
            return self._enhance_with_pil(image_path)
        
        # Read image
        img = cv2.imread(image_path)
        
        # Convert to RGB (OpenCV uses BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Apply automatic color equalization
        lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        enhanced_lab = cv2.merge((cl, a, b))
        enhanced_img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        # Convert back to PIL image
        enhanced_img = Image.fromarray(enhanced_img)
        
        # Apply additional PIL enhancements
        enhancer = ImageEnhance.Sharpness(enhanced_img)
        enhanced_img = enhancer.enhance(1.3)
        
        return enhanced_img
    
    def get_text_suggestions(self, current_text, category):
        """Get AI-powered text suggestions as the user types"""
        if not current_text:
            return []
        
        suggestions = []
        
        # Get templates for the category
        templates = self.templates.get(category, [])
        if not templates:
            templates = [item for sublist in self.templates.values() for item in sublist]
        
        # Find templates that start with the current text (case insensitive)
        for template in templates:
            if template.lower().startswith(current_text.lower()):
                suggestions.append(template)
        
        # If no direct matches, find templates containing the words
        if not suggestions:
            words = current_text.lower().split()
            if words:
                last_word = words[-1]
                for template in templates:
                    template_words = template.lower().split()
                    for i, word in enumerate(template_words):
                        if word.startswith(last_word) and i < len(template_words) - 1:
                            suggestion = current_text + template_words[i][len(last_word):] + " " + template_words[i+1]
                            suggestions.append(suggestion)
        
        # Limit to 3 suggestions
        return suggestions[:3]

# Initialize the AI helper
ai_helper = AIGreetingHelper()

# Function to get a greeting suggestion
def get_ai_greeting(category, recipient=None, sender=None, style="standard"):
    """Get an AI-generated greeting"""
    return ai_helper.generate_greeting(category, recipient, sender, style)

# Function to enhance an image
def enhance_image_with_ai(image_path):
    """Enhance an image using AI techniques"""
    return ai_helper.enhance_image(image_path)

# Function to get text suggestions
def get_text_suggestions(current_text, category):
    """Get AI-powered text suggestions"""
    return ai_helper.get_text_suggestions(current_text, category)
