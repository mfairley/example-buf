from acme.greeter.v1.greeter_connect import GreeterService, GreeterServiceASGIApplication
from acme.greeter.v1.greeter_pb2 import GreetResponse
from acme.server.validation_interceptor import ValidationInterceptor


class Greeter(GreeterService):
    async def greet(self, request, ctx):
        response = GreetResponse(greeting=f"Hello, {request.name}!")
        ctx.response_headers()["greet-version"] = "v1"
        return response


app = GreeterServiceASGIApplication(Greeter(), interceptors=(ValidationInterceptor(),))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
