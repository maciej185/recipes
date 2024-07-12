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

    @classmethod
    def save_recipe_images(cls, recipe_id: int, uploaded_files: list[UploadFile]) -> list[Path]:
        """Save images related to a given Recipe."""
        recipe_images_path = Path(
            cls.file_storage_root_path,
            "recipes",
            str(recipe_id),
        )
        image_paths = []
        recipe_images_path.mkdir(exist_ok=True, parents=True)
        for file in uploaded_files:
            recipe_image_path = Path(recipe_images_path, file.filename)
            with open(recipe_image_path, "wb") as f:
                f.write(file.file.read())
            image_paths.append(recipe_image_path)
        return image_paths
