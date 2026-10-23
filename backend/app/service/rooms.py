import secrets
import string

from app.core.exceptions import (NicknameTakenError, PlayerNotInRoomError,
                                 RoomFullError, RoomNotFoundError)
from app.models import Room
from app.repository import rooms as room_repository

MAX_PLAYERS = 8
CODE_LENGTH = 5
ALPHABET = string.ascii_uppercase + string.digits

def _generate_code() -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def get_room(code: str) -> Room:
    code = code.upper()
    room = room_repository.get_room(code)
    if room is None:
        raise RoomNotFoundError(code)
    return room


def join_room(code: str, nickname: str) -> Room:
    room = get_room(code)
    if len(room.players) >= MAX_PLAYERS:
        raise RoomFullError(room.code)
    if any(nickname.casefold() == player.casefold() for player in room.players):
        raise NicknameTakenError(room.code, nickname)

    room.players.append(nickname)
    room_repository.save_room(room)
    return room


def leave_room(code: str, nickname: str) -> Room | None:
    room = get_room(code)

    player = next(
        (p for p in room.players if p.casefold() == nickname.casefold()),
        None,
    )
    if player is None:
        raise PlayerNotInRoomError(room.code, nickname)

    room.players.remove(player)

    if not room.players:
        room_repository.delete_room(room.code)
        return None

    room_repository.save_room(room)
    return room


def create_room(nickname: str) -> Room:
    code = _generate_code()
    while room_repository.room_exists(code):
        code = _generate_code()

    room = Room(code=code, players=[nickname])
    room_repository.save_room(room)
    return room
