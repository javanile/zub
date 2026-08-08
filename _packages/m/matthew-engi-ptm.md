---
title: ptm
description: Library responsible for reading .ptm files (own sprites format)
license: MIT
author: matthew-engi
author_github: matthew-engi
repository: https://github.com/matthew-engi/ptm
keywords:
  - animation
  - image
  - image-processing
  - sprites
  - spritesheet
  - spritesheet-packer
date: 2026-08-08
category: game-development
updated_at: 2026-08-08T02:06:22+00:00
last_sync: 2026-08-08T02:06:22Z
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
permalink: /packages/matthew-engi/ptm/
---

# "Protomap" Sprite Library

![Static Badge](https://img.shields.io/badge/Zig-0.16.0-2?style=flat&color=orange&link=https%3A%2F%2Fziglang.org%2Fdownload%2F0.16.0%2Frelease-notes.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This is a library to read and write .ptm files containing sprites for byter-zig

## Install & Build

Via the terminal, run the following command:

```sh
zig fetch --save git+https://github.com/matthew-engi/ptm
```

Inside of your  `build.zig` file, add the following:

```zig
const ptm_dep = b.dependency("ptm", .{
    .target = target,
    .optimize = optimize,
});

exe.root_module.addImport("ptm", ptm_dep.module("ptm"));
```
