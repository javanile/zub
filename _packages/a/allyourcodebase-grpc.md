---
title: grpc
description: "libgrpc's core ported to the Zig build system"
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/grpc
keywords:
date: 2026-04-26
updated_at: 2026-04-26T09:46:15+00:00
last_sync: 2026-04-26T09:46:15Z
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
permalink: /packages/allyourcodebase/grpc/
---

# gRPC packaged for the Zig build system

## Status

| Architecture \ OS | Linux | MacOS |
|:------------------|:-----:|:-----:|
| x86_64            | ✅    | ✅    |
| arm 64            | ✅    | ✅    |

| Refname    | libGRPC version        | Core version | Zig `0.16.x` | Zig `0.15.x` |
|:-----------|:-----------------------|-------------:|:------------:|:------------:|
| `1.80.0`   | `v1.80.0` "glimmering" |     `53.0.0` | ✅           | ✅           |
| `1.78.1+1` | `v1.78.1` "gusty"      |     `52.0.0` | ✅           | ✅           |
| `1.76.0+2` | `v1.76.0` "genuine"    |     `51.0.0` | ✅           | ✅           |

## Use

Add the dependency to your `build.zig.zon` by running the following command:
```zig
zig fetch --save git+https://github.com/allyourcodebase/grpc#master
```

Then, in your `build.zig`:
```zig
const grpc = b.dependency("grpc", {
	.target = target,
	.optimize = optimize,
	.link_mode = .dynamic,
	.pic = true,
});

// to use from Zig:
mod.addImport("cgrpc", grpc.module("cgrpc"));

// to use from C:
exe.linkLibrary(grpc.artifact("grpc"));
```

## Options

```
  -Dlink_mode=[enum]           Compile static or dynamic libraries. Defaults to dynamic
                                 Supported Values:
                                   static
                                   dynamic
  -Dpic=[bool]                 Produce Position Independent Code. Defaults to true when link_mode is dynamic
```
