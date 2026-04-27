---
title: zig-pam
description: Zig wrapper around the PAM C library (libpam)
license: MIT
author: AshAmetrine
author_github: AshAmetrine
repository: https://github.com/AshAmetrine/zig-pam
keywords:
  - bindings
  - libpam
date: 2026-04-17
category: systems
updated_at: 2026-04-17T19:09:55+00:00
last_sync: 2026-04-17T19:09:55Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/AshAmetrine/zig-pam/
---

# Zig PAM Wrapper

A Zig wrapper around the PAM (Pluggable Authentication Modules) C library (libpam).

## Features

- Minimal, direct mapping to PAM calls.
- Typed flags and items for common operations.
- Conversation helpers (`Messages`, `Prompt.respond`).

## Requirements

- Zig 0.16.0.
- `libc`.
- `libpam`.

## Usage

Add the dependency with `zig fetch`:

```sh
zig fetch --save git+https://github.com/ashametrine/zig-pam
```

Then add it as an import in `build.zig`:

```zig
const pam = b.dependency("zig_pam", .{
    .target = target,
    .optimize = optimize,
});

exe.root_module.addImport("pam", pam.module("pam"));
```

## Example

The example program lives at `example/main.zig`.

To build the included example:

```sh
zig build example
```

Run it:

```sh
./zig-out/bin/example <user>
```
