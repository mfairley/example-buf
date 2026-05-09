import asyncio

from acme.greeter.v1.greeter_connect import GreeterServiceClient
from acme.greeter.v1.greeter_pb2 import GreetRequest


async def main() -> None:
    client = GreeterServiceClient("http://localhost:8000")
    res = await client.greet(GreetRequest(name="Jane"))
    print(res.greeting)


if __name__ == "__main__":
    asyncio.run(main())
