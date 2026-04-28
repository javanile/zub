---
title: abcrypt-zig
description: A simple, modern and secure file encryption library for Zig
license: ""
author: sorairolake
author_github: sorairolake
repository: https://github.com/sorairolake/abcrypt-zig
keywords:
  - abcrypt
  - abcrypt-encryption
  - argon2
  - argon2id
  - blake2
  - blake2b
  - chacha20
  - chacha20-poly1305
  - encryption
  - poly1305
  - xchacha20
  - xchacha20-poly1305
date: 2026-04-17
updated_at: 2026-04-17T15:18:25+00:00
last_sync: 2026-04-17T15:18:25Z
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
permalink: /packages/sorairolake/abcrypt-zig/
---

<!--
SPDX-FileCopyrightText: 2024 Shun Sakai

SPDX-License-Identifier: CC-BY-4.0
-->

# abcrypt-zig

[![CI][ci-badge]][ci-url]

**abcrypt-zig** is an implementation of the [abcrypt encrypted data format].

This package supports version 1 of the abcrypt format.

## Usage

Add this package to your `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/sorairolake/abcrypt-zig.git
```

Add the following to your `build.zig`:

```zig
const abcrypt = b.dependency("abcrypt", .{});
exe.root_module.addImport("abcrypt", abcrypt.module("abcrypt"));
```

### Documentation

See the [documentation][docs-url] for more details.

## Zig version

This library is compatible with Zig version 0.15.1.

## Source code

The upstream repository is available at
<https://github.com/sorairolake/abcrypt-zig.git>.

## Changelog

Please see [CHANGELOG.adoc].

## Contributing

Please see [CONTRIBUTING.adoc].

## License

Copyright (C) 2024 Shun Sakai (see [AUTHORS.adoc])

This library is distributed under the terms of either the _Apache License 2.0_
or the _MIT License_.

This project is compliant with version 3.3 of the [_REUSE Specification_]. See
copyright notices of individual files for more details on copyright and
licensing information.

[ci-badge]: https://img.shields.io/github/actions/workflow/status/sorairolake/abcrypt-zig/CI.yaml?branch=develop&style=for-the-badge&logo=github&label=CI
[ci-url]: https://github.com/sorairolake/abcrypt-zig/actions?query=branch%3Adevelop+workflow%3ACI++
[abcrypt encrypted data format]: https://sorairolake.github.io/abcrypt/book/format.html
[docs-url]: https://sorairolake.github.io/abcrypt-zig/
[CHANGELOG.adoc]: CHANGELOG.adoc
[CONTRIBUTING.adoc]: CONTRIBUTING.adoc
[AUTHORS.adoc]: AUTHORS.adoc
[_REUSE Specification_]: https://reuse.software/spec-3.3/
