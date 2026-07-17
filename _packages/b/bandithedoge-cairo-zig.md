---
title: cairo.zig
description: Cairo packaged for Zig
license: MIT
author: bandithedoge
author_github: bandithedoge
repository: https://github.com/bandithedoge/cairo.zig
keywords:
date: 2026-07-10
updated_at: 2026-07-10T20:56:56+00:00
last_sync: 2026-07-10T20:56:56Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 1
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/bandithedoge/cairo.zig/
---

# [Cairo](https://cairographics.org/) packaged for Zig

This repo builds Cairo using Zig's build system and C compiler frontend. Its primary use is to simplify cross-compiling and static linking for [zigplug](https://github.com/bandithedoge/zigplug).

**These are not language bindings.** You still have to use Cairo's C headers to do anything useful with this in your own projects.

Several packages in the `pkg/` directory were copied from [Ghostty](https://github.com/ghostty-org/ghostty/tree/main/pkg).
