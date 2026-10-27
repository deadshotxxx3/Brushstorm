from app.api.v1.rooms import router as rooms_router
from app.core.exceptions import (BrushstormError, NicknameTakenError,
                                 PlayerNotInRoomError, RoomFullError,
                                 RoomNotFoundError)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

ERROR_STATUS_CODES: dict[type[BrushstormError], int] = {
    RoomNotFoundError: 404,
    PlayerNotInRoomError: 404,
    NicknameTakenError: 409,
    RoomFullError: 409,
}

app = FastAPI(title="Brushstorm")

app.include_router(rooms_router, prefix="/api/v1")

@app.exception_handler(BrushstormError)
async def brushstorm_error_handler(request: Request, exc: BrushstormError) -> JSONResponse:
    status_code = ERROR_STATUS_CODES.get(type(exc), 400)
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})
