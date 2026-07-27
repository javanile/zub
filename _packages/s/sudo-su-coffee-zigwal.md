---
title: zigwal
description: Write-Ahead Log (WAL) primitive written in pure Zig — zero dependencies, single binary, crash-safe durability layer
license: MIT
author: sudo-su-coffee
author_github: sudo-su-coffee
repository: https://github.com/sudo-su-coffee/zigwal
keywords:
date: 2026-07-27
updated_at: 2026-07-27T07:49:50+00:00
last_sync: 2026-07-27T07:49:50Z
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
permalink: /packages/sudo-su-coffee/zigwal/
---

# zigwal

A crash-safe, dependency-free write-ahead-log primitive, written in pure
Zig. Part of the [`sudo-su-coffee`](https://github.com/sudo-su-coffee)
infrastructure collection — no C libraries, no runtime dependencies,
single-binary CLI included.

## What it is

`zigwal` is an ordered, append-only, checksummed log of byte-string
records, physically stored as a directory of segment files. It's the kind
of primitive you put underneath something else — a KV store's durability
layer, an event sourcing system, a replicated state machine's input log —
not a standalone database.

- Every record carries its own **LSN** (log sequence number), a
  monotonically increasing `u64` assigned at append time.
- Every record is **CRC-32 checksummed** (header fields + payload), using
  a self-contained checksum implementation — no `std.hash` dependency.
- The log is **segmented**: it rotates to a new file once the active
  segment passes a configurable size, so old data can be deleted in whole
  segments (`truncateBefore`) without rewriting anything.
- Replay is **crash-tolerant**: a process that dies mid-write leaves a
  structurally-detectable torn record at the tail, which iteration
  recognizes and stops at cleanly — it does not error out, and it does
  not lose any record that was fully flushed before the crash.
- All I/O goes through `std.fs.File`'s low-level positional calls
  (`pwriteAll` / `preadAll` / `sync`) — see [Design choices](#design-choices)
  for why.

## On-disk format

**Segment file** (`<20-digit zero-padded id>.wal`):

```
[0..8)   magic       "ZIGWAL1\n"
[8..16)  segment_id  u64 little-endian
[16..)   records...
```

**Record**, repeated until end of segment:

```
[0..8)   lsn          u64 little-endian
[8..12)  payload_len  u32 little-endian
[12..16) crc32        u32 little-endian, over (lsn ++ record_type ++ payload)
[16..17) record_type  u8   (application-defined; 0 is reserved)
[17..)   payload      payload_len bytes
```

`record_type == 0` is reserved specifically so that a zeroed disk region
left behind by a crash — or a bug — is never mistaken for a real record;
every real record must use type 1-255.

## Durability model

`Options.sync_policy` controls when `fsync` happens:

| Policy                    | Behavior                                              |
| ------------------------- | ------------------------------------------------------ |
| `.none`                   | Never fsync explicitly; relies on OS page cache flush   |
| `.every_write`            | fsync after every single `append()` — strongest, slowest |
| `.every_n_writes = n`     | fsync every `n` appends, or on manual `sync()`          |

Default is `.every_n_writes = 1`, i.e. equivalent to `.every_write`, so
the out-of-the-box behavior is the safe one; relax it deliberately if you
need the throughput.

## API sketch

```zig
const zigwal = @import("zigwal");

var wal = try zigwal.Wal.open(allocator, "data/wal", .{});
defer wal.deinit();

const result = try wal.append(1, "some payload bytes");
// result.lsn, result.segment_id, result.offset_in_segment

var it = try wal.iterator();
defer it.deinit();
while (try it.next()) |record| {
    defer allocator.free(record.payload);
    // record.lsn, record.record_type, record.payload
}

try wal.rotate();               // force a new segment
try wal.truncateBefore(seg_id); // delete fully-checkpointed old segments
```

**Address stability:** `Wal` owns an open `std.fs.File` handle inside its
`active` segment field. Don't copy a `Wal` *value* around after `open()`
(returning it into a new local by value, storing it in a container that
reallocates, etc.) — hold it by pointer, or heap-allocate it with your
allocator if it needs to live somewhere that moves. This is the standard
rule for any Zig struct wrapping a raw file handle plus derived state; it
isn't special to this library, but it's worth saying explicitly since
getting it wrong fails silently until something reads through a stale
pointer.

## CLI

```
zig build run -- write <dir> <record_type:u8> <payload>
zig build run -- dump  <dir>
zig build run -- stat  <dir>
zig build run -- bench <dir> <count> <payload_bytes> [--sync-policy none|every_write|<n>]
```

`bench` prints throughput numbers it just measured on your machine, for
your disk, under whichever `--sync-policy` you pass (defaults to
`every_1_writes`, i.e. fsync after every append). Below is one real,
reported-back run (100,000 records, 256-byte payloads) — this is one
person's machine on one day, not a portability claim, but it's a real
measured run, not an invented number:

| `--sync-policy` | records/sec | MB/sec  |
| --------------- | ----------: | ------: |
| `every_write` (default) | 404     | 0.10    |
| `100`            | 35,349      | 8.63    |
| `1000`           | 165,906     | 40.50   |
| `10000`          | 288,734     | 70.49   |
| `100000`         | 326,274     | 79.66   |
| `none`           | 589,422     | 143.90  |

That's the expected shape for a WAL: durability and throughput trade off
directly against each other, and the biggest jump is between "fsync every
write" and "fsync occasionally" — the fsync syscall itself, not the write,
is what's expensive. Run it yourself and it'll print your own numbers;
don't take the table above as a promise about your hardware.

## Building

```
zig build            # library + CLI, both to zig-out/
zig build test        # unit tests (inline in every src/*.zig file)
zig build run -- help # run the CLI
```

## Project layout

```
build.zig, build.zig.zon   — Zig 0.15.2 build graph + package manifest
src/root.zig                — public API surface (@import("zigwal"))
src/wal.zig                 — Wal: open/append/rotate/sync/truncate/iterate
src/segment.zig              — segment file create/open/append (positional I/O)
src/record.zig                — record header encode/decode/checksum
src/iterator.zig               — crash-tolerant cross-segment record iterator
src/crc32.zig                   — self-contained CRC-32 (IEEE 802.3)
src/main.zig                     — CLI: write / dump / stat / bench
```

## Design choices

**Why raw `pwriteAll`/`preadAll` instead of `std.Io.Writer`/`std.Io.Reader`?**
Zig 0.15 rewrote the buffered stream stack top to bottom ("Writergate" —
non-generic `std.Io.Writer`/`Reader`, buffer moved into the interface,
`File.Reader`/`File.Writer` wrapper types). It's the single largest
breaking-change surface in this release, and therefore the one I'm least
confident about getting byte-perfect without a compiler on hand. The
lower-level positional I/O calls (`pwriteAll`, `preadAll`, `sync`,
`stat`, `createFile`, `openFile`) predate that rework and are closer to
thin POSIX wrappers, so they're both a safer bet to have written
correctly here and, arguably, the more appropriate tool anyway: a
durability primitive wants every write to be an explicit, positioned
syscall with a known byte range and an explicit fsync boundary, not
buffering it doesn't control. The CLI's `stdout` printing (`main.zig`)
*does* use the new `std.Io.Writer` interface, following the exact pattern
from the official 0.15.1 release notes — that's the one place in this
project where I'm relying on the newest API, and it's isolated to
output formatting, not the durability path.

**Why is the LSN embedded in every record instead of computed from file
position?** So each record is self-describing and reopening an existing
WAL doesn't require replaying every prior segment to resume numbering —
`Wal.open()` only needs to scan the *last* segment (see `findNextLsn` in
`wal.zig`) to find where to continue. That scan is structural-only (checks
lengths and the reserved record_type, doesn't verify checksums) for
speed; call `iterator()` and consume it fully if you want full corruption
detection across old segments before trusting them.

**Why not `std.ArrayList(T).init(allocator)`?** Zig 0.15 made the
unmanaged variant the default `std.ArrayList(T)`; the idiom is
`var list: std.ArrayList(T) = .empty;` followed by
`list.append(allocator, item)` and `list.deinit(allocator)`. Used this
way in `wal.zig` for the reusable per-append encode buffer and the
segment-id scan.

## Known risk areas

`zig build` and `zig build run -- bench ...` are confirmed working, which
resolves most of what used to be listed here (`File.OpenMode` field
names, `ArgIterator`, `std.sort.asc`, the absolute-path `openDir` call —
all exercised by `Wal.open` on every single run above). What's **not**
confirmed yet:

1. **`zig build test`** — the bench runs above only exercise `open()` and
   `append()`. They don't touch `iterator()`, `rotate()`,
   `truncateBefore()`, or a checksum mismatch — that's what the inline
   tests in `wal.zig`/`iterator.zig`/`segment.zig` cover, and none of them
   have been confirmed to run yet. Worth running `zig build test` and
   pasting back the result (or just "all tests passed").
2. **The new `--sync-policy` flag parsing** in `main.zig` — added after
   the build/run above, to make the shipped CLI match what was actually
   being benchmarked. Only checked statically (brace/paren balance,
   structural review), not compiled.

If either turns up an error, the message + file/line is usually enough
for me to fix it without needing anything else from you.
