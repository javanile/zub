---
title: boringssl
description: boringssl packaged with Zig
license: Zlib
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/boringssl
keywords:
date: 2026-07-14
updated_at: 2026-07-14T07:59:06+00:00
last_sync: 2026-07-14T07:59:06Z
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
permalink: /packages/allyourcodebase/boringssl/
---

# BoringSSL

This is [BoringSSL](https://github.com/google/boringssl), packaged for Zig.

## Installation

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/lukaskastern/boringssl.git
```

You can then import `boringssl` in your `build.zig` with:

```zig
const boringssl_dependency = b.dependency("boringssl", .{
    .target = target,
    .optimize = optimize,
});
your_exe.linkLibrary(boringssl_dependency.artifact("bcm"));
your_exe.linkLibrary(boringssl_dependency.artifact("ssl"));
your_exe.linkLibrary(boringssl_dependency.artifact("crypto"));
```

And use the library like this:
```zig
const ssl = @cImport({
    @cInclude("openssl/ssl.h");
});

const ctx = ssl.EVP_CIPHER_CTX_new();
...
...
```

## Notes

### Windows support:
At the moment only x86_64-windows-gnu is functional. MSVC doesn't work!

GNU doesn't seem an official target by boringssl for windows which is why we need the [patch](patches/p256_gnuc.patch).

### Zig Version
The target zig version is 0.16.0
