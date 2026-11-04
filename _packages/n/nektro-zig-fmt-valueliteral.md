---
title: zig-fmt-valueliteral
description: Print a value to a writer as it would be written in Zig syntax as a (x) literal.
license: MIT
author: nektro
author_github: nektro
repository: https://github.com/nektro/zig-fmt-valueliteral
keywords:
date: 2026-10-21
updated_at: 2026-10-21T06:47:30+00:00
last_sync: 2026-10-21T06:47:30Z
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
permalink: /packages/nektro/zig-fmt-valueliteral/
---

# zig-fmt-valueliteral

![loc](https://sloc.xyz/github/nektro/zig-fmt-valueliteral)
[![license](https://img.shields.io/github/license/nektro/zig-fmt-valueliteral.svg)](https://github.com/nektro/zig-fmt-valueliteral/blob/master/LICENSE)
[![nektro @ github sponsors](https://img.shields.io/badge/sponsors-nektro-purple?logo=github)](https://github.com/sponsors/nektro)
[![Zig](https://img.shields.io/badge/Zig-0.17-f7a41d)](https://ziglang.org/)
[![Zigmod](https://img.shields.io/badge/Zigmod-latest-f7a41d)](https://github.com/nektro/zigmod)

Print a value to a writer as it would be written in Zig syntax as a (x) literal.

## Api
- `pub fn fmtValueLiteral(w: std.io.Writer, value: anytype, comptime print_type_name: bool) !void`
    - `w` is an `anytype` for any value that implements `std.io.Writer`. It will then print the respective syntax literal to it.
    - `value` is anything you'd like it to print. Should it fail to print a value you feel it should be able to please open an issue.
    - `print_type_name` is a bool for whether or not you'd like it to print `@typeName(T)` or `.` when printing structs, enums, and unions.
