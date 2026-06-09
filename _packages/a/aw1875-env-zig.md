---
title: env.zig
description: Type-safe, schema based environment variable loading for Zig
license: ""
author: aw1875
author_github: aw1875
repository: https://github.com/aw1875/env.zig
keywords:
  - env
date: 2026-06-02
updated_at: 2026-06-02T05:44:05+00:00
last_sync: 2026-06-02T05:44:05Z
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
permalink: /packages/aw1875/env.zig/
---

# env.zig

Type-safe environment variable loading for Zig. Define your schema once and get validated, typed access to environment variables across your entire app.

## Features

- Schema-driven — declare the variables your app needs as a struct
- Type coercion — strings, integers, and floats are parsed automatically
- Fail-fast — logs every missing variable and returns an error at startup
- `.env` file support in Debug builds

## Installation

```sh
zig fetch --save git+https://github.com/aw1875/env.zig
```

Then add the module in your `build.zig`:

```zig
const env = b.dependency("env", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("env", env.module("env"));
```

## Usage

Create a file in your project (e.g. `src/env.zig`) that defines your schema:

```zig
// src/env.zig
pub const env = @import("env").Env(struct {
    GOOGLE_CLIENT_ID: []const u8,
    GOOGLE_CLIENT_SECRET: []const u8,
    GOOGLE_CALLBACK_URL: []const u8,
    APP_PORT: u16,
});
```

Call `init` once at startup, typically in `main`:

```zig
// src/main.zig
const env = @import("env.zig").env;

pub fn main(init: std.process.Init) !void {
    const allocator = init.gpa;
    const io = init.io;

    try env.init(io, allocator, init.environ_map);
    defer env.deinit(allocator);
}
```

Then access variables from anywhere in your app:

```zig
const env = @import("env.zig").env;

std.debug.print("{s}", .{env.vars.GOOGLE_CLIENT_ID});
```

If any required variables are missing at startup, each one is logged and `error.MissingEnvVar` is returned:

```
error(env.zig): Missing required environment variable: GOOGLE_CLIENT_SECRET ([]const u8)
error(env.zig): Missing required environment variable: APP_PORT (u16)
```

## Examples

See the [examples](./examples) directory for a full web server example using GitHub OAuth2 authentication.

## Supported types

| Zig type | Behavior |
|---|---|
| `[]const u8` | Copied from the environment as-is |
| `[]const []const u8` | Split on commas and copied as an array of strings |
| `u8`, `i32`, `u16`, etc. | Parsed with `std.fmt.parseInt` |
| `f32`, `f64`, etc. | Parsed with `std.fmt.parseFloat` |

## `.env` files

In `Debug` builds, env.zig automatically loads a `.env` file from the current working directory before reading the process environment. The process environment always takes precedence.

```sh
# .env
GOOGLE_CLIENT_ID=my_client_id
GOOGLE_CLIENT_SECRET="my_client_secret"
APP_PORT=8080
```

Lines beginning with `#` and blank lines are ignored. Values may optionally be wrapped in double quotes.

The `.env` file is silently ignored if it does not exist.
