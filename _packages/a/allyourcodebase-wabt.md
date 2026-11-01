---
title: wabt
description: WebAssembly Binary Toolkit (wabt) and Binaryen on the zig build system
license: Apache-2.0
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/wabt
keywords:
  - wabt
  - wasm
  - wasm2wat
date: 2026-10-21
category: systems
updated_at: 2026-10-21T10:47:55+00:00
last_sync: 2026-10-21T10:47:55Z
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
permalink: /packages/allyourcodebase/wabt/
---

# [WebAssembly Binary Toolkit](https://github.com/WebAssembly/wabt.git) on the zig build system

uses the [Zig](https://ziglang.org/) build system to build WebAssembly's binary
C tools.

## building

```zig build
zig build
```

## add to your zig project

```bash
zig fetch --save git+https://github.com/allyourcodebase/wabt.git
```

## Cli usage

```
> ./zig-out/bin/wasm2c --help
usage: wasm2c [options] filename

  Read a file in the WebAssembly binary format, and convert it to
  a C source file and header.
```
