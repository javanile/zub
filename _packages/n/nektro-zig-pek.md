---
title: zig-pek
description: A comptime HTML preprocessor with a builtin template engine for Zig.
license: MPL-2.0
author: nektro
author_github: nektro
repository: https://github.com/nektro/zig-pek
keywords:
date: 2026-04-23
updated_at: 2026-04-23T11:21:52+00:00
last_sync: 2026-04-23T11:21:52Z
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
permalink: /packages/nektro/zig-pek/
---

# Pek

![loc](https://sloc.xyz/github/nektro/zig-pek)
[![license](https://img.shields.io/github/license/nektro/zig-pek.svg)](https://github.com/nektro/zig-pek/blob/master/LICENSE)
[![nektro @ github sponsors](https://img.shields.io/badge/sponsors-nektro-purple?logo=github)](https://github.com/sponsors/nektro)
[![Zig](https://img.shields.io/badge/Zig-0.14-f7a41d)](https://ziglang.org/)
[![Zigmod](https://img.shields.io/badge/Zigmod-latest-f7a41d)](https://github.com/nektro/zigmod)

A comptime HTML preprocessor with a builtin template engine for Zig.

## Example Document

```fsharp
html[lang="en"](
    head(
        title("Pek Example")
        meta[charset="UTF-8"]
        meta[name="viewport" content="width=device-width,initial-scale=1"]
    )
    body(
        h1("Pek Example")
        hr
        p("This is an example HTML document written in "a[href="https://github.com/nektro/zig-pek"]("Pek")".")
    )
)
```

## Example Usage

See [test.zig](test.zig).
