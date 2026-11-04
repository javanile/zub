---
title: gld-kiln-zig
description: From-scratch Kiln wire format codec for Zig
license: MIT
author: leo-gan
author_github: leo-gan
repository: https://github.com/leo-gan/gld-kiln-zig
keywords:
  - binary-format
  - kiln
  - serialization
  - serializer
date: 2026-11-01
category: data-formats
updated_at: 2026-11-01T07:11:59+00:00
last_sync: 2026-11-01T07:11:59Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 3
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/leo-gan/gld-kiln-zig/
---

# gld-kiln-zig

A from-scratch Kiln codec for Zig. The runtime and the code generator are Zig. They do not wrap, link, or vendor a C, C++, or Rust Kiln library.

`testdata/reference/kiln_ref.py` is a test oracle for Frozen values. It is not used at run time.

This repository is a standalone library.

Documentation: [Why Kiln](https://leo-gan.github.io/gld-kiln-zig/why-kiln/),
[Instructions](https://leo-gan.github.io/gld-kiln-zig/instructions/),
[Examples](https://leo-gan.github.io/gld-kiln-zig/examples/),
[Techniques](https://leo-gan.github.io/gld-kiln-zig/techniques/),
[Test data](https://leo-gan.github.io/gld-kiln-zig/test-data/).

## Install

```bash
zig fetch --save git+https://github.com/leo-gan/gld-kiln-zig
```

The import name is `kiln`. The generator command is `gld-kilngen-zig`.

```zig
const kiln = @import("kiln");

const schema = try kiln.parseTypeText(arena, "struct{x:i32,y:i32}");
const fields = [_]kiln.FieldValue{
    .{ .name = "x", .value = .{ .int = 9 } },
    .{ .name = "y", .value = .{ .int = -4 } },
};
const raw = try kiln.encode(gpa, schema, .{ .structure = &fields }, .{});
defer gpa.free(raw);
var back = try kiln.decode(gpa, schema, raw, .{});
defer back.deinit(gpa);
```

Build the generator from a checkout with `zig build`. Zig 0.16.0 is the minimum version.

## License

MIT. Copyright (c) 2026 Leonid Ganeline.
