"""Main app file."""

from fastapi import FastAPI

from src.routes import auth
from src.utils import ConfigManager

config = ConfigManager.get_config()

app = FastAPI(
    title=config.app_name,
    description="Simple API for learning purposes.",
)

app.include_router(auth.router)
