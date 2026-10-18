from dataclasses import dataclass


@dataclass
class Room:
    code: str
    players: list[str]
