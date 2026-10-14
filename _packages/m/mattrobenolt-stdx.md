---
title: stdx
description: A small library of Zig standard-library extensions and data structures, built on Zig 0.16.
license: MIT
author: mattrobenolt
author_github: mattrobenolt
repository: https://github.com/mattrobenolt/stdx
keywords:
date: 2026-10-14
updated_at: 2026-10-14T14:56:45+00:00
last_sync: 2026-10-14T14:56:45Z
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
permalink: /packages/mattrobenolt/stdx/
---

# stdx

A small library of Zig standard-library extensions and data structures,
built on Zig 0.16.

The same helpers kept showing up copy-pasted across projects: strict
number parsing, IPv4 and CIDR handling, fixed-capacity buffers, a bounded
writer, a slab allocator. stdx is where they live now — tested
standalone, no dependencies.

The modules mirror the std namespaces they extend (`memx`, `fmtx`,
`netx`, `posixx`, `heapx`); the data structures (`ArrayBuffer`,
`SliceBuffer`, `BoundedWriter`, `multi_array`) sit at the top level. The
source is the documentation: every type and function carries doc
comments that render with `zig doc`, alongside its own tests.

## Use it

```
zig fetch --save git+https://github.com/mattrobenolt/stdx.git
```

Then import it as `stdx` in your build, as normal.

## Work on it

```
zig build test
```

Zig 0.16. `nix develop` gives you the toolchain, ziglint, and zigdoc.

MIT licensed — see `LICENSE`. A few pieces were adapted from other code;
`THIRD_PARTY.md` says which, and under what terms.

## Related projects

Other pieces of the same effort — low-level primitives Zig is missing:

- [fastmem](https://github.com/mattrobenolt/fastmem-zig) — SIMD
  memcpy, memmove, and memset
- [ztls](https://github.com/mattrobenolt/ztls) — a TLS library
- [zcompress](https://github.com/mattrobenolt/zcompress) — fast,
  self-contained compression codecs
- [ztest](https://github.com/mattrobenolt/ztest) — a test runner that
  writes plain text instead of a TUI
- [zig-benchmark](https://github.com/mattrobenolt/zig-benchmark) — a
  benchmark harness
