---
title: ta-lib-zig
description: "Zig wrapper for TA-Lib (http://ta-lib.org)"
license: ""
author: TA-Lib
author_github: TA-Lib
repository: https://github.com/TA-Lib/ta-lib-zig
keywords:
date: 2026-07-03
updated_at: 2026-07-03T18:08:04+00:00
last_sync: 2026-07-03T18:08:04Z
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
permalink: /packages/TA-Lib/ta-lib-zig/
---

# TA-Lib

This is a Zig wrapper for [TA-LIB](http://ta-lib.org).

## Installation

1) Add ta-lib-zig as a dependency in your `build.zig.zon`:

```bash
zig fetch --save "git+https://github.com/ta-lib/ta-lib-zig#main"
```

2) In your `build.zig`, add the `ta-lib` module as a dependency you your program:

```zig
const ta_lib = b.dependency("ta_lib", .{
    .target = target,
    .optimize = optimize,
});

// the executable from your call to b.addExecutable(...)
exe.root_module.addImport("ta_lib", ta_lib.module("ta_lib"));
```
## Examples

A simple example using the Momentum indicator:

```zig
const ta = @import("ta_lib");

const prices = [_]f64{ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 };

const result = try ta.MOM(allocator, &prices, 5);
defer allocator.free(result);
```
