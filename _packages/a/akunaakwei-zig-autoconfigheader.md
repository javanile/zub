---
title: zig-autoconfigheader
description: compile checks for config header
license: Zlib
author: akunaakwei
author_github: akunaakwei
repository: https://github.com/akunaakwei/zig-autoconfigheader
keywords:
date: 2026-08-02
updated_at: 2026-08-02T05:57:39+00:00
last_sync: 2026-08-02T05:57:39Z
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
permalink: /packages/akunaakwei/zig-autoconfigheader/
---

# Auto Config Header
Adds the ability for compile checks (e.g. header exists or function exists) to the config header of the zig build system.

## Usage
Add this package as a dependency in your `build.zig.zon`, then you can use it as followed:
```zig
const std = @import("std");
const AutoConfigHeaderStep = @import("autoconfigheader").AutoConfigHeaderStep;

pub fn build(b: *std.Build) void {
    // ...
    const config_step = AutoConfigHeaderStep.create(b, target, .{ .style = .{ .cmake = b.path("config.h.in") } });

    // access for non compile checked values
    config_step.config_header.addValues(.{
        .SIZEOF_OFF_T = 4,
        .SIZEOF_SIZE_T = 8,
    });

    // check if a header exists
    config_step.addHaveHeader("HAVE_STRINGS_H", "strings.h");

    // check if a function exists
    config_step.addHaveFunction("HAVE_STRCASECMP", "strcasecmp(NULL, NULL)", &.{"strings.h"});
    // ...

    // add the config header to your executable or library
    exe.addConfigHeader(config_step.config_header);
}
```
