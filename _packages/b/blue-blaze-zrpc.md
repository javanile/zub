---
title: Zrpc
description: "gRPC for Zig, built on zinet. All four call kinds on both sides, HTTP/2 and TLS 1.3 with ALPN h2, gRPC-Web, the Connect protocol, name resolution and load balancing, keepalive, health checking, compile-time reflection, a protoc plugin, and OpenTelemetry over OTLP — every protocol checked against somebody else's implementation."
license: MIT
author: blue-blaze
author_github: blue-blaze
repository: https://github.com/blue-blaze/Zrpc
keywords:
  - code-generation
  - connect-rpc
  - grpc
  - grpc-web
  - http2
  - load-balancing
  - networking
  - opentelemetry
  - protobuf
  - rpc
  - tls
date: 2026-08-28
category: tooling
updated_at: 2026-08-28T17:50:57+00:00
last_sync: 2026-08-28T17:50:57Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 4
distributable_binary_count: 4
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/blue-blaze/Zrpc/
---

# Zrpc

gRPC for Zig, built on [zinet](https://github.com/blue-blaze/zinet).

One RPC is one HTTP/2 stream, and zinet already gives every stream its own
pipeline on the connection's single reader task — so handler state needs no
locks. Zrpc is the layer between that and an application: gRPC's HTTP/2 header
mapping, its length-prefixed framing, status, metadata, deadlines, and the four
call kinds.

## Status

Under construction. This section states what works, checked by tests, rather than
what is planned:

| Piece | State |
|---|---|
| Toolchain anchoring, build graph | Works. `zig build test`, `fuzz`, `fmt`, `fmt-check`, `check` |
| Status codes, `grpc-message` encoding, error mapping | Works. `src/status.zig` |
| Length-prefixed framing | Works. `src/framing.zig`, with a chunk-independence fuzz target |
| Metadata, `-bin` base64, limits | Works. `src/metadata.zig` |
| `grpc-timeout` parsing and formatting | Works. `src/timeout.zig` |
| HTTP/2 header mapping | Works. `src/wire.zig` |
| Unary calls, server side | Works. `src/server/`, on a socket and with no socket |
| The other three call kinds, server side | Works. `src/server/stream.zig`, `src/server/stream_test.zig` |
| The client: all four kinds, from an ordinary task | Works. `src/client/` |
| Interoperability: Python grpcio, `grpcurl`, both directions | Works. `zig build interop` |
| Deadlines and cancellation, both sides | Works. `src/server/deadline_test.zig` |
| Compression: gzip and deflate, with a bounded decompressor | Works. `src/compression.zig` |
| TLS 1.3 with ALPN `h2`, both sides | Works. `src/tls.zig`, `src/tls_test.zig` |
| Rich status (`grpc-status-details-bin`), interceptors, an observability seam | Works. `src/details.zig`, `src/stats.zig` |
| Health checking, server reflection, descriptors synthesized at compile time | Works. `src/health.zig`, `src/reflection.zig`, `src/descriptor.zig` |
| Bounds enforced against a hostile peer, with a fuzz target per parser | Works. `src/server/hardening_test.zig`, `src/fuzz.zig` |
| Code generation from `.proto` files: `protoc-gen-zig` | Works. `src/generate.zig`, `tools/protoc-gen-zig.zig`, `zig build generate` |
| gRPC-Web over HTTP/1.1, both variants, with CORS | Works. `src/web.zig`, `src/server/web.zig`, checked against sonora and curl |
| The Connect protocol: unary, streaming, and cacheable `GET` | Works. `src/connect.zig`, `src/server/connect.zig`, checked against connect-go and curl |
| Name resolution and load balancing: a channel over many endpoints | Works. `src/resolver.zig`, `src/balancer.zig`, `src/client/channel.zig`, checked against two grpcio servers |
| Benchmarks: evidence for the performance claims | Works. `zig build bench`, and it found a seventy-fold latency defect |
| Keepalive: `PING`, and a peer that stopped answering | Works. `src/keepalive.zig`, both transports, off by default |
| `GOAWAY` honoured on both sides: draining, and streams a peer disowned | Works. `src/client/transport.zig`, `src/server/transport.zig`, with frames written by hand |
| OpenTelemetry: spans and metrics over OTLP/HTTP | Works. `src/otel.zig`, `src/otel/exporter.zig`, checked against OpenTelemetry's own protobuf classes |

A service is a Zig struct, checked at compile time:

```zig
const Greeter = struct {
    pub const service_name = "helloworld.Greeter";
    pub const methods = .{
        .SayHello = .{ .kind = .unary, .Request = HelloRequest, .Response = HelloReply },
    };

    pub fn SayHello(_: *Greeter, call: *zrpc.Call, request: *const HelloRequest) !HelloReply {
        return .{ .message = try std.fmt.allocPrint(call.arena, "hello {s}", .{request.name}) };
    }
};
```

An entry in `methods` with no function, or a function whose types disagree with it, is
a compile error rather than a method that returns `UNIMPLEMENTED` in production.

A streaming method returns an object instead, because messages arrive over time and
the flow-control window opens and closes:

```zig
const Stream = zrpc.ServerStream(HelloRequest, HelloReply);

pub fn SayHelloStream(_: *Greeter, stream: Stream, request: *const HelloRequest) !Greetings {
    return .{ .name = try stream.arena().dupe(u8, request.name), .remaining = 5 };
}

const Greetings = struct {
    name: []const u8,
    remaining: usize,

    // Called whenever the stream can take more. Send while writable, stop when not:
    // the transport calls back when the queue drains.
    pub fn onWritable(self: *Greetings, stream: Stream) !void {
        while (self.remaining > 0 and stream.isWritable()) {
            self.remaining -= 1;
            try stream.send(&.{ .message = "hello" });
        }
        if (self.remaining == 0) try stream.finishOk();
    }
};
```

Which callbacks a kind needs is checked too: a client-streaming handler without
`onMessage` has nowhere to deliver to, and a server-streaming handler without
`onWritable` could never be resumed past the first window. Both are compile errors.

## Toolchain

Zig 0.17 is not released yet, and 0.16 cannot compile this project — it has no
`std.Io`. The floor is zinet's own: `0.17.0-dev.1476+91a29d707`, recorded in
`.zigversion` and checked by `build.zig`, which fails with one sentence rather
than a wall of standard-library errors.

```
./scripts/zig.sh build test      # finds the right compiler for you
ZIG=/path/to/zig ./scripts/zig.sh build check
```

## Running it

```
./scripts/zig.sh build run-greeter_server -- 50051

grpcurl -plaintext -proto proto/greeter.proto \
    -d '{"name":"zig"}' localhost:50051 helloworld.Greeter/SayHello

./scripts/zig.sh build run-greeter_client -- 50051
```

## Calling

A method on the calling side is a path and two types. Calls are made from an ordinary
task; the connection keeps its own, which is what keeps handler state lock free:

```zig
const say_hello: zrpc.ClientMethod(HelloRequest, HelloReply) = .{
    .path = "/helloworld.Greeter/SayHello",
};

const client = try zrpc.Client.connect(.{ .gpa = gpa, .io = io, .address = address });
defer client.deinit();

const reply = try client.unary(say_hello, &.{ .name = "zig" }, arena, .{});
const replies = try client.serverStream(stream_method, &request, arena, .{});
```

A status becomes an ordinary Zig error — `error.NotFound`, not a number — so a caller
switches on it like any other. The streaming kinds collect their messages up to an
explicit bound rather than buffering without one, and PROTOCOL.md explains why that is
the honest shape from another task: zinet replenishes a receive window before any handler
sees the data, so a consumer on another task cannot exert HTTP/2 backpressure. An
application that needs true streaming implements `client.Sink` and runs on the
connection's task, where the backpressure is real.

## Around a call

An interceptor refuses or annotates a call with the same API a handler has, so an
authentication stage is a dozen lines and can say why as expressively as a method can:

```zig
fn requireToken(_: ?*anyopaque, call: *zrpc.Call) !void {
    const token = call.metadata.get("authorization") orelse
        return call.fail(.init(.unauthenticated, "no token"));
    if (!std.mem.eql(u8, token, expected)) return error.PermissionDenied;
}

const chain = [_]zrpc.ServerInterceptor{.{ .before = requireToken }};
```

A refused call never reaches the application — that is the difference between this and a
check at the top of a handler — and `after` sees every outcome in reverse order, so a
chain nests.

Failures can carry typed details, which peers read: `google.rpc.ErrorInfo`, `RetryInfo`
and `BadRequest` are declared, and any other message with a `type_url` packs the same
way.

```zig
try call.failWith(.init(.resource_exhausted, "sold out"), &.{
    try zrpc.details.pack(call.arena, zrpc.details.ErrorInfo, &.{
        .reason = "OUT_OF_STOCK",
        .domain = "example.com",
    }),
});
```

On the calling side the same block comes back through `CallOptions.outcome`, because a
Zig error can carry a code and nothing else.

Observability is one function pointer: a call began, a message went each way, a call
ended with a status. The events come from the transport's own funnels rather than a
wrapper, so a consumer sees the calls that fail before the application too — an unknown
method, a deadline — and it runs on the connection's task, which is what bounds what it
may do.

```zig
var counters: zrpc.stats.Counters = .{};
const options = .{ .transport = .{ .call = .{ .stats = counters.handler() } } };
```

## Discovery

Two services every deployment wants, and neither is special to the framework — both are
ordinary services, registered the ordinary way:

```zig
var health: zrpc.Health = .{};
var reflection: zrpc.Reflection = .{};

const services = [_]zrpc.Registration{
    zrpc.register(Greeter, &greeter),
    zrpc.register(zrpc.Health, &health),
    zrpc.register(zrpc.Reflection, &reflection),
};
reflection.services = &services;      // it describes the list it is in
try health.setStatus("helloworld.Greeter", .SERVING);
```

With reflection installed, a caller needs no `.proto` file at all:

```
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe helloworld.Greeter
grpcurl -plaintext -d '{"name":"zig"}' localhost:50051 helloworld.Greeter/SayHello
```

The descriptors those commands read are synthesized from the Zig declarations during
compilation — `protobuf.encode` is ordinary Zig, so it runs at `comptime` and the bytes
end up in the binary's constant data. A server that never answers a reflection request
pays for the bytes and nothing else. It also means the descriptor cannot drift from the
service, because there is only one declaration of either; PROTOCOL.md explains what a
`.proto` file can say that Zig types cannot, and why each of those is a compile error or
a separate declaration rather than a guess.

A watch on the health service notices a status change made from any task, because each
watch reads the table on its own task rather than being pushed to — the reason is a
lifetime one and PROTOCOL.md gives it.

## Encryption

TLS is a different constructor rather than a flag, so a program that serves cleartext
says so:

```zig
var identity = try zrpc.tls.loadIdentity(gpa, io, "cert.pem", "key.pem");
defer identity.deinit(gpa);

const server = try zrpc.Server.listenTls(options, .{ .identity = &identity });

var roots = try zrpc.tls.bundleFromFile(gpa, io, "cert.pem");
defer roots.deinit(gpa);

const client = try zrpc.Client.connectTls(options, .{
    .host = "localhost",
    .trust = .{ .bundle = &roots },
});
```

ALPN is `h2` and nothing else, on both sides: a handshake that agreed on anything else
is refused before the first call rather than discovered by one. The server certificate
must be ECDSA P-256 or Ed25519, because `std.crypto` can verify RSA signatures but not
produce them — an RSA key is refused when it is loaded, not when a client connects.

Everything above the socket is the same code, and PROTOCOL.md explains the two things
that are not: a TLS connection is not a `Channel`, so it has neither the task hop every
client call needs nor the tick that notices a deadline. Both are replaced by one seam —
a message our own handler recognises at the tail of the pipeline — and one timer task
per server.

## Interoperability

Every protocol here is checked against somebody else's code rather than only its own
counterpart — zinet's discipline, kept because it keeps finding things. `zig build
interop` starts the example server and points Python's grpcio and Go's `grpcurl` at
it: unary calls, a default-valued request, metadata including a binary header, a
status whose message needs percent-encoding, fifty calls on one connection, a 200 KiB
response that has to cross the flow-control window several times before its trailers
may go out, and all three streaming kinds — including 1.6 MiB of streamed replies, an
empty client stream, and a bidirectional call the client abandons halfway, after which
the connection has to keep working — and a deadline on a method that answers nothing,
which the server has to end itself with `DEADLINE_EXCEEDED`, and gzip in both directions
at once. Then it turns the direction around: our client against grpcio's server, all four
kinds plus its own deadline and a compressed request, which is what checks our HTTP/2, our
framing and our status parsing against somebody else's rather than against their mirror
image.

Rich status goes both ways as well, and is checked by grpcio-status's own parser rather
than by ours — which decodes the detail block *and* verifies that the code and message
inside it match the trailers, so the duplication rule is tested along with the encoding.

The synthesized descriptors are checked against two foreign parsers, which turned out to
matter: `grpcurl` lists the services, reconstructs `helloworld.Greeter` and calls it with
no `-proto` at all, and Python builds a descriptor pool from nothing but our reflection
responses and then makes a dynamic unary call and a dynamic stream through it. Go's
parser is the stricter of the two — it refused an enum value whose zero number was
implied rather than written, which Python's pool had accepted — which is the argument for
running both. The health service is checked through grpcio's own generated stubs,
compiled from the published `.proto` rather than from anything of ours.

gRPC-Web is checked against two more strangers. sonora is a complete third-party
gRPC-Web client — another language, another author — and it drives the binary variant
through unary calls, a status in a trailer frame, a hundred-message stream, fifty calls
on one keep-alive connection and a deadline the server has to notice itself. curl and
the system `base64` cover the `-text` variant, which sonora does not use: the response is
decoded in a single call by a decoder that is not ours, which is the only way to check
that a streamed base64 body stayed one document. The `0x80` flag is asserted on the bytes,
and the CORS preflight is asserted to carry the headers a browser refuses to proceed
without.

Connect gets the same treatment from connect-go, which is Buf's own implementation and the
one the specification was written alongside: the unary shape with no framing, the HTTP
status a failure carries, the JSON error body, typed details, both streaming shapes it can
use, a refusal of the third, fifty calls on one keep-alive connection and a cacheable GET.
That comparison found nothing wrong with the code and confirmed something worth confirming
— the sixteen-row HTTP status table agrees with connect-go's line for line, including
`FAILED_PRECONDITION` being `400` rather than the `412` an HTTP reader would guess.

curl covers what connect-go cannot: that the protocol is usable *by hand*. A unary call is
one `--data-binary`, the failure body is parsed by Python's `json` rather than matched as a
string, and the `GET` is assembled with `--data-urlencode`. If that stopped working,
Connect would have no advantage left over gRPC and no generated client would notice.

The OTLP export is checked by OpenTelemetry's own generated protobuf classes, in a
collector that shares no code with this library. That is the only way to find a field number
that is merely plausible: OTLP's timestamps are `fixed64`, and a varint in their place
decodes to a different number rather than failing, so the mistake would ship and show up as
spans dated 1970. The collector also asserts the convention *names* — a span called
`SayHello` rather than `helloworld.Greeter/SayHello` is valid telemetry that joins nothing —
and the invariant a real collector rejects a payload over, that a histogram has one bucket
per boundary plus one above the last. The export it reads comes from one process serving
calls and making them with a single exporter on both halves, so `SERVER` spans and `CLIENT`
spans arrive together, along with a span for an unimplemented method that no handler ever
ran — which is what the seam sees and a wrapper around the application would not.

Load balancing is checked against two of grpcio's servers at once, and the evidence comes
from *them*: each is started with a tag it puts in its replies, so "the calls were spread"
is asserted from the far side rather than inferred from a counter of ours. Then one of the
two is killed and the run is repeated — the surviving server identifies itself, with the
dead address still in the channel's configuration, which is the only way to tell failover
apart from a channel that had quietly been using one endpoint all along.

Then all of it again over TLS: grpcurl and grpcio against our TLS server, and our TLS
client against grpcio's — which is OpenSSL underneath, so the handshake, the ALPN token
and our chain verification are checked against somebody else's rather than against
ours. The certificate is generated at run time rather than committed: a PEM private key
in a repository is what secret scanners exist to stop.

It skips with a message rather than failing when the tools are absent:

```
python3 -m venv .venv-interop
./.venv-interop/bin/pip install grpcio grpcio-tools
brew install grpcurl
```

## Generating from a `.proto` file

A service can be declared as a Zig struct, and often the schema is somebody else's: a
file another team owns, or one that four other languages already generate from. So
there is a `protoc` plugin.

```
zig build tools
protoc --plugin=protoc-gen-zig=zig-out/bin/protoc-gen-zig \
       --zig_out=generated -I proto proto/greeter.proto
```

Messages become structs with their field numbers declared, enums keep protobuf's own
value names, and a service becomes a table plus a set of client handles. A generated
service is deliberately not an implementation — the framework finds handlers by name on
the struct that declares `methods`, so an application borrows two lines and writes the
rest:

```zig
const Greeter = struct {
    pub const service_name = pb.Greeter.service_name;
    pub const methods = pb.Greeter.methods;

    pub fn SayHello(_: *@This(), call: *zrpc.Call, request: *const pb.HelloRequest) !pb.HelloReply {
        return .{ .message = try std.fmt.allocPrint(call.arena, "hello {s}", .{request.name}) };
    }
};

const reply = try client.unary(pb.Greeter.client.SayHello, &.{ .name = "zig" }, arena, .{});
```

Every compile-time check still applies to that struct: a method in `methods` with no
function, or one whose types disagree, is a compile error exactly as it would be for a
hand-written service.

The generator refuses rather than approximates. proto2, `group` fields, extensions and
integers narrower than 32 bits are all errors with a sentence explaining why, printed by
`protoc` next to the file that caused them — because a generator that emits something
almost right turns a schema mistake into a wire-format bug in production. The one
exception is `oneof`, which becomes one optional field per member: the wire format is
identical and the *guarantee* is what is lost, which the generated code says at the point
where it matters.

`zig build generate` closes the loop. It regenerates, fails if the committed output has
drifted, and then compares the descriptors this library *synthesizes* from the generated
types against the ones `protoc` produced from the `.proto` file — field for field, method
for method. Two independent translations of one file; when they disagree, one is wrong
and it does not matter which.

## From a browser

A browser cannot speak gRPC: it hands a request body over in one piece, and until
recently could not read HTTP trailers, which is where the status lives. gRPC-Web is the
mapping that removes both obstacles, and it is a second listener over the same services:

```zig
const services = [_]zrpc.Registration{ zrpc.register(Greeter, &greeter) };

const grpc = try zrpc.Server.listen(.{ .address = ..., .services = &services });
const web = try zrpc.Server.listenWeb(.{ .address = ..., .services = &services }, .{
    .cors = .{ .origins = &.{"https://app.example.com"} },
});
```

Two listeners rather than one flag, because gRPC is HTTP/2 and gRPC-Web is HTTP/1.1 —
one port would mean deciding from a connection's first bytes which protocol it is, and a
protocol inferred from a prefix is one a peer can lie about. The `services` slice is
borrowed, so the two cannot drift apart.

The status travels as a frame in the body, flagged `0x80` — the flag `framing.zig` has
recognised since it was written. The `-text` variants base64 the body, and there the
encoder keeps up to two bytes back so that **the whole response is a single valid base64
document** rather than a run of them concatenated; PROTOCOL.md explains why the stronger
property is worth two bytes of state, and the interoperability check decodes a streamed
response in one call with the system's `base64` to prove it.

Only unary and server-streaming methods are reachable, because a browser cannot stream a
request body. The other two are refused with a sentence saying so, before a call exists —
a client-streaming handler waiting for a message that cannot arrive would hang until its
deadline. sonora, an independent gRPC-Web client, refuses those two kinds for the same
reason, which the checks assert rather than assume.

CORS is part of the protocol rather than decoration: a browser will not send the call
until a preflight comes back, and will not let a script read `grpc-status` unless it is
exposed — so without it a failed call is indistinguishable from a network error. The
default allows no origin at all, because an origin list is the only thing between a
browser-reachable RPC and any page calling it with the user's cookies.

Everything else is the same code. The four call kinds, deadlines, cancellation,
interceptors, compression, the status mapping and the observability events are shared
with the HTTP/2 transport, because what a call needs from a connection turned out to be
six operations and making them a seam was cheaper than a second state machine.

## As an ordinary HTTP API

The Connect protocol asks a different question from gRPC's: what if a unary call were just
an HTTP request? No length prefix, no trailers, no HTTP/2. The body is the message, the
status is the HTTP status, and a failure is JSON a person can read.

```
curl --data-binary @request.bin \
     -H 'content-type: application/proto' \
     http://localhost:8080/helloworld.Greeter/SayHello
```

That is a complete client. A failure looks like this, with the HTTP status set to match:

```json
{"code":"not_found","message":"no such thing"}
```

It is a third listener over the same services:

```zig
const api = try zrpc.Server.listenConnect(.{ .address = ..., .services = &services }, .{});
```

A method that has no side effects can say so, and then it is reachable by `GET` — with the
message base64url-encoded in the query string, which makes the response cacheable by
anything that caches HTTP:

```zig
pub const methods = .{
    .SayHello = .{ .kind = .unary, .Request = Request, .Response = Reply, .idempotent = true },
};
```

That defaults to false on purpose. Nothing about a method's signature says whether it
mutates, and a mutation reachable by a cacheable `GET` is a bug that shows up much later
as stale data.

Three of the four call kinds work here, one more than gRPC-Web: an ordinary HTTP client can
send a chunked request body even though a browser cannot, so client-streaming is reachable.
Bidirectional streaming is refused, and Connect's own specification refuses it for the same
structural reason — interleaving means reading the request while writing the response, and
a body that arrives complete cannot interleave with anything.

The `json` codec is refused rather than approximated. Protobuf's JSON mapping is a
specification of its own — 64-bit integers as strings, enums by name, well-known types with
bespoke forms — and nine tenths of it is worse than none, because the tenth appears as a
field silently reading zero. PROTOCOL.md says what a `json` request gets instead.

## Many servers behind one name

A `Client` is one connection to one address, which is the honest unit and not what a
deployment has. A deployment has a name that stands for several processes, and for a
different several tomorrow. `Channel` resolves the name, keeps a connection per endpoint,
and chooses one per call — with the same four methods and the same signatures, so moving
between the two is a change of constructor:

```zig
var round_robin: zrpc.balancer.RoundRobin = .{};
var endpoints: zrpc.resolver.Static = .{ .addresses = &addresses };

const channel = try zrpc.Channel.open(.{
    .gpa = gpa,
    .io = io,
    .resolver = endpoints.resolver(),
    .picker = round_robin.picker(),
});
defer channel.deinit();

const reply = try channel.unary(say_hello, &.{ .name = "zig" }, arena, .{});
```

A target string says where to look, and it is parsed rather than assumed — `ipv4:a:1,b:2`
is a list somebody wrote down and `service.internal:50051` is a name that needs a DNS
server, and which one it was decides what the channel does:

```zig
switch (try zrpc.resolver.parseTarget(target)) {
    .literal => |addresses| ...,
    .name => |name| ...,   // needs zrpc.resolver.Dns and its servers
}
```

A target with no port is an error rather than a guess, because 443 is the TLS convention
and a channel may be cleartext. `Dns` has no default nameserver for a sharper reason: a
library that defaulted to a public resolver would send every name a program looks up to a
third party the application never chose. `systemServers` reads the ones the machine was
configured with, and it is a function you call.

There is no background task. Connections are made by the caller that needs one, because a
maintenance task's job would be to destroy a connection while another task might be calling
on it — which is the shape of every ownership bug this project has had. What follows from
that is written down rather than discovered: an idle channel holds nothing open, a dead
endpoint is noticed by a call rather than a timer, and `refresh` is a door for an
application that wants a resolution on a schedule and owns a task to ask from.

Two policies: `pick_first` keeps one connection, `round_robin` spreads over all of them.
They differ in exactly one rule — whether an idle endpoint is preferred to a ready one —
and getting it backwards produces something that looks like a working round robin and
never dials a second endpoint. `Picker` is one function, so a third policy is a few lines.

A server that is being replaced says so, and the channel listens. `GOAWAY` names the last
stream a peer processed, which makes everything above it *provably* not applied — the only
unambiguous version of that news in HTTP/2, and stronger than a closed socket can be. A
draining connection keeps serving the calls already on it and takes no new ones, so a
rolling deployment costs latency rather than errors. PROTOCOL.md explains why a second
GOAWAY may only lower the watermark, and what the balancer had to learn to stop treating
"open" as "usable".

Retries draw a line that most libraries blur. An error that came back *without* a status
means no server saw the call, so trying another endpoint cannot duplicate anything and
needs no permission. An error that *is* a status means a server saw it and may have applied
it anyway — no status distinguishes "refused" from "done, then the answer was lost" — so
repeating that one requires saying `retry_after_send`. It defaults to off, because retrying
by default turns one payment into two on exactly the failure that looks most retryable.
PROTOCOL.md explains why that question is decidable rather than a guess, and why there is
no sleep anywhere in the retry loop.

## Telemetry

The observability seam said, when it was written, that an OpenTelemetry exporter would be a
`Handler` in an application's own code and that `stats.zig` would not grow when one arrived.
It did not grow: the exporter reads the same four facts every other consumer does, and adds
no event, no field and no callback.

```zig
var exporter: zrpc.otel.Exporter = .init(io, .{
    .endpoint = collector_address,
    .service_name = "greeter",
});

var options: zrpc.ServerOptions = .{ .gpa = gpa, .io = io, .address = ..., .services = &services };
options.transport.call.stats = exporter.handler();

// Later, from a task the application owns:
const report = try exporter.flush(gpa);
```

Spans are one per call, named `helloworld.Greeter/SayHello` and carrying `rpc.system`,
`rpc.service`, `rpc.method` and `rpc.grpc.status_code`. Metrics are `rpc.server.duration`
and `rpc.client.duration` in milliseconds, plus the four message-size histograms. The names
and the bucket boundaries are the specification's rather than ours, because a dashboard and
an alert are written against those strings — a spelling of our own would be valid telemetry
that joins nothing.

The split between the two halves of that snippet is the whole design. `handler()` runs **on
the connection's task**, so it records into fixed arrays under a spinlock and cannot
allocate, block or grow; when its storage is full it drops the newest span and counts it.
`flush` builds the OTLP payload and posts it, on whatever task calls it, and allocates and
blocks and fails there. There is no background task for the same reason `Channel` has none.

Metrics are cumulative, so a lost export costs resolution rather than data. Spans are
removed from the buffer only once the collector has answered 2xx — a collector under load
answers 503, and treating that as delivery is how telemetry disappears quietly.

A span here is a root: PROTOCOL.md explains why attaching an incoming `traceparent` needs a
call identifier that is unique in the process rather than on its connection, and names the
one-field change that would provide one.

## A connection that died quietly

A TCP connection whose peer vanished stays open on this side indefinitely. Nothing arrives
and nothing fails, so a call on it waits for its deadline and a call without one waits
forever. A `PING` is the only cure, because HTTP/2 obliges a peer to answer one:

```zig
options.transport.keepalive = .{
    .interval_ns = 30 * std.time.ns_per_s,
    .timeout_ns = 20 * std.time.ns_per_s,
};
```

Off by default on both sides, because it is traffic on every connection a program holds
forever and it only buys something for a program that keeps connections idle long enough
for something in the path to forget them. The decision lives in `src/keepalive.zig`, which
has no `Io`, no allocator and no frames in it — one question answered from timestamps — so
both transports share it and its awkward cases are unit tests rather than integration ones.

Keepalive is usually two features described as one, and only half of it is here. Sending
pings and giving up on silence is this; *refusing* a peer that pings abusively was already
done a layer down, because a `PING` obliges a reply and is therefore an amplification
primitive. zinet counts control frames and closes a connection that sends too many with
`ENHANCE_YOUR_CALM`. So there is no interval floor enforced in this library — the
enforcement is at the peer, where it belongs, and PROTOCOL.md gives the number and points
at the test that aims our own client at our own server to prove it.

There is no keepalive task. The tick that had to exist for deadlines already wakes every
connection on its own task, which is exactly what a periodic ping needs.

## Against a hostile peer

Every bound has a number, an owner and an answer, and PROTOCOL.md tabulates all of them.
The answer is the part worth checking: each one refuses a *call* and leaves the
connection working, because gRPC multiplexes and a bound that closes connections is a
denial of service with extra steps. `src/server/hardening_test.zig` drives a real
transport past each bound and then makes an ordinary call on the same connection.

Every parser that reads bytes a peer chose has a fuzz target with a property attached,
not just "it did not crash": framing is chunk-independent, a decompressor never exceeds
its limit, formatting a deadline never shortens it, percent and base64 round-trip, and a
rich status block from a hostile server stays inside its declared element and length
bounds.

```
./scripts/zig.sh build fuzz
```

Auditing that led to one substantive fix. `status.zig` maps errors to codes through an
explicit table, and anything missing from it became `UNKNOWN` — which tells a peer
nothing. Eight errors were in that position, the worst being corrupt compressed data:
both the commonest transport corruption and a plausible attack, answered `UNKNOWN`. It is
`INTERNAL` now, and every arm of the table has a test.

## Measuring it

```
zig build bench            # or `zig build bench -- 20000` for more calls
```

Every other claim here is checked by a test, a fuzz target, or somebody else's
implementation. The performance claims were not, so there is a benchmark. It calls through
the public API over a real socket, reports the interesting things as *differences* between
two otherwise identical runs, and is always ReleaseFast — including the library and zinet,
which the first version of it got wrong.

It earned its place on the first run. A sequential unary call took nine milliseconds and one
connection managed 151 calls a second, because of a single unset option: a call is handed
from an ordinary task to the connection's task, and on a connection whose peer is silent —
which is every connection between two sequential calls — that handover waits for the reader
to come out of a blocking read. The bound on that wait defaulted to ten milliseconds.
It is now five hundred microseconds, which is about ten thousand calls a second with a
median near ninety. No test could have found it: every test passes at either speed.

What it confirms is the claim this file makes about observability. Installing `stats.Counters`
or the OpenTelemetry exporter moves the median call latency by less than the noise between
runs, and the **allocation count per call is identical to two decimal places** in all three
configurations — so "it cannot allocate" is measured, not asserted.

It also prints two things nobody claimed. A unary call allocates about two dozen times across
both sides, which is the obvious next thing to attack. And reading the monotonic clock once
per read cycle instead of once per event, which PROTOCOL.md argues for, is worth two
hundredths of a percent on a unary call and about fifteen percent per message on a stream —
reported in proportion, because overselling a real decision is how a document stops being
trusted about the rest.

## Continuous integration

```
zig build check            # everything below, in one command
./scripts/install-zig.sh   # the pinned compiler, read from .zigversion
```

`.github/workflows/ci.yml` installs the dependencies and runs that one command, rather than
restating the pipeline in YAML where it would drift from what a contributor runs. It does two
things a local run does not.

It **treats a skip as a failure**. The interoperability and generator scripts skip with a
message when a tool is missing, which is right on a laptop and wrong on a build server: a
green run that quietly checked nothing is worse than a red one. That rule immediately found
something — the Connect check had been skipping on every fresh clone, because the generated Go
client is not committed and nothing regenerated it. It is generated now, from the same
`proto/greeter.proto` the Zig side uses, with no second copy of the schema.

And it runs on **Linux**, which the development machine is not. Everything here is `std.Io`,
so the two platforms are genuinely different backends under one interface — `io_uring` against
`kqueue` — and the tests are what would notice.

The compiler is pinned by URL rather than resolved by an action: 0.17 is unreleased and
ziglang.org's index carries only the current master, which this pin is older than. The
tarball is still hosted, and when it eventually is not, moving the pin forward is a
deliberate act with a full `check` attached — the same rule as bumping zinet.

## Reading order

* [PROTOCOL.md](PROTOCOL.md) — the gRPC mapping, decision by decision, with the
  rule that forced each one and what is deliberately absent.
* [MEMORY.md](MEMORY.md) — the ten ownership rules and how each is verified.

## License

MIT.
