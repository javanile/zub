---
title: mawk
description: zig build for awk
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/mawk
keywords:
date: 2026-07-06
updated_at: 2026-07-06T00:51:32+00:00
last_sync: 2026-07-06T00:51:32Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 3
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/allyourcodebase/mawk/
---

# zig build for MAWK - an implementation of new/posix awk

awk interpreter built with zig.

<https://invisible-island.net/mawk>

## Usage

```bash
>>> zig build
>>> ./zig-out/bin/awk --help
Usage: mawk [Options] [Program] [file ...]
```

## License

while the source code of mawk is licensed GPLv2,
the zig build scripts are made available with MIT.
