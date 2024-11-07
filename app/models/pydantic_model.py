from pydantic import BaseModel, validator, ValidationError
from typing import List, Dict, Optional

class Transformation(BaseModel):
    name: str
    params: Optional[Dict[str, object]] = None  # Use a generic type here

    @validator('name')
    def validate_name(cls, v):
        allowed_transformations = {"resize", "rotate", "flip", "brightness", "crop", "blur", "grayscale"}
        if v not in allowed_transformations:
            raise ValueError(f"Transformation '{v}' is not supported. Supported transformations: {allowed_transformations}")
        return v

    @validator('params', always=True)
    def validate_params(cls, v, values):
        name = values.get('name')
        if name in {"resize", "rotate", "crop", "brightness", "blur"} and not v:
            raise ValueError(f"Transformation '{name}' requires parameters.")

        if v:
            # Specific checks for each transformation
            if name == "resize":
                if "width" not in v or "height" not in v:
                    raise ValueError(f"'resize' requires 'width' and 'height' parameters.")
                if not isinstance(v["width"], int) or not isinstance(v["height"], int):
                    raise ValueError(f"'width' and 'height' must be integers for 'resize' transformation.")

            if name == "rotate":
                if "angle" not in v:
                    raise ValueError(f"'rotate' requires 'angle' parameter.")
                if not isinstance(v["angle"], int):
                    raise ValueError(f"'angle' must be an integer for 'rotate' transformation.")

            if name == "flip":
                if "horizontal" not in v:
                    raise ValueError(f"'flip' requires 'horizontal' parameter.")
                if not isinstance(v["horizontal"], bool):
                    raise ValueError(f"'horizontal' must be a boolean (True or False) for 'flip' transformation.")

            if name == "crop":
                if "size" not in v:
                    raise ValueError(f"'crop' requires 'size' parameter.")
                if not isinstance(v["size"], int):
                    raise ValueError(f"'size' must be an integer for 'crop' transformation.")

            if name == "brightness":
                if "factor" not in v:
                    raise ValueError(f"'brightness' requires 'factor' parameter.")
                if not isinstance(v["factor"], float):
                    raise ValueError(f"'factor' must be a float for 'brightness' transformation.")

            if name == "blur":
                if "radius" not in v:
                    raise ValueError(f"'blur' requires 'radius' parameter.")
                if not isinstance(v["radius"], int):
                    raise ValueError(f"'radius' must be an integer for 'blur' transformation.")

        return v


class ImageRequest(BaseModel):
    prompt: str
    format: Optional[str] = None
    transformations: Optional[List[Transformation]] = None

    @validator('prompt')
    def validate_prompt(cls, v):
        if not v or not v.strip():
            raise ValueError("Prompt must be a non-empty string.")
        return v

    @validator('format')
    def validate_format(cls, v):
        allowed_formats = {"PNG", "JPG", "JPEG", "BMP"}
        if v.upper() not in allowed_formats:
            raise ValueError(f"Format '{v}' is not supported. Supported formats: {allowed_formats}") 
        if v.upper() == 'JPG':
            return "JPEG"
        return v.upper()
