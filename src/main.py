"""Main app file."""

from fastapi import FastAPI

from src.routes import auth, ratings, recipes, tags
from src.utils import ConfigManager

config = ConfigManager.get_config()

app = FastAPI(
    title=config.app_name,
    description="Simple API for learning purposes.",
)

app.include_router(auth.router)
app.include_router(auth.admin_router)
app.include_router(recipes.router)
app.include_router(recipes.admin_router)
app.include_router(tags.router)
app.include_router(tags.admin_router)
app.include_router(ratings.router)
