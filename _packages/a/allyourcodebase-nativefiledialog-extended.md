---
title: nativefiledialog-extended
description: nativefiledialog-extended ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/nativefiledialog-extended
keywords:
date: 2026-08-17
updated_at: 2026-08-17T17:15:44+00:00
last_sync: 2026-08-17T17:15:44Z
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
permalink: /packages/allyourcodebase/nativefiledialog-extended/
---

[![CI](https://github.com/allyourcodebase/nativefiledialog-extended/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/nativefiledialog-extended/actions)

# nativefiledialog-extended

This is [nativefiledialog-extended](https://github.com/btzy/nativefiledialog-extended), packaged for [Zig](https://ziglang.org/).

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/nativefiledialog-extended.git#1.3.0
```

You can then import `nativefiledialog-extended` in your `build.zig` with:

```zig
const nfd_dependency = b.dependency("nativefiledialog-extended", .{
    .target = target,
    .optimize = optimize,
});
your_exe.linkLibrary(nfd_dependency.artifact("nfd"));
```

## Dependencies

See https://github.com/btzy/nativefiledialog-extended/tree/v1.3.0#dependencies
