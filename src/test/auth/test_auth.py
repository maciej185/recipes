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
        client.register_user(username="username", password="password")
        client.login(username="username", password="password")
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
        client.register_user(username="username", password="password")
        client.login(username="username", password="password")
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

    def test_user_logged_in_followed_user_exists_follow_successful(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        follow_res = client.post(
            "/auth/follow/3",
        )

        assert follow_res.status_code == 200

        client.logout()

    def test_user_logged_in_attempting_to_follow_themselves_exception_raised(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        follow_res = client.post(
            "/auth/follow/2",
        )

        assert follow_res.status_code == 403
        assert follow_res.json()["detail"] == "Users can't follow themselves."

        client.logout()

    def test_user_logged_in_another_user_already_followed_exception_raised(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        client.post(
            "/auth/follow/3",
        )
        follow_res = client.post(
            "/auth/follow/3",
        )

        assert follow_res.status_code == 403
        assert follow_res.json()["detail"] == "The first user already follows the second one."

        client.logout()

    def test_user_logged_in_followed_user_does_not_exist_exception_raised(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        follow_res = client.post(
            "/auth/follow/100",
        )

        assert follow_res.status_code == 404
        assert follow_res.json()["detail"] == "User with the given ID was not found in the DB."

        client.logout()

    def test_user_not_logged_in_exception_raised(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")
        follow_res = client.post(
            "/auth/follow/3",
        )

        assert follow_res.status_code == 401
        assert follow_res.json()["detail"] == "Not authenticated"

    def test_user_logged_in_unfollowing_user_who_is_followed_unfollow_successful(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        client.post(
            "/auth/follow/3",
        )

        unfollow_res = client.post(
            "/auth/unfollow/3",
        )

        assert unfollow_res.status_code == 200

        client.logout()

    def test_user_logged_in_unfollowing_user_who_is_not_followed_exception_raised(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        unfollow_res = client.post(
            "/auth/unfollow/3",
        )

        assert unfollow_res.status_code == 403
        assert unfollow_res.json()["detail"] == "The user was not followed."

        client.logout()

    def test_user_logged_in_fetching_followers_fetch_successfull(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        client.post(
            "/auth/follow/3",
        )

        followers_res = client.get(
            "/auth/followers/3",
        )

        res_data = followers_res.json()
        assert followers_res.status_code == 200
        assert len(res_data) == 1
        assert res_data[0]["username"] == "user1"
        assert res_data[0]["user_id"] == 2

        client.logout()

    def test_user_logged_in_fetching_followers_user_does_not_exists_exception_raised(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")

        followers_res = client.get(
            "/auth/followers/100",
        )

        assert followers_res.status_code == 404
        assert followers_res.json()["detail"] == "User with the given ID was not found in the DB."

        client.logout()

    def test_user_not_logged_in_fetching_followers_fetch_successful(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        client.post(
            "/auth/follow/3",
        )
        client.logout()

        followers_res = client.get(
            "/auth/followers/3",
        )

        res_data = followers_res.json()
        assert followers_res.status_code == 200
        assert len(res_data) == 1
        assert res_data[0]["username"] == "user1"
        assert res_data[0]["user_id"] == 2

    def test_user_logged_in_fetching_followed_users_fetch_successful(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        client.post(
            "/auth/follow/3",
        )

        followers_res = client.get(
            "/auth/followed/2",
        )

        res_data = followers_res.json()
        assert followers_res.status_code == 200
        assert len(res_data) == 1
        assert res_data[0]["username"] == "user2"
        assert res_data[0]["user_id"] == 3

        client.logout()

    def test_user_logged_in_fetching_followed_users_user_does_not_exists_exception_raised(
        self,
    ) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")

        followers_res = client.get(
            "/auth/followed/100",
        )

        assert followers_res.status_code == 404
        assert followers_res.json()["detail"] == "User with the given ID was not found in the DB."

        client.logout()

    def test_user_not_logged_in_fetching_followed_users_fetch_successful(self) -> None:
        client.register_user(username="user1", password="password")
        client.register_user(username="user2", password="password")

        client.login(username="user1", password="password")
        client.post(
            "/auth/follow/3",
        )

        followers_res = client.get(
            "/auth/followed/2",
        )

        res_data = followers_res.json()
        assert followers_res.status_code == 200
        assert len(res_data) == 1
        assert res_data[0]["username"] == "user2"
        assert res_data[0]["user_id"] == 3

        client.logout()
