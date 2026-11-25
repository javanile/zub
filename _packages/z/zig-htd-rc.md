---
title: rc
description: Reference-counted data container for Zig
license: ""
author: zig-htd
author_github: zig-htd
repository: https://github.com/zig-htd/rc
keywords:
date: 2026-11-25
updated_at: 2026-11-25T05:27:27+00:00
last_sync: 2026-11-25T05:27:27Z
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
permalink: /packages/zig-htd/rc/
---

# rc

rc provides reference-counted data containers that solve the problem of releasing data after it has been shared.

## Installation

Add the dependency to `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/zig-htd/rc
```

Add the module to `build.zig`:

```zig
const rc = b.dependency("rc", .{});
// ...
exe.root_module.addImport("rc", rc.module("rc"));
```

## Usage

Data that needs to be shared:

```zig
const Data = struct {
    bytes: []u8,

    /// Implements `rc.Interface.clone`
    pub fn clone(self: *const Data, allocator: Allocator) Allocator.Error!Data {
        // Return a deep-cloned copy
        return .{
            bytes = try allocator.dupe(u8, self.bytes)
        };
    }

    /// Implements `rc.Interface.release`
    pub fn release(self: *Data, allocator: Allocator) void {
        // Release memory (similar to deinit, or call your own deinit here)
        allocator.free(self.bytes);
        self.* = undefined;
    }
};
```

Increment the reference count and share it:

```zig
// Create a shared data type based on Data
const AtomicSharedData = rc.AtomicShared(Data);
// Create shared data
const data: Data = .{ .bytes = try allocator.dupe(u8, "some_bytes") };
var shared_data: AtomicSharedData = try .fromOwned(&data, allocator);
// var shared_data: AtomicSharedData = try .new(&data, allocator);  // Alternative: use `.new` to deep-clone the original data (the container owns the data)
// defer data.release(allocator);                                   // If `.new` is used, release the original data afterward

// Increment the reference count and send it to multiple consumers
for (consumer in consumers) {
    shared_data.retain();                   // Increment the reference count before sharing
    consumer.push(shared_data) catch {      // Data release will be handed over to consumer
        shared_data.release(allocator);     // Sharing failed; call release to undo this share
    }
}
```

Every consumer releases it uniformly, without having to consider whether another party has already released it:

```zig
for (consumer in consumers) {
    const shared_data: AtomicSharedData = try consumer.get();
    shared_data.release(allocator);         // Consumer releases it
}
```

Memory is released only when the counter inside the rc container reaches zero (that is, `Data.release` is actually called). Otherwise, `AtomicShared.release` only decreases the reference count.

## Other

This library also provides `AnyAtomicShared`, a container that can store shared data of any type. The data type only needs to implement `rc.Interface`. Usage is shown below:

```zig
// Create data of different types
var foo = try Foo.init(a, "FooData");
defer foo.deinit(a);
var bar = try Bar.init(a, "BarData");
defer bar.deinit(a);
// Wrap them in AnyAtomicShared
const shared_foo = try rc.AnyAtomicShared.new(a, &foo);
const shared_bar = try rc.AnyAtomicShared.new(a, &bar);
// Put them into one container
const list: [2]rc.AnyAtomicShared = .{ shared_foo, shared_bar };
for (list) |item| {
    // Even if the original data types of items differ, AnyAtomicShared
    // provides uniform primitives and type compatibility
    item.release(a);
}
```
