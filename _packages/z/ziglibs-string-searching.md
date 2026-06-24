---
title: string-searching
description: "String(not limited to []const u8)-searching algorithms in zig"
license: MIT
author: ziglibs
author_github: ziglibs
repository: https://github.com/ziglibs/string-searching
keywords:
  - bitap-algorithm
  - boyer-moore
date: 2026-06-19
updated_at: 2026-06-19T22:57:02+00:00
last_sync: 2026-06-19T22:57:02Z
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
permalink: /packages/ziglibs/string-searching/
---

# string-searching

![CI](https://github.com/ziglibs/zig-string-searching/workflows/CI/badge.svg)

Implementation of some string-search algorithms in
[zig](https://ziglang.org). Compatible with zig 0.13.0.

### Boyer-Moore string searching

Ported from the implementation in the Go standard library:
[strings/search.go](https://golang.org/src/strings/search.go).

### Bitap algorithm

Inspired by the code on the [Wikipedia
article](https://en.wikipedia.org/wiki/Bitap_algorithm).
