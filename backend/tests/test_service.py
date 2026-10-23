import pytest
from app.core.exceptions import (NicknameTakenError, PlayerNotInRoomError,
                                 RoomFullError, RoomNotFoundError)
from app.models import Room
from app.service import rooms as room_service
from app.service.rooms import ALPHABET, CODE_LENGTH, MAX_PLAYERS


def make_room(*nicknames: str) -> Room:
    """Create a room: the first nickname is the host, the rest join in order."""
    room = room_service.create_room(nicknames[0])
    for nickname in nicknames[1:]:
        room_service.join_room(room.code, nickname)
    return room


class TestCreateRoom:
    def test_code_has_right_length_and_symbols(self):
        room = room_service.create_room("Vasya")
        assert len(room.code) == CODE_LENGTH
        assert all(symbol in ALPHABET for symbol in room.code)

    def test_creator_is_only_player_and_host(self):
        room = room_service.create_room("Vasya")
        assert room.players == ["Vasya"]
        assert room.host == "Vasya"

    def test_created_room_can_be_found(self):
        room = room_service.create_room("Vasya")
        assert room_service.get_room(room.code) is room

    def test_two_rooms_get_different_codes(self):
        first = room_service.create_room("Vasya")
        second = room_service.create_room("Petya")
        assert first.code != second.code


class TestGetRoom:
    def test_code_is_case_insensitive(self):
        room = make_room("Vasya")
        assert room_service.get_room(room.code.lower()) is room

    def test_unknown_room_raises(self):
        with pytest.raises(RoomNotFoundError):
            room_service.get_room("NOPE1")


class TestJoinRoom:
    def test_player_is_added_to_the_end(self):
        room = make_room("Vasya")
        room_service.join_room(room.code, "Petya")
        assert room.players == ["Vasya", "Petya"]

    def test_host_does_not_change_when_someone_joins(self):
        room = make_room("Vasya")
        room_service.join_room(room.code, "Petya")
        assert room.host == "Vasya"

    def test_lowercase_code_works(self):
        room = make_room("Vasya")
        room_service.join_room(room.code.lower(), "Petya")
        assert "Petya" in room.players

    def test_same_nickname_is_rejected(self):
        room = make_room("Vasya")
        with pytest.raises(NicknameTakenError):
            room_service.join_room(room.code, "Vasya")

    def test_same_nickname_in_other_case_is_rejected(self):
        room = make_room("Vasya")
        with pytest.raises(NicknameTakenError):
            room_service.join_room(room.code, "VASYA")

    def test_full_room_is_rejected(self):
        room = make_room(*[f"Player{i}" for i in range(MAX_PLAYERS)])
        with pytest.raises(RoomFullError):
            room_service.join_room(room.code, "Extra")
        assert len(room.players) == MAX_PLAYERS

    def test_unknown_room_raises(self):
        with pytest.raises(RoomNotFoundError):
            room_service.join_room("NOPE1", "Vasya")


class TestLeaveRoom:
    def test_player_is_removed(self):
        room = make_room("Vasya", "Petya", "Masha")
        room_service.leave_room(room.code, "Petya")
        assert room.players == ["Vasya", "Masha"]

    def test_next_player_becomes_host_when_host_leaves(self):
        room = make_room("Vasya", "Petya", "Masha")
        room_service.leave_room(room.code, "Vasya")
        assert room.host == "Petya"

    def test_nickname_is_case_insensitive(self):
        room = make_room("Vasya", "Petya")
        room_service.leave_room(room.code.lower(), "petya")
        assert room.players == ["Vasya"]

    def test_last_player_leaving_deletes_room(self):
        room = make_room("Vasya")
        assert room_service.leave_room(room.code, "Vasya") is None
        with pytest.raises(RoomNotFoundError):
            room_service.get_room(room.code)

    def test_unknown_player_raises(self):
        room = make_room("Vasya")
        with pytest.raises(PlayerNotInRoomError):
            room_service.leave_room(room.code, "Kolya")

    def test_unknown_room_raises(self):
        with pytest.raises(RoomNotFoundError):
            room_service.leave_room("NOPE1", "Vasya")
