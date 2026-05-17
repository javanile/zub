---
title: SVT-AV1
description: SVT-AV1 on the Zig Build System
license: BSD-3-Clause-Clear
author: KNnut
author_github: KNnut
repository: https://github.com/KNnut/SVT-AV1
keywords:
  - av1
  - svt-av1
date: 2026-05-17
updated_at: 2026-05-17T10:35:40+00:00
last_sync: 2026-05-17T10:35:40Z
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
permalink: /packages/KNnut/SVT-AV1/
---

# SVT-AV1

[SVT-AV1](https://gitlab.com/AOMediaCodec/SVT-AV1) on the [Zig Build System](https://ziglang.org/learn/build-system/).

## Usage

Add this package to `build.zig.zon`:

```sh
zig fetch --save=SVT-AV1 git+https://github.com/KNnut/SVT-AV1
```

And then import `SVT-AV1` in `build.zig` with:

```zig
const svt_av1_dep = b.dependency("SVT-AV1", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.linkLibrary(svt_av1_dep.artifact("SvtAv1Enc"));
```
