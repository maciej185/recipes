from datetime import datetime

from fastapi.testclient import TestClient

from src.main import app


class IncorrectCredentialsException(Exception):
    """Raised when provided login credentials are incorrect."""

    def __init__(self, *args: object) -> None:
        self.message = "Incorrect username or password."
        super().__init__(self.message, *args)


class BaseTestClient(TestClient):
    """TestClient with additional utilities for the app."""

    AUTHENTICATION_ENDPOINT_URL = "/auth/token"
    REGISTRATION_ENDPOINT_URL = "/auth/register"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def register_user(self, username: str, password: str) -> None:
        """Register a user with given credentials."""
        client.post(
            "/auth/register",
            json={
                "first_name": "FirstName",
                "last_name": "LastName",
                "email": "username@email.com",
                "username": username,
                "date_of_birth": datetime.now().date().strftime("%Y-%m-%d"),
                "description": "Description",
                "plain_text_password": password,
            },
        )

    def login(self, username: str, password: str) -> None:
        """Add authentication headers to every request."""
        token_res = self.post(
            self.AUTHENTICATION_ENDPOINT_URL, data={"username": username, "password": password}
        )

        if token_res.status_code == 401:
            raise IncorrectCredentialsException

        self.headers = {"Authorization": f"Bearer {token_res.json()["access_token"]}"}

    def logout(self) -> None:
        """Remove authentication headers."""
        try:
            self.headers.pop("Authorization")
        except KeyError:
            pass


client = BaseTestClient(app)
