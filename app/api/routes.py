from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from app.models.pydantic_model import ImageRequest  
from app.services.ml import StableDiffusionModel  
from app.services.ml import ImageCaptioningPipeline  
from app.utils.bounding_box_drawer import BoundingBoxDrawer  
from app.utils.image_processor import ImageProcessor
from app.utils.app_logger import logger
from PIL import Image
from app.config.stable_diffusion_config import StableDiffusionConfig
from app.config.image_captioning_config import ImageCaptioningConfig
from app.config.image_config import UploadImageFileConfig
from app.config.image_config import ImageFileValidation
import io

# Initialize configurations
upload_image_file_config = UploadImageFileConfig()
image_file_validator = ImageFileValidation(upload_image_file_config)
stable_diffusion_config = StableDiffusionConfig()
image_captioning_config = ImageCaptioningConfig()

router = APIRouter()

@router.post("/generate")
async def generate_image(request : ImageRequest):
    logger.info(f"Received request to process image with prompt: {request.prompt}")

    # Generate image from prompt
    # Load and Generate Image from Prompt
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        stable_diffusion_model = StableDiffusionModel()
        with torch.cuda.amp.autocast() if device == "cuda" else torch.no_grad():
            image = stable_diffusion_model.generate_image(request.prompt)
        logger.info("Image generated successfully from prompt")
    except Exception as e:
        logger.error(f"Error generating image from prompt: {str(e)}")
        raise HTTPException(status_code=500, detail="Image generation failed")

    # Apply Transformations
    try:
        image = ImageProcessor.apply_transformations(image, transformationList)
        width, height = image.size
        logger.info(f"Final image size after transformations: {width}x{height}")
    except Exception as e:
        logger.error(f"Error applying transformations: {str(e)}")
        raise HTTPException(status_code=500, detail="Image transformation failed")

    # Convert Image to Base64 for Transmission
    try:
        image_format = request.format.upper()
        base64_image = ImageProcessor.convert_to_base64(image, request.image_format)
        logger.info("Image processing complete")
    except Exception as e:
        logger.error(f"Error encoding image to Base64: {str(e)}")
        raise HTTPException(status_code=500, detail="Image encoding failed")

    # Return Base64 Image Data
    return {"status": "success", "image_data": base64_image,"image_format":image_format}

# Endpoint to caption an uploaded image
@router.post("/caption")
async def caption_image(file: UploadFile = File(...)):
    # Validate image format and size
    image_file_validator.validate_image_format(file)
    image_file_validator.validate_image_size(file)

    # Read and open the uploaded image
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read image: {str(e)}"
        )

    # Generate caption and process bounding boxes
    try:
        image_caption = ImageCaptioningPipeline(image_captioning_config)
        caption_data = image_caption.generate_caption_bbox(image)["<OD>"]
        print("type caption_data",type(caption_data))
        print("caption_data",caption_data)
        if not caption_data:
            raise ValueError("Caption data or object detection results not found in parsed answer.")
        
        # Extract bounding boxes and labels
        bboxes, labels = caption_data['bboxes'], caption_data['labels']
        answer = ', '.join(labels)

        # Draw bounding boxes on the image
        drawer = BoundingBoxDrawer(image, bboxes, labels)
        drawer.draw_boxes()

        # Convert image to Base64 format
        base64_image = ImageProcessor.convert_to_base64(drawer.image, "JPEG")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate caption: {str(e)}"
        )

    # Return the caption and encoded image as a response
    return JSONResponse(content={"caption": answer, "image_data": base64_image})
# Health check endpoint to verify that the service is running
@router.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})
