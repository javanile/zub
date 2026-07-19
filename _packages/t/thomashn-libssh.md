---
title: libssh
description: libssh ported to the zig build system
license: MIT
author: thomashn
author_github: thomashn
repository: https://github.com/thomashn/libssh
keywords:
date: 2026-07-19
updated_at: 2026-07-19T08:40:22+00:00
last_sync: 2026-07-19T08:40:22Z
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
permalink: /packages/thomashn/libssh/
---

# libssh
[![Zig Version](https://img.shields.io/badge/Zig-0.16.0-orange.svg?logo=zig)](https://ziglang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This is [libssh](https://www.libssh.org/),
packaged for [Zig](https://ziglang.org/).

## How to use it
First, update your `build.zig.zon`:

```
zig fetch --save git+https://github.com/thomashn/libssh#<commit|tag>
```

Next, add this snippet to your `build.zig` script:
```zig
const libssh_dep = b.dependency("libssh", .{
    .target = target,
    .optimize = optimize,
    // The Zig mbedtls is preferred because its build replacement
    // is more complete than the OpenSSL one. OpenSSL only works
    // as a static build in Linux.
    .mbedtls = true,
});
your_compilation.linkLibrary(libssh_dep.artifact("libssh"));
```

This will provide libssh as a static library to `your_compilation`.

## Run tests
Run the original libssh [cmocka](https://cmocka.org/) based unittests. For now,
tests are limited to those that do not require external processes like sshd and
Putty.
```bash
zig build test -Dmbedtls=true
```
