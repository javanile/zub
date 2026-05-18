---
title: urg_library_zig
description: URG library ported to the Zig build system
license: MIT
author: JurMax
author_github: JurMax
repository: https://github.com/JurMax/urg_library_zig
keywords:
  - laser
  - lidar
date: 2026-05-14
updated_at: 2026-05-14T14:28:10+00:00
last_sync: 2026-05-14T14:28:10Z
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
permalink: /packages/JurMax/urg_library_zig/
---

# urg_library_zig

This is a port of the [URG library](https://github.com/UrgNetwork/urg_library) to the [Zig](https://ziglang.org/) build system. It does not provide any Zig bindings.

## How to use it

Run any of the samples:

```bash
zig build get_distance
zig build get_distance_handshake
zig build get_distance_intensity
zig build get_multiecho
zig build get_multiecho_intensity
zig build sync_time_stamp
zig build sensor_parameter
zig build calculate_xy
zig build find_port
zig build timeout_test
zig build reboot_test
zig build angle_convert_test
```

Or any of the C++ samples:

```bash
zig build -Dcpp get_distance
zig build -Dcpp get_distance_handshake
zig build -Dcpp get_distance_intensity
zig build -Dcpp get_multiecho
zig build -Dcpp get_multiecho_intensity
zig build -Dcpp sync_time_stamp
zig build -Dcpp sensor_parameter
```

### As a library

First, fetch this repository:

```sh
zig fetch --save git+https://github.com/JurMax/urg_library_zig
```

Next, add it to your `build.zig`:

```zig
const urg_dependency = b.dependency("urg_library_zig", .{
    .target = target,
    .optimize = optimize,
    .cpp = false, // Set to true to use the C++ bindings.
});
exe.root_module.linkLibrary(urg_dependency.artifact("urg_library"));
```

This will add the URG library and headers to `exe`.
