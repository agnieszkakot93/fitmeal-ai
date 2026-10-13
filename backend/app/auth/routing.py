from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute


class HideInputRoute(APIRoute):
    """422 responses without the submitted values: they may be tokens (§7.7)."""

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        handler = super().get_route_handler()

        async def route(request: Request) -> Response:
            try:
                return await handler(request)
            except RequestValidationError as exc:
                errors = [
                    {k: v for k, v in e.items() if k not in ("input", "ctx")} for e in exc.errors()
                ]
                raise RequestValidationError(errors) from None

        return route
