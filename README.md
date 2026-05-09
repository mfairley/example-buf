# example-buf

ConnectRPC greeter service used to exercise Pants's buf-based Python protobuf
code generator.

## Prerequisite

Clone `pantsbuild/pants` as a sibling directory:

```
parent-dir/
  pants/
  example-buf/
```

(Or set `PANTS_SOURCE=/path/to/pants` before invoking.)

## What to run

```bash
# Generate _pb2 / _pb2.pyi / _connect via buf.
./pants_from_sources export-codegen ::

# Confirm runtime-dep inference picks up connectrpc + protobuf from the
# `_connect` and `_pb2` imports (driven by the plugins in buf.gen.yaml).
./pants_from_sources dependencies --transitive company/server/server.py

# Start the server (binds 0.0.0.0:8000).
./pants_from_sources run company/server:server-bin
```

In another shell, hit the endpoint:

```bash
curl --header "Content-Type: application/json" \
     --data '{"name": "Jane"}' \
     http://localhost:8000/services.greeter.GreeterService/Greet
# {"greeting":"Hello, Jane!"}
```

Or run the matching async client:

```bash
./pants_from_sources run company/client:client-bin
```
