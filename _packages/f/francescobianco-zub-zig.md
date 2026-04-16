---
title: zub.zig
description: Zig-native installer for Zig binaries published in the ZUB registry.
license: MIT
author: francescobianco
author_github: francescobianco
repository: https://github.com/francescobianco/zub.zig
keywords:
  - linux
  - macos
  - package-index
  - package-manager
  - ubuntu
  - version-manager
  - windows
  - zig
  - zig-cli
  - zig-package
  - ziglang
date: 2026-04-16
updated_at: 2026-04-16T10:35:25+00:00
last_sync: 2026-04-16T10:35:25Z
package_kind: binary
has_library: false
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: true
sync_priority: sponsor
sync_source: sponsors
permalink: /packages/francescobianco/zub.zig/
---

# zub

`zub` is a Zig-native installer for Zig binaries published in the ZUB registry.

Its job is simple:

- install `zvm` by default
- detect the Zig version required by a package
- provision that Zig version automatically
- build the package
- place the resulting executable in `$HOME/.local/bin`

The registry source is:

`https://zub.javanile.org/packages.json`

## Install

The intended bootstrap flow is:

```bash
curl -fsSL https://yafb.net/zub.zig/install.sh | bash
```

The published installer is stored at `docs/install.sh` in this repository.

The installer:

- installs `zvm` if it is missing
- installs a bootstrap Zig version
- builds `zub`
- installs `zub` into `$HOME/.local/bin`

## Usage

Install a package from the registry:

```bash
zub install pbm
```

Search packages in the registry:

```bash
zub search http
```

What `zub` does under the hood:

1. downloads the package index from `https://zub.javanile.org/packages.json`
2. resolves the package repository from the registry entry
3. clones or updates the source in the local cache
4. reads `build.zig.zon` to detect `minimum_zig_version` when available
5. uses `zvm` to install that Zig version
6. runs `zig build`
7. copies the produced executable into `$HOME/.local/bin`

## Paths

- binary install dir: `$HOME/.local/bin`
- source cache: `$HOME/.cache/zub/src`
- temp build cache: `$HOME/.cache/zub/tmp`

## Notes

- `zub` currently assumes registry package URLs follow the GitHub pattern `/packages/<owner>/<repo>/`.
- if a package does not expose `minimum_zig_version`, `zub` falls back to `master`
- build output resolution prefers `zig-out/bin/<package-name>` and otherwise picks a single executable found in `zig-out/bin`

## Development

Build locally:

```bash
zig build
```

Run:

```bash
./zig-out/bin/zub
```
