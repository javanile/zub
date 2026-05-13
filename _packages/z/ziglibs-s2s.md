---
title: s2s
description: A zig binary serialization format.
license: MIT
author: ziglibs
author_github: ziglibs
repository: https://github.com/ziglibs/s2s
keywords:
  - binary-data
  - serialization
  - serialization-library
date: 2026-05-06
category: data-formats
updated_at: 2026-05-06T13:30:18+00:00
last_sync: 2026-05-06T13:30:18Z
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
permalink: /packages/ziglibs/s2s/
---

# struct to stream | stream to struct

A Zig binary serialization format and library.

![Project logo](design/logo.png)

## Features

- Convert (nearly) any Zig runtime datatype to binary data and back.
- Computes a stream signature that prevents deserialization of invalid data.
- No support for graph like structures. Everything is considered to be tree data.

**Unsupported types**:

- All `comptime` only types
- Unbound pointers (c pointers, pointer to many)
- `volatile` pointers
- Untagged or `external` unions
- Opaque types
- Function pointers
- Frames

## API

The library itself provides only some APIs, as most of the serialization process is not configurable.

```zig
/// Serializes the given `value: T` into the `stream`.
/// - `stream` is a instance of `std.Io.Writer`
/// - `T` is the type to serialize
/// - `value` is the instance to serialize.
fn serialize(stream: *std.Io.Writer, comptime T: type, value: T) std.Io.Writer.Error!void;

/// Deserializes a value of type `T` from the `stream`.
/// - `stream` is a instance of `std.Io.Reader`
/// - `T` is the type to deserialize
fn deserialize(stream: *std.Io.Reader, comptime T: type) (std.Io.Reader.Error || error{UnexpectedData,EndOfStream})!T;

/// Deserializes a value of type `T` from the `stream`.
/// - `stream` is a instance of `std.Io.Reader`
/// - `T` is the type to deserialize
/// - `allocator` is an allocator require to allocate slices and pointers.
/// Result must be freed by using `free()`.
fn deserializeAlloc(stream: *std.Io.Reader, comptime T: type, allocator: std.mem.Allocator) (std.Io.Reader.Error || error{ UnexpectedData, OutOfMemory,EndOfStream })!T;

/// Releases all memory allocated by `deserializeAlloc`.
/// - `allocator` is the allocator passed to `deserializeAlloc`.
/// - `T` is the type that was passed to `deserializeAlloc`.
/// - `value` is the value that was returned by `deserializeAlloc`.
fn free(allocator: std.mem.Allocator, comptime T: type, value: T) void;
```

## Usage and Development

### Adding the library

Just add the `s2s.zig` as a package to your Zig project. It has no external dependencies.

### Running the test suite

```sh-session
[user@host s2s]$ zig test s2s.zig
All 3 tests passed.
[user@host s2s]$
```

## Project Status

Most of the serialization/deserialization is implemented for the _trivial_ case.

Pointers/slices with non-standard alignment aren't properly supported yet.
