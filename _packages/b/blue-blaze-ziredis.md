---
title: ziRedis
description: "Redis client SDK for Zig with a Redisson-style distributed sync layer: locks, rwlock, fairlock, semaphore, latch, rate limiter and more. RESP2/RESP3, pipelining, Pub/Sub, connection pool."
license: MIT
author: blue-blaze
author_github: blue-blaze
repository: https://github.com/blue-blaze/ziRedis
keywords:
  - distributed-lock
  - distributed-systems
  - redis
  - redis-client
  - redisson
date: 2026-08-14
category: data-formats
updated_at: 2026-08-14T14:30:28+00:00
last_sync: 2026-08-14T14:30:28Z
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
permalink: /packages/blue-blaze/ziRedis/
---

# ziRedis

A Redis client SDK for Zig, built on [zinet](https://github.com/blue-blaze/zinet)
(the Netty-of-Zig) and Zig 0.17's `std.Io`. RESP2 and RESP3, typed commands,
pipelining, transactions, Lua scripts, blocking commands, Pub/Sub, and a
bounded connection pool.

## Quick start

`build.zig.zon`:

```sh
zig fetch --save "https://github.com/blue-blaze/ziRedis/archive/refs/tags/v0.1.0.tar.gz"
```

`build.zig`:

```zig
const ziredis = b.dependency("ziredis", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("ziredis", ziredis.module("ziredis"));
```

Then:

```zig
const std = @import("std");
const ziredis = @import("ziredis");

pub fn main() !void {
    var debug = std.heap.DebugAllocator(.{}).init;
    defer _ = debug.deinit();
    const gpa = debug.allocator();

    // One call: I/O runtime, address, pool. Defaults to localhost:6379.
    var client = try ziredis.Client.create(gpa, .{});
    defer client.destroy();

    try client.set("greeting", "hello");
    const greeting = (try client.getAlloc(gpa, "greeting")).?;
    defer gpa.free(greeting);
    std.debug.print("{s}\n", .{greeting}); // hello
}
```

Connecting elsewhere:

```zig
// host/port and friends…
var client = try ziredis.Client.create(gpa, .{
    .host = "10.0.0.5",
    .port = 6380,
    .password = "sekret",
    .database = 3,
});

// …or a URL, the go-redis way:
var client = try ziredis.Client.create(gpa, .{
    .url = "redis://:sekret@10.0.0.5:6380/3",
});

// Sharing your program's Io instead of the built-in runtime:
var client = try ziredis.Client.create(gpa, .{ .io = threaded.io() });
```

`create` heap-allocates the client (it needs a stable address) and, when
no `.io` is given, owns a `std.Io.Threaded` internally; `destroy` tears
both down. The in-place expert path is still there:

```zig
var client: ziredis.Client = undefined;
try client.init(.{ .gpa = gpa, .io = io, .address = address });
defer client.deinit();
```

For reads, pick the flavour that fits:

```zig
// Zero-copy: the reply owns an arena, one deinit frees everything.
var reply = try client.get("key");        // Reply(?[]const u8)
defer reply.deinit();

// Copy-out: a plain slice on your allocator, no wrapper to hold.
const value = try client.getAlloc(gpa, "key") orelse return; // ?[]u8
defer gpa.free(value);
```

## What's in the box

| Area | API |
|---|---|
| Strings | `get` `set` `setWith` (EX/PX/EXAT/NX/XX/KEEPTTL) `getDel` `incr` `incrBy` `incrByFloat` `decr` `decrBy` `append` `strlen` `getRange` `setRange` `mset` `mget` |
| Keys | `del` `unlink` `exists` `expire` `pexpire` `expireAt` `ttl` `pttl` `persist` `typeOf` `rename` `renameNx` `touch` `randomKey` `dbsize` `flushDb` |
| Hashes | `hset` `hsetNx` `hget` `hgetAll` `hmget` `hdel` `hexists` `hlen` `hkeys` `hvals` `hincrBy` `hincrByFloat` |
| Lists | `lpush` `rpush` `lpop` `rpop` `lrange` `llen` `lindex` `lset` `ltrim` `lrem` `lmove` |
| Sets | `sadd` `srem` `smembers` `sismember` `scard` `spop` `srandmember` `smove` `sinter` `sunion` `sdiff` |
| Sorted sets | `zadd` `zscore` `zincrBy` `zcard` `zcount` `zrank` `zrem` `zrange` `zrangeWithScores` `zrangeByScore` `zpopMin` `zpopMax` |
| Iteration | `scan` `hscan` `sscan` `zscan` — cursor iterators, one page per round trip; the iterator owns copies of key and pattern |
| Blocking | `blpop` `brpop` `blmove` — a lapsed wait is `null`, not an error |
| Batching | `Pipe` — N commands, one write, one round trip |
| Transactions | `Tx` — `watch`/`queue`/`exec`; MULTI is confirmed in its own round trip first, so a rejected MULTI can never leak queued commands outside the transaction; WATCH conflict = `error.TxAborted` |
| Scripts | `Script` — EVALSHA with automatic NOSCRIPT load-and-retry |
| Pub/Sub | `PubSub` — dedicated connection, dynamic (p)subscribe, opt-in reconnect with resubscription; `awaitConfirmations` waits until the server acknowledged — publish-after-subscribe needs it |
| Distributed sync | `ziredis.sync` — reentrant `Lock` with lease watchdog, `RwLock` (read-write, downgrading), `FairLock` (FIFO), `MultiLock`, `Semaphore`, `CountDownLatch`, `AtomicLong`, `RateLimiter`, `IdGenerator`, `BloomFilter`; Redisson interop mode (below) |
| Anything else | `client.command(&.{ "OBJECT", "ENCODING", "k" })` — the generic interface |

The protocol is negotiated per connection: `HELLO 3` first, RESP2 when the
server predates it (or when `prefer_resp3 = false`). AUTH (password or
username+password) and SELECT happen in the same handshake.

## Distributed sync (`ziredis.sync`)

The Redisson-shaped layer: ten distributed primitives built entirely on
the SDK below them — `Lock` (reentrant, lease watchdog), `RwLock`
(read-write, downgrading), `FairLock` (FIFO), `MultiLock`, `Semaphore`,
`CountDownLatch`, `AtomicLong`, `RateLimiter`, `IdGenerator`,
`BloomFilter`.

```zig
var ctx: ziredis.sync.Context = undefined;
try ctx.init(.{ .client = client });
defer ctx.deinit();

var lock = try ctx.lock("order:42");
defer lock.deinit();

if (try lock.acquire(.{ .wait = .fromSeconds(5) })) {
    defer lock.unlock() catch {};
    // …the critical section…
}
```

The three sentences to know:

* **Reentrancy is per handle** (threads mean nothing under `std.Io`),
  and **leases always expire** — a crashed holder frees itself within
  one lease; the context's single watchdog task renews held locks until
  unlock.
* **Waiting** is a per-process choice: `.signal` (token lists, BLPOP in
  slices), `.pubsub` (the context's shared subscriber connection — no
  pooled connection held while waiting), or `.poll` — and processes
  using different strategies still wake each other.
* **Redisson interop is a switch**: `.interop = .redisson` puts every
  wire-compatible primitive (locks, semaphore, latch, rate limiter) on
  the Java client's keyspace and channels, so Zig and Java services
  contend for the same objects.

**[SYNC.md](SYNC.md)** is the full documentation: identity model, every
primitive's API and data model, wait-strategy tradeoffs, the interop
matrix, and the safety bounds (this is a single-node lock — same as
Redisson). `examples/sync_tour.zig` walks everything against a live
Redis.

## Memory ownership

One rule: **a reply that carries strings owns an arena, and `deinit` frees
everything at once.**

```zig
var reply = try client.hgetAll("config");   // Reply([]const Pair)
defer reply.deinit();                        // one call frees keys, values, slice
```

Commands whose replies carry nothing (SET → `void`, INCR → `i64`,
EXPIRE → `bool`) convert and free internally — nothing to hold, nothing to
free. Absent keys are `null` (`?T`), never an error.

Arguments always *borrow*: the SDK copies what it needs before returning,
so stack buffers and temporaries are fine.

## Error model

```
error.ServerError            the server said -ERR …; the command reached Redis
error.UnexpectedReplyType    reply shape does not match the typed method
error.ConnectionLost         the connection died — from a send, this is proof
                             the command never entered the write queue
error.CommandOutcomeUnknown  the command entered the write queue but delivery
                             could not be confirmed; it may have executed
error.Timeout                no reply in time; the connection is discarded
error.Canceled               the calling task was cancelled mid-wait; if a
                             command was in flight, its connection is discarded
error.RequestTooLarge        the encoded command exceeds addressable size
error.PoolTimeout            pool at capacity, nothing came free
error.TxAborted              EXEC returned null: a WATCH conflict
error.AuthenticationFailed / error.HandshakeFailed
```

A `Timeout` poisons its connection on purpose: the abandoned reply would
otherwise answer the *next* command. So does a cancellation while a reply
is owed, and for the same reason. The pool discards poisoned connections
and opens fresh ones.

Retries are **off by default**. Opt in for failures that provably happened
before the command reached the server:

```zig
.retry = .{ .max_attempts = 3, .backoff_initial = .fromMilliseconds(50) },
```

The dividing line is the write queue. `error.ConnectionLost` from a send
means the command never entered it — retryable. `error.CommandOutcomeUnknown`
means it did and the flush failed after — the command may have executed,
and is never retried. Neither are `Timeout` and `Canceled`, where the
command was fully sent.

## Concurrency

Any number of tasks may share one `Client`; every command borrows a pooled
connection for exactly one round trip. `Pipe`, `Tx`, blocking commands and
`PubSub` hold a connection longer (`PubSub` owns a dedicated one outside
the pool). The pool is bounded (`pool.capacity`, default 8) and blocking —
backpressure, not unbounded growth.

`Client` is initialized in place and must not move afterwards.

## Testing

```sh
zig build test              # unit tests; integration tests skip without Redis
scripts/redis-test.sh       # Docker: redis:7, redis:7+AUTH, redis:5 — full suite
zig build check             # fmt + tests + examples, what CI runs
```

All tests run under a leak-checking allocator.

## Known limitations

* **RESP3 attributes**: the pinned zinet decoder does not know the `|`
  attribute marker; a server that sends one closes the connection. No
  Redis feature this SDK exposes elicits attributes today, but enabling
  ones that do (`CLIENT TRACKING` with certain modes) needs a zinet
  upgrade first.
* **Pushes on pooled connections are discarded** (they would otherwise
  wedge the reader when nothing consumes them). Client-side caching wants
  a consumer API — see the roadmap.
* **Shutdown contract**: `client.deinit()` requires every `Pipe`/`Tx`/
  `PubSub`/`Scan` and in-flight command to be finished first (asserted in
  safe builds). Concurrent shutdown is not supported.
* **Routing is standalone-only**: typed commands do not yet describe
  their key layout to the executor; that work is the bulk of cluster
  support (below).

## Roadmap

The `Executor` interface (`acquire(routing_key)` / `release`) is the seam
the next deployments plug into, without touching the typed commands:

* **ClusterExecutor** — hash the key to a slot, route to that node's pool,
  follow MOVED/ASK, refresh topology.
* **SentinelExecutor** — discover the primary via sentinels, re-resolve on
  failover.
* A multiplexing executor (many tasks, one connection) for read-heavy
  workloads.
* Client-side caching: RESP3 invalidation pushes already arrive on their
  own queue; what is missing is only the cache.

## License

MIT
