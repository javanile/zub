---
title: zig-sbi
description: Zig wrapper around the RISC-V SBI specification
license: BSD-3-Clause
author: CascadeOS
author_github: CascadeOS
repository: https://github.com/CascadeOS/zig-sbi
keywords:
  - osdev
  - risc-v
  - riscv
  - riscv32
  - riscv64
  - sbi
date: 2026-06-23
category: embedded
updated_at: 2026-06-23T14:40:21+00:00
last_sync: 2026-06-23T14:40:21Z
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
permalink: /packages/CascadeOS/zig-sbi/
---

# zig-sbi

Zig wrapper around the [RISC-V SBI specification](https://github.com/riscv-non-isa/riscv-sbi-doc).

Compatible with SBI Specification v3.0-rc1.

## Installation

Add the dependency to `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/leecannon/zig-sbi
```

Then add the following to `build.zig`:

```zig
const sbi = b.dependency("sbi", .{});
exe.root_module.addImport("sbi", sbi.module("sbi"));
```
