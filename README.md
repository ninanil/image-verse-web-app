# FastAPI Image Generation and Captioning Application

 Imageverse Web App: A FastAPI-based application that provides advanced image generation and captioning functionalities using AI models.
* Generate images based on a given prompt with optional transformations.
* Caption an uploaded image with object detection and bounding boxes.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Directory Structure](#directory-structure)

## Features
- **Image Generation**: Generates high-quality, realistic images from text prompts using the Stable Diffusion model, CompVis/stable-diffusion-v1-4 
- **Image Captioning**: Creates captions for images using Microsoft/Florence-2-large

---

## Requirements

- Python 3.9+
- [Replicate API](https://replicate.com/) account and API key
- `.env` file with the following content:
  ```
  REPLICATE_API_TOKEN=your_replicate_api_token
  ```

---

## Installation

### Non-Docker Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ninanil/image-verse-web-app.git
   cd image-verse-web-app
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**: You can install dependencies with either `pip` or `poetry`:
   Using `pip`:

```bash
  pip install -r requirements.txt
```

Using `poetry` (if Poetry is installed):

```bash
poetry install
```

5. **Set up environment variables**:
   - Create a `.env` file in the project root directory and add your Replicate API token:
     ```bash
     touch .env
     echo "NGROK_AUTH_TOKEN=your_ngrok_auth_token" > .env
     ```
### Docker Setup
Docker: Ensure Docker is installed on your system. 

---

## Running the Application

### Non-Docker Setup
1. **Start the FastAPI Server with ngrok**

To start the server and create a public URL with ngrok, run the following command in your terminal:

```
python main.py
```

2. **Access the API documentation**:

After running the command, the application will display a public ngrok URL in the logs.
Open your browser and navigate to this URL (e.g., `http://<ngrok-public-url>/docs`)


### Docker Setup
1. **Build the Docker Image**

Navigate to your project directory in the terminal and build the Docker image with the following command:

```
docker build -t image-verse-web-app .
 ```

2. **Run the Docker Container**
Run the Docker container with your ngrok authentication token as an environment variable:

```
docker run -e NGROK_AUTH_TOKEN=your_token_here -p 8000:8000 image-verse-web-app 
```

3. **Access the API Documentation**

- After starting the container, check the logs to find the public ngrok URL.
- Open your browser and navigate to this URL (e.g., `http://<ngrok-public-url>`) 

---


## API Endpoints

### 1. **Generate Image**
- **Endpoint**: `/generate`
- **Method**: `POST`
- **Parameters**:

- **`prompt`** *(required, str)*: Text prompt based on which the image is generated.
- **`transformations`** *(optional, dict)*: Allows users to specify a series of transformations to apply to the generated image. Available transformations:
  - **rotate**: Rotate the image by a specified angle.
  - **flip**: Flip the image horizontally or vertically.
  - **resize**: Resize the image to specified dimensions.
  - **grayscale**: Convert the image to grayscale.
  - **brightness**: Adjust the brightness of the image.

- **Request Body**:
```json
  {
  "prompt": "A sunset over the mountains",
  "transformations": [
    {"name": "resize", "params": {"width": 256, "height": 256}},
    {"name": "rotate", "params": {"angle": 45}},
    {"name": "brightness", "params": {"factor": 1.5}},
    {"name": "flip", "params": {"horizontal": true}},
    {"name": "grayscale"}
  ],
  "format": "JPEG"
}
```

- **Response**:
```json
 {
  "status": "success",
  "image_data": "<base64_encoded_image>",
  "image_format": "JPEG"
}
```

### 2. **Image Captioning**
- **Endpoint**: `/caption`
- **Method**: `POST`
- **Request Body**:
 Upload an image file directly via form-data.
- **Response**: 
```json
 
{
  "caption": "A beautiful fashion girl on a rocky terrain",
  "image_data": "<base64_encoded_image_with_bounding_boxes>"
}

```
---

## Directory Structure

```plaintext
image-verse-web-app/
├── __init__.py                        # Optional, marks the root as a package
├── app/
│   ├── __init__.py                    # Marks 'app' as a package
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                  # Defines API endpoints (e.g., /generate, /caption)
│   ├── config/                        # Configuration files for different modules
│   │   ├── __init__.py
│   │   ├── app_config.py              # General app configurations
│   │   ├── image_captioning_config.py # Configuration specific to the captioning model
│   │   ├── image_config.py            # Configuration for image transformations
│   │   └── stable_diffusion_config.py # Configuration for the Stable Diffusion model
│   ├── models/
│   │   ├── __init__.py
│   │   └── pydantic_model.py          # Pydantic models for request and response validation
│   ├── services/
│   │   ├── __init__.py
│   │   └── image_service.py           # Service functions for image generation and captioning
│   ├── utils/                         # Utility functions for the app
│   │   ├── __init__.py
│   │   ├── app_logger.py              # Logger configuration for application events
│   │   ├── bounding_box_drawer.py     # Draws bounding boxes on images for captioning
│   │   ├── image_file_validation.py   # Utility for validating image files
│   │   └── image_processor.py         # Handles image transformations and processing
├── tests/
│   ├── __init__.py                    # Marks the tests directory as a package
│   ├── test_generate.py               # Tests for the /generate endpoint
│   └── test_caption.py                # Tests for the /caption endpoint
├── Dockerfile                         # Docker configuration for containerizing the application
├── README.md                          # Project documentation
├── .env                               # Environment variables (e.g., NGROK_AUTH_TOKEN)
├── requirements.txt                   # Python dependencies (for non-Poetry setups)
├── poetry.lock                        # Locked dependencies for Poetry
├── pyproject.toml                     # Poetry configuration for dependencies
└── main.py                            # Main entry point for the FastAPI application

```

---



