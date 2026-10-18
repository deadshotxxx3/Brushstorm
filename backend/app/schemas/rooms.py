from pydantic import BaseModel, ConfigDict, Field


class NicknameRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nickname: str = Field(min_length=1, max_length=20)


class RoomResponse(BaseModel):
    code: str
    players: list[str]
    host: str
