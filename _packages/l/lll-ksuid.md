---
title: ksuid
description: K-Sortable Globally Unique IDs
license: MIT
author: lll
author_github: lll
repository: https://github.com/lll/ksuid
keywords:
  - ksuid
date: 2026-05-30
updated_at: 2026-05-30T15:21:26+00:00
last_sync: 2026-05-30T15:21:26Z
package_kind: library
has_library: true
has_binary: false
has_distributable_binary: false
binary_count: 0
distributable_binary_count: 0
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/lll/ksuid/
---

# ksuid
[![zig version](https://img.shields.io/badge/0.16.0-orange?style=flat&logo=zig&label=Zig&color=%23eba742)](https://ziglang.org/download/)
[![zig doc](https://img.shields.io/badge/zigdoc%20-pages-orange?color=%23eba742)](https://lll.github.io/ksuid/)
[![reference Zig](https://img.shields.io/badge/deps%20-0-orange?color=%23eba742)](https://github.com/lll/ksuid/blob/main/build.zig.zon)
[![build](https://github.com/lll/ksuid/actions/workflows/build.yml/badge.svg)](https://github.com/lll/ksuid/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Zig implementation K-Sortable Globally Unique IDs based on [Segment's KSUID](https://github.com/segmentio/ksuid). KSUIDs are 20-byte binary identifiers with a 32-bit timestamp (seconds since 2014-05-13) and 128 bits of random payload. The text representation is 27 base62 characters that sort lexicographically by generation time.

## Usage

Fetch as a dependency in `build.zig.zon`:

```sh
zig fetch --save "git+https://github.com/lll/ksuid#zig-0.16"
```

Add the module in `build.zig`:

```zig
const ksuid_mod = b.dependency("ksuid", .{ .target = target, .optimize = optimize }).module("ksuid");
your_exe.root_module.addImport("ksuid", ksuid_mod);
```

Then in your code:

```zig
const ksuid = @import("ksuid");

// Generate a new KSUID
const id = ksuid.KSUID.generate();
std.debug.print("{s}\n", .{id.string()});

// Parse from string
const parsed = try ksuid.KSUID.parse("0ujtsYcgvSTl8PAuAdqWYSMnLOv");
std.debug.print("timestamp: {d}\n", .{parsed.timestamp()});

// Use a custom random source
var prng = std.Random.DefaultPrng.init(12345);
const id2 = ksuid.KSUID.random(prng.random());

// Sequence for ordered KSUIDs
var seq = ksuid.Sequence.init(ksuid.KSUID.generate());
const next_id = try seq.next();

// Compressed set
const set = ksuid.CompressedSet.compress(&.{id, id2});
var it = set.iter();
while (it.next()) |k| {
    std.debug.print("{s}\n", .{k.string()});
}
```
