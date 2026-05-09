from acme.proto.services.greeter.greeter_connect import (
    GreeterService,
    GreeterServiceASGIApplication,
)
from acme.proto.services.greeter.greeter_pb2 import GreetResponse


class Greeter(GreeterService):
    async def greet(self, request, ctx):
        print("Request headers:", ctx.request_headers())
        response = GreetResponse(greeting=f"Hello, {request.name}!")
        ctx.response_headers()["greet-version"] = "v1"
        return response


app = GreeterServiceASGIApplication(Greeter())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
