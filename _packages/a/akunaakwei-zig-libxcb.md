---
title: zig-libxcb
description: libxcb for zig
license: Zlib
author: akunaakwei
author_github: akunaakwei
repository: https://github.com/akunaakwei/zig-libxcb
keywords:
date: 2026-08-03
updated_at: 2026-08-03T18:42:01+00:00
last_sync: 2026-08-03T18:42:01Z
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
permalink: /packages/akunaakwei/zig-libxcb/
---

# libxcb
This is [libxcb](https://gitlab.freedesktop.org/xorg/lib/libxcb) packaged for the zig build system.

# generating code
libxcb generates some code with python. These files are pregenerated and live in the `src` directory, so depending on this package does not require a python installation.  
After updating the upstream, you should regenerate the code. This command requires a `python3` executable in path.
```bash
zig build gen
```
