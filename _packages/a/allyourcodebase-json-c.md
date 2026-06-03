---
title: json-c
description: json-c ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/json-c
keywords:
date: 2026-05-30
updated_at: 2026-05-30T21:03:09+00:00
last_sync: 2026-05-30T21:03:09Z
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
permalink: /packages/allyourcodebase/json-c/
---

# `build.zig` for json-c

Provides a package to be used by the zig package manager for C programs.

## Status

For now the hard-coded config assumes linux.

| Refname  | json-c version         | Zig `0.16.x` | Zig `0.15.x` | Zig `0.14.x` | Zig `0.13.x` | Zig `0.12.x` |
|----------|------------------------|--------------|--------------|--------------|--------------|--------------|
| `0.18+3` | `json-c-0.18-20240915` | ✅           | ✅           | ❌           | ❌           | ❌           |
| `0.18+2` | `json-c-0.18-20240915` | ❌           | ✅           | ✅           | ❌           | ❌           |
| `0.18`   | `json-c-0.18-20240915` | ❌           | ❌           | ❌           | ✅           | ✅           |
| `0.17`   | `json-c-0.17-20230812` | ❌           | ❌           | ❌           | ✅           | ✅           |

## Use

Add the dependency in your `build.zig.zon` by running the following command:
```bash
zig fetch --save git+https://github.com/allyourcodebase/json-c#master
```

Then, in your `build.zig`:
```zig
const jsonc = b.dependency("jsonc", { .target = target, .optimize = optimize });
const libjsonc = jsonc.artifact("json-c");
// wherever needed:
exe.linkLibrary(libjsonc);
```
