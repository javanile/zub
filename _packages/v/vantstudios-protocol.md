---
title: Protocol
description: Minecraft Bedrock protocol library for Zig
license: MIT
author: VantStudios
author_github: VantStudios
repository: https://github.com/VantStudios/Protocol
keywords:
  - bedrock
date: 2026-06-17
updated_at: 2026-06-17T07:12:50+00:00
last_sync: 2026-06-17T07:12:50Z
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
permalink: /packages/VantStudios/Protocol/
---

# Protocol

Minecraft Bedrock protocol library for Zig 0.16.0.

## Installation

Add the dependency with `zig fetch`:

```sh
zig fetch --save git+https://github.com/VantStudios/Protocol.git
```

Then in your `build.zig`:

```zig
const protocol_dep = b.dependency("protocol", .{
    .target = target,
    .optimize = optimize,
});

exe.root_module.addImport("Protocol", protocol_dep.module("Protocol"));
```

## Usage

```zig
const protocol = @import("Protocol");
```

## License

[MIT](LICENCE)
