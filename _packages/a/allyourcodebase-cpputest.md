---
title: cpputest
description: Package for CppUTest
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/cpputest
keywords:
date: 2026-09-15
updated_at: 2026-09-15T08:34:51+00:00
last_sync: 2026-09-15T08:34:51Z
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
permalink: /packages/allyourcodebase/cpputest/
---

# CppUTest Zig

Using zig build system to build [CppUTest](https://github.com/cpputest/cpputest) unit test library.

**ATTENTION** this port only support "*Plateform/Gcc*" with stdlib enable."

## Adding It to your project

First update your *build.zig.zon* with:

```bash
zig fetch --save git+https://github.com/lcp5y3/cpputest-zig.git#b409129f4472213c222ce861e4f891fefa4d1c5e
```

After that you can link `CppUTest` with your project by adding the following
lines to your `build.zig`

```zig
const cpputest_dep = b.dependency("cpputest", .{
  .target = target,
  .optimize = optimize,
});

exe.root_module.linkLibrary(cpputest_dep.artifact("CppUTest"));
exe.root_module.linkLibrary(cpputest_dep.artifact("CppUTestExt"));
```

## Building the lib

If you only want to build CppUTest to get .a and header, run:

```bash
zig build
```
