---
title: flow-themes
description: Themes compiler for Flow Control, the text editor
license: MIT
author: neurocyte
author_github: neurocyte
repository: https://github.com/neurocyte/flow-themes
keywords:
date: 2026-04-10
updated_at: 2026-04-10T10:02:16+00:00
last_sync: 2026-04-10T10:02:16Z
package_kind: binary
has_library: false
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/neurocyte/flow-themes/
---

# flow-themes
Themes compiler for Flow-Control, the text editor

## Requirements

 - zig 0.15.1
 - hjson (installed in your PATH)

## Build

`zig build`

This will download and compile all the themes and create a zig module
in `zig-out` that can be referenced as a dependency from another project's
`build.zig.zon`.
