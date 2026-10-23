from app.models import Room
from app.repository.rooms import delete_room, get_room, room_exists, save_room


class TestSaveRoom:
    def test_saved_room_can_be_found(self):
        room = Room(code="ABCDE", players=["Vasya"])
        save_room(room)
        assert get_room("ABCDE") is room

    def test_saving_same_code_overwrites_room(self):
        first = Room(code="ABCDE", players=["Vasya"])
        second = Room(code="ABCDE", players=["Vasya", "Petya"])
        save_room(first)
        save_room(second)
        stored = get_room("ABCDE")
        assert stored is not None
        assert stored.players == ["Vasya", "Petya"]


class TestGetRoom:
    def test_unknown_code_returns_none(self):
        assert get_room("ABCDE") is None


class TestRoomExists:
    def test_saved_room_exists(self):
        save_room(Room(code="ABCDE", players=["Vasya"]))
        assert room_exists("ABCDE")

    def test_unknown_room_does_not_exist(self):
        assert not room_exists("ABCDE")


class TestDeleteRoom:
    def test_deleted_room_is_gone(self):
        save_room(Room(code="ABCDE", players=["Vasya"]))
        delete_room("ABCDE")
        assert not room_exists("ABCDE")
        assert get_room("ABCDE") is None

    def test_deleting_unknown_room_does_nothing(self):
        delete_room("ABCDE")
        assert not room_exists("ABCDE")
