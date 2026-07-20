---
title: zig-itertools
description: "WIP. Implementation of some useful iterators in Zig. Inspired by Python's itertools module."
license: ""
author: insolor
author_github: insolor
repository: https://github.com/insolor/zig-itertools
keywords:
  - zigang
date: 2026-07-20
updated_at: 2026-07-20T10:49:51+00:00
last_sync: 2026-07-20T10:49:51Z
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
permalink: /packages/insolor/zig-itertools/
unsafe: true
unsafe_reason: "contains a URL pointing to a .zip file"
---

# Zig Itertools

[![zig build test](https://github.com/insolor/zig-collections/actions/workflows/zig-build-test.yml/badge.svg)](https://github.com/insolor/zig-collections/actions/workflows/zig-build-test.yml)

> [!WARNING]  
> WORK IN PROGRESS

Implementation of some useful data structures in Zig. Inspired by Python's [`itertools`](https://docs.python.org/3/library/itertools.html) module.

Implemented so far:

- `ChainIterator` - "glues" two iterator in one, returns their elements in succession
- `SliceIterator` - iterates over a slice
- `EmptyIterator` - emits no elements. Implemented only for testing purposes.

Supported zig versions:

| Version | Support   |
| :-----: | :-------: |
| 0.14.0  | In v0.0.1 |
| 0.14.1  | In v0.0.1 |
| 0.15.1  | ✅        |
| 0.15.2  | ✅        |
| 0.16.0  | ✅        |

## Installation

1. In the root directory of your project, run the following command to add `zig_itertools` to your `build.zig.zon` file (replace 0.0.1 with the latest release number):

    ```bash
    zig fetch --save https://github.com/insolor/zig-itertools/archive/refs/tags/0.0.1.zip
    ```

    Replace `0.0.1` in the URL with the tag you want to use.

2. Add zig_itertools as a dependency module in your `build.zig` file, example:

    ```zig
    const zig_itertools = b.dependency("zig_itertools", .{});
    exe.root_module.addImport("zig_itertools", zig_itertools.module("zig_itertools"));
    ```

After that, you'll be able to import `zig_itertools` namespace from your code:

```zig
const zig_itertools = @import("zig_itertools");
const ChainIterator = zig_itertools.ChainIterator;
```
