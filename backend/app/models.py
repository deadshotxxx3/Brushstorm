from dataclasses import dataclass


@dataclass
class Room:
    code: str
    players: list[str]

    @property
    def host(self) -> str:
        return self.players[0]
