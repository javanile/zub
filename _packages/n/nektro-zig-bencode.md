---
title: zig-bencode
description: Bencode parser for Zig.
license: MIT
author: nektro
author_github: nektro
repository: https://github.com/nektro/zig-bencode
keywords:
  - bencode
date: 2026-10-21
updated_at: 2026-10-21T06:47:32+00:00
last_sync: 2026-10-21T06:47:32Z
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
permalink: /packages/nektro/zig-bencode/
---

# zig-bencode

![loc](https://sloc.xyz/github/nektro/zig-bencode)
[![license](https://img.shields.io/github/license/nektro/zig-bencode.svg)](https://github.com/nektro/zig-bencode/blob/master/LICENSE)
[![nektro @ github sponsors](https://img.shields.io/badge/sponsors-nektro-purple?logo=github)](https://github.com/sponsors/nektro)
[![Zig](https://img.shields.io/badge/Zig-0.17-f7a41d)](https://ziglang.org/)
[![Zigmod](https://img.shields.io/badge/Zigmod-latest-f7a41d)](https://github.com/nektro/zigmod)

Bencode parser for Zig.

https://en.wikipedia.org/wiki/Bencode

https://www.bittorrent.org/beps/bep_0003.html#bencoding

## Usage

Add the following to the bottom of your `zigmod.yml`

```yml
dependencies:
  - src: git https://github.com/nektro/zig-bencode
```

In your code

```zig
const bencode = @import("bencode");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const alloc = &gpa.allocator;

    const file = @embedFile("./some/path/to.torrent");
    var buf = std.io.fixedBufferStream(file);
    const r = buf.reader();
    const ben = try bencode.parse(r, alloc);

    // do something with `ben`...
}
```
