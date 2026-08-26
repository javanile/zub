---
title: zig-libglvnd
description: libglvnd for zig
license: Zlib
author: akunaakwei
author_github: akunaakwei
repository: https://github.com/akunaakwei/zig-libglvnd
keywords:
date: 2026-08-26
updated_at: 2026-08-26T06:07:40+00:00
last_sync: 2026-08-26T06:07:40Z
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
permalink: /packages/akunaakwei/zig-libglvnd/
---

# libglvnd
This is [libglvnd](https://gitlab.freedesktop.org/glvnd/libglvnd) packaged for the zig build system.

# generating code
libglvnd generates some code with python. These files are pregenerated and live in the `include` directory, so depending on this package does not require a python installation.  
After updating the upstream, you should regenerate the code. This command requires a `python3` executable in path.
```bash
zig build gen
```
