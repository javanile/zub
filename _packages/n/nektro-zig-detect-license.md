---
title: zig-detect-license
description: Given an input text guess which SPDX license it most likely is an instance of
license: MIT
author: nektro
author_github: nektro
repository: https://github.com/nektro/zig-detect-license
keywords:
date: 2026-10-21
updated_at: 2026-10-21T06:47:58+00:00
last_sync: 2026-10-21T06:47:58Z
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
permalink: /packages/nektro/zig-detect-license/
---

# zig-detect-license

![loc](https://sloc.xyz/github/nektro/zig-detect-license)
[![license](https://img.shields.io/github/license/nektro/zig-detect-license.svg)](https://github.com/nektro/zig-detect-license/blob/master/LICENSE)
[![nektro @ github sponsors](https://img.shields.io/badge/sponsors-nektro-purple?logo=github)](https://github.com/sponsors/nektro)
[![Zig](https://img.shields.io/badge/Zig-0.17-f7a41d)](https://ziglang.org/)
[![Zigmod](https://img.shields.io/badge/Zigmod-latest-f7a41d)](https://github.com/nektro/zigmod)

Given an input text guess which SPDX license it most likely is an instance of

## Usage
- `pub fn detect(alloc: *std.mem.Allocator, license_src: []const u8) ![]const u8`
    - Given an input string, will return the SPDX license identifier for the closest guess to which one it might be

- `pub fn detectInDir(alloc: *std.mem.Allocator, dir: std.fs.Dir) !?[]const u8`
    - Given a directory, will search for a `LICENSE` file and return the guess for which one it is. Will return `null` if the license file can not be found. If this returns null when you do indeed have a license file, please help expand the search examples by submitting a bug report.
