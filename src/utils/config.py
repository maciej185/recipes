"""Configuration-related utilites."""

import json
from pathlib import Path

from pydantic import BaseModel


class ConfigView(BaseModel):
    db_engine: str
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_name: str

    def get_db_connection_string(self) -> str:
        """Return a connection string to the db."""
        db_address = f"{self.db_host}:{self.db_port}" if self.db_port else self.db_host
        return (
            f"{self.db_engine}://{self.db_username}:{self.db_password}@{db_address}/{self.db_name}"
        )


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
