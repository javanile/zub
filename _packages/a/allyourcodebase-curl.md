---
title: curl
description: curl ported to the zig build system
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/curl
keywords:
date: 2026-04-16
updated_at: 2026-04-16T22:34:14+00:00
last_sync: 2026-04-16T22:34:14Z
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
permalink: /packages/allyourcodebase/curl/
---

[![CI](https://github.com/allyourcodebase/curl/actions/workflows/ci.yaml/badge.svg)](https://github.com/allyourcodebase/curl/actions)

# curl

This is [curl](https://github.com/curl/curl), packaged for [Zig](https://ziglang.org/).

## Installation

> [!WARNING]
>
> Curl depends on https://github.com/allyourcodebase/openssl which currently doesn't work on macOS. Consider using a different ssl implementation.

### Standalone library (libcurl) and command-line tool (curl)

```bash
git clone https://github.com/allyourcodebase/curl
cd curl
zig build -Doptimize=ReleaseFast
```

The library and CLI tool can be found in the newly created `./zig-out` directory. The `zig build run` build step may be used to directly run curl.

#### Avoid system dependencies

By default, curl requires some system dependencies that have not been ported to the zig build system yet. These dependencies may be either manually installed on the host system or disabled with the following build command:

```bash
# Windows
zig build -Doptimize=ReleaseFast -Dlibpsl=false -Dlibssh2=false -Dlibidn2=false -Dnghttp2=false
# Posix
zig build -Doptimize=ReleaseFast -Dlibpsl=false -Dlibssh2=false -Dlibidn2=false -Dnghttp2=false -Ddisable-ldap
```

### Zig Build System

First, update your `build.zig.zon`:

```
# Initialize a `zig build` project if you haven't already
zig init
zig fetch --save git+https://github.com/allyourcodebase/curl.git
```

You can then import curl in your `build.zig` with:

```zig
const curl_dependency = b.dependency("curl", .{
    .target = target,
    .optimize = optimize,
});

// A custom `artifact` function is provided because the build system
// provides no way to differentiate between the library (libcurl) and
// the command-line tool (curl) since they are both named "curl" in
// the build system.
// See https://github.com/ziglang/zig/issues/20377
const curlExe = @import("curl").artifact(curl_dependency, .exe);
const libCurl = @import("curl").artifact(curl_dependency, .lib);

your_exe.root_module.linkLibrary(libCurl);
```

#### Avoid system dependencies

By default, curl requires some system dependencies that have not been ported to the zig build system yet. These dependencies may be either manually installed on the host system or disabled with the following change to the `build.zig`:

```zig
const curl_dependency = b.dependency("curl", .{
    .target = target,
    .optimize = optimize,
    .libpsl = false,
    .libssh2 = false,
    .libidn2 = false,
    .nghttp2 = false,
    .@"disable-ldap" = true,
});
```
