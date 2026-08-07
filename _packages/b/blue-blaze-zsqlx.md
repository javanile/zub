---
title: zsqlx
description: A SQL toolkit for Zig 0.16 — native PostgreSQL, MySQL and SQLite drivers on std.Io, with build-time checked queries
license: MIT
author: blue-blaze
author_github: blue-blaze
repository: https://github.com/blue-blaze/zsqlx
keywords:
  - database
  - mysql
  - postgresql
  - sql
  - sqlite
  - sqlx
date: 2026-08-06
category: data-formats
updated_at: 2026-08-06T07:29:05+00:00
last_sync: 2026-08-06T07:29:05Z
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
permalink: /packages/blue-blaze/zsqlx/
---

# zsqlx

[![CI](https://github.com/blue-blaze/zsqlx/actions/workflows/ci.yml/badge.svg)](https://github.com/blue-blaze/zsqlx/actions/workflows/ci.yml)
[![Zig 0.16.0](https://img.shields.io/badge/zig-0.16.0-f7a41d.svg)](https://ziglang.org/download/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A SQL toolkit for Zig 0.16, modeled after Rust's [sqlx](https://github.com/launchbadge/sqlx).

- **Native drivers** — PostgreSQL (wire protocol v3) and MySQL implemented from scratch on `std.Io.net`; SQLite via the bundled amalgamation. No external client libraries.
- **`std.Io` throughout** — every operation takes an explicit `io: std.Io`; runs on `Io.Threaded` today and picks up evented backends as they land in the stdlib.
- **Build-time checked queries** — `zsqlx prepare` validates `queries/*.sql` against a live database (or the committed `.zsqlx/` offline cache) and generates strongly-typed Zig functions.

## Install

```sh
zig fetch --save git+https://github.com/blue-blaze/zsqlx
```

```zig
// build.zig
const zsqlx = b.dependency("zsqlx", .{
    .target = target,
    .optimize = optimize,
    // .postgres = false, .mysql = false, .sqlite = false,  // drop drivers
    // .@"bundle-sqlite" = false,                           // link system libsqlite3
});
exe.root_module.addImport("zsqlx", zsqlx.module("zsqlx"));
```

## Quick taste

```zig
const zsqlx = @import("zsqlx");
const pg = zsqlx.pg;

var conn = try pg.PgConnection.connect(gpa, io, opts);
defer conn.close(io);

const User = struct { id: i64, name: []const u8, age: ?i32 };
const users = try zsqlx.query(pg.Postgres, gpa,
    "SELECT id, name, age FROM users WHERE age > $1")
    .bind(i32, 18)
    .fetchAll(User, gpa, io, &conn);
defer zsqlx.freeRows(gpa, User, users);
```

## Feature parity with sqlx

| sqlx | zsqlx | Notes |
|---|---|---|
| PostgreSQL driver | ✅ | wire v3, extended protocol, binary formats |
| — auth: SCRAM-SHA-256 / MD5 / password | ✅ | |
| — auth: SCRAM-SHA-256-PLUS | ✅ | RFC 5929 tls-server-end-point binding; **sqlx has no -PLUS** |
| — TLS (sslmode 6 modes) | ✅ | vendored stdlib TLS (see below) |
| — TLS client certificates (mTLS) | ✅ | EC P-256/P-384, Ed25519 |
| — LISTEN/NOTIFY | ✅ | auto-reconnect listener |
| — COPY IN/OUT | ✅ | text/csv/binary passthrough |
| — advisory locks | ✅ | session lock/tryLock guard |
| — arrays, numeric, uuid, timestamptz... | ✅ | |
| — geometry, ranges, inet/cidr/macaddr, money, bit/varbit, timetz | ✅ | 7 geometry types + cube; 6 range types via `types.Range(T)` |
| — hstore, citext, ltree/lquery | ✅ | dynamic per-database OID lookup, cached |
| MySQL driver | ✅ | text + binary protocol, 16MB packet splits |
| — auth: caching_sha2 / native_password | ✅ | |
| — caching_sha2 full-auth, sha256_password | ✅ | cleartext over TLS, RSA-OAEP over plaintext |
| — mysql_clear_password | ✅ | opt-in via `enable_cleartext_plugin` |
| — TLS (5 ssl_modes) + mTLS | ✅ | mid-handshake SSLRequest upgrade |
| — Unix socket | ✅ | |
| SQLite driver | ✅ | bundled 3.50.4 or system lib |
| Connection pool | ✅ | min/max, timeouts, lifetime, hooks, health checks, reaper |
| Transactions + savepoints | ✅ | rollback-on-deinit, `withTransaction` |
| Streaming queries | ✅ | pull iterator; rows borrow the read buffer |
| `query!` compile-time checking | ✅ | `zsqlx prepare` codegen, online + offline `.zsqlx/` cache |
| — describe: PostgreSQL / SQLite / MySQL | ✅ | all three drivers |
| `#[derive(FromRow)]` | ✅ | comptime reflection + `zsqlx_columns` rename overrides |
| QueryBuilder | ✅ | placeholder style per driver |
| Any driver | ✅ | tagged-union dispatch, URL scheme routing |
| `Executor` (pool / transaction as a query target) | ✅ | plus explicit checkouts |
| Statement logging + slow-query warnings | ✅ | `std.log` scope `.zsqlx`; parameter values never logged |
| Pool metrics | ✅ | `pool.stats(io)`: gauges + 10 cumulative counters |
| Migrations | ✅ | SHA-384 checksums, dirty detection, revert, per-driver locking |
| CLI (`sqlx-cli`) | ✅ | `database create/drop/reset/setup`, `migrate add/run/revert/info` (`--dry-run`, `--target-version`, `--ignore-missing`), `prepare` |
| `#[sqlx::test]` harness | ✅ | fresh DB per test, drop-on-success, keep-on-failure, stale GC |
| MSSQL | ❌ | not in mainline sqlx either |

### Remaining limitations

| | why |
|---|---|
| Socket-level read deadline | `Io.Threaded` in 0.16.0 exposes no per-read timeout (and `Io.net.IpAddress.ConnectOptions.timeout` panics as unimplemented), so every bound here is enforced by running the operation on a cancellable task rather than by the reader. In practice that covers what matters — `connect_timeout` bounds the entire handshake and `withTimeout` bounds a query — but it costs one task per bounded operation, so a per-statement default is not free enough to enable globally. Prefer the server-side `statement_timeout`. |
| RSA client certificates for mTLS | `std.crypto` has no RSA *private-key* primitives (only verification and public-key encryption, which is what MySQL's RSA auth path needs). EC and Ed25519 client keys work. |
| Encrypted private keys (PKCS#8 / PBES2) | Would need PBKDF2 + a cipher wired into the DER walker; supply an unencrypted key. |
| Multidimensional arrays | Only 1-D is decoded — sqlx is 1-D only as well. |
| SQLite worker-thread offload | SQLite calls block the calling thread. Under `Io.Threaded` a worker pool adds hops without adding concurrency; revisit when an evented backend lands. |
| MSSQL | Not in mainline sqlx either. |

Defaults worth knowing: `ssl_mode` is `prefer`, which matches libpq and sqlx — TLS is
attempted but the certificate chain and host name are **not** verified, and the
connection silently falls back to plaintext if the server declines. Use
`verify-full` for anything crossing a trust boundary.

TLS lives in `src/tls/` — a vendored copy of the stdlib TLS client, because
`std.crypto.tls.Client` rejects a `CertificateRequest` outright (no mTLS) and
discards the server certificate after the handshake (no channel binding for
SCRAM-PLUS). The vendored copy only depends on public `std` APIs; the delta
against upstream is client certificates, the TLS 1.3 Certificate/CertificateVerify
flight, and exporting the end-entity certificate.

## Executors

Terminal query methods take any executor, so a pool or a transaction is a
query target on its own:

```zig
// A pool acquires a connection for the call and returns it afterwards —
// including on every error path.
const n = try zsqlx.query(pg.Postgres, gpa, "SELECT count(*) FROM users")
    .fetchScalar(i64, gpa, io, &pool);

// Inside a transaction, target the transaction itself.
var tx = try zsqlx.Transaction(pg.Postgres).begin(&conn, io, .{});
defer tx.deinit(io);
_ = try zsqlx.query(pg.Postgres, gpa, "INSERT INTO users (name) VALUES ($1)")
    .bind([]const u8, "ada").execute(io, &tx);
try tx.commit(io);

// A bare connection and an explicit checkout both still work.
_ = try zsqlx.query(pg.Postgres, gpa, "SELECT 1").execute(io, &conn);
_ = try zsqlx.query(pg.Postgres, gpa, "SELECT 1").execute(io, pooled);
```

Streaming holds the checkout for as long as rows are readable — they point into
the connection's read buffer — and `FetchResult.deinit(io)` returns it.

## Timeouts and cancellation

Three independent bounds, in the order you should reach for them:

```zig
// 1. Bound the whole handshake — TCP, TLS, startup and auth (default 30s;
//    URL: ?connect_timeout=10, 0 disables). A server that accepts the socket
//    and then goes silent is caught here, not left hanging.
opts.connect_timeout = .fromSeconds(10);

// 2. Let the server enforce a per-session statement bound. Cheapest and
//    safest: no extra task, no second connection, and the connection stays
//    usable afterwards. URL: ?statement_timeout=5000 or
//    ?options=-c%20statement_timeout%3D5000
opts.options = &.{ .{ "statement_timeout", "5000" } };

// 3. Bound one specific query. On overrun zsqlx sends a PostgreSQL
//    CancelRequest and waits for the query to come back as SQLSTATE 57014,
//    so the connection is left reusable rather than discarded.
const rows = try conn.withTimeout(gpa, io, .fromSeconds(2), Ctx, ctx, run);
// → error.QueryTimedOut
```

To cancel from elsewhere — a shutdown signal, a request that went away — copy
a handle before running the query; the owning task is blocked on the socket and
cannot make the call itself:

```zig
const handle = conn.cancelHandle();   // plain value, safe to move to another task
// ... later, from that other task:
try handle.cancel(gpa, io);           // target query fails with SQLSTATE 57014
```

## Observability

Statement logging rides on `std.log`, so it costs nothing when the scope is
filtered out and needs no allocator:

```zig
zsqlx.log.settings = .{
    .log_statements = true,               // DEBUG per statement
    .slow_statement_threshold = .fromMilliseconds(200),  // above this: WARN
    .max_sql_bytes = 512,                 // truncate long SQL in log lines
};
```

```
[zsqlx] (warn): slow statement: 55ms, 1 row(s); 1 param(s); SELECT $1::text
[zsqlx] (warn): statement failed in 1ms: DatabaseError [42703]; 0 param(s); SELECT no_such_column
```

**Bound parameter values are never logged** — only the parameter count. Values
are exactly the things most likely to be secrets or personal data, and a log
line is the easiest place to leak them.

Pools expose gauges and cumulative counters for a metrics endpoint:

```zig
const s = pool.stats(io);
// s.size / s.idle / s.in_use / s.waiters
// s.counters.acquires / acquires_waited / acquire_timeouts / acquires_slow
// s.counters.connects / connect_errors / closes / reaped
// s.counters.discarded_broken / discarded_in_transaction
```

`discarded_in_transaction` is worth an alert: a non-zero value means some code
path returned a connection to the pool without committing or rolling back.

## Requirements

- Zig 0.16.0
- Docker (integration tests only)

## Building and testing

```sh
zig build              # library + zsqlx CLI
zig build test         # unit tests — no database required (protocol codecs,
                       # SCRAM vectors, pool-on-mock + concurrency stress,
                       # full SQLite suite, migrator, prepare parsing/codegen,
                       # and fault injection against a scriptable fake server)
zig build examples     # compile the examples so they cannot rot

tests/docker/gen-pg-certs.sh     # once: CA + server + client certs for the
tests/docker/gen-mysql-certs.sh  # ssl_mode and mTLS suites (keys gitignored)
docker compose up --wait
export ZSQLX_TEST_POSTGRES_URL=postgres://zsqlx:zsqlx@localhost:5433/zsqlx_test
export ZSQLX_TEST_MYSQL_URL=mysql://zsqlx:zsqlx@localhost:3307/zsqlx_test
zig build test-integration     # auth matrices, ssl modes, type round trips,
                               # pool concurrency, LISTEN/NOTIFY, COPY,
                               # migrations, Any, test harness
```

Build options: `-Dpostgres=false`, `-Dmysql=false`, `-Dsqlite=false` disable drivers; `-Dbundle-sqlite=false` links the system libsqlite3.

## Fuzzing

Every parser that consumes untrusted bytes has a target in `src/fuzz_tests.zig`.
Under a plain `zig build test` each target replays its corpus as a regression
test; real fuzzing needs the dedicated step:

```sh
zig build test-fuzz --fuzz=300K -j2 -- "fuzz pg binary value decode"
```

A `--fuzz` run only ever fuzzes one target per invocation, hence the filter.
Never pass a bare `--fuzz`: it spawns one never-terminating worker per CPU.

Corpus entries are not the raw bytes a target sees — `Smith` reads its own
framing out of them — so build them with the `entry()` helper in that file.

`.github/workflows/ci.yml` runs unit tests, the dockerized integration matrix,
and a bounded fuzz job per target.

One platform caveat: on x86_64-linux, `zig build --fuzz` under Zig 0.16.0 fails
at startup with `corrupted coverage file: pcs_len was zero` — the instrumented
binary registers no program counters before any fuzzing begins. The same command
fuzzes normally on aarch64-macos, so CI runs the fuzz matrix on macOS runners.
Corpus replay is unaffected and runs everywhere as an ordinary test under
`zig build test`.

## Benchmarks

`zig build bench` (ReleaseFast; end-to-end rows need `ZSQLX_TEST_*_URL`).
Reference numbers on an Apple-silicon laptop against dockerized
postgres:18beta1 / mysql:8.4 (loopback TCP):

| benchmark | median |
|---|---|
| pg encode i64 / text(64) / uuid | 1ns / 3ns / 27ns |
| pg encode numeric | 75ns |
| pg encode i32 array(100) | 483ns |
| pg frame scan (3 DataRows) | 18ns |
| mysql packet write (256B) | 10ns |
| url parse | 37ns |
| sqlite prepared select round trip | 215ns (~4.7M ops/s) |
| pg prepared select round trip | ~1.1ms (network) |
| mysql prepared select round trip | ~0.55ms (network) |
| pg fetchAll 10k rows | ~3.6ms |

## Checked queries workflow

```sh
mkdir queries
cat > queries/get_user.sql <<'EOF'
-- name: getUser :optional
SELECT id, name, email FROM users WHERE id = $1
EOF

DATABASE_URL=postgres://... zsqlx prepare   # validates + writes .zsqlx/ + queries.zig
zsqlx prepare --offline                     # CI / no database: cache only
zsqlx prepare --check                       # CI freshness gate
```

Generated code is plain Zig — a `GetUserRow` struct and a `getUser(gpa, io, conn, p1)` function; binding a wrong type is an ordinary compile error. See `examples/checked/` for a complete consumer package.

## Test harness

```zig
test "user creation" {
    try zsqlx.testing.run(pg.Postgres, gpa, io, .{
        .admin_options = opts,
        .with_database = withDb,
        .migrations = &.{ ... },
        .fixtures = &.{ "INSERT INTO ..." },
    }, ctx, struct {
        fn f(c: @TypeOf(ctx), t: *zsqlx.testing.TestDb(pg.Postgres)) !void {
            // t.conn is connected to a fresh _zsqlx_test_<pid>_<n> database
        }
    }.f);
}
```

## Contributing

Issues and pull requests are welcome. Before opening a PR:

```sh
zig build test          # unit + fault injection, no database needed
zig fmt --check build.zig src bench tests examples
```

Integration tests need Docker; see [Building and testing](#building-and-testing).
New behaviour should come with a test — the suite is the reason the fixes in
[CHANGELOG.md](CHANGELOG.md) could be made with any confidence.

## License

MIT — see [LICENSE](LICENSE).
