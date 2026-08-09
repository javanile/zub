---
title: zprobe
description: A tracing library for Zig, makes use of USDT for zero cost probe points in release builds
license: MIT
author: M3dry
author_github: M3dry
repository: https://github.com/M3dry/zprobe
keywords:
date: 2026-08-01
updated_at: 2026-08-01T13:06:41+00:00
last_sync: 2026-08-01T13:06:41Z
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
permalink: /packages/M3dry/zprobe/
---

# zprobe

A tracing library for Zig, makes use of USDT for zero cost probe points in release builds

## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .zprobe = .{
        .url = "https://github.com/M3dry/zprobe/archive/refs/heads/main.tar.gz",
    },
},
```
