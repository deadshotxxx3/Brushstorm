class BrushstormError(Exception):
    """Base class for all error in game."""


class RoomNotFoundError(BrushstormError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Room {code} not found")


class NicknameTakenError(BrushstormError):
    def __init__(self, code: str, nickname: str) -> None:
        self.code = code
        self.nickname = nickname
        super().__init__(f"Nickname {nickname} is already taken in room {code}")


class RoomFullError(BrushstormError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Room {code} is full")


class PlayerNotInRoomError(BrushstormError):
    def __init__(self, code: str, nickname: str) -> None:
        self.code = code
        self.nickname = nickname
        super().__init__(f"Player {nickname} is not in room {code}")
