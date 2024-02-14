from typing import Any
from fastapi import Request, status
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware

from utils.config import Settings

class HTTPIntercept(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next, **kwargs):
        state = Settings.get_state("app", "status")

        if not state:
            return FileResponse("public/views/down.html", status_code=status.HTTP_403_FORBIDDEN)

        response = await call_next(request)

        if response.status_code == 404:
            return FileResponse("public/views/fallback.html", status_code=status.HTTP_404_NOT_FOUND)

        return response
 