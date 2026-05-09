"""ConnectRPC interceptor that runs `protovalidate.Validator` on every unary
request and rejects with `INVALID_ARGUMENT` on failure."""

from __future__ import annotations

from connectrpc.code import Code
from connectrpc.errors import ConnectError
from protovalidate import ValidationError, Validator


class ValidationInterceptor:
    """A `connectrpc.interceptor.UnaryInterceptor` (structural)."""

    def __init__(self) -> None:
        self._validator = Validator()

    async def intercept_unary(self, call_next, request, ctx):
        try:
            self._validator.validate(request)
        except ValidationError as e:
            raise ConnectError(Code.INVALID_ARGUMENT, str(e))
        return await call_next(request, ctx)
