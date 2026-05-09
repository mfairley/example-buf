from connectrpc.code import Code
from connectrpc.errors import ConnectError
from protovalidate import ValidationError, Validator

from acme.greeter.v1.greeter_connect import GreeterService, GreeterServiceASGIApplication
from acme.greeter.v1.greeter_pb2 import GreetResponse

_validator = Validator()


class Greeter(GreeterService):
    async def greet(self, request, ctx):
        try:
            _validator.validate(request)
        except ValidationError as e:
            raise ConnectError(Code.INVALID_ARGUMENT, str(e))
        response = GreetResponse(greeting=f"Hello, {request.name}!")
        ctx.response_headers()["greet-version"] = "v1"
        return response


app = GreeterServiceASGIApplication(Greeter())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
