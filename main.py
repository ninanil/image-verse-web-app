from fastapi import FastAPI
from app.utils.app_logger import logger
from app.config.image_config import UploadImageFileConfig
from app.utils.image_file_validation import ImageFileValidation
from app.api import routes  
import nest_asyncio
from pyngrok import ngrok
import uvicorn
from app.config.app_config import AppConfig

# Initialize the FastAPI app
config = AppConfig()
app = FastAPI(title=config.app_name)

# Initialize logger

# Set the ngrok authtoken
ngrok.set_auth_token(config.ngrok_auth_token)

# Include the router
app.include_router(routes.router)

# Run ngrok and Uvicorn if this is the main script
if __name__ == "__main__":
    # Specify the port
    port = 8000
    ngrok_tunnel = ngrok.connect(port)

    # Print the public URL where the FastAPI app is accessible
    logger.info(f"Public URL:{ngrok_tunnel.public_url}" )

    # Apply nest_asyncio to allow ngrok to work within async environments
    nest_asyncio.apply()

    # Finally, run the app with Uvicorn
    uvicorn.run(app, port=port)
