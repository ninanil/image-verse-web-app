from PIL import Image, ImageDraw, ImageFont
from app.utils.app_logger import logger

class BoundingBoxDrawer:
    def __init__(self, image, bboxes, labels):
        """
        Initialize the BoundingBoxDrawer with image path, bounding boxes, and labels.
        
        Parameters:
            image_path (str): Path to the image file.
            bboxes (list): List of bounding boxes, each in the format [x_min, y_min, x_max, y_max].
            labels (list): List of labels corresponding to each bounding box.
        """
        self.image = image
        self.bboxes = bboxes
        self.labels = labels
        self.draw = ImageDraw.Draw(self.image)
        
        # Attempt to load a font
        try:
            self.font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            self.font = ImageFont.load_default()
    
    def draw_boxes(self):
        """
        Draws bounding boxes and labels on the image.
        """
        for bbox, label in zip(self.bboxes, self.labels):
            # Convert bbox coordinates from float to int
            x_min, y_min, x_max, y_max = map(int, bbox)
            
            # Draw the bounding box
            self.draw.rectangle(((x_min, y_min), (x_max, y_max)), outline="red", width=3)
            
            # Calculate text bounding box and position text above the bounding box
            text_bbox = self.draw.textbbox((x_min, y_min), label, font=self.font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x, text_y = x_min, y_min - text_height - 2  # Position 2 pixels above the box
            
            # Draw a background rectangle for the text label
            self.draw.rectangle(((text_x, text_y), (text_x + text_width, text_y + text_height)), fill="red")
            self.draw.text((text_x, text_y), label, fill="white", font=self.font)
            
    def show_image(self):
        """Displays the image with bounding boxes and labels."""
        self.image.show()
    
    def save_image(self, output_path):
        """
        Saves the image with bounding boxes and labels to a specified path.
        
        Parameters:
            output_path (str): Path to save the output image.
        """
        self.image.save(output_path)
        logger(f"Image saved to {output_path}")
