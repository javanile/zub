---
title: gifsicle
description: gifsicle using the zig build system
license: GPL-2.0
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/gifsicle
keywords:
  - gif
  - gifsicle
date: 2026-04-14
updated_at: 2026-04-14T17:04:41+00:00
last_sync: 2026-04-14T17:04:41Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/allyourcodebase/gifsicle/
---

# Gifsicle

This is [gifsicle](https://github.com/kohler/gifsicle) packaged using Zig build system

Needs zig version `0.15.2` or higher


## Options

You can set these options when importing as a dependency with `b.dependency("gifsicle", .{ option=value })`
or when building directly with `zig build -Doption=value`

|Option Name|default |description                                   |
|-----------|:------:|----------------------------------------------|
| linkage   | static | Linkage mode too build lib (dynamic library) |
| tools     | true   | Build cli tools (gifsicle, gifview, gifdiff) |
| terminal  | true   | Output gif to terminal                       |

---

Thanks to Andrew's fork of [ffmpeg](https://github.com/andrewrk/ffmpeg) for the knowhow
