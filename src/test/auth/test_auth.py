"""Tests for the endpoints in the auth package/route."""

from datetime import datetime

from src.test.client import client


class TestAuth:
    """Tests for the endpoints in the auth package/route."""

    def test_register_correct_data_user_created(self) -> None:
        res = client.post(
            "/auth/register",
            json={
                "first_name": "FirstName",
                "last_name": "LastName",
                "email": "username@email.com",
                "username": "username",
                "date_of_birth": datetime.now().date().strftime("%Y-%m-%d"),
                "description": "Description",
                "plain_text_password": "password",
            },
        )

        assert res.status_code == 201

    def test_register_user_with_that_username_aleready_exists(self) -> None:
        client.post(
            "/auth/register",
            json={
                "first_name": "FirstName",
                "last_name": "LastName",
                "email": "username@email.com",
                "username": "username",
                "date_of_birth": datetime.now().date().strftime("%Y-%m-%d"),
                "description": "Description",
                "plain_text_password": "password",
            },
        )

        res = client.post(
            "/auth/register",
            json={
                "first_name": "FirstName",
                "last_name": "LastName",
                "email": "username@email.com",
                "username": "username",
                "date_of_birth": datetime.now().date().strftime("%Y-%m-%d"),
                "description": "Description",
                "plain_text_password": "password",
            },
        )

        assert res.status_code == 400
        assert res.json()["detail"] == "Username taken."

    def test_register_incomplete_data_user_not_created(self) -> None:
        res = client.post(
            "/auth/register",
            json={
                "first_name": "FirstName",
                "email": "username@email.com",
                "username": "username",
                "date_of_birth": datetime.now().date().strftime("%Y-%m-%d"),
                "description": "Description",
                "plain_text_password": "password",
            },
        )

        assert res.status_code == 422

    def test_login_correct_credientials_token_received(self) -> None:
        client.register_user(username="username", password="password")
        res = client.post("/auth/token", data={"username": "username", "password": "password"})

        assert res.status_code == 200

    def test_login_incorrect_credentials_401_returned(self) -> None:
        client.register_user(username="username", password="password")
        res = client.post(
            "/auth/token", data={"username": "incorrect_username", "password": "password"}
        )

        assert res.status_code == 401
        assert res.json()["detail"] == "Incorrect username or password"

    def test_me_user_logged_in_info_returned(self) -> None:
        client.register_user(username="username", password="password")
        client.login(username="username", password="password")
        res = client.get("/auth/me")

        assert res.status_code == 200

        res_data = res.json()
        assert res_data["first_name"] == "FirstName"
        assert res_data["last_name"] == "LastName"
        assert res_data["username"] == "username"
        assert res_data["email"] == "username@email.com"
        assert res_data["description"] == "Description"
        assert res_data["user_id"] == 1

        client.logout()

    def test_me_user_not_logged_in_exception_raised(self) -> None:
        res = client.get("/auth/me")

        print(res.json())
        assert res.status_code == 401

    def test_update_user_logged_in_correct_data_user_updated(self) -> None:
        client.register_user(username="Username", password="Password")
        client.login(username="Username", password="Password")
        res = client.put(
            "/auth/update",
            json={
                "first_name": "FirstNameUpdated",
            },
        )
        assert res.status_code == 200
        assert res.json()["first_name"] == "FirstNameUpdated"

        client.logout()

    def test_update_user_logged_in_incorrect_data_exception_raised(self) -> None:
        client.register_user(username="Username", password="Password")
        client.login(username="Username", password="Password")
        res = client.put(
            "/auth/update",
            json={
                "first_name": 3,
            },
        )
        assert res.status_code == 422

        client.logout()

    def test_update_user_not_logged_in_exception_raised(self) -> None:
        res = client.put(
            "/auth/update",
            json={
                "first_name": "FirstNameUpdated",
            },
        )
        assert res.status_code == 401
