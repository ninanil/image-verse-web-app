from fastapi.testclient import TestClient
from main import app  # Import the FastAPI app

# Initialize the TestClient with the FastAPI app
client = TestClient(app)

def test_generate_image_with_transformations():
    # Define the request payload with transformations
    payload = {
        "prompt": "a beautiful fashion girl with realistic, sharp eyes and a well-defined face, wearing stylish, futuristic clothing, walking on the red rocky terrain of Mars under a clear, pale pink sky, highly detailed, photorealistic",
        "transformations": [
            {
                "name": "resize",
                "params": {
                    "width": 256,
                    "height": 256
                }
            },
            {
                "name": "rotate",
                "params": {
                    "angle": 45
                }
            },
            {
                "name": "brightness",
                "params": {
                    "factor": 1.5
                }
            },
            {
                "name": "flip",
                "params": {
                    "horizontal": True
                }
            },
            {
                "name": "grayscale"
            }
        ],
        "format": "JPEG"
    }

    # Send a POST request to the /generate endpoint
    response = client.post("/generate", json=payload)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content
    response_json = response.json()
    assert response_json["status"] == "success"
    assert "image_data" in response_json
    assert response_json["image_format"] == "JPEG"

def test_generate_image_without_transformations():
    # Define the request payload without transformations
    payload = {
        "prompt": "a futuristic cityscape at night, glowing with neon lights, and detailed skyscrapers",
        "format": "JPEG"
    }

    # Send a POST request to the /generate endpoint
    response = client.post("/generate", json=payload)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content
    response_json = response.json()
    assert response_json["status"] == "success"
    assert "image_data" in response_json
    assert response_json["image_format"] == "JPEG"

def test_generate_image_unsupported_format():
    # Define the request payload with an unsupported format
    payload = {
        "prompt": "a spaceship flying through a colorful nebula",
        "transformations": [],
        "format": "GIF"  # Assuming GIF is not supported
    }

    # Send a POST request to the /generate endpoint
    response = client.post("/generate", json=payload)

    # Assert the response status code
    assert response.status_code == 400

    # Assert the response content
    response_json = response.json()
    assert response_json["detail"] == "Unsupported image format"

def test_generate_image_invalid_transformation():
    # Define the request payload with an invalid transformation
    payload = {
        "prompt": "a serene forest landscape with a waterfall and mist",
        "transformations": [
            {
                "name": "resize",
                "params": {
                    "width": "invalid",  # Invalid width type
                    "height": 256
                }
            }
        ],
        "format": "JPEG"
    }

    # Send a POST request to the /generate endpoint
    response = client.post("/generate", json=payload)

    # Assert the response status code
    assert response.status_code == 400

    # Assert the response content
    response_json = response.json()
    assert "detail" in response_json
    assert response_json["detail"] == "Invalid transformation parameters"

def test_generate_image_missing_prompt():
    # Define the request payload without a prompt
    payload = {
        "transformations": [
            {
                "name": "rotate",
                "params": {
                    "angle": 90
                }
            }
        ],
        "format": "JPEG"
    }

    # Send a POST request to the /generate endpoint
    response = client.post("/generate", json=payload)

    # Assert the response status code
    assert response.status_code == 422  # Unprocessable Entity

    # Assert the response content
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "prompt"]
    assert response_json["detail"][0]["msg"] == "field required"
