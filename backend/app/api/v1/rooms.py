from app.models import Room
from app.schemas.rooms import NicknameRequest, RoomResponse
from app.service import rooms as room_service
from fastapi import APIRouter, status

router = APIRouter(prefix="/rooms", tags=["rooms"])

def _to_response(room: Room) -> RoomResponse:
    return RoomResponse(code=room.code, players=room.players, host=room.host)

@router.post("", status_code=status.HTTP_201_CREATED)
def create_room(request: NicknameRequest) -> RoomResponse:
    room = room_service.create_room(request.nickname)
    return _to_response(room)

@router.get("/{code}")
def get_room(code: str) -> RoomResponse:
    room = room_service.get_room(code)
    return _to_response(room)

@router.post("/{code}/players")
def join_room(code: str, request: NicknameRequest) -> RoomResponse:
    room = room_service.join_room(code, request.nickname)
    return _to_response(room)

@router.delete("/{code}/players/{nickname}", status_code=status.HTTP_204_NO_CONTENT)
def leave_room(code: str, nickname: str) -> None:
    room_service.leave_room(code, nickname)

