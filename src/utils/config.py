"""Configuration-related utilites."""

import json
from pathlib import Path

from pydantic import BaseModel


class ConfigView(BaseModel):
    app_name: str


class ConfigManager:
    """Configuration parser."""

    _instance: ConfigView | None = None

    @classmethod
    def load_from_file(cls, config_file_path: Path) -> None:
        """Load given config file.

        Args:
            config_file_path (Path): config file path.
        """
        with open(config_file_path) as f:
            config_file = json.load(f)
        cls._instance = ConfigView(**config_file)

    @classmethod
    def get_config(cls) -> ConfigView | None:
        """Get current configuration.

        Returns:
            Current configuration.
        """
        return cls._instance
