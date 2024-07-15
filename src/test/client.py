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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

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
