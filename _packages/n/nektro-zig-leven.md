---
title: zig-leven
description: Measure the difference between two slices using the Levenshtein distance algorithm
license: MIT
author: nektro
author_github: nektro
repository: https://github.com/nektro/zig-leven
keywords:
date: 2026-10-21
updated_at: 2026-10-21T06:47:54+00:00
last_sync: 2026-10-21T06:47:54Z
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
permalink: /packages/nektro/zig-leven/
---

# zig-leven

![loc](https://sloc.xyz/github/nektro/zig-leven)
[![license](https://img.shields.io/github/license/nektro/zig-leven.svg)](https://github.com/nektro/zig-leven/blob/master/LICENSE)
[![nektro @ github sponsors](https://img.shields.io/badge/sponsors-nektro-purple?logo=github)](https://github.com/sponsors/nektro)
[![Zig](https://img.shields.io/badge/Zig-0.17-f7a41d)](https://ziglang.org/)
[![Zigmod](https://img.shields.io/badge/Zigmod-latest-f7a41d)](https://github.com/nektro/zigmod)

Measure the difference between two slices using the Levenshtein distance algorithm

Adapted from https://github.com/sindresorhus/leven

## Usage

`pub fn leven(comptime T: type, alloc: *std.mem.Allocator, a: []const T, b: []const T, max: ?usize) !usize`

## Future

TODO Unicode support for strings
