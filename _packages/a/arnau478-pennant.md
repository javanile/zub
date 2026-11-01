---
title: pennant
description: Argument parser for Zig
license: GPL-3.0
author: Arnau478
author_github: Arnau478
repository: https://github.com/Arnau478/pennant
keywords:
  - argprase
date: 2026-10-21
updated_at: 2026-10-21T07:47:58+00:00
last_sync: 2026-10-21T07:47:58Z
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
permalink: /packages/Arnau478/pennant/
---

<div align="center">
  <img src="logo.svg" width="50%" />
</div>

# Pennant

Argument parser for Zig.

## Features
- Opposite flags (`--foo`/`--no-foo`, `--uppercase`/`--lowercase`), which act on a single variable and are mutually exclusive
- Values with and without equals sign (`--foo bar` and `--foo=bar` are both valid and equivalent)
- Bool flags never take a value, non-bool flags always do
- Shorthands for bool flags
- Everything is defined in a single struct, with the power of Zig's `comptime`

## Examples

Examples are available in the `examples` folder. They can also be run via `zig build example-[name]`.
