---
title: openssl
description: openssl zig package
license: MIT
author: allyourcodebase
author_github: allyourcodebase
repository: https://github.com/allyourcodebase/openssl
keywords:
date: 2026-04-20
updated_at: 2026-04-20T10:58:40+00:00
last_sync: 2026-04-20T10:58:40Z
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
permalink: /packages/allyourcodebase/openssl/
---

# openssl zig package

This is openssl ported to the Zig Build System.

## Status

I was able to use this to build [CPython](https://github.com/thejoshwolfe/cpython) for x86_64-linux.

Adding support for other operating systems and CPU architectures is straightforward and will
require fiddling with the build script to take into account the target.

## Zig version compatibility

- `0.16.x`
- `0.15.x`
- `0.14.x`

## Anti-Endorsement

I do not endorse openssl. I think it is a pile of trash. My motivation for this
project is because it is a dependency of CPython, which is a dependency of the
most active YouTube downloader, [ytdlp](https://github.com/yt-dlp/yt-dlp).
