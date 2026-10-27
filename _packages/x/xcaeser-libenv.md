---
title: libenv
description: Load, parse, and manage environment variables from .env files efficiently in zig.
license: MIT
author: xcaeser
author_github: xcaeser
repository: https://github.com/xcaeser/libenv
keywords:
date: 2026-10-22
updated_at: 2026-10-22T11:40:40+00:00
last_sync: 2026-10-22T11:40:40Z
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
permalink: /packages/xcaeser/libenv/
---

# libenv

<div>

A powerful Zig library for loading, parsing, and managing environment variables from `.env` files.

[![Version](https://img.shields.io/badge/Zig_Version-0.17.0-orange.svg?logo=zig)](README.md)
[![MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg?logo=cachet)](LICENSE)
[![Version](https://img.shields.io/badge/libenv-v0.12.0-green)](https://github.com/xcaeser/libenv/releases)

</div>

## Docs:

[libenv reference docs](https://xcaeser.github.io/libenv)

## ✅ Features

- Load environment variables from `.env` files
- Type-safe access using enums
- Read from and copy the current process environment map
- Modify the supplied process environment map with `setProcessEnv`
- Supports comments, quoted values, and whitespace trimming
- Supports `$KEY` and `${KEY}` interpolation from previously parsed values or the process environment map; single-quoted values stay literal
- Missing keys return an empty string
- Clean, testable API

## 🚀 Usage

```zig
const std = @import("std");
const libenv = @import("libenv");

pub const EnvKeys = enum {
    OPENAI_API_KEY,
    AWS_ACCESS_KEY_ID,
    COGNITO_CLIENT_SECRET,
    S3_BUCKET,
};

pub fn main(process_init: std.process.Init) !void {
    var env = libenv.init(process_init, EnvKeys);
    defer env.deinit();

    try env.load(.{
        .filename = ".env.local",
        .include_current_process_envs = true,
    });

    const openai = env.key(.OPENAI_API_KEY);
    std.debug.print("OPENAI_API_KEY={s}\n", .{openai});

    const aws_key = env.get("AWS_ACCESS_KEY_ID");
    std.debug.print("AWS_ACCESS_KEY_ID={s}\n", .{aws_key});
}
```

## 📄 Example `.env` File

```dotenv
OPENAI_API_KEY=sk-your-api-key-here
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
S3_BUCKET="my-bucket"
COGNITO_CLIENT_SECRET='abcdef123456'
HOME_DIR=$HOME
USER_NAME=${USER}
```

## 📦 Installation

### using `zig fetch`

```bash
zig fetch --save=libenv https://github.com/xcaeser/libenv/archive/v0.12.0.tar.gz
```

### Add to `build.zig`

```zig
const libenv_dep = b.dependency("libenv", .{ .target = target, .optimize = optimize });

exe.root_module.addImport("libenv", libenv_dep.module("libenv"));

// Optional: add for unit tests
exe_unit_tests.root_module.addImport("libenv", libenv_dep.module("libenv"));
```

## 📚 API Summary

### Initialization

`libenv` requires Zig `0.17.0` or newer and uses its `std.process.Init` API. Zig `0.16.0` is not supported. Accept `process_init` in `main`, then create an env manager with your enum type:

```zig
pub fn main(process_init: std.process.Init) !void {
    var env = libenv.init(process_init, EnvKeys);
    defer env.deinit();
}
```

### Env API

| Method                                                  | Description                                      |
| ------------------------------------------------------- | ------------------------------------------------ |
| `libenv.init(process_init, EnvKey)`                     | Initializes a new Env manager                    |
| `deinit()`                                              | Frees all allocated memory                       |
| `load(.{ .filename, ... })`                            | Loads variables from a `.env` file               |
| `loadCurrentProcessEnvs()`                              | Copies process variables into the internal map   |
| `parse(content)`                                        | Parses raw `.env`-formatted text                 |
| `get("KEY")`                                            | Gets a value by string key, or `""` if missing   |
| `key(.ENUM_KEY)`                                        | Gets a value by enum key, or `""` if missing     |
| `setProcessEnv("KEY", "VALUE")`                         | Sets a value in the supplied process map         |
| `setProcessEnv("KEY", null)`                            | Unsets a value in the supplied process map       |

### Load Options

| Option                         | Default | Description                                      |
| ------------------------------ | ------- | ------------------------------------------------ |
| `filename`                     | `.env`  | File to load                                     |
| `include_current_process_envs` | `false` | Copies `process_init.environ_map` into the map; its values win over the file |
| `export_to_process_env`        | `false` | Copies parsed values into the supplied process map |

## 🧪 Testing

Run:

```bash
zig build test
```

Includes tests for parsing, file I/O, interpolation precedence, process environment import/export, mutation, and lookup behavior.

## 🤝 Contributing

Issues and PRs welcome! Star the repo if it helped you.

## 📝 License

MIT – see [LICENSE](LICENSE).
