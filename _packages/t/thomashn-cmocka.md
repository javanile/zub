---
title: cmocka
description: cmocka build system implemented in Zig
license: MIT
author: thomashn
author_github: thomashn
repository: https://github.com/thomashn/cmocka
keywords:
date: 2026-07-18
updated_at: 2026-07-18T14:56:44+00:00
last_sync: 2026-07-18T14:56:44Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/thomashn/cmocka/
---

# cmocka
[![Zig Version](https://img.shields.io/badge/Zig-0.16.0-orange.svg?logo=zig)](https://ziglang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This is [cmocka](https://cmocka.org/),
packaged for [Zig](https://ziglang.org/).

## How to use it
First, update your `build.zig.zon`:

```bash
zig fetch --save git+https://github.com/thomashn/cmocka#<commit>
```

Next, add this snippet to your `build.zig` script:
```zig
const cmocka_dep = b.dependency("cmocka", .{
    .target = target,
    .optimize = optimize,
});
your_compilation.linkLibrary(cmocka_dep.artifact("cmocka"));
```

This will provide cmocka as a static library to `your_compilation`.

## How to run tests
To compile and run the comprehensive unit test suite:

```bash
zig build test
```
