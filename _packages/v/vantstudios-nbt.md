---
title: Nbt
description: NBT(Named Binary Tag) library for Zig
license: MIT
author: VantStudios
author_github: VantStudios
repository: https://github.com/VantStudios/Nbt
keywords:
  - bedrock
date: 2026-06-17
updated_at: 2026-06-17T07:12:27+00:00
last_sync: 2026-06-17T07:12:27Z
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
permalink: /packages/VantStudios/Nbt/
---

# Nbt

NBT (Named Binary Tag) library for Zig 0.16.0.

## Installation

Add the dependency with `zig fetch`:

```sh
zig fetch --save git+https://github.com/VantStudios/Nbt.git
```

Then in your `build.zig`:

```zig
const nbt_dep = b.dependency("nbt", .{
    .target = target,
    .optimize = optimize,
});

exe.root_module.addImport("nbt", nbt_dep.module("nbt"));
```

## Usage

```zig
const nbt = @import("nbt");
```


## License

[MIT](LICENCE)
