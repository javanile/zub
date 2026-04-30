---
title: ChibiHash-zig
description: ChibiHash in Zig - a small, fast 64-bit hash function
license: MIT
author: thevilledev
author_github: thevilledev
repository: https://github.com/thevilledev/ChibiHash-zig
keywords:
  - hash-functions
date: 2026-04-22
updated_at: 2026-04-22T18:19:38+00:00
last_sync: 2026-04-22T18:19:38Z
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
permalink: /packages/thevilledev/ChibiHash-zig/
---

# ChibiHash64-Zig

A Zig port of [ChibiHash64](https://github.com/N-R-K/ChibiHash) - a small, fast 64-bit hash function. See the article [ChibiHash: A small, fast 64-bit hash function](https://nrk.neocities.org/articles/chibihash) for more information.

All credit for the algorithm goes to [N-R-K](https://github.com/N-R-K).

## Features

- Simple 64-bit hash function
- Supports both v1 and v2 of the hash function
- HashMap implementation
- Thoroughly tested with known test vectors

## Usage

```
const std = @import("std");
const ChibiHash64v1 = @import("chibihash64_v1.zig");
const ChibiHash64v2 = @import("chibihash64_v2.zig");

// Basic hashing v1
const hash = ChibiHash64v1.hash("Hello, world!", 0);

// Using HashMap v1
var map = ChibiHash64v1.HashMap([]const u8, i32).init(allocator);
defer map.deinit();

// Basic hashing v2
const hash = ChibiHash64v2.hash("Hello, world!", 0);

// Using HashMap v2
var map = ChibiHash64v2.HashMap([]const u8, i32).init(allocator);
defer map.deinit();
```

See `example/example.zig` for a complete example. Run it with `zig build run-example`.

## License

MIT.
