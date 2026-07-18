---
title: zig-toml
description: Zig TOML (v1.0.0) parser
license: MIT
author: sam701
author_github: sam701
repository: https://github.com/sam701/zig-toml
keywords:
  - parser
  - toml
date: 2026-07-16
category: data-formats
updated_at: 2026-07-16T19:37:25+00:00
last_sync: 2026-07-16T19:37:25Z
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
permalink: /packages/sam701/zig-toml/
---

# zig-toml
[![Zig Docs](https://img.shields.io/badge/docs-zig-%23f7a41d)](https://sam701.github.io/zig-toml)

Zig [TOML v1.1.0](https://toml.io/en/v1.1.0) parser.

This is a top-down LL parser that parses directly into Zig structs.

## Features
* TOML Syntax
  * [x] Integers, hexadecimal, octal, and binary numbers
  * [x] Floats
  * [x] Booleans
  * [x] Comments
  * [x] Arrays
  * [x] Tables
  * [x] Array of Tables
  * [x] Inline Table
  * [x] Single-line strings
  * [x] String escapes (also unicode)
  * [x] Multi-line strings
  * [x] Multi-line string leading space trimming
  * [x] Trailing backslash in multi-line strings
  * [x] Date, time, date-time, time offset
* Struct mapping
  * [x] Mapping to structs
  * [x] Mapping to enums
  * [x] Mapping to slices
  * [x] Mapping to arrays
  * [x] Mapping to pointers
  * [x] Mapping to integer and floats with lower bit number than defined by TOML, i.e. `i16`, `f32`.
  * [x] Mapping to optional fields
  * [x] Mapping to HashMaps
* [ ] Serialization
    * [x] Basic types like integers, floating points, strings, booleans etc.
    * [x] Arrays
    * [x] Top level tables
    * [x] Sub tables
    * [x] Pointers
    * [x] Date, time, DateTime, time offset
    * [x] Enums
    * [x] Unions

## Using with the Zig package manager
Add `zig-toml` to your `build.zig.zon`
```
# For zig-master
zig fetch --save git+https://github.com/sam701/zig-toml

# For zig 0.16
zig fetch --save git+https://github.com/sam701/zig-toml#zig-0.16

# For zig 0.15
zig fetch --save git+https://github.com/sam701/zig-toml#zig-0.15
```

## Example
See [`example1.zig`](./examples/example1.zig) for the complete code that parses [`example.toml`](./examples/example1.toml)

Run it with `zig build examples`
```zig
// ....

const Address = struct {
    port: i64,
    host: []const u8,
};

const Config = struct {
    master: bool,
    expires_at: toml.DateTime,
    description: []const u8,

    local: *Address,
    peers: []const Address,
};

pub fn main(init: std.process.Init) anyerror!void {
    var parser = toml.Parser(Config).init(init.gpa);
    defer parser.deinit();

    var result = try parser.parseFile(init.io, "./examples/example1.toml");
    defer result.deinit();

    const config = result.value;
    std.debug.print("{s}\nlocal address: {s}:{}\n", .{ config.description, config.local.host, config.local.port });
    std.debug.print("peer0: {s}:{}\n", .{ config.peers[0].host, config.peers[0].port });
}
```

## Error Handling
TODO

## License
MIT
