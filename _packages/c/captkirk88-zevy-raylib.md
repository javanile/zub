---
title: zevy-raylib
description: zevy-raylib is a abstraction for Raylib with zevy-ecs. It provides a plugin-based architecture for rapid game prototyping. (work in progress)
license: NOASSERTION
author: captkirk88
author_github: captkirk88
repository: https://github.com/captkirk88/zevy-raylib
keywords:
  - raylib
  - raylib-zig
  - zevy
  - zevy-ecs
date: 2026-05-24
category: game-development
updated_at: 2026-05-24T11:07:24+00:00
last_sync: 2026-05-24T11:07:24Z
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
permalink: /packages/captkirk88/zevy-raylib/
---

# Zevy Raylib

[license]: https://img.shields.io/github/license/captkirk88/zevy-raylib?style=for-the-badge&logo=opensourcehardware&label=License&logoColor=C0CAF5&labelColor=414868&color=8c73cc

[![][license]](https://github.com/captkirk88/zevy-raylib/blob/main/LICENSE)

[![Zig Version](https://img.shields.io/badge/zig-0.16.0-blue.svg)](https://ziglang.org/)

> [!WARNING]
> This library and its APIs are experimental.
> The API and internal behavior can and will change without backward compatibility guarantees.
> Tests and cross-platform coverage are limited — treat this as a development-ready library, not production-ready.
> Please open issues or submit PRs if you rely on features that should be stabilized or suggested.

### Table of contents

- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Contributing](#contributing)
- [Projects](#projects)
- [License](#license)

---

## Introduction

Zevy Raylib is a small library that wires the Raylib runtime into a Zevy ECS-based app. It handles window creation, input harvesting, asset management and sets up RayGui-based UI systems with multiple layout options.

---

## Quick Start

[Examples](examples/) can be ran with:

```bash
zig build examples
```

---

## Contributing

- Follow existing Zig patterns
- Register new plugins in `src/root.zig` by adding them to `plug()`
- Add unit tests beside features in the `src/*` directory. Prefer tests to be named `*_tests.zig`.

## Projects
- [zevy-alloy](https://github.com/captkirk88/zevy-alloy)
- [zevy-ecs](https://github.com/captkirk88/zevy-ecs)
