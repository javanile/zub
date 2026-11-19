---
title: TernLib
description: Library for Balanced Ternary Logic on Bit Planes
license: MIT
author: lina-torovoltas
author_github: lina-torovoltas
repository: https://github.com/lina-torovoltas/TernLib
keywords:
  - balanced-ternary
  - ternary-logic
date: 2026-11-11
updated_at: 2026-11-11T17:10:11+00:00
last_sync: 2026-11-11T17:10:11Z
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
permalink: /packages/lina-torovoltas/TernLib/
---

<p align="center">
  <img src="TernLib.png" width="480">
</p>

<h1 align="center">TernLib</h1>

<p align="center">
  <img src="https://img.shields.io/badge/release-v0.4.5-0078D4">
  <img src="https://img.shields.io/badge/language-Zig-orange">
  <img src="https://img.shields.io/github/license/lina-torovoltas/TernLib">
  <img src="https://img.shields.io/github/last-commit/lina-torovoltas/TernLib">
</p>

### Was ist das???

TernLib is a library that provides balanced ternary logic operations (e.g. `min`, `max`, `webb`, `neg`)</br>
and ternary data types represented using binary bit planes (e.g. `Trit`, `Tryte`, `Verbum`, `t27`).

### Wozu ist das???

To experiment with ternary logic in algorithms and programs,</br>
explore ternary computing, and, well... just for fun lol.

## Docs

Docs??? Who even reads docs???</br>
(hahaha, i'll add them later, just a placeholder for now)


## Installation

1. Add the dependency to your project:

```
zig fetch --save=ternlib git+https://github.com/lina-torovoltas/TernLib#main
```

2. Add the module to your `build.zig`:

```zig
const ternlib = b.dependency("ternlib", .{});
exe.root_module.addImport("ternlib", ternlib.module("ternlib"));
```

3. Import the library:

```zig
const tern = @import("ternlib");
```


## Contributing

Contributions are welcome!</br>
If thou hast found a bug or wish to propose an improvement,</br>
feel free to open an [issue](../../issues) or submit a [pull request](../../pulls).

***
Developed by <a href="https://lina-kiratorasu.codeberg.page/" style="color:#ff4f00">Lina Kiratorasu</a> (c) 2026-2027 (yeah, i'm in the future rn),</br>
released under the [MIT License](LICENSE).
