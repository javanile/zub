---
title: libglob
description: Allocation-free pattern matching in pure Zig.
license: MIT
author: xcaeser
author_github: xcaeser
repository: https://github.com/xcaeser/libglob
keywords:
date: 2026-10-26
updated_at: 2026-10-26T20:53:02+00:00
last_sync: 2026-10-26T20:53:02Z
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
permalink: /packages/xcaeser/libglob/
---

# libglob

Allocation-free glob matching for byte strings in pure Zig.

[Reference docs](https://xcaeser.github.io/libglob)

[![Tests](https://github.com/xcaeser/libglob/actions/workflows/main.yml/badge.svg)](https://github.com/xcaeser/libglob/actions/workflows/main.yml)
[![Zig Version](https://img.shields.io/badge/Zig-0.17.0-orange.svg?logo=zig)](build.zig.zon)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)
[![Version](https://img.shields.io/badge/libglob-v0.3.0-green)](https://github.com/xcaeser/libglob/releases)

## Features

- `*`, `?`, sets (`[abc]`), ranges (`[a-z]`), and negated sets (`[!abc]`, `[^abc]`)
- Backslash escaping
- Optional pathname, leading-period, ASCII case-insensitive, and no-escape behavior
- Malformed patterns return an error
- Constant stack use, no allocation, and no dependencies

Matching is byte-oriented. `?` consumes one byte, not one Unicode scalar.

## Installation

```sh
zig fetch --save=libglob https://github.com/xcaeser/libglob/archive/v0.3.0.tar.gz
```

Add the module to your executable or library:

```zig
const glob_dep = b.dependency("libglob", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("libglob", glob_dep.module("libglob"));
```

## Usage

```zig
const std = @import("std");
const glob = @import("libglob");

pub fn main() !void {
    std.debug.assert(try glob.match("src/*.zig", "src/main.zig", .{}));
    std.debug.assert(try glob.match("file[0-9].txt", "file7.txt", .{}));
    std.debug.assert(!try glob.match("*.tmp", "notes.txt", .{}));

    // `*` cannot cross `/`.
    std.debug.assert(!try glob.match("src/*.zig", "src/lib/main.zig", .{ .pathname = true }));
    std.debug.assert(try glob.match("README.*", "readme.md", .{ .ignore_case = true }));

    // Malformed patterns are errors, not non-matches.
    std.debug.assert(glob.match("[a-z", "a", .{}) == error.UnclosedBracket);
}
```

## API

```zig
pub fn match(pattern: []const u8, text: []const u8, options: Options) ParseError!bool
```

`ParseError` is `UnclosedBracket`, `EmptyBracket`, `InvalidRange`, or
`TrailingBackslash`. To negate a match, use `!` on the result; to match a list
of patterns, loop over it.

## Pattern syntax

| Pattern            | Meaning                         |
| ------------------ | ------------------------------- |
| `*`                | Zero or more bytes              |
| `?`                | Exactly one byte                |
| `[abc]`            | One byte in the set             |
| `[a-z]`            | One byte in the inclusive range |
| `[!abc]`, `[^abc]` | One byte outside the set        |
| `\*`, `\?`, `\[`   | Escaped literal byte            |

`-` is literal at either edge of a class or when escaped. A leading `!` is an
ordinary byte.

## Options

All default to `false` except `escapes`.

- `pathname` — `*`, `?`, and `[...]` never match `/`; `/` must be matched literally
- `period` — a leading `.` (at the start, or after `/` with `pathname`) must be
  matched by a literal `.` or `\.`
- `ignore_case` — fold ASCII letter case
- `escapes = true` — `\` escapes the next pattern byte, inside and outside brackets

## Development

```sh
zig fmt --check .
zig build test --summary all
zig build docs
```

MIT licensed. See [LICENSE](LICENSE) and [CONTRIBUTING.md](CONTRIBUTING.md).
