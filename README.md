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
/workspaces/
  pants/         # https://github.com/pantsbuild/pants checkout
  example-buf/   # this repo
```

Invoke Pants from source via:

```bash
cd /workspaces/example-buf
PANTS_SOURCE=/workspaces/pants /workspaces/pants/pants <goal> <args>
```

Examples:

```bash
# List all targets.
PANTS_SOURCE=/workspaces/pants /workspaces/pants/pants list ::

# Inferred runtime deps for the server (should pull in connectrpc + protobuf).
PANTS_SOURCE=/workspaces/pants /workspaces/pants/pants dependencies --transitive company/server/server.py

# Generate the connectrpc + protocolbuffers Python sources via buf.
PANTS_SOURCE=/workspaces/pants /workspaces/pants/pants export-codegen ::
```

## Testing

The new buf path is exercised via the `protobuf_generator='buf'` field on
`company/proto/services/greeter:greeter`. Module mapping reads `buf.gen.yaml`
to learn that the connectrpc plugin produces `_connect` modules and the
protocolbuffers plugin produces `_pb2` modules; runtime-dep inference uses the
same plugin list to add `connectrpc` and `protobuf` runtime requirements.
