from app.service.rooms import MAX_PLAYERS
from fastapi.testclient import TestClient

ROOMS_URL = "/api/v1/rooms"


def create_room(client: TestClient, nickname: str = "Vasya") -> str:
    """Create a room through the API and return its code."""
    response = client.post(ROOMS_URL, json={"nickname": nickname})
    assert response.status_code == 201
    return response.json()["code"]


def join_room(client: TestClient, code: str, nickname: str):
    return client.post(f"{ROOMS_URL}/{code}/players", json={"nickname": nickname})


class TestCreateRoom:
    def test_returns_201_and_room(self, client: TestClient):
        response = client.post(ROOMS_URL, json={"nickname": "Vasya"})

        assert response.status_code == 201
        body = response.json()
        assert len(body["code"]) == 5
        assert body["players"] == ["Vasya"]
        assert body["host"] == "Vasya"

    def test_nickname_is_trimmed(self, client: TestClient):
        response = client.post(ROOMS_URL, json={"nickname": "  Vasya  "})

        assert response.status_code == 201
        assert response.json()["players"] == ["Vasya"]

    def test_blank_nickname_returns_422(self, client: TestClient):
        response = client.post(ROOMS_URL, json={"nickname": "   "})
        assert response.status_code == 422

    def test_too_long_nickname_returns_422(self, client: TestClient):
        response = client.post(ROOMS_URL, json={"nickname": "x" * 21})
        assert response.status_code == 422

    def test_missing_nickname_returns_422(self, client: TestClient):
        response = client.post(ROOMS_URL, json={})
        assert response.status_code == 422


class TestGetRoom:
    def test_returns_room(self, client: TestClient):
        code = create_room(client)

        response = client.get(f"{ROOMS_URL}/{code}")

        assert response.status_code == 200
        assert response.json() == {"code": code, "players": ["Vasya"], "host": "Vasya"}

    def test_code_is_case_insensitive(self, client: TestClient):
        code = create_room(client)

        response = client.get(f"{ROOMS_URL}/{code.lower()}")

        assert response.status_code == 200
        assert response.json()["code"] == code

    def test_unknown_room_returns_404(self, client: TestClient):
        response = client.get(f"{ROOMS_URL}/NOPE")

        assert response.status_code == 404
        assert "NOPE" in response.json()["detail"]


class TestJoinRoom:
    def test_returns_200_and_adds_player(self, client: TestClient):
        code = create_room(client)

        response = join_room(client, code, "Petya")

        assert response.status_code == 200
        assert response.json()["players"] == ["Vasya", "Petya"]

    def test_taken_nickname_in_other_case_returns_409(self, client: TestClient):
        code = create_room(client)

        response = join_room(client, code, "VASYA")

        assert response.status_code == 409
        assert "VASYA" in response.json()["detail"]

    def test_full_room_returns_409(self, client: TestClient):
        code = create_room(client, "Player0")
        for i in range(1, MAX_PLAYERS):
            assert join_room(client, code, f"Player{i}").status_code == 200

        response = join_room(client, code, "Extra")

        assert response.status_code == 409

    def test_unknown_room_returns_404(self, client: TestClient):
        response = join_room(client, "NOPE1", "Vasya")
        assert response.status_code == 404


class TestLeaveRoom:
    def test_returns_204_without_body(self, client: TestClient):
        code = create_room(client)
        join_room(client, code, "Petya")

        response = client.delete(f"{ROOMS_URL}/{code}/players/Petya")

        assert response.status_code == 204
        assert response.content == b""

    def test_next_player_becomes_host(self, client: TestClient):
        code = create_room(client)
        join_room(client, code, "Petya")

        client.delete(f"{ROOMS_URL}/{code}/players/Vasya")

        assert client.get(f"{ROOMS_URL}/{code}").json()["host"] == "Petya"

    def test_last_player_leaving_deletes_room(self, client: TestClient):
        code = create_room(client)

        client.delete(f"{ROOMS_URL}/{code}/players/Vasya")

        assert client.get(f"{ROOMS_URL}/{code}").status_code == 404

    def test_unknown_player_returns_404(self, client: TestClient):
        code = create_room(client)

        response = client.delete(f"{ROOMS_URL}/{code}/players/Kolya")

        assert response.status_code == 404
