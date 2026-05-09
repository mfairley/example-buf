# example-buf

Minimal repo demonstrating Pants's buf-based Python protobuf code generation
with a ConnectRPC greeter service.

## Layout

```
buf.yaml                                # buf v2 module config (modules: company/proto/services)
buf.gen.yaml                            # plugin config: protocolbuffers/python + pyi + connectrpc/python
3rdparty/requirements.txt               # connectrpc, protobuf, uvicorn
company/
  proto/
    services/greeter/greeter.proto      # the GreeterService definition
    gen/                                 # generated *_pb2.py / *_connect.py land here
  server/server.py                       # ASGI server
  client/client.py                       # async client
```

The `company` and `company/proto/gen` directories are both Pants source roots:

- `company/server/server.py` resolves as the `server.server` Python module.
- `company/proto/gen/services/greeter/greeter_pb2.py` resolves as
  `services.greeter.greeter_pb2`, matching the proto's `package` declaration.

## Running Pants from a sibling Pants source tree

Per <https://www.pantsbuild.org/prerelease/docs/contributions/development/running-pants-from-sources>,
this repo expects a clone of `pants` as a sibling directory:

```
parent-dir/
  pants/         # https://github.com/pantsbuild/pants checkout
  example-buf/   # this repo
```

Invoke Pants via the bundled `./pants_from_sources` wrapper (it auto-derives
`PANTS_VERSION` from the sibling source tree, disables pantsd, and adds
`--no-verify-config`):

```bash
cd example-buf
./pants_from_sources <goal> <args>
```

Override the source path with `PANTS_SOURCE=/some/other/pants ./pants_from_sources …`.

Examples:

```bash
# List all targets.
./pants_from_sources list ::

# Inferred runtime deps for the server (pulls in connectrpc, protobuf, uvicorn).
./pants_from_sources dependencies --transitive company/server/server.py

# Generate the connectrpc + protocolbuffers Python sources via buf.
./pants_from_sources export-codegen ::

# Run the ASGI server on http://0.0.0.0:8000.
./pants_from_sources run company/server:server-bin

# Run the async client (in another shell, after the server is up).
./pants_from_sources run company/client:client-bin
```

A quick curl while the server is running:

```bash
curl --header "Content-Type: application/json" \
     --data '{"name": "Jane"}' \
     http://localhost:8000/services.greeter.GreeterService/Greet
# {"greeting":"Hello, Jane!"}
```

## Testing

The new buf path is exercised via the `protobuf_generator='buf'` field on
`company/proto/services/greeter:greeter`. Module mapping reads `buf.gen.yaml`
to learn that the connectrpc plugin produces `_connect` modules and the
protocolbuffers plugin produces `_pb2` modules; runtime-dep inference uses the
same plugin list to add `connectrpc` and `protobuf` runtime requirements.
