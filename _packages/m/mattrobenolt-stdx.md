---
title: stdx
description: Moved to baskingspot/stdx. Archived.
license: MIT
author: mattrobenolt
author_github: mattrobenolt
repository: https://github.com/mattrobenolt/stdx
keywords:
date: 2026-10-16
updated_at: 2026-10-16T16:22:33+00:00
last_sync: 2026-10-16T16:22:33Z
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
permalink: /packages/mattrobenolt/stdx/
---

# Moved to baskingspot/stdx

This repository is archived. stdx lives at [baskingspot/stdx](https://github.com/baskingspot/stdx), with its full history. The guide is at https://baskingspot.dev/stdx/.

This repository stopped at commit `87db8fa`. The module name is unchanged.

## Migrate

Fetch it from the new location:

```sh
zig fetch --save git+https://github.com/baskingspot/stdx
```

Your `build.zig` stays the same:

```zig
const stdx = b.dependency("stdx", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("stdx", stdx.module("stdx"));
```

If another package depends on the old URL, its `build.zig.zon` needs the new `.url` and `.hash`. Run `zig fetch --save` there too.
