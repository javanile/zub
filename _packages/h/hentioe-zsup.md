---
title: zsup
description: A process management/supervision library written in Zig
license: ""
author: Hentioe
author_github: Hentioe
repository: https://github.com/Hentioe/zsup
keywords:
date: 2026-11-05
updated_at: 2026-11-05T23:47:10+00:00
last_sync: 2026-11-05T23:47:10Z
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
permalink: /packages/Hentioe/zsup/
---

# zsup

使用 Zig 编写的进程管理库。

## 安装

添加 `zsup` 到 `build.zig.zon`：

```sh
zig fetch --save git+https://github.com/Hentioe/zsup
```

然后，在 `build.zig`：

```zig
const zsup = b.dependency("zsup", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("zsup", zsup.module("zsup"));
```

## 例子

_待写。_
