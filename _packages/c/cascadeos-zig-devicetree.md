---
title: zig-devicetree
description: A read-only Flattened Device Tree (DTB) API.
license: BSD-2-Clause
author: CascadeOS
author_github: CascadeOS
repository: https://github.com/CascadeOS/zig-devicetree
keywords:
  - device-tree
  - devicetree
  - dtb
  - fdt
date: 2026-04-20
updated_at: 2026-04-20T11:32:07+00:00
last_sync: 2026-04-20T11:32:07Z
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
permalink: /packages/CascadeOS/zig-devicetree/
---

# zig-devicetree

A read-only Flattened Devicetree (DTB) API.

None of the API requires allocation except the various list builders in `Property.Value` which are completely optional.

Compatible with [Devicetree Specification v0.4](https://github.com/devicetree-org/devicetree-specification/releases/tag/v0.4).

[Auto-generated docs](https://cascadeos.github.io/zig-devicetree/)

This started as a wrapper around [libfdt](https://github.com/dgibson/dtc/tree/main/libfdt) but is now a fresh implementation.

## Installation

Add the dependency to `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/CascadeOS/zig-devicetree
```

Then add the following to `build.zig`:

```zig
const devicetree_dep = b.dependency("devicetree", .{});
exe.root_module.addImport("DeviceTree", devicetree_dep.module("DeviceTree"));
```
