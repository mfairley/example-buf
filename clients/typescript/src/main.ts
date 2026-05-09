import { GreeterService, GreetRequestSchema } from "@acme/proto/gen/greeter/v1/greeter_pb.js";
import { create } from "@bufbuild/protobuf";
import { createClient } from "@connectrpc/connect";
import { createConnectTransport } from "@connectrpc/connect-node";

const transport = createConnectTransport({
  baseUrl: "http://localhost:8000",
  httpVersion: "1.1",
});

const client = createClient(GreeterService, transport);
const req = create(GreetRequestSchema, { name: "Jane" });
const res = await client.greet(req);
console.log(res.greeting);
