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
# Resolve buf.yaml deps into buf.lock.
./pants_from_sources generate-lockfiles --resolve=buf

# Generate _pb2 / _pb2.pyi / _connect via buf (also pulls buf.validate from BSR).
./pants_from_sources export-codegen ::

# Confirm runtime-dep inference picks up connectrpc + protobuf + uvicorn from the
# `_connect` / `_pb2` / hand-written imports.
./pants_from_sources dependencies --transitive acme/server/server.py

# Run the validator unit tests.
./pants_from_sources test acme/server:tests

# Start the server (binds 0.0.0.0:8000).
./pants_from_sources run acme/server:server-bin
```

In another shell, hit the endpoint:

```bash
# Valid input → 200.
curl --header "Content-Type: application/json" \
     --data '{"name": "Jane"}' \
     http://localhost:8000/acme.greeter.v1.GreeterService/Greet
# {"greeting":"Hello, Jane!"}

# Empty name violates `[(buf.validate.field).string.min_len = 1]` → 400.
curl --header "Content-Type: application/json" \
     --data '{"name": ""}' \
     http://localhost:8000/acme.greeter.v1.GreeterService/Greet
# {"code":"invalid_argument","message":"invalid GreetRequest"}
```

Or run the matching async client:

```bash
./pants_from_sources run acme/client:client-bin
```

## `buf.lock`

Pants's `generate-lockfiles` goal also resolves `buf.yaml` deps. The resolve is
named after the directory containing the `buf.yaml` (`buf` for repo-root):

```bash
./pants_from_sources generate-lockfiles --resolve=buf
```

Bare `generate-lockfiles` (no `--resolve`) regenerates everything Pants knows
about, including `buf.lock`.
