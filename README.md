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
- [Contact](#contact)

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

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ninanil/image-verse-web-app.git
   cd fastapi-image-generation
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the project root directory and add your Replicate API token:
     ```bash
     touch .env
     echo "NGROK_AUTH_TOKEN=your_ngrok_auth_token" > .env
     ```

---

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation**:
   - Open your browser and navigate to `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

## API Endpoints

### 1. **Generate Image**
- **Endpoint**: `/generate`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "prompt": "A fantasy landscape with castles and dragons",
    "negative_prompt": "low quality, blurry",
    "num_outputs": 3,
    "num_inference_steps": 50,
    "guidance_scale": 7.5
  }
  ```
- **Response**: List of URLs pointing to the generated images.

### 2. **Fine-Tune Model**
- **Endpoint**: `/caption`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "fine_tune_model_name": "your-model-name",
    "training_data": "path-to-your-training-data",
    "num_epochs": 10,
    "prompt": "Fine-tuned prompt"
  }
  ```
- **Response**: URL of the fine-tuned model or image.

---

## Directory Structure

```plaintext
.
├── app/
│   ├── api/
│   │   ├── models.py        # Request/Response models
│   │   └── routes.py        # API route definitions
│   ├── services/
│   │   └── replicate_service.py  # Logic for interacting with Replicate API
│   ├── utils/
│   │   └── image_utils.py    # Utility for saving images
│   ├── config.py             # Configuration settings (e.g., API tokens)
│   └── main.py               # FastAPI app initialization
├── .env                      # Environment variables
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

---

## Image Storage

Generated images are saved in the `static/images` folder with timestamped filenames. Ensure this directory exists:
```bash
mkdir -p static/images
```

---

## Contact

For any issues or inquiries, please contact:
- **Name**: Naveen V
- **Email**: naveenv3112000@gmail.com
