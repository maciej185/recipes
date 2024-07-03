"""Main app file."""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from src.utils import ConfigManager

load_dotenv()

ConfigManager.load_from_file(Path(os.environ.get("CONFIG_PATH")))
config = ConfigManager.get_config()

app = FastAPI(
    title=config.app_name,
    description="Simple API for learning purposes.",
)
