from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    """General application settings loaded from environment variables."""
    app_name: str = "Image Verse Web App"
    debug: bool = False
    environment: str = "development"
    ngrok_auth_token: str

    class Config:
        env_file = ".env"  # Loads environment variables from .env if available
