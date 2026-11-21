---
title: zig-bplus-tree
description: A robust, generic, and idiomatic B+ tree implementation in Zig (0.15+). This package is designed for high performance, reliability, and ease of use perfect for use as a dependency or as a learning resource for advanced data structures in Zig.
license: MIT
author: dayvster
author_github: dayvster
repository: https://github.com/dayvster/zig-bplus-tree
keywords:
  - zig-libary
  - zig-pkg
date: 2026-06-22
updated_at: 2026-06-22T19:27:01+00:00
last_sync: 2026-06-22T19:27:01Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 1
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/dayvster/zig-bplus-tree/
unsafe: true
unsafe_reason: "contains a URL pointing to a .zip file"
---

# Zig B+ Tree

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Zig](https://img.shields.io/badge/zig-0.17%2B-f7a41d?logo=zig)](https://ziglang.org/)

A robust, generic B+ tree implementation in Zig. High performance, memory-safe, and designed for both production use and learning.

## What is a B+ Tree?

A self-balancing tree data structure for fast sorted access. All values live in leaf nodes; internal nodes store only keys for navigation. Used in databases and filesystems.

## Features

- **Generic**: Any comparable key/value type
- **Self-balancing**: O(log n) operations
- **Memory-safe**: Proper allocator patterns
- **Tested**: Full test coverage
- **MIT licensed**: Free for any use

## Installation

**With `zig fetch`:**
```sh
zig fetch --save git+https://github.com/dayvster/zig-bplus-tree
```

Add to `build.zig.zon`:
```json
"bplustree": { "url": "https://github.com/dayvster/zig-bplus-tree/archive/refs/heads/main.zip" }
```

Then import: `const BPlusTree = @import("bplustree").BPlusTree(i32, 4);`

**Or copy manually:** `src/bplustree.zig` to your project.

## Usage

```zig
var tree = BPlusTree(i32, i32, 4).init(allocator);  // MemoryPool strategy (faster)
defer tree.deinit();

try tree.insert(42, 100);
const found = tree.search(42);
```

See `examples/` for more patterns and stress tests.

## Development

- **Build**: `zig build`
- **Test**: `zig build test`
- **Format**: `zig fmt src/`

## Contributing

Issues and PRs welcome! Start a discussion or open an issue on GitHub.

## License
MIT. See [LICENSE](./LICENSE).
