---
title: blackmagic
description: C preprocessor tricks, explained
license: MIT
author: agagniere
author_github: agagniere
repository: https://github.com/agagniere/blackmagic
keywords:
  - c
  - preprocessor
  - tutorial
date: 2026-05-30
updated_at: 2026-05-30T18:41:17+00:00
last_sync: 2026-05-30T18:41:17Z
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
permalink: /packages/agagniere/blackmagic/
---

# Black Magic

*`impossible` is not a C keyword*

**Learn about C preprocessor tricks**

This book delves into techniques to generate C code with the preprocessor,
starting with a reminder about what the preprocessor is and how it is integrated in the C compilation pipeline,
then building up increasingly complex tools anyone can use in their C projects.

[Read it online !](https://agagniere.github.io/blackmagic/)

## Tools
Add this project as a dependency to your C project today (using Zig, Nix or Conan) to get:
- ANSI color codes as a string literal by writing `COLOR(UNDERLINED, BOLD, RED)` [`blackmagic/color.h`](include/blackmagic/color.h)
- Convert enums to/from strings [`blackmagic/enum.h`](include/blackmagic/enum.h)
- Logs with a compile-time configurable format and level [`blackmagic/log.h`](include/blackmagic/log.h). Possible formats include:
   - colored console
   - JSON
   - Markdown table
   - custom callback

## Roadmap
I would like to explain the following tricks in the book:
- [x] Logging
- [ ] Default arguments
- [ ] Function overloading
- [ ] Enum to/from string
- [ ] Serialization / Deserialization of a structure
- [ ] Unit-tests library

## Extras
- Sphinx directive to show C code before and after preprocessing
- Custom pygment lexer to color the code the way the preprocessor sees it

## Use it

### With Zig build as your C package manager

Add the dependency in your `build.zig.zon` by running the following command:
```shell
zig fetch --save git+https://github.com/agagniere/blackmagic#master
```

Then, in your `build.zig`:
```zig
const blackmagic = b.dependency("blackmagic", .{});
// wherever needed:
exe.addIncludePath(blackmagic.path("include"));
```

### With Conan

Add the dependency in your `conanfile.txt`
```toml
[requires]
blackmagic/0.3
```
