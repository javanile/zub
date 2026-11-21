---
title: argh
description: A modern, minimal argument parser for Zig.
license: MIT
author: dayvster
author_github: dayvster
repository: https://github.com/dayvster/argh
keywords:
date: 2026-04-05
updated_at: 2026-04-05T17:03:46+00:00
last_sync: 2026-04-05T17:03:46Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 8
distributable_binary_count: 8
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/dayvster/argh/
---

# argh

A modern, minimal, high-performance argument parser for Zig.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![zig 0.17](https://img.shields.io/badge/zig-0.17-f7a41d?logo=zig)](https://ziglang.org/)

---

**argh** is a type-safe, memory-efficient argument parser for Zig projects. Built on Zig 0.17's modern APIs with zero-copy parsing and optional compile-time prebaking for maximum performance.

## Key Features

- **Type-Safe**: Compile-time validated option types (string, int, float, bool)
- **Memory-Safe**: Zero-copy parsing, no undefined behavior, no leaks
- **High-Performance**: Optional compile-time prebaking support for zero-runtime overhead
- **Flexible**: Long/short flags, positional arguments with constraints, aliases
- **Batteries Included**: Grouped help output, custom error handling, required args, mutex groups
- **Modern**: Built for Zig 0.17+ with latest stdlib integration
## Quick Start

```zig
const argh = @import("argh");
const std = @import("std");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    // Collect CLI arguments using Zig 0.17 API
    var args_list: std.ArrayList([:0]const u8) = .{ .items = &.{}, .capacity = 0, .pointer_stability = .{} };
    var args_iter = try std.process.Args.Iterator.initAllocator(std.process.Args{ .vector = undefined }, allocator);
    defer args_iter.deinit();
    while (args_iter.next()) |arg| try args_list.append(allocator, arg);
    const args = try args_list.toOwnedSlice(allocator);

    var parser = argh.Parser.init(allocator, args);
    try parser.addFlag("-h", "--help", "Show help message");
    try parser.addOption("--name", "-n", "World", "Name to greet");
    try parser.addIntOption("--count", "-c", 1, "How many times", 1, 10);
    try parser.addBoolOption("--loud", "-L", false, "Loud greeting");
    try parser.parse();

    if (parser.flagPresent("--help")) {
        parser.printHelpWithOptions(.simple_grouped);
        return;
    }

    const name = parser.getOption("--name") orelse "World";
    const count = try parser.getOptionInt("--count") orelse 1;
    const loud = try parser.getOptionBool("--loud") orelse false;

    for (0..count) |_| {
        if (loud) {
            std.debug.print("HELLO, {s}!\n", .{name});
        } else {
            std.debug.print("Hello, {s}.\n", .{name});
        }
    }
}
```

## Features

- **Simple & Declarative**: Minimal API surface, no macros or code generation
- **Type-Safe**: Compile-time validated option types (string, int, float, bool)
- **Memory-Safe**: Zero undefined behavior, proper error handling via error sets
- **Performance**: Optional compile-time prebaking for zero-runtime overhead
- **Flexible Parsing**:
  - Long and short flags/options (`--help`, `-h`, `-n value`)
  - Type-safe int/float options with min/max constraints
  - Positional arguments with min/max count constraints
  - Option aliases for common variations
  - Mutually exclusive argument groups
- **Developer Friendly**:
  - Helpful error messages with argument context
  - Multiple help output styles (flat, simple_grouped, complex_grouped)
  - Hidden arguments for internal/debug options
  - Fully documented API with Zig doc comments
- **Modern**: Built for Zig 0.17+ with latest stdlib patterns

## Installation

Add to your Zig project with the package manager:

```bash
zig fetch --save git+https://github.com/dayvster/argh
```

Then in your `build.zig`:

```zig
const argh_pkg = b.dependency("argh", .{
    .target = target,
    .optimize = optimize,
});

const exe = b.addExecutable(.{ /* ... */ });
exe.root_module.addImport("argh", argh_pkg.module("argh"));
```

Requires **Zig 0.17.0** or later.

## Type-Safe Options

argh supports multiple option types with compile-time type checking and runtime validation:

```zig
try parser.addOption("--name", "-n", "default", "String option");
try parser.addIntOption("--count", "-c", 5, "Integer option", 0, 100);
try parser.addFloatOption("--ratio", "-r", 0.5, "Float option", 0.0, 1.0);
try parser.addBoolOption("--verbose", "-v", false, "Boolean flag");

const name = parser.getOption("--name");
const count = try parser.getOptionInt("--count");
const ratio = try parser.getOptionFloat("--ratio");
const verbose = try parser.getOptionBool("--verbose");
```

All numeric options support min/max constraints enforced at parse time.

## API Overview

```zig
// Flags (on/off switches)
try parser.addFlag("-h", "--help", "Show help");
try parser.addHiddenFlag("-d", "--debug", "Debug mode");

// Options (with values)
try parser.addOption("--name", null, "default", "Name option");
try parser.addOption("--port", "-p", "8080", "Port number");

// Positional arguments
try parser.addPositional("input", "Input file", true, null);
try parser.addPositionalWithCount("files", "Files to process", 1, 5);

// Option aliases
try parser.addOptionAlias("--output", "--out");
try parser.addFlagAlias("-v", "--verbose");

// Parse all arguments
try parser.parse();

// Check for errors
if (parser.errors.items.len > 0) parser.printErrors();

// Query results
const verbose = parser.flagPresent("--verbose");
const name = parser.getOption("--name");
const files = parser.positionals.items;
```

## Help Output Styles

argh supports three help formatting modes:

```zig
parser.printHelp();  // Default: flat style
parser.printHelpWithOptions(.flat);
parser.printHelpWithOptions(.simple_grouped);
parser.printHelpWithOptions(.complex_grouped);
```

## Performance & Optimization

argh is designed for zero-overhead abstractions:

- **Zero-Copy Parsing**: Arguments are parsed without unnecessary allocations
- **Stack-Based Storage**: Unmanaged collections reduce heap pressure
- **Compile-Time Prebaking** (planned): Future support for compile-time argument validation and code generation for zero-runtime parsing overhead

## Why argh?

- **Minimal**: No macros, no codegen, no dependencies
- **Type-Safe**: Compile-time option validation, runtime constraints
- **Memory-Safe**: Explicit error handling, no undefined behavior
- **Clear**: Straightforward API, easy to debug
- **Fast**: Zero-copy parsing, optional compile-time prebaking
- **Modern**: Built for Zig 0.17+ with latest patterns

## Examples

Check out the `examples/` directory for complete runnable examples:

- `basic.zig` - Simple greeting program
- `advanced.zig` - Complex options and flags
- `int_float_options.zig` - Numeric constraints
- `positional_minmax.zig` - Positional argument ranges
- `errors_and_help.zig` - Error handling and help formatting
- `hidden_args.zig` - Hidden/debug arguments
- `repeat_flags.zig` - Repeatable flags

Run any example:

```bash
zig build example-basic -- --help
zig build example-advanced -- --name Alice --verbose
```

## Contributing

Contributions are welcome! Please maintain the minimal, clear style and ensure all changes work with Zig 0.17+.

## License

MIT
