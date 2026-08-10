---
title: velo
description: "A pure-Zig web framework built on Zig 0.16's std.Io — HTTP/1.1, HTTP/2 and HTTP/3 over a pluggable QUIC transport, TLS 1.3 with ALPN, WebSocket. Echo-style Context plus Axum-style comptime extractors. Every bound declared, zero heap allocation on the request hot path (TigerStyle). Pre-1.0 — pin a tag."
license: MIT
author: blue-blaze
author_github: blue-blaze
repository: https://github.com/blue-blaze/velo
keywords:
  - async
  - http-server
  - http2
  - http3
  - quic
  - tls
  - web-framework
  - websocket
date: 2026-08-10
category: networking
updated_at: 2026-08-10T05:54:54+00:00
last_sync: 2026-08-10T05:54:54Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/blue-blaze/velo/
---

# Velo

A production-grade, **pure-Zig (0.16.x, with 0.17 on a branch)** web framework, targeting feature
parity with Rust's [Axum](https://github.com/tokio-rs/axum) and Go's
[Echo](https://github.com/labstack/echo). Velo embraces Zig 0.16's `std.Io`
async model and is built to the [Zig Style Guide](https://ziglang.org/documentation/master/#Style-Guide)
and [TigerStyle](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md).

> **Status:** v1 (HTTP/1.1) and v1.1 are implemented and tested. **HTTP/2**
> (pure-Zig framing + HPACK + Huffman), **TLS 1.3** (ALPN), and **HTTP/3** all
> work end-to-end. HTTP/3 uses a **pluggable QUIC backend**: the default
> (`-Dquic=openssl`) runs Velo's HTTP/3 layer over OpenSSL's QUIC transport
> (loopback-verified), while `-Dquic=zig` selects Velo's experimental
> self-hosted QUIC transport (see [Roadmap](#roadmap)).

## Why Velo

- **Colorblind async, on a choice of backends.** Built on `std.Io`, so the same
  handler code runs over a thread pool or an event loop with no function coloring
  and no rewrites. Backend selection lives behind `velo.Io` and no application
  names a backend: `-Dreactor` selects Velo's own kqueue reactor (one fiber per
  connection), `-Dzio` selects [zio](https://github.com/lalinsky/zio) (a
  third-party `std.Io` implementation over io_uring/epoll/kqueue/IOCP), and the
  portable threaded backend is the verified default. Both fiber backends cut 515
  OS threads to 9 and per-connection memory from 97 KB to 64 KB. `-Devented`
  wires up upstream's `std.Io.Evented`, which has no working networking in any
  released Zig — the measured reason both of the others exist, in
  [Backends & conformance](#backends--conformance).
- **Two APIs, one runtime.** An Echo-style explicit `Context` API for
  approachability, plus Axum-style comptime **extractors** for type-safe,
  zero-overhead handlers — and they interoperate.
- **One app, every transport.** A single `App` (routes + middleware + `Context`)
  is served unchanged over cleartext HTTP/1.1 + h2c (`serve`), TLS with ALPN
  HTTP/2 or HTTP/1.1 (`serveTls`), or HTTP/3 over QUIC (`serveHttp3`).
- **Bounded by design (TigerStyle).** Every buffer, queue, and pool has a fixed
  upper bound declared in `src/limits.zig`. The request hot path performs **zero
  heap allocation** (per-connection buffers live on task stacks; per-request
  scratch is a fixed arena). Parsers are non-recursive, bounded state machines.
  [`docs/MEMORY.md`](docs/MEMORY.md) is the counterpart for *your* code: what the
  process, connection and request tiers cost, when `ctx.arena` is the right place for
  data and when it is not, and what each bound does when it is reached.
- **Safety first.** Request-smuggling defenses, path-traversal protection,
  strict header/URI limits, and fuzz-tested parsers.

## Using Velo in your project

```sh
zig fetch --save git+https://github.com/blue-blaze/velo.git#<tag>
```

```zig
const velo_dep = b.dependency("velo", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("velo", velo_dep.module("velo"));
```

That is the whole setup: the default build is pure Zig with no system dependencies,
and the entire public API is reachable through `@import("velo")`. TLS and HTTP/3 are
opt-in build options you forward through the same `b.dependency` call.

Velo is **pre-1.0**, so pin a tag or a commit rather than a branch.
[`docs/VERSIONING.md`](docs/VERSIONING.md) states what is already stable, what may
still move, and the conditions for 1.0. That claim is not left to good intentions:
[`tools/consume-check.sh`](tools/consume-check.sh) builds and tests a throwaway
consumer project against Velo on every CI run, as both a path dependency and a
fetched archive.

That checks *packaging*, not API surface — a generated consumer imports a handful of
names and cannot notice a signature change. [`tools/downstream-check.sh`](tools/downstream-check.sh)
covers the other half by building a real one: [zig-mcp-sdk](https://modelcontextprotocol.io),
a Model Context Protocol implementation whose Streamable HTTP transport is built on
Velo's HTTP server and client, with its own suite of ~690 tests. It runs against a local
checkout beside the repository and does nothing when there is none, so it stays out of
CI rather than becoming a step that can only pass.

It earns its place: reverting the ALPN parameter recently added to
`tls.ClientContext.init` leaves Velo entirely green and breaks that consumer. And it does
so only in the consumer's **TLS** build — its default build passes, because the call sits
behind comptime gating — which is why the script builds both.

## Quick start

Requires Zig **0.16.0**. Velo pins this release deliberately: `std.Io` is still
evolving upstream and several `std` APIs moved within the 0.16 cycle. The exact
dependency surface, the breakages already absorbed, and the CI drift detector
are documented in [`docs/ZIG_VERSION.md`](docs/ZIG_VERSION.md).

**Zig 0.17 is adapted on the `zig-0.17` branch**, against `master` since 0.17 is not
released yet. One source tree builds on both releases — every condition is a comptime feature
test rather than a version comparison — and the default, `-Devented`, `-Dreactor`, `-Dtls` and
`-Dtls -Dquic=zig` suites all pass on it. `-Dzio` does not, and not because of Velo: the
dependency is pinned at 0.16.0 and its own source still uses `**`, which 0.17 removed from the
language. The branch also absorbed `@cImport`'s removal by moving C interop into the build
graph. Details and the full list are in [`docs/ZIG_VERSION.md`](docs/ZIG_VERSION.md).

```sh
zig build test        # run the unit + fuzz test suite
zig build fmt         # check formatting
zig build run-hello   # start the hello server on :8080
# then: curl http://127.0.0.1:8080/
```

### Minimal server

```zig
const velo = @import("velo");

pub fn main() !void {
    var app: velo.App(void) = undefined;
    app.init({});
    try app.get("/", hello);
    try app.listen(8080); // owns a runtime, handles Ctrl-C, binds loopback
}

fn hello(ctx: *velo.Context) !void {
    try ctx.text(.ok, "Hello, Velo");
}
```

`listen` is a composition of public parts, not a privileged path: it creates a
`Runtime`, resolves the address, installs signal handlers so Ctrl-C drains
in-flight requests, and blocks. When you need the runtime yourself — background
tasks, shared subsystems, your own shutdown — use `serve` instead:

```zig
var rt = try velo.Runtime.init(std.heap.page_allocator, .{});
defer rt.deinit();
var addr = try velo.net.Address.parse("127.0.0.1", 8080);
try app.serve(rt.io(), &addr, .{});
```

It binds `127.0.0.1` by default. That is deliberate — Velo adds no authentication
of its own, so a first experiment should not be reachable from the network before
it has any. `listenOn("0.0.0.0", port, .{})` opts out explicitly.

### Extractors (Axum-style)

```zig
const UserPath = struct { id: u32 };

fn showUser(ctx: *velo.Context, p: velo.Path(UserPath)) !void {
    try ctx.sendJson(.ok, .{ .user_id = p.value.id });
}

// register with the comptime adapter:
try app.get("/users/:id", velo.handler(showUser));
```

### Middleware (onion model)

```zig
fn auth(ctx: *velo.Context, next: velo.http.context.Next) !void {
    if (ctx.header("authorization") == null) {
        ctx.setStatus(.unauthorized);
        return; // short-circuit: do not call next
    }
    try next.run(ctx); // run inner layers + handler
}

try app.use(auth);
```

### Examples by scenario

[`examples/`](examples/) has one runnable program per scenario, each with `curl`
commands in its header and comments explaining *why*, not just what — enough to
get productive without opening the reference:

| | |
|---|---|
| [`hello`](examples/hello.zig) | the smallest useful server |
| [`routing`](examples/routing.zig) | params, wildcards, groups, automatic HEAD/OPTIONS/405 |
| [`json_api`](examples/json_api.zig) | extractors and error→status mapping |
| [`state`](examples/state.zig) | typed application state |
| [`auth`](examples/auth.zig) | auth, CORS, security headers, rate limits, timeouts |
| [`upload`](examples/upload.zig) | forms, multipart, static files |
| [`streaming`](examples/streaming.zig) | chunked responses, SSE, WebSocket |
| [`db_streaming`](examples/db_streaming.zig) | a result set whose size you do not control |
| [`sessions`](examples/sessions.zig) | cookies, signed cookies, server-side sessions |
| [`observability`](examples/observability.zig) | logs, metrics, tracing, OTLP |
| [`client`](examples/client.zig) | the HTTP client and its connection pool |
| [`x402`](examples/x402.zig) | charging for a request with the x402 payment protocol |
| [`api`](examples/api.zig) | most of the above in one app |

See [`examples/README.md`](examples/README.md) for the index, ports, and the
`listen`-versus-`serve` guidance. Full API documentation lives in
[`docs/API.md`](docs/API.md), and the memory model — including which allocator
application code should reach for — in [`docs/MEMORY.md`](docs/MEMORY.md).

## Features (v1)

- HTTP/1.1: bounded parser (chunked + content-length), keep-alive, correct
  response framing. **Production hardening:** a `Date` response header
  (RFC 9110 §6.6.1), `Host` validation (RFC 9112 §3.2 — a missing or duplicated
  `Host` on HTTP/1.1 is a `400`, as is a duplicated `Content-Length`),
  `Expect: 100-continue` (interim `100`, or `417` for an expectation we do not
  implement), and **connection timeouts** (`408`) bounding both the request head
  (also the keep-alive idle window) and the body-consuming phase — slowloris
  protection, on by default via `server.Timeouts`, and applied to the HTTP/2
  frame loop as well so h2c cannot bypass it.
- Radix-trie router: static / `:param` / `*wildcard`, priority matching.
  Route groups (`app.group(prefix, middleware)`) share a path prefix and
  middleware across a set of routes. Method-aware (RFC 9110): a path matched
  with an unregistered method returns **405 Method Not Allowed** with an
  `Allow` header; **HEAD** is auto-served by the matching `GET` handler (body
  suppressed, headers/`Content-Length` intact); **OPTIONS** is auto-answered
  (`204` + `Allow`). Explicitly registered `HEAD`/`OPTIONS` routes take
  precedence over the automatic behavior.
- Middleware onion with `next()` semantics and error propagation. Global
  (`app.use`), per-route, and per-group middleware compose uniformly. A
  handler or middleware error is mapped to **500** at the dispatcher, so one
  failing request never tears down the (keep-alive) connection. Built-in
  CORS (`velo.middleware.cors(.{...})`), gzip response compression
  (`velo.middleware.gzip(.{...})`), a per-request timeout
  (`velo.middleware.timeout(ms)`, cancels I/O-bound handlers → `503`),
  secure response headers (`velo.middleware.secure(.{...})`: HSTS,
  `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, CSP), a
  request body-size limit (`velo.middleware.bodyLimit(max)` → `413`),
  request-id propagation (`velo.middleware.requestId(.{})`), HTTP Basic/Bearer
  auth (`velo.middleware.basicAuth`/`bearerAuth`, constant-time credential
  compare → `401`), and a token-bucket rate limiter
  (`velo.middleware.rateLimiter` + `RateLimiter` → `429`), a per-client
  (peer-IP) rate limiter (`velo.middleware.clientRateLimiter` +
  `ClientRateLimiter`, bounded key table → `429`), CSRF protection
  (`velo.middleware.csrf(.{...})`, double-submit cookie → `403`), and API-key
  auth (`velo.middleware.keyAuth(.{...})`, header or query, constant-time →
  `401`), and a `Cache-Control` header builder
  (`velo.middleware.cacheControl(.{...})`, e.g. `max-age`/`immutable`/`no-store`)
  — all comptime-built with zero runtime allocation.
- **Error → response convention.** Handlers return `anyerror!void`, and a
  returned error is mapped to a status instead of a blanket `500`: semantic
  errors (`error.NotFound`, `error.BadRequest`, `error.Conflict`, …) become
  their matching code, framework errors with unambiguous meaning map too
  (extractor `MissingField` → `400`, `PayloadTooLarge` → `413`, a malformed
  JSON body → `400`), and anything unrecognized stays `500` so real bugs are
  never masked as client errors. Add
  `velo.middleware.problemJson(.{})` to also emit RFC 9457
  `application/problem+json` bodies — for both returned errors and error
  statuses set by inner middleware (401/413/429), preserving their headers.
- **Streaming responses** (`ctx.stream(status, content_type, func, user)`): for a
  body whose length is not known up front, the handler hands over a *producer* and
  each chunk it writes is framed by the active protocol — chunked
  transfer-encoding on HTTP/1.1, DATA frames on HTTP/2 and HTTP/3. Nothing is
  buffered, keep-alive is preserved (unlike the connection-takeover SSE path), and
  a producer error deliberately omits the terminator so the peer sees an
  incomplete response rather than a truncated one that looks complete.
- **Streaming uploads**: a request body declared larger than the per-stream buffer
  is delivered to the handler as it arrives (HTTP/1.1 always was; HTTP/2 now is
  too), with receive-window credit returned as it is consumed — without that half
  of flow control an upload stalls once the peer's initial window is spent. Credit
  is returned for buffered bodies as well, which is a subtler version of the same
  bug: HTTP/2's connection-level window is shared by every stream and only stream 0
  WINDOW_UPDATEs replenish it, so a long-lived connection carrying many *small*
  uploads used to stall after ~64 KB of aggregate body regardless of request count.
- **Consistent response headers across transports.** `Server` and a derived
  `Content-Length` are emitted on HTTP/1.1, HTTP/2 *and* HTTP/3 from one shared
  decision (`Response.derivedContentLength`). They used to be added only by the
  HTTP/1.1 encoder: legal on HTTP/2 and HTTP/3, where DATA frames delimit the body,
  but it made a single app answer differently depending on the transport and left
  clients unable to show download progress. The length is omitted exactly where it
  would be a contradiction — a streaming body (unknown by construction), a
  connection upgrade, a body-forbidden status (204/304) — and a handler's explicit
  value is never overridden. A HEAD response still carries the length it would have
  sent, which is the point of HEAD.
- Redirects: `ctx.redirect(status, location)` (301/302/303/307/308).
- Responses: `ctx.text` / `ctx.textf` / `ctx.html` / `ctx.sendJson`, plus
  **Server-Sent Events** (`ctx.sse(stream, user)` streams `data:`/`event:`/
  comment frames over the connection-takeover path).
- **HTTP/2 client** (`velo.http2.client`): the other half of the HTTP/2 work. The
  frame layer is symmetric by construction and HPACK is the same algorithm in both
  directions, so what was missing was not protocol but *shape* —
  `src/http2/connection.zig` is built around accepting streams and dispatching
  handlers. `Connection` takes a `std.Io` reader/writer pair rather than a socket,
  which is what lets one implementation serve **h2c** (cleartext, prior knowledge) and
  **h2 over TLS**: `tls.ClientContext.init(verify, .prefer_h2)` offers `h2` via ALPN
  and the caller dispatches on what the server chose.

  It does connection setup, HPACK-compressed request headers (with static-table
  indexing, so a second request on the same connection is cheaper than the first),
  HEADERS/CONTINUATION splitting, DATA framing that **waits for flow-control credit**
  rather than overrunning the peer's window, receive-side WINDOW_UPDATEs at both the
  stream and connection level, and trailers. While awaiting a response it still
  answers PING, acknowledges SETTINGS, credits WINDOW_UPDATE and reports GOAWAY —
  a client that ignored those would hang against a *conforming* server.

  `request` occupies the connection for one round trip, so this gives up
  multiplexing and keeps HTTP/2's other benefits. That is a stated limit, not an
  oversight: overlapping streams need a reader task owning the connection and a
  per-stream mailbox, which is a different API (async handles, not a blocking call)
  built on exactly this frame loop.

  Verified by round trips against Velo's own server — the one that scores 145/146 on
  h2spec — over a real socket for h2c and over TLS with ALPN, plus canned-frame tests
  for the cases Velo's server does not produce. Two of those tests were
  negative-verified: dropping the request-header lowercasing makes Velo's server
  `RST_STREAM` the request, and treating a trailer block as a second head turns every
  trailered response into an error.
- HTTP client (`velo.http.client`): a minimal `std.Io` HTTP/1.1 client with DNS
  resolution and chunked decoding, for server-to-server calls. `Client` keeps a
  **bounded pool of reused connections** (keep-alive, LRU eviction, one retry when
  a server closed an idle connection); `get`/`request` remain available for a
  one-shot connection. Reuse required reading a *framed* response rather than
  reading to end of stream — the latter forces every request to ask the server to
  close. `https://` works when built with `-Dtls` (reusing the OpenSSL layer for
  the handshake) but is not pooled, for a documented reason.
- `Context` API + comptime extractors: `Query(T)`, `Path(T)`, `Json(T)`,
  `Form(T)` (urlencoded body), `Multipart`, `Cookie(name)`, `Body` (raw bytes),
  `State(T)`, `Header(name)`. Query values and path params are percent-decoded
  (`query` also maps `+` to space); `queryRaw` returns the undecoded value.
  The peer (client) address is exposed via `ctx.peer()` (HTTP/1.1, HTTP/2, and
  the self-hosted HTTP/3 transport).
- Cookies: read request cookies with `ctx.cookie(name)`; set them with
  `ctx.setCookie(.{ .name, .value, .path, .max_age, .http_only, .secure,
  .same_site })` (appends a `Set-Cookie` per call). **Signed cookies**
  (tamper-proof via HMAC-SHA256) are available with
  `ctx.setSignedCookie(secret, cookie)` / `ctx.signedCookie(secret, name)` —
  the foundation for sessions and remember-me tokens (integrity, not secrecy).
- **Sessions** (`velo.http.session.Store(Data, capacity)`): server-side session
  state keyed by an opaque, signed, `HttpOnly` session id, so the payload never
  reaches the client and logout invalidates immediately. The store is a fixed
  slot table (no heap, no growth) that evicts the entry closest to expiry when
  full, uses value semantics (`load` copies out, `save` copies in) so a slot can
  never be evicted from under a handler, and slides the idle deadline on every
  load. Session ids come from a ChaCha CSPRNG seeded from the OS; if that entropy
  is unavailable `save` fails rather than falling back to a guessable id.
- Bodies: JSON (`std.json`), `application/x-www-form-urlencoded`,
  `multipart/form-data` (with file fields).
- Static files: zero-copy `sendFile`, HTTP Range, ETag/If-None-Match, MIME,
  path-traversal protection. File bodies are **streamed on every transport**:
  HTTP/1.1 hands the descriptor to `sendFile`, while HTTP/2 and HTTP/3 (which must
  frame the bytes) read it in bounded chunks. This was a bug worth calling out —
  H2 used to buffer the file into the per-request arena, so a file larger than
  `limits.request_body_bytes_max` was delivered *truncated with END_STREAM* and no
  error for the client to notice, and H3 sent an empty body. Both are now
  regression-tested.
- WebSocket: RFC 6455 handshake + frame codec (masking, fragmentation,
  ping/pong/close), bounded messages.
- **Global middleware runs for unmatched requests too.** A 404 or 405 used to
  return before the middleware chain, so unmatched requests were invisible to the
  access log and the metrics — precisely what you look for when a client
  integration is wrong — and carried none of the security or CORS headers every
  other response got. A 404 a browser cannot read because the CORS header is
  missing is a 404 the developer on the other end cannot diagnose. Relatedly, a
  handler that *returns an error* is now recorded with the status the client
  actually receives (`error.NotFound` → 404, unrecognized → 500) rather than being
  skipped by the observability layers or, in the OTLP span, recorded as the 200 the
  response still held while unwinding.
- Observability: structured access logs (with client IP), Prometheus metrics,
  W3C `traceparent` propagation, and **OTLP trace export**
  (`velo.otlp.Exporter` + `velo.otlp.tracing`) — one server span per request,
  inheriting the incoming trace context, POSTed to a collector as OTLP/HTTP+JSON.
  Propagating `traceparent` only lets *someone else* correlate the request; this
  is what makes Velo's own spans show up. The span buffer is fixed-size and drops
  (counting the drops) when full, because telemetry must never be the reason a
  traffic spike takes the process down.
- Lifecycle: configuration, graceful shutdown (drains in-flight requests),
  POSIX signal handling.
- **x402 payments** (`velo.x402`): the server half of the
  [x402](https://x402.org) protocol, which activates `402 Payment Required` so a
  client — usually an autonomous agent, with nobody to fill in a signup form — can
  pay per request instead of holding an API key. `velo.x402.required(.{...})` is a
  middleware: an unpaid request is answered with machine-readable terms in the
  `PAYMENT-REQUIRED` header and body, a retry carrying `PAYMENT-SIGNATURE` is
  verified and settled, and the receipt comes back in `PAYMENT-RESPONSE`.

  This is **pure Zig with no blockchain dependency**: the signature and on-chain
  work belongs to a *facilitator*, which is itself an HTTP service, so Velo needs
  only base64, JSON, and its own HTTP client. `Verifier.custom` is the extension
  point for local verification, prepaid credits, or a test double.

  The ordering is the part worth reviewing: verify → handler → settle → respond. A
  request is never handled before payment is verified, and — the property a payment
  layer must not get wrong — a handler that *fails* is never settled, so the service
  cannot take money for a response it did not deliver. Each of those three orderings
  has a regression test that was verified to fail when the ordering is broken.

## Features (v1.1)

- **HTTP/2** (pure Zig): frame layer, HPACK (static + bounded dynamic table +
  Huffman decode, and **static-table indexing on the encode side** — `:status: 200`
  is one byte instead of fourteen, cutting a typical response header block by ~32%;
  sensitive fields such as `set-cookie` are emitted *never-indexed* per RFC 7541
  §7.1.3 so an intermediary cannot park a credential in a shared compression
  context), stream handling. Works over cleartext h2c (prior knowledge)
  and over TLS via ALPN. Verified with `curl --http2-prior-knowledge`.
- **TLS 1.3** (opt-in, `-Dtls`): certificate loading, ALPN (`h2` + `http/1.1`),
  and `std.Io.Reader`/`Writer` adapters so the H1/H2 handlers run over TLS
  unchanged. Backed by a system `libssl` (OpenSSL here; BoringSSL is a link-time
  swap via `-Dtls-prefix`). The default build stays pure-Zig and dependency-free.
- **HTTP/3**: Velo's HTTP/3 layer — QPACK (RFC 9204 static table + all
  static/literal field-line representations + Huffman) and the H3 message/frame
  layer — runs over a **pluggable QUIC transport**:
  - `-Dquic=openssl` (default): OpenSSL 3.5+ owns the QUIC transport (handshake,
    packet protection, loss recovery, streams); Velo runs HTTP/3 on the QUIC
    streams. Verified end-to-end with a Velo-vs-Velo QUIC loopback **and against
    an independent third-party client** ([aioquic](https://github.com/aiortc/aioquic)):
    ALPN `h3` is negotiated and requests return `200` over a real UDP socket
    (see [`interop/`](interop/)).
  - `-Dquic=zig` (experimental): Velo's self-hosted QUIC transport, using
    OpenSSL only for the TLS 1.3 handshake crypto via the QUIC-TLS callback API
    (`SSL_set_quic_tls_cbs`). It **serves HTTP/3 end-to-end over Velo's own
    transport** — TLS 1.3 handshake over AEAD + header-protected Initial/
    Handshake packets, then 1-RTT (short-header) packets carrying QUIC STREAM
    frames — and has been hardened toward production with **receive-timeout
    (PTO) driven retransmission** for both handshake and 1-RTT loss, a **NewReno
    congestion controller**, **connection demultiplexing by connection ID**,
    RFC 9114 **control/SETTINGS/QPACK stream setup**, **connection- and
    stream-level flow control** (MAX_DATA / MAX_STREAM_DATA credit, *and* enforcement
    in both directions: a peer that sends past a limit we advertised is met with
    CONNECTION_CLOSE(FLOW_CONTROL_ERROR) rather than having the overrun silently
    dropped, which bounds memory but leaves a misbehaving peer connected),
    **RFC 9000 §8 anti-amplification** (before the peer's address is validated the
    server sends at most 3x what it received — without that cap a QUIC server is a
    reflector that multiplies a spoofed-source packet into an attack on a third
    party),
    **connection migration** with PATH_CHALLENGE/PATH_RESPONSE path validation,
    and **many requests per connection**. **TLS session resumption works over
    the transport** — the server's NewSessionTicket is carried as post-handshake
    CRYPTO and processed via `SSL_read_ex` (which, unlike `SSL_do_handshake`,
    drives post-handshake messages), and a resumed connection is confirmed via
    `SSL_session_reused`. **Server-side 0-RTT** is in place: the mux loop issues
    a NewSessionTicket as post-handshake 1-RTT CRYPTO so a peer can persist it —
    verified against aioquic, which receives the ticket (early-data capability
    advertised), **resumes the session, and reports `early_data_accepted`** — and
    on a resumed connection the Velo server **yields the EARLY read secret** (so
    `recv` decrypts inbound 0-RTT packets and buffers the early request; the
    decrypt path is unit-tested). It now **interoperates with two independent
    third-party clients** ([aioquic](https://github.com/aiortc/aioquic) and
    [quic-go](https://github.com/quic-go/quic-go), the latter exercising
    variable-length connection IDs): the QUIC + TLS 1.3 handshake completes and
    `GET` requests return `200` over a real UDP socket, single and concurrent
    (see [`interop/`](interop/)). Remaining before parity: on-wire 0-RTT with
    aioquic is not demonstrated end-to-end (aioquic finishes the loopback
    handshake before using its 0-RTT window, sending as 1-RTT); the client
    *offering* early data from Velo is still blocked (OpenSSL's QUIC-TLS callback
    path declines to yield the *client* early secret even with an
    early-data-capable ticket); and at-scale real-network validation, for which [`interop/quic-network.sh`](interop/quic-network.sh) is now the harness: it runs the two sides on separate hosts (the only way to exercise real PMTU, NAT rebinding and WAN congestion), and its single-host mode — over this machine's LAN interface rather than loopback — passes 4/4 clean and 8/8 under 5% loss with 20 ms delay and 15 ms jitter. So the
    **default and supported serving route remains Path A**.

Enable TLS and run the HTTPS demo:

```sh
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem \
  -days 365 -nodes -subj "/CN=localhost"
zig build -Dtls run-tls   # https://127.0.0.1:8443  (ALPN: h2, http/1.1)
```

## Architecture

```
Application  handlers · router DSL · middleware
    |
Core         Router (radix trie) · Context · comptime Extractors · codecs · observability
    |
Protocol     protocol-agnostic Request/Response · HTTP/1.1 (state machine)
    |
Transport    TCP listener/connection  (TLS · HTTP/2 · HTTP/3 → v1.1)
    |
velo.Io      abstraction over std.Io  (backends: Threaded · io_uring/kqueue/IOCP)
```

The `Request`/`Response` types are protocol-agnostic so routing, middleware,
and handlers are unchanged when HTTP/2 and HTTP/3 land. Source layout:

```
src/
  velo.zig            public API re-exports
  io.zig              velo.Io abstraction + Runtime (backend selection)
  app.zig             App: routing + middleware + serve
  extractor.zig       comptime extractors + handler adapter
  lifecycle.zig       Config, graceful shutdown, signals
  limits.zig          all upper bounds (TigerStyle)
  assert.zig          assertion helpers
  net/listener.zig    TCP listener, accept loop, backpressure
  http/               method, status, headers, request, response,
                      parser, encoder, server, router, context,
                      static, websocket
  http2/              frame, hpack (+ huffman), connection
  quic/               varint, packet, udp        (HTTP/3 foundation)
  http3/              frame
  tls/                openssl (opt-in, -Dtls)
  codec/              form (urlencoded), multipart
  middleware/         observability (log, metrics, trace)
examples/             hello, api (showcase), bench, tls
bench/                wrk scripts + methodology
```

## Testing

### Testing *your* application

`velo.testing` drives your `App` through the real HTTP/1.1 stack — the same parser,
router, middleware chain and encoder that serve production traffic — over in-memory
buffers. No sockets, no ports, no sleeps, and no mocks, so a test fails for the
reasons production would:

```zig
test "the users endpoint" {
    var app: velo.App(void) = undefined;
    app.init({});
    try app.get("/users/:id", showUser);

    var t = try velo.testing.harness(std.testing.allocator, &app);
    defer t.deinit();

    const res = try t.get("/users/42");
    try res.expectStatus(.ok);
    try res.expectContentType("application/json");
    try res.expectBodyContains("\"id\":42");
}
```

Cookies are carried between calls by a bounded jar, so a login → authenticated
request → logout flow reads like the flow it tests rather than like plumbing. A
chunked response is decoded before assertions, and `expectContentType` compares the
media type without the `charset` parameter — small things, but they decide whether
tests get written. [`examples/testing_example.zig`](examples/testing_example.zig) is
a complete, runnable test file to copy from (`zig build test-example`).

The harness's own tests include a case that drives every assertion helper into its
failing branch, because a test tool that cannot fail is worse than no test tool.

### Testing Velo itself

```sh
zig build test   # unit tests + deterministic fuzz tests (parser, ws frames)
```

Tests use `std.testing.allocator`, which fails on leaks. The parser and
WebSocket frame reader are fuzzed against thousands of random and truncated
inputs to guarantee they never panic.

**Coverage-guided fuzzing.** Beyond those deterministic pseudo-fuzz tests,
[`src/fuzz.zig`](src/fuzz.zig) defines ten targets driven by Zig's built-in
fuzzer — the HTTP/1.1 request head parser, the client's response parser, HPACK,
the HTTP/2 frame header, QPACK field sections, the QPACK *encoder stream*, QUIC
varints + HTTP/3 frame headers, the WebSocket frame reader, and the
urlencoded/multipart body codecs:

```sh
zig build fuzz                                  # replay the seed corpus (fast)
zig build fuzz -Dfuzz-filter=QPACK --fuzz=200000  # coverage-guided
```

Every target seeds a corpus of valid inputs, which both gives the fuzzer a
reachable starting point and makes `zig build fuzz` a fast regression check on
inputs that previously crashed something.

This was worth doing for a concrete reason: within minutes the fuzzer found a
**remotely triggerable panic in the QPACK decoder** that the deterministic tests
had never reached. HPACK's integer decoder had been hardened against over-long
encodings after an earlier fuzz finding; QPACK implements the same algorithm but
had kept the naive version, where the shift counter (a `u6`) overflowed *itself*
before the range check could reject the input. Random bytes essentially never
produce the required shape — an all-ones prefix followed by ten zero-payload
continuation bytes — but coverage feedback walks straight to it. Fixed, with a
regression test that panics on the old code.

Note that this step uses a vendored test runner, because Zig 0.16.0's own runner
does not compile in fuzz mode; see [`tools/README.md`](tools/README.md) for the
reproduction and the condition for deleting it.

**Soak / leak verification.** `zig build test` includes a sustained-load test
(`src/soak_test.zig`) that drives many requests over concurrent, *reused*
connections through the real socket path and then checks what a leak would
break: outstanding allocations (the testing allocator fails on any), connection
slots (a post-soak probe needs a returned permit), and tasks (teardown joins
them). For the process-level view over a longer horizon —
resident memory and file descriptors — [`bench/soak.sh`](bench/soak.sh) drives a
real server and gates on RSS/fd growth after warm-up; measured here, fds stay
flat across 96 000 requests and RSS plateaus (see
[`bench/README.md`](bench/README.md)).

### Continuous integration

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs ten jobs on every
push and pull request (plus a nightly one, below): a dependency-free **pure-Zig** job (default + `-Devented`
builds + `zig build fmt`) on Linux — `-Devented` compiles the evented wiring and,
because `std.Io.Evented` is currently gated off in 0.16 (see below), cleanly
falls back to the threaded backend; an informational **benchmark** job
([`bench/regression.sh`](bench/regression.sh), `continue-on-error`) that gates
gross throughput regressions; a **TLS/QUIC** job on macOS (needs OpenSSL 3.5+
for QUIC, so it uses Homebrew's `openssl@3`) covering `-Dtls` and
`-Dtls -Dquic=zig`; a **TLS/QUIC-on-Linux** job that runs the same suite on
Ubuntu; and an **interop** job that runs two external HTTP/3 clients (aioquic
and quic-go) against both QUIC backends — see [`interop/`](interop/); plus an
informational **soak** job that gates on RSS/fd growth under sustained load
([`bench/soak.sh`](bench/soak.sh)); plus an
**`zig-drift`** job that builds the pure-Zig core against Zig `master` to surface
upstream `std`/`std.Io` API changes early. It **reports** rather than gates
([`tools/zig-drift-report.sh`](tools/zig-drift-report.sh)): drift is the expected state
when a project pins one Zig release, so the job writes what moved to the run summary and
succeeds having said so. It used to fail on drift, which made it permanently red and
therefore unread — and worse, its first fatal step hid the rest, because `build.zig` is
compiled before any build step runs and one changed `std.Build` API made every command
fail identically. So it also compiles the module *without* `build.zig`, which is the only
way to see Velo's own drift when the build script is what broke (see
[`docs/ZIG_VERSION.md`](docs/ZIG_VERSION.md)); an **upstream-probes** job that
reproduces each upstream defect Velo works around and fails when one *stops*
reproducing, because a workaround that outlives its bug is dead code nobody
notices (see [`docs/UPSTREAM.md`](docs/UPSTREAM.md)); and a **fuzz-corpus** job that
replays every fuzz target's seed corpus. Coverage-guided fuzzing needs wall-clock
time, so it is a separate **nightly** job that rotates through the ten targets
(the fuzzer works on one at a time) and uploads the offending input as an artifact
if a target crashes.
GitHub's Ubuntu images still ship OpenSSL 3.0 (too old for the QUIC-TLS callback
API), so the Linux job **builds OpenSSL 3.5 from source using only Zig as the C
toolchain** (`zig cc`/`zig ar`, via
[`interop/build-openssl-zigcc.sh`](interop/build-openssl-zigcc.sh), cached across
runs) — no system C toolchain needed. That build + the `-Dtls -Dquic=zig` suite
(177/178) was verified locally in a Debian (glibc 2.36) container.

## Benchmarks

See [`bench/README.md`](bench/README.md). Two views:

**Server-limited hot path** (in-process, single core, ReleaseFast) — the CPU
cost of Velo's own request pipeline (parse → route → middleware → encode), with
no sockets so the number isolates framework overhead:

```sh
zig build -Doptimize=ReleaseFast run-bench_hotpath
```

| Scenario | req/s | ns/req |
|---|---:|---:|
| plaintext `GET /` | ~3.5 M | ~284 |
| json `GET /json` | ~2.8 M | ~361 |
| dynamic `GET /users/:id` | ~3.2 M | ~313 |
| plaintext + 2 middleware | ~2.2 M | ~447 |

**Against other frameworks** (real sockets, same machine, same load generator,
one server at a time — see [`bench/compare/`](bench/compare)):

**Throughput** needs the load generator out of the way first. At one request per
connection, a client's `write` + `read` syscalls cost more than "hello world" costs
any of these servers, so every framework lands within noise of the same number and
the rps column measures the *generator*. Pipelining (`loadgen -depth 64`) moves the
bottleneck back to the server, which is the only condition under which the column
means anything:

| 8 connections, depth 64 | rps | p50 | p99 | CPU/req | resident | threads |
|---|---:|---:|---:|---:|---:|---:|
| Velo (`-Dreactor`) | 458 662 | 15 µs | 80 µs | 1.43 µs | 6.4 MB | 9 |
| Velo (threaded) | 446 682 | 15 µs | 81 µs | 1.41 µs | 2.5 MB | 11 |
| Velo (`-Dzio`) | 442 598 | 15 µs | 85 µs | 1.68 µs | 3.6 MB | 9 |
| axum (Rust) | 310 694 | 20 µs | 126 µs | 8.72 µs | 3.6 MB | 9 |
| Echo (Go) | 102 221 | 78 µs | 136 µs | 27.16 µs | 21.0 MB | 14 |

**CPU per request** is the metric that survives a saturated client: server process
CPU time divided by requests served, so it is the same number whichever side is the
bottleneck. Velo is ~8x cheaper per request than axum here and ~25x cheaper than
Echo. That gap is the framework's own pipeline (parse → route → middleware → encode)
plus the syscalls it takes to deliver a response; the biggest single contributor on
Velo's side was learning to batch pipelined responses into one `sendmsg`.

**Binary size** is worth one line because it moved by two orders of magnitude. A
hello-world Velo server was **158 MB**; it is now **0.7 MB**. The pool of per-request
buffers is 148 MB of address space, and a four-byte free-list link with a
comptime-computed initial value every 148 KB was enough to keep the linker from
placing it in `.bss` — so the whole pool was emitted into the executable as file
content. Building the free list lazily instead leaves the array uninitialized, which
also stopped Linux from reading ahead on pool faults: 61 KB of resident memory per
connection became 7 KB.

**Memory and the tail** are what 512 connections measure. All four saturate the
generator here, so read the right-hand columns, not the rps:

| 512 connections, depth 1 | rps | p50 | p99 | resident | threads | KB/conn |
|---|---:|---:|---:|---:|---:|---:|
| Echo (Go) | 44 862 | 11.10 ms | 16.26 ms | 34.2 MB | 16 | 27 |
| Velo (`-Dzio`) | 44 617 | 11.18 ms | 18.06 ms | 36.9 MB | 9 | 64 |
| axum (Rust) | 44 492 | 11.24 ms | 17.99 ms | 23.5 MB | 9 | 40 |
| Velo (`-Dreactor`) | 43 901 | 11.37 ms | 17.49 ms | 38.6 MB | 9 | 64 |
| Velo (threaded) | 40 926 | 12.19 ms | 18.76 ms | 51.5 MB | 515 | 97 |

`KB/conn` is the marginal cost, from the 64-to-512 delta.

The thread column used to be the honest remaining difference: on the threaded backend
Velo is one OS thread per connection, which cost 515 threads and ~97 KB per connection
against axum's 9 and ~39 KB. It showed up as memory and as the tail, not as throughput.

Either fiber backend removes it, and — worth noting, because it is the kind of thing
that gets attributed to the scheduler — they remove it *identically*: 64 KB per
connection on both. That number is the 16 KB pages Velo's connection frame touches, not
a property of the event loop underneath, so closing the remaining 1.6x against axum is
arithmetic on the frame rather than a change of concurrency model. Where the backends do
differ is the tail and the baseline: zio has the best p99 of the three and a 2.5 MB base
RSS against the reactor's 5.8 MB, because Velo's reactor preallocates a 16 384-entry
fiber table where zio grows on demand. See
[Backends & conformance](#backends--conformance) for why one of them is Velo's own code,
and for the conditions under which that file gets deleted.

### The same numbers on Linux

Every table above is macOS/aarch64. Measuring a second OS was worth doing on its own
terms, and it also found a defect the first one hid — see
[Cross-platform, measured](#cross-platform-measured). Linux/aarch64, in a 2-core
container, so **read the columns against each other and not against the tables
above**:

| 4 connections, depth 64 | rps | p50 | p99 | CPU/req | resident | threads |
|---|---:|---:|---:|---:|---:|---:|
| Velo (threaded) | 232 653 | 7 µs | 113 µs | 1.38 µs | 3.1 MB | 9 |
| Velo (`-Dzio`, io_uring) | 201 152 | 12 µs | 92 µs | 1.68 µs | 2.1 MB | 3 |
| Velo (`-Dzio`, epoll) | 200 755 | 16 µs | 67 µs | 1.92 µs | 1.5 MB | 3 |
| Echo (Go) | 95 437 | 34 µs | 145 µs | 11.09 µs | 11.5 MB | 8 |

| 256 connections, depth 1 | rps | p99 | resident | threads | KB/conn |
|---|---:|---:|---:|---:|---:|
| Velo (`-Dzio`, io_uring) | 109 343 | 10.11 ms | 10.2 MB | 3 | 32 |
| Velo (`-Dzio`, epoll) | 100 867 | 9.43 ms | 9.8 MB | 3 | 33 |
| Velo (threaded) | 101 281 | 40.16 ms | 76.1 MB | 259 | 292 |
| Echo (Go) | 56 016 | 15.84 ms | 16.8 MB | 9 | 23 |

On a fiber backend Velo now costs **32 KB per connection here and 10.2 MB in total at
256 connections** — less total memory than Echo, which has the smaller per-connection
figure. Getting there was one change, and not the one that looked obvious: the
per-request buffer pool used to be *initialized* data, so its pages were file-backed,
and Linux reads ahead on a file-backed fault. One touched page brought in a
neighbourhood. Making the pool `.bss` took pool residency from 61 KB per connection to
**7 KB** and the binary from 152 MB to 4.5 MB — see
[Benchmarks](#benchmarks)'s note on binary size.

The threaded backend's 292 KB per connection is **not** Velo's memory, and chasing it
as if it were would have been wasted work. 256 KB of it is one `std` default meeting
one `std` bug: `std.options.signal_stack_size` is 256 KB and lives in a `threadlocal`,
and Zig's Linux thread spawn `@memset`s the whole thread-local area even though it was
just handed zero-filled pages by `mmap`. So every thread — every *connection*, on this
backend — makes 256 KB resident. Adding one line to an application's root module,
`pub const std_options: std.Options = .{ .signal_stack_size = null };`, takes the
measured cost from 292 KB per connection to roughly what the fiber backends cost. Details, the probe, and the tradeoff (a stack trace on stack
overflow) are in [`docs/UPSTREAM.md`](docs/UPSTREAM.md) §6. macOS pays ~15 KB for the
same default, one page, which is the second thing measuring a second OS turned up.

The CPU-per-request ratio against Echo survives the change of kernel, which is the
point of measuring it: ~8x on Linux, ~19x on macOS, same order either way.

Two things differ from macOS. The fiber backend's advantage is *larger* here — on two
cores, 259 threads cost a p99 of 32 ms against zio's 10.9, and 90 MB against 29 — and
io_uring is not the fastest option at low concurrency: epoll beats it on throughput at
depth 64 and loses to it on the tail at 256 connections. Neither is a large enough gap
to recommend one over the other without measuring your own workload, which is why
`-Dzio-backend=` exists.

**End-to-end** (real sockets, load-tested — client-bound on a single host):

```sh
zig build -Doptimize=ReleaseFast run-bench
bench/wrk.sh
```

## Cross-platform, measured

Velo's platform support used to be a claim inherited from its dependencies. It is now
partly a measurement, and this section says which parts are which, because the
difference turned out to matter.

**Linux/aarch64 — verified.** The full suite runs there: **328 passed / 9 skipped /
0 failed** on the threaded backend, the same on `-Dreactor` (whose own tests correctly
*skip*, since it is a kqueue reactor — a Linux build falls back rather than failing to
compile), and **330 / 9 / 0** on `-Dzio` with either event loop. `h2spec` scores the
same **145/146** as on macOS on all three, which is the useful part: the score is
unchanged across io_uring, epoll *and* kqueue, so it is measuring the HTTP/2
implementation rather than one I/O path. Throughput numbers are in
[Benchmarks](#benchmarks).

Getting there needed no Linux machine: `zig build test -Dtarget=aarch64-linux-musl`
produces a statically-linked ELF test binary that runs in any container, so a
second-platform check costs a cross-compile rather than a CI round trip.

**What measuring Linux found.** Two defects, neither of them small, and neither
visible from macOS.

The first was Velo's. **Velo never set `TCP_NODELAY`.** Nagle's algorithm holds a trailing partial segment until the peer
acknowledges what is already in flight, and Linux delays that acknowledgement by up to
40 ms — so as soon as a batch of pipelined responses crossed a segment boundary, the
server stalled. Measured at pipeline depth 64 on Linux: **1 459 rps, with a uniform
~44 ms per batch**, against 93 621 rps for the same binary at depth 1. The macOS
loopback path never exhibited it, which is exactly why one OS is not enough: every
benchmark in this README was run on the machine that hides it. With the option set,
the same case is **104 128 rps** — 71x — and the 512-connection macOS figures improved
about 10% as well.

It is on by default and it is not free: on macOS loopback at depth 64 it costs ~35%
more CPU per request (1.03 → 1.40 µs), because the kernel is no longer coalescing the
batch. That is the right trade — a 40 ms stall is a defect, 0.35 µs is a tuning
question — but it is a trade, so `ListenOptions.tcp_nodelay` exists for a deployment
that has measured its own link. Both states are regression-tested by reading the
option back off an accepted socket, on Linux and macOS.

**On Windows the option has no effect**, and finding that out took a wrong turn worth
recording. `std.posix.setsockopt` is a compile error there and `std.Io` exposes no
socket-option operation, so the fix looked like calling Winsock directly — which compiled,
shipped, and cannot work: `std.Io.Threaded` opens sockets on `\Device\Afd` via
`NtCreateFile`, so the handle is an NT file handle rather than a SOCKET registered with
the Winsock catalog, and `ws2_32` rejects it. The evidence is the readback test failing
with `GetSockOptFailed` on the Windows runner, which needs the same registration
`setsockopt` does. `std` has a private `setSocketOptionAfd` that does it properly. So the
Windows branch is now an explicit no-op that says why, the two readback tests skip there,
and closing the gap needs either an upstream `std.Io` socket-option operation or the AFD
ioctl reimplemented in Velo.

**The second was upstream's, and it was the larger number.** Velo's threaded backend
measured 337 KB of resident memory per connection on Linux against 97 KB on macOS. The
tempting reading — thread-per-connection is simply more expensive here — was wrong.
`std.options.signal_stack_size` defaults to 256 KB and is a `threadlocal`, and Zig's
Linux `std.Thread.spawn` calls `@memset(area, 0)` over the whole thread-local area
that `mmap` had just returned zero-filled. A large thread-local is free while its
pages stay untouched and a redundant memset is free over a small area; together they
make 256 KB resident per thread, which on this backend means per *connection*.
Removing it: 345 → **93 KB per connection**, the same as the fiber backends, which is
the measurement that proves the diagnosis. Velo cannot fix this from inside a library
— `std.options` belongs to an executable's root module — so it is documented with a
probe in [`docs/UPSTREAM.md`](docs/UPSTREAM.md) §6, along with the one-line remedy and
what it costs.

**A deployment note that follows from how zio works.** zio selects its event loop at
*compile* time, with no runtime fallback, and on Linux it defaults to io_uring —
which **Docker's default seccomp profile blocks**. So a `-Dzio` build that passes
everything on the host fails to start in an ordinary container. Two things address it:
`-Dzio-backend=epoll` builds the portable loop instead (verified: 330/339 under the
default profile, where io_uring gives 2 failures), and when the backend was chosen by
`.auto` rather than named by the caller, Velo logs the cause and the fix and falls back
to the threaded backend instead of refusing to serve. Naming a backend explicitly
still fails, because silently ignoring an explicit request is worse than not starting.

**Windows — verified.** `zig build test -Dtarget=x86_64-windows-gnu` succeeds with and
without `-Dzio`, and the suite now *runs* there too. CI's `windows` job covers the
threaded backend and zio's IOCP backend.

That sentence used to name `zig build -Dtarget=x86_64-windows-gnu`, and the difference is
the whole lesson. That command builds artifacts, and comptime gating means a platform's
code is analyzed only when something forces it — so it passed while two Windows paths did
not compile at all. The `windows` job found the first on its first run: `setNoDelay`'s
Winsock branch called `std.os.windows.ws2_32.setsockopt`, which does not exist in any Zig
release (0.16's `ws2_32` declares only types and constants, and there is no `setsockopt`
anywhere in `std` for Windows — it is now an `extern "ws2_32"` declaration here, with
`callconv(.winapi)`, which matters on 32-bit x86 where Winsock is `__stdcall`).

Building the *test* binary is what reaches that code, so `zig build test` now compiles
and links for a foreign target without trying to run it. One command later, that found
the second defect: `Io.net.Server.options` is `void` on POSIX and a struct on Windows, so
a test helper writing `.options = {}` could never have compiled there. A cross-platform
check that cannot be run in one command is a check that does not get run.

With those fixed the suite *runs* on Windows for the first time, and what it found is
recorded rather than summarised as "it hangs". Getting there took two additions, because a
timeout on its own names nothing: the suite is also run as a standalone binary, whose
runner prints each test as it starts, and
[`tools/probes/shutdown_unblocks_read.zig`](tools/probes/shutdown_unblocks_read.zig) tests
the one mechanism most likely to be missing.

Three results, in the order they matter:

1. **`shutdown` does not unblock a pending read on Windows.** The probe says so directly —
   no return within three seconds, against ~50 ms on macOS. That is what the reaper is
   built on, so the reaper does not work there; the read bounds now use the racing fallback
   on Windows instead, which the same run showed passing. `write_ms` has no fallback and
   stays inert. Both halves are in [Security notes](#security-notes).

   Worth recording how that was distinguished, because the first conclusion drawn was
   simply "the bounds do not work on Windows" and it was too strong. In the same run, three
   tests exercising the *fallback* path passed and two exercising the *reaper* path failed.
   One measurement covering five results is what separates a broken feature from a broken
   mechanism inside a working one.
2. **`zig build test-example` passes**, so the parser, router, middleware and encoder are
   fine and nothing about Velo is fundamentally broken on the platform.
3. **Two `TCP_NODELAY` tests failed for a reason unrelated to any of this.** They read the
   option back off an accepted socket, and the Windows branch of that helper was
   `return error.SkipZigTest` — which does not work from inside an `io.async` task whose
   handler collapses errors into a boolean, so the skip was lost and the test reported
   `GetSockOptFailed`. `std` has no `getsockopt` for Windows either, so it is now declared
   here the same way `setsockopt` is, and the option is genuinely read back on all three
   platforms.
4. **One test hangs for a reason none of the above explains**: `pipelined requests each get
   a response, batched into one write`. It is the next thing to characterise, and it is
   worth noting that it is a *write*-path test on the one platform where the write bound
   cannot fire.

**The suite now passes on Windows: 360 passed, 17 skipped, 0 failed** on the default
threaded backend, so the `windows` job gates like every other one. That took four rounds of
narrowing, and the sequence is the point — a timeout, then a per-test name, then a probe of
the one mechanism, then the twelve failures the fixed hang finally made visible. None of
those steps could have been skipped, and each was only obvious after the one before it.

Two platform gaps remain, both measured and both documented rather than quietly skipped:
`shutdown` does not unblock a pending read (above), and `ListenOptions.tcp_nodelay` has no
effect because `ws2_32` will not accept the AFD handles `std.Io` creates (see
[Benchmarks](#benchmarks)'s `TCP_NODELAY` note). Four tests skip on Windows for those two
reasons.

`-Dzio` on Windows is still `continue-on-error`, and what that tolerates is now located
rather than suspected: the loopback round trip **blocks** inside zio's IOCP backend. Getting
to that took eliminating two of Velo's own defects and one wrong method. A future awaited
only on success turned a read error into `panic: reached unreachable code` — a test defect
POSIX hid because the read never failed there. Awaiting it unconditionally replaced the panic
with a silent six-minute timeout, which was worse: `zig build` withholds a test binary's
stderr until the step ends, so the hang discarded the diagnostics written to explain it. Run
as an installed binary instead (`zig build test-bin`), stderr is live and the log reads
`12/368 ... loopback round trip...` followed by nothing — with no error from `accept`, the
server's read or its write, so the task is blocked rather than failing. And it is not the
`Server.options` the test hand-built for the accepted socket, a struct that exists only on
Windows and was therefore the obvious suspect: replacing it with the options `listen`
produced left the hang unchanged. That test skips there now, so the step exercises the rest
of the suite over IOCP.

## Security notes

- Example servers are **unauthenticated** and bind to loopback for local
  development. Add authentication / a reverse proxy before exposing them.
- Velo enforces strict bounds on request head size, header count, and body size,
  and rejects `Content-Length` + `Transfer-Encoding` combinations (smuggling),
  duplicated `Content-Length`, and a missing/duplicated `Host`.
- **Slowloris protection is on by default**, covering both request phases and
  both protocols: `server.Timeouts.head_ms` (15s) bounds delivery of a request
  head (and the keep-alive idle window), and `body_ms` (30s) bounds the phase
  that consumes the body — a complete head advertising a large
  `Content-Length` followed by a dribbled body is the variant a head-only bound
  misses. The same bounds apply to the **HTTP/2** frame loop, so h2c is not a way
  around them. On expiry HTTP/1.1 answers `408` and closes; HTTP/2 sends GOAWAY.
  Each variant is regression-tested over a real socket (silent client, partial
  head, stalled body, quiet h2c peer), and each test was verified to fail with
  the bound disabled.
- Both bounds are skipped when the bytes are already buffered, and when they do
  apply they are enforced by **one reaper task for the whole process**
  ([`src/http/reaper.zig`](src/http/reaper.zig)) rather than by racing each read
  against a timer.

  That distinction was expensive to learn. The bounds used to be a per-request
  `Io.Select` race, and this section previously claimed they "cost nothing
  measurable on the hot path (~286 ns/req vs ~284 ns/req)". That was true of the
  in-process microbenchmark and false of a real server: the harness has no sockets,
  so the read never blocks and the race never arms. Measured over real sockets
  against axum and Echo ([`bench/compare/`](bench/compare)), each arm of the race is
  an `io.async` task — an OS thread on the threaded backend — so a server was running
  ~3 threads per connection and losing **30% of its throughput with a p99 15x
  worse** (30 410 rps / 29 ms at 64 connections, versus 43 317 / 2.0 ms with the
  bounds off). With the reaper the bounds are on *and* the numbers are axum's
  (43 293 rps / 2.14 ms). A default-on security feature has to be cheap, or people
  turn it off.

  The same exercise found a real hole: the h2c prior-knowledge peek ran before any
  bound applied, so a client that connected and sent nothing held its connection slot
  indefinitely. The earlier slowloris tests all called `serveHttp1` directly and never
  reached that code. It is bounded now, and tested through the wiring production uses.

  Set `.timeouts = .disabled` if a proxy in front already bounds slow clients.
- **The reaper cannot work on Windows, so Windows uses the fallback instead.**
  The reaper breaks a stalled connection by calling `shutdown` on it, which POSIX
  guarantees returns a pending read. Winsock documents `shutdown` as affecting only
  *subsequent* calls, and
  [`tools/probes/shutdown_unblocks_read.zig`](tools/probes/shutdown_unblocks_read.zig)
  measures the consequence directly: the blocked read does not return within three
  seconds, where macOS takes ~50 ms.

  The read bounds still hold there, because the mechanism the reaper *replaced* still
  exists — one `Io.Select` per read, raced against a timer. `connectionLoop` selects it on
  Windows. It costs the 30% of throughput that motivated the reaper, and that trade is the
  right way round on a platform where the fast path silently does nothing: paying for a
  bound beats advertising one that cannot fire.

  **`write_ms` is the exception and stays inert on Windows.** It is armed only around the
  write, and only by the reaper; a blocked write has no per-read race to fall back to. So a
  peer that stops reading holds its connection slot there. `CancelIoEx` is the documented
  Windows mechanism for cancelling pending I/O and is what a fix would use.

  This split is measured, not reasoned: on Windows the three tests driving the fallback
  path pass — silent client, stalled mid-head, stalled mid-body, each answered with `408` —
  while the two driving the reaper path failed, which is what identified the mechanism as
  the thing at fault rather than the bounds.
- **Slow readers are bounded too, and now by default.** A peer that stops reading
  fills the kernel send buffer and blocks the flush forever, pinning the connection —
  the mirror image of a slow request, and the same denial of service. `write_ms`
  (30s) closes it.

  This section used to call it a known gap and ship it off by default, because
  bounding a write meant racing every response against a timer: there is no sound way
  to tell in advance whether a write will block, since the attack case is precisely a
  full send buffer. That reasoning was about the mechanism, not about the bound. The
  same reaper enforces this one — arming costs three atomic stores, and the measured
  cost of turning it on is **1.50 → 1.52 µs of CPU per request** at pipeline depth 64,
  inside the session noise.

  The one real difference from the read bounds is *which half* of the socket the
  reaper shuts down. `head_ms`/`body_ms` shut down the receive side, which is what
  lets a `408` still reach a client that has stopped talking. A write bound shuts down
  the **send** side: the peer is not reading, so there is no status to deliver.

  Getting there corrected a wrong conclusion worth repeating. The first measurement
  said `shutdown` does not interrupt a blocked write — on macOS *and* Linux, on all
  three backends, 4 005 ms against a 300 ms bound. Two operating systems agreeing to
  ignore `shutdown` was implausible enough to check, and the real cause was that the
  reaper task's start condition still read `head_ms > 0 or body_ms > 0`, so with only
  `write_ms` set nothing was sweeping. With that fixed the bound fires in ~310 ms on
  every backend and both platforms.

  The test asserts a *duration*, not that the connection eventually ended: an earlier
  version waited for the server task to finish, which passes with the bound disabled,
  because the client's own close breaks the blocked write too. It now requires the
  server to have given up long before the client let go, and was verified to fail
  (4 002 ms) with the bound off.

## Roadmap

**v1 (done):** HTTP/1.1 full-feature stack — routing, middleware, extractors,
JSON/form/multipart, static files, WebSocket, observability, graceful shutdown.

**v1.1 (done):** HTTP/2 (pure-Zig framing + HPACK + Huffman + stream handling),
TLS 1.3 (ALPN `h2`/`http/1.1`, opt-in `-Dtls`), and HTTP/3 (Velo's QPACK + H3
message/frame layer over a pluggable QUIC transport — OpenSSL by default,
loopback-verified). The RFC 9001-verified Initial packet protection, QUIC
varint/packet parsing, and UDP transport for the self-hosted (`-Dquic=zig`)
backend are in place.

**Also planned:** taking the self-hosted Zig QUIC transport the last mile to
production (on-wire client 0-RTT early-data offer — currently blocked: OpenSSL's
QUIC-TLS callback yields no EARLY secret to a resuming *client*, probed and
documented in [`interop/`](interop/) — and at-scale real-network validation; it
already does RFC 9002 loss recovery (RTT-adaptive PTO, ACK-based fast retransmit,
gapped ACKs) over NewReno congestion control, connection demultiplexing, RFC 9114
stream setup, connection- and stream-level flow control, connection migration,
many requests per connection, TLS session resumption, **server-side 0-RTT**
(NewSessionTicket offer + early-read-secret decrypt), and — after root-causing a
WAN-jitter fragility against aioquic — **RFC 9000 §5.7 buffering of early 1-RTT
packets**, **§12.2 coalesced-packet processing**, and skipping of unrecognized
1-RTT frames, which took delay+jitter reliability from ~33% to ~90–100% (a 40/40
sweep observed, with a rare timing-dependent intermittent residual); all
loopback-verified **and interoperable with two
third-party clients (aioquic and quic-go, including variable-length connection
IDs)**); and — no longer blocked — evented I/O:
upstream's own `std.Io.Evented` still implements no networking in any released Zig
(nor in master), so `listen` returns `error.NetworkDown`, but Velo now ships two
working fiber backends anyway: its own kqueue reactor (`-Dreactor`, BSD/macOS) and
the third-party [zio](https://github.com/lalinsky/zio) (`-Dzio`, which adds Linux
and Windows). What remains is a Windows-verified build and deleting Velo's reactor
once upstream catches up; see [Backends & conformance](#backends--conformance).
The upstream **`h2spec` suite is wired into CI** with a ratcheted pass count
(145/146 today — see [Backends & conformance](#backends--conformance)), alongside
an in-process h2spec-style suite and a **CI benchmark-regression gate**
([`bench/regression.sh`](bench/regression.sh)).

HTTP/2 now dispatches request handlers **concurrently per stream** (a single
frame reader; handlers run as bounded `io.async` tasks writing responses through
a shared `Io.Mutex`), and HTTP/3 serves **connections concurrently** (one task
per connection over a thread-assisted, multi-threaded OpenSSL QUIC domain).

### Backends & conformance

- **Evented I/O** (`-Devented`): wires `std.Io.Evented` into `velo.Io`. Every
  target is gated off, so `-Devented` compiles the wiring and falls back to the
  threaded backend. The reason is more basic than this section used to claim, and it
  is measured rather than remembered ([`tools/upstream-probe.sh`](tools/upstream-probe.sh)):

  **The evented backends `std.Io.Evented` selects implement no networking.** On
  macOS it selects `Dispatch`, whose vtable wires `netListenIp`, `netAccept`,
  `netConnectIp`, `netRead` and `netWrite` to "unavailable" stubs — a server on it
  gets `error.NetworkDown` from `listen`, observed directly. Linux's `Uring` is
  stubbed the same way and additionally does not compile as shipped. The one backend
  with real socket support, `Kqueue`, is stale against the `Io.VTable` in its own
  release (it references three vtable fields that do not exist) and is not what
  `Evented` selects on macOS anyway. This holds for 0.16.0 *and* for
  0.17.0-dev.1471, the newest downloadable nightly.

  What does work is the scheduler: `Dispatch` runs `async`/`await` and timers
  correctly, and only its `deinit` fails to compile (it passes a non-slice to
  `Allocator.free`) — which Zig's lazy analysis makes skippable. So the earlier
  diagnosis, "a teardown deadlock", was the wrong half of the problem.

  Zig's **git master** restructured the vtable — 109 fields down to 51, and macOS
  `Evented` now selects `Kqueue` — and this section used to conclude from that the
  capability was "coming". It is not. The vtable *field names* match; the functions
  do not exist. Master's `Kqueue.zig` still has **42 `@panic("TODO")`**, one more
  than 0.16.0's, and `netListenIp`, `netAccept`, `netWrite`, `netClose`, `now`,
  `sleep`, `cancel` and the whole `group*` family are all among them, verbatim:

  ```zig
  fn netAccept(userdata: ?*anyopaque, server: net.Socket.Handle) net.Server.AcceptError!net.Stream {
      const k: *Kqueue = @ptrCast(@alignCast(userdata));
      _ = k;
      _ = server;
      @panic("TODO");
  }
  ```

  Of master's 54 vtable entries, 13 are implemented: `async`, `await`,
  `concurrent`, `cancelRequested`, `conditionWait`, `conditionWake`, `netBindIp`,
  `netRead`, `netSend`. The *scheduler* is written and the *I/O* is not, in every
  version. The probe asks the gating question — does `listen` work? — so neither a
  fixed `deinit` nor a matching vtable can produce a false "ready".

- **Velo's own reactor** (`-Dreactor`, BSD/macOS, aarch64): because of the above,
  Velo implements the missing half itself, in one file
  ([`src/io/reactor.zig`](src/io/reactor.zig)) that is **built to be deleted**. One
  fiber per connection on `mmap`ed guard-paged stacks, a carrier thread per CPU with
  a kqueue each, and cooperative read/write/accept/timer/futex. Measured: 515 OS
  threads become 9, per-connection memory 97 KB becomes 64 KB, and p99 at 512
  connections 19.69 ms becomes 19.45 ms against axum's 17.25 ms.

  The scope is small because the vtable is **copied from `std.Io.Threaded`** and only
  15 of its 109 entries are overridden: `Threaded` sits at offset 0 of `Reactor`, so
  a forwarded entry receives a pointer it can cast to `*Threaded` and keeps working.
  Files, directories, DNS, processes and randomness are inherited rather than
  rewritten. The price is that a forwarded operation blocks its carrier —
  `sendFile` and hostname lookups do — and HTTP/3's UDP path is forwarded too, so
  h3-on-reactor works (interop is green on both QUIC backends) but does not scale.

  **Native UDP for the reactor was considered and deliberately declined.** It is the
  one obvious gap left in this file, and closing it would still be the wrong work:
  `-Dzio` already provides non-blocking UDP on Linux, macOS and Windows, while the
  reactor covers BSD only — so the change would reimplement, for one platform, what a
  better-supported dependency already does everywhere, inside a file whose stated
  purpose is to be deleted. The recommendation for scaling HTTP/3 is `-Dzio`, and the
  reactor's UDP path stays forwarded. This is recorded rather than left implicit
  because an unexplained gap invites someone to fill it.

  `App.listen` asks for `Backend.auto`, so no application names a backend. When the
  probe reports that `std.Io.Evented` can `listen`, `.auto` prefers it and this file
  goes away.

  Two things it found are worth knowing if you use fibers on 0.16.
  `std.Io.fiber.contextSwitch`'s clobber list names 81 registers and **not `x29`**,
  while the assembly writes `x29` — fine in `Debug`, which keeps a real frame
  pointer, and silently corrupting in optimized builds, where Velo served exactly one
  request and then died with `KERN_PROTECTION_FAILURE`.
  [`src/io/fiber.zig`](src/io/fiber.zig) replaces it with a naked function that
  pushes every callee-saved register, so there is no clobber list to be wrong. And a
  fiber must not publish its own completion: the moment it does, another thread can
  claim the fiber and reuse the stack it is still standing on.

  Conformance is the evidence that the parking and waking is faithful rather than
  merely functional: **h2spec scores the same 145/146 on all three backends**, and that
  suite is what found 53 failures in this HTTP/2 implementation the first time it
  ran.
- **zio** (`-Dzio`, all platforms): [zio](https://github.com/lalinsky/zio) is a
  third-party implementation of what `std.Io.Evented` is supposed to become, and
  unlike it, it exists — fibers over io_uring/epoll/kqueue/IOCP, async files and
  DNS, cancelation, task groups, growable coroutine stacks, optional work stealing.
  Velo's reactor covers BSD only and forwards file and DNS work to blocking threads;
  zio does not. Where they overlap this is the better-supported code, and it is not
  Velo's to maintain, so `Backend.auto` prefers it when both are built in.

  It is **off by default, and that default is enforced rather than promised**: the
  dependency is declared `lazy` in `build.zig.zon` and reached through
  `b.lazyDependency`, so a build that does not pass `-Dzio` never fetches it.
  Verified by deleting the package from the global cache and running the suite —
  green, with the two zio-specific tests skipping. The default build remains
  dependency-free, which is what `tools/consume-check.sh` gates.

  The one configuration decision worth recording is `enable_main_executor = false`.
  Velo's accept loop runs on the *caller's* thread, which is not one of zio's
  fibers; with the main executor enabled that thread is executor 0, and blocking it
  in `accept` would stall every fiber scheduled onto it.

  Conformance is measured here too: h2spec is 145/146 on zio, and the HTTP/3 interop
  suite is green on it.
- **HTTP/2 conformance (measured)**: the upstream
  [`h2spec`](https://github.com/summerwind/h2spec) suite — the one used to vet
  nginx/H2O/Go — runs against Velo's h2c server via
  [`interop/h2spec.sh`](interop/h2spec.sh) and in CI, where `MIN_PASS` ratchets
  the score so it can improve but not silently regress. Current result:
  **145/146 passing** (stable across repeated runs).

  Running it for the first time was the single most informative thing done to the
  HTTP/2 layer. The score started at **93/146** even though an in-process
  "h2spec-style" suite was green, because that suite only covered cases we had
  thought of. Two root causes accounted for nearly everything:

  1. The frame loop *ignored* every frame type it did not implement. Ignoring is
     not neutral — the spec makes several of those cases connection errors, so a
     conformant peer that sent one and waited for GOAWAY simply hung. 46 of the
     53 failures were timeouts.
  2. Request assembly read CONTINUATION and DATA frames from **nested** loops, so
     any rule could be bypassed by sending the offending frame mid-body. A
     `WINDOW_UPDATE` with a zero increment — a required connection error — was
     silently dropped when it arrived while a body was being collected.

  Fixing (1) was frame and header validation (§4.2 sizes, §6 stream-id rules,
  §5.1 idle streams, §8.4 PUSH_PROMISE, §6.5.2 SETTINGS ranges, §8.1.2
  pseudo-header and field-name rules) → 119. Fixing (2) meant restructuring the
  connection so the frame loop is the **single reader**, with explicit per-stream
  state, which then made the rest expressible: §5.1 stream lifecycle
  (half-closed/closed, and *how* a stream closed, since a reset and a completed
  response require different errors), §6.10 header-block interlock, trailers,
  §8.1.2.6 `content-length`-vs-DATA cross-check, §5.1.2 concurrency refusal
  (`REFUSED_STREAM` instead of blocking the whole connection), and §6.9
  **flow-control accounting** — connection and per-stream send windows, credit
  granted by WINDOW_UPDATE and shifted (not reset) by
  SETTINGS_INITIAL_WINDOW_SIZE, windows tracked as signed so a shrink can go
  negative, and DATA frames that wait for credit instead of overrunning the peer.
  → **145**.

  The one remaining failure is *not satisfiable on this port*: §3.5 requires a
  GOAWAY in reply to an invalid connection preface, but h2spec sends
  `INVALID CONNECTION PREFACE\r\n\r\n`, which on a port that also serves
  HTTP/1.1 is indistinguishable from a malformed HTTP/1.1 request — and answering
  every malformed HTTP/1.1 request with an HTTP/2 GOAWAY would be wrong. On a
  dedicated h2 port (TLS + ALPN `h2`) the preface check is reached directly and
  does emit GOAWAY(PROTOCOL_ERROR); that path has a unit test, since the upstream
  suite cannot reach it here.
- **HTTP/2 error handling**: the connection layer enforces RFC 9113 error handling
  — GOAWAY (with `FRAME_SIZE_ERROR`/`PROTOCOL_ERROR`) for connection errors,
  RST_STREAM for stream errors, stream-id validation (odd, strictly
  increasing), SETTINGS length/stream checks, PING length/stream checks
  (§6.7), and required pseudo-headers. An in-process, h2spec-style test suite
  exercises these cases (valid GET, bad SETTINGS length, HEADERS/SETTINGS on the
  wrong stream, even & non-increasing stream ids, missing `:path`, PING↔PONG,
  malformed PING).

## Authorship

Velo was designed and written by **blue-blaze**, working with **Kiro CLI** (Claude)
as the implementing agent — the architecture decisions, the protocol conformance
targets, and the review are the author's; most of the code, tests and prose were
produced by the agent under that direction.

The `LICENSE` copyright line names only the human author, and deliberately so.
Copyright requires human authorship: the US Copyright Office has repeatedly held
that material generated by AI without sufficient human creative control is not
copyrightable and cannot be registered to the AI, and courts have agreed
(*Thaler v. Perlmutter*). Naming a tool as a copyright holder would therefore have
no legal effect, and could muddy who actually holds the rights. Attribution and
copyright are different things — so the credit lives here, in prose, where it is
accurate.

## License

[MIT](LICENSE) — the same license as Zig itself, and as Axum and Echo, so Velo
adds no licensing friction to a project that already uses any of them (it is also
GPLv2-compatible, which Apache-2.0 is not).

MIT carries no explicit patent grant. If that becomes a requirement, the
conventional step is to dual-license as `MIT OR Apache-2.0`; doing so is
straightforward now and gets harder once there are outside contributors whose
consent would be needed.
