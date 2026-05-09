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

## TypeScript client (without Pants, via workspaces)

The protobuf bindings are exposed as their own workspace package
(`@acme/proto`) and consumed by client packages. Pants is not involved.

```bash
pnpm install              # or: bun install
pnpm buf:generate         # writes idl/gen/acme/greeter/v1/greeter_pb.ts
cd clients/typescript
pnpm start                # runs src/main.ts against the running server
```

Layout:

```
package.json              # workspace root; lists devDeps for codegen
pnpm-workspace.yaml       # declares packages: idl, clients/typescript
buf.gen.ts.yaml           # buf template for TS only (out: idl/gen)
idl/                      # @acme/proto package
├── package.json          #   exports: { "./greeter/v1": "./gen/.../greeter_pb.ts" }
├── acme/greeter/v1/...   #   source .protos
└── gen/                  #   generated TS, gitignored
clients/typescript/       # consumer package
├── package.json          #   depends on "@acme/proto": "workspace:*"
├── tsconfig.json
└── src/main.ts           #   import { … } from "@acme/proto/greeter/v1"
```

Why this shape:

- **`idl/` is the `@acme/proto` package.** Its `package.json` `exports` uses
  a single wildcard pattern — `"./gen/*.js": "./gen/acme/*.ts"` — so any
  proto added under `idl/acme/` is importable without touching package.json.
  Consumers write `from "@acme/proto/gen/greeter/v1/greeter_pb.js"` — `gen/`
  in the import path is intentional: it matches the connectrpc-node
  convention, signals "this is generated" at every callsite, and helps tools
  (and LLMs) reason about provenance.
- **`workspace:*`** in `clients/typescript/package.json` tells the package
  manager to satisfy `@acme/proto` from the local workspace, not the npm
  registry. pnpm and bun both honor this protocol; npm 9+ also accepts it.
- **Two `buf.gen.*` templates** keep the Python and TS codegen flows
  independent. Pants's `export-codegen` reads `buf.gen.yaml` (Python) and
  the npm-driven `buf:generate` script reads `buf.gen.ts.yaml` (TS).
  Neither one steps on the other.

The Python server and TS client share the same `idl/`, `buf.yaml`, and
`buf.lock` — both are reproducible against the same BSR commit pins.

### Adding a second TS package

A new client (e.g. a web frontend) is two files:

```bash
mkdir -p clients/web/src
cat > clients/web/package.json <<'EOF'
{
  "name": "@example-buf/web-client",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "dependencies": { "@acme/proto": "workspace:*", "@connectrpc/connect": "^2.0.2" }
}
EOF
```

Add `clients/web` to `pnpm-workspace.yaml` (and the root `workspaces`
field if you also use bun/npm). `pnpm install` from the root links
`@acme/proto` into `clients/web/node_modules/`.
