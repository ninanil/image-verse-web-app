from fastapi import HTTPException, UploadFile, status
from app.config.image_config import UploadImageFileConfig

class ImageFileValidation:
    def __init__(self, config: UploadImageFileConfig):
        self.config = config

    def validate_image_format(self, image: UploadFile):
        file_extension = image.filename.split(".")[-1].upper()
        if file_extension not in self.config.allowed_formats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type."
            )

    def validate_image_size(self, file: UploadFile):
        file_size = file.size
        max_size_bytes = self.config.max_size_mb * 1024 * 1024 
        if file_size > max_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds the maximum allowed limit of {self.config.max_size_mb} MB."
            )
    
