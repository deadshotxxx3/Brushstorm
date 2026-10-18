from app.models import Room

_ROOMS: dict[str, Room] = {}

def room_exists(code: str) -> bool:
    return code in _ROOMS

def get_room(code: str) -> Room | None:
    return _ROOMS.get(code)

def save_room(room: Room) -> None:
    _ROOMS[room.code] = room

def delete_room(code: str) -> None:
    _ROOMS.pop(code, None)
