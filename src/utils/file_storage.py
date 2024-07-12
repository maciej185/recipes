"""Utilities for accessing the file storage."""

import shutil
from pathlib import Path

from fastapi import UploadFile

from .config import ConfigManager

config = ConfigManager.get_config()


class FileStorageManager:
    """Utility class for interacting with the file storage."""

    file_storage_root_path = config.file_storage_path

    @classmethod
    def save_profile_picture(cls, user_id: int, profile_pic_file: UploadFile) -> Path:
        """Save profile picture of a given user."""
        profile_pic_file_path = Path(
            cls.file_storage_root_path,
            "auth",
            str(user_id),
            "profile_picture",
            profile_pic_file.filename,
        )
        if profile_pic_file_path.parent.exists():
            shutil.rmtree(profile_pic_file_path.parent)
        profile_pic_file_path.parent.mkdir(parents=True)
        with open(profile_pic_file_path, "wb") as f:
            f.write(profile_pic_file.file.read())
        return profile_pic_file_path
