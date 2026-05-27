---
title: spsc-queue
description: Fast bounded SPSC queue written in Zig
license: MIT
author: freref
author_github: freref
repository: https://github.com/freref/spsc-queue
keywords:
  - spsc-queue
date: 2026-05-24
updated_at: 2026-05-24T20:00:25+00:00
last_sync: 2026-05-24T20:00:25Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/freref/spsc-queue/
---

# spsc-queue
A single producer single consumer wait-free and lock-free fixed size queue written in Zig. Inspired by [rigtorp's](https://github.com/rigtorp/SPSCQueue/tree/master) implementation in C++. This implementation is faster than [rigtorp/SPSCQueue](https://github.com/rigtorp/SPSCQueue/tree/master),
[*boost::lockfree::spsc*](https://www.boost.org/doc/libs/1_76_0/doc/html/boost/lockfree/spsc_queue.html), [cdolan/zig-spsc-ring](https://github.com/cdolan/zig-spsc-ring.git), and [*folly::ProducerConsumerQueue*](https://github.com/facebook/folly/blob/master/folly/docs/ProducerConsumerQueue.md).

## Implementation
This library provides a **managed** and an **unmanaged** version of the queue, following the Zig standard library conventions. There are **2 implementations** of the queue:
- One that uses a slack space in the buffer and allows the user to set any capacity.
- One that enforces power-of-2 (po2) capacity and is faster due to less expensive arithmetic operations.

The user can choose which implementation they want to use by setting the ``enforce_po2`` flag to ``true`` when defining the queue type. I opted for this interface over detecting if the capacity is po2, because the flag makes the choice explicit and known at comptime. It's clear to the user that there are two distinct implementations with different trade-offs. I borrowed this idea from [joadnacer/atomic_queue](https://github.com/joadnacer/atomic_queues.git).

## Usage
You can find a basic example [here](./src/example.zig). You can run this example with the following command:
```sh
zig build run-example
```

**Unmanaged version:**
```zig
pub fn initBuffer(buffer: []T) Self
pub fn initCapacity(allocator: std.mem.Allocator, num: usize) !Self
pub fn deinit(self: *Self, allocator: std.mem.Allocator) void
```

**Managed version:**
```zig
pub fn initCapacity(allocator: std.mem.Allocator, num: usize) !Self
pub fn fromOwnedSlice(allocator: std.mem.Allocator, buffer: []T) Self
pub fn deinit(self: *Self) void
```

**General API:**
```zig
pub fn isEmpty(self: *Self) bool
pub fn size(self: *Self) usize
pub fn push(self: *Self, value: T) void
pub fn tryPush(self: *Self, value: T) bool
pub fn front(self: *Self) ?*T
pub fn pop(self: *Self) void
```
