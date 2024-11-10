# Use NVIDIA's CUDA image with Python 3.10 and Ubuntu 20.04
FROM nvidia/cuda:12.3.0-devel-ubuntu20.04

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Set up Python 3.10 as the default Python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Set environment variables for Poetry and Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in Docker
WORKDIR /image-verse-web-app

# Copy the current directory contents into the container at /image-verse-web-app
COPY . /image-verse-web-app
#
RUN poetry lock

# Install dependencies and the app itself using Poetry
RUN poetry config virtualenvs.create false && poetry install

# Expose the port for FastAPI
EXPOSE 8000

# Create an entrypoint script to write the .env file and start the app
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'echo "NGROK_AUTH_TOKEN=${NGROK_AUTH_TOKEN}" > /image-verse-web-app/app/.env' >> /entrypoint.sh && \
    echo 'exec poetry run python app/main.py' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
