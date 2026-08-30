---
title: zig-spirv-tools
description: ""
license: Zlib
author: akunaakwei
author_github: akunaakwei
repository: https://github.com/akunaakwei/zig-spirv-tools
keywords:
date: 2026-08-30
updated_at: 2026-08-30T09:12:59+00:00
last_sync: 2026-08-30T09:12:59Z
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
permalink: /packages/akunaakwei/zig-spirv-tools/
---

# SPIRV-Tools
This is [SPIRV-Tools](https://github.com/khronosGroup/SPIRV-Tools) packaged for the zig build system.

# generating code
SPIRV-Tools generates some code with python. These files are pregenerated and live in the `include` directory, so depending on this package does not require a python installation.  
After updating the upstream, you should regenerate the code. This command requires a `python3` executable in path.
```bash
zig build gen
```
