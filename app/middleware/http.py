from typing import Any
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from utils.config import Settings

class HTTPIntercept(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next, **kwargs):
        state = Settings.get_state("app", "status")

        if not state:
            return Response("Opps! looks like we're offline...", status_code=404)

        response = await call_next(request)

        if response.status_code == 404:
            return Response("This service does not exist!", status_code=404)

        return response
