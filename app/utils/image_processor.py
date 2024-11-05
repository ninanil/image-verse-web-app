from PIL import Image, ImageFilter
import torchvision.transforms as transforms
import torch
import io
import base64

class ImageProcessor:
    
    @staticmethod
    def resize_image(image: Image.Image, width: int, height: int):
        """
        Resize the image to the specified size.
        
        Parameters:
            image: A PIL Image to resize.
            size: A tuple (width, height) for resizing.
            
        Returns:
            Resized PIL Image.
        """
        size = (width, height)
        return image.resize(size)

    @staticmethod
    def to_grayscale(image: Image.Image):
        """
        Convert an image to grayscale.
        
        Parameters:
            image: A PIL Image to convert.
            
        Returns:
            Grayscale PIL Image.
        """
        transform = transforms.Grayscale()
        return transform(image)

    @staticmethod
    def set_format(image: Image.Image, format: str = "PNG"):
        """
        Save the image in a specified format.
        
        Parameters:
            image: A PIL Image to save.
            format: The desired format ('PNG', 'JPEG', 'BMP', etc.).
            
        Returns:
            The saved image's file path.
        """
        file_path = f"output_image.{format.lower()}"
        image.save(file_path, format=format)
        return file_path
    
    @staticmethod
    def rotate_image(image: Image.Image, angle: float):
        """
        Rotate the image by a specified angle.

        Parameters:
            image: A PIL Image to rotate.
            angle: The angle to rotate the image, in degrees.

        Returns:
            Rotated PIL Image.
        """
        return transforms.functional.rotate(image, angle)
    
    @staticmethod
    def flip_image(image: Image.Image, horizontal: bool = True):
        """
        Flip the image horizontally or vertically.

        Parameters:
            image: A PIL Image to flip.
            horizontal: If True, flip horizontally; if False, flip vertically.

        Returns:
            Flipped PIL Image.
        """
        if horizontal:
            return transforms.functional.hflip(image)
        else:
            return transforms.functional.vflip(image)
    
    @staticmethod
    def adjust_brightness(image: Image.Image, factor: float):
        """
        Adjust the brightness of the image.

        Parameters:
            image: A PIL Image to adjust.
            factor: A factor for brightness adjustment (1.0 keeps the original brightness).

        Returns:
            Brightness-adjusted PIL Image.
        """
        return transforms.functional.adjust_brightness(image, factor)
    
    @staticmethod
    def apply_blur(image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.BLUR)
    
    @staticmethod
    def crop_image(image: Image.Image,size: int) -> Image.Image:
        transform = transforms.CenterCrop(128)
        return transform(image)

    @staticmethod
    def convert_to_base64(image, image_format="JPEG"):
        """
        Converts a PIL Image to a base64-encoded string.
        
        Parameters:
            image (PIL.Image.Image): The image to be converted.
            image_format (str): The format to save the image in (e.g., "JPEG", "PNG").
        
        Returns:
            str: Base64-encoded string of the image.
        """
        buffer = io.BytesIO()
        image.save(buffer, format=image_format)
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return base64_image
    
    @staticmethod
    def apply_transformation(image: Image.Image, transform_name: str, **kwargs):
        """
        Apply a transformation based on the transform name.

        Parameters:
            image: A PIL Image to transform.
            transform_name: Name of the transformation to apply.
            kwargs: Additional parameters for the transformation.

        Returns:
            Transformed image.
        """
        transformations = {
            'resize': ImageProcessor.resize_image,
            'grayscale': ImageProcessor.to_grayscale,
            'rotate': ImageProcessor.rotate_image,
            'flip': ImageProcessor.flip_image,
            'brightness': ImageProcessor.adjust_brightness,
            'blur':ImageProcessor.apply_blur,
            'crop':ImageProcessor.crop_image,
        }
        if transform_name in transformations:
            return transformations[transform_name](image, **kwargs)
        else:
            raise ValueError(f"Transformation '{transform_name}' is not supported.")

    @staticmethod
    def apply_transformations(image: Image.Image, transformations: list):
        """
        Apply a sequence of transformations.

        Parameters:
            image: A PIL Image to transform.
            transformations: A list of dictionaries where each dictionary contains
                             'name' of the transformation and 'params' as its parameters.

        Returns:
            Transformed image.
        """
        for transformation in transformations:
            transform_name = transformation.name
            params = transformation.params or {}
            logger.info(f"Applying transformation: {transform_name}")
            image = ImageProcessor.apply_transformation(image, transform_name, **params)
        return image
    
    @staticmethod
    def available_transformations():
        """
        Return a list of available transformations.

        Returns:
            List of transformation names.
        """
        return ["resize", "grayscale", "rotate", "flip", "brightness","crop", "blur"]
