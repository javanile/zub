---
title: lru
description: LRU cache for zig
license: NOASSERTION
author: loftafi
author_github: loftafi
repository: https://github.com/loftafi/lru
keywords:
date: 2026-09-19
updated_at: 2026-09-19T23:07:19+00:00
last_sync: 2026-09-19T23:07:19Z
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
permalink: /packages/loftafi/lru/
---

## LRU

An LRU cache for zig projects. Compatible with Zig 0.17-master. Use previous
commit for Zig 0.14

This code is for my personal use, and works for my purposes. There is no
guarantee that it will be suitable and reliable for your purposes. The
code is released under the MIT licence, you are free to use it, but
strongly urged to fully test that the code functions correctly for your
use cases.

## How to use

LRU caches are usually expected to automatically free objects when the cache
is full. This example demonstrates how to provide an optional callback function
to free an object.

```zig
/// Implement a `destroy` function.
const Sample = struct {
    age: u8 = 10,
    pub const Self = @This();
    pub fn destroy(self: *Self, gpa: Allocator) void {
        gpa.destroy(self);
    }
};
```

Create an LRU cache that holds a maximum of 100 objects. 

```zig
var lru = LRU(u32, *Sample).init(100);
defer lru.deinit(allocator);
// Tell the lru cache to call the destroy function on free:
lru.entry_dealloc = Sample.destroy;
```

Put and get items from the cache:
```zig
const sample = try allocator.create(Sample);
sample.*.age = 20;

const sample2 = try allocator.create(Sample);
sample2.*.age = 30;

try lru.put(allocator, io, 20, sample);
try lru.put(allocator, io, 30, sample2);
try lru.put(allocator, io, 40, sample3);

if(try lru.get(io, 20)) |entry| {
    std.log.info("Age: {d}", .{entry.age});
}
```

## Strings as keys

If you wish to use strings as keys, you can hash your string key into a u64.
This is exactly how zigs `StringHashMap` operates.


```zig
var lru = LRU(u64, *Sample).init(100);
defer lru.deinit(allocator);

const key = std.hash.Wyhash.hash(0, "andrew@example.com");
try lru.put(allocator, io, key, sample);
```
