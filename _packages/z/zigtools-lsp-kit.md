---
title: lsp-kit
description: The necessary building blocks to develop LSP implementations in Zig.
license: MIT
author: zigtools
author_github: zigtools
repository: https://github.com/zigtools/lsp-kit
keywords:
  - lsp
date: 2026-06-14
updated_at: 2026-06-14T09:53:55+00:00
last_sync: 2026-06-14T09:53:55Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 4
distributable_binary_count: 4
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/zigtools/lsp-kit/
---

[![CI](https://github.com/zigtools/lsp-kit/actions/workflows/main.yml/badge.svg)](https://github.com/zigtools/lsp-kit/actions)
[![codecov](https://codecov.io/gh/zigtools/lsp-kit/graph/badge.svg?token=C3HCN59E4C)](https://codecov.io/gh/zigtools/lsp-kit)
[![Documentation](https://img.shields.io/badge/Docs-grey?logo=zig)](https://zigtools.github.io/lsp-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Zig LSP Kit

Provides the necessary building blocks to develop Language Server Protocol implementations in Zig.

# Installation

> [!NOTE]
> The default branch requires Zig `0.17.0-dev.667+0569f1f6a` or later. Checkout the `0.16.x` branch when using Zig 0.16

```bash
# Initialize a `zig build` project if you haven't already
zig init
# Add the `lsp_kit` package to your `build.zig.zon`
zig fetch --save git+https://github.com/zigtools/lsp-kit.git
```

You can then import the `lsp` module in your `build.zig` with:

```zig
const lsp = b.dependency("lsp_kit", .{}).module("lsp");
const exe = b.addExecutable(...);
exe.root_module.addImport("lsp", lsp);
```
