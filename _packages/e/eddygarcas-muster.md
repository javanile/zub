---
title: muster
description: Muster - Inventory Agent in Zig
license: MIT
author: eddygarcas
author_github: eddygarcas
repository: https://github.com/eddygarcas/muster
keywords:
  - hardware
  - metrics
date: 2026-07-28
category: embedded
updated_at: 2026-07-28T16:11:39+00:00
last_sync: 2026-07-28T16:11:39Z
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
permalink: /packages/eddygarcas/muster/
---

# muster

A dependency-free device inventory agent, written in Zig as a structured
learning project. `muster` collects hardware, OS, and software inventory
from a machine and reports it as JSON — to stdout, and eventually to a
remote endpoint on an hourly interval.

This repo is both a real tool and a Zig course: every milestone is scoped
to force fluency with a specific part of the language (allocators, slices,
comptime reflection, error unions, `std.Io`) rather than just "get the
exercise to pass."

## Status

🚧 Early development — see [Milestones](#milestones) below.

## Why

Endpoint inventory — CPU/RAM/disk, installed packages with versions,
hardware identity — is a natural fit for a language that compiles to a
tiny, static, dependency-free binary you can drop on a fleet of machines
with zero runtime to install. `muster` is also a testbed for evaluating
**Zig + Ruby as a stack pairing**: Zig at the edge, Ruby in the middle,
talking over a versioned JSON contract.

## Stack

| Concern | Choice |
|---|---|
| Agent | Zig **0.16.0** (pinned — see `build.zig.zon`) |
| Target platform (phase 1) | Arch Linux, x86_64 |
| Runtime dependencies | None — single static binary, stdlib only |
| Test/dev receiver | Ruby (Sinatra) — see [`tools/receiver`](tools/receiver) |
| Editor | [Zed](https://zed.dev) — project tasks in [`.zed/tasks.json`](.zed/tasks.json) |

## Quick start

```sh
# Requires Zig 0.16.0 exactly — mismatched versions will not compile.
zig version

zig build
zig build run -- --once      # print one inventory snapshot as JSON
zig build test               # run unit + golden tests
zig fmt --check .            # matches the CI formatting check
```

If you're using Zed, all of the above (plus fixture capture, fuzzing, and
the Ruby receiver) are available as one-keystroke tasks — open the task
picker (`task: spawn`) and filter by `zig:` or `receiver:`.

## What it collects

`os`, `cpu`, `memory`, `storage` (devices + filesystems), `dmi`
(hardware identity), `network` interfaces, `power` (batteries), and
`packages` (full `name + version` inventory, for vulnerability matching
and application-change tracking). Full field-by-field schema, sources,
and parsing notes: [`docs/schema-v1.md`](docs/schema-v1.md).

Example (abridged):

```json
{
  "schema_version": 1,
  "agent": { "name": "muster", "version": "0.1.0" },
  "device_id": "sha256-of-machine-id",
  "collected_at": 1753700000,
  "os": { "id": "arch", "kernel": "6.15.4-arch1-1", "hostname": "..." },
  "cpu": { "vendor": "...", "model": "...", "cores": 8, "threads": 16 },
  "packages": { "manager": "pacman", "count": 1342,
                "list": [ { "name": "firefox", "version": "139.0-1", "explicit": true } ] }
}
```

## Architecture, in brief

- **Collectors** are isolated units, one per section of the schema. A
  failing collector never takes down the snapshot — its error is recorded
  in an `errors` section instead.
- **SysRoot**: every collector reads through an injectable filesystem
  root (`/` in production, a fixture directory in tests), which is what
  makes `/proc` and `/sys` parsing unit-testable without mocks.
- **Per-cycle arena allocator**: one arena per collection cycle, freed in
  one shot — no manual `free` calls anywhere in collector code.
- Privacy: identifiers (device id, serials, MACs) are hashed or
  opt-in — see [`docs/schema-v1.md`](docs/schema-v1.md) for the policy.

Full architecture and rationale: see the project's development plan
(architecture doc, kept alongside this repo / linked in the wiki).

## Repository layout

```
muster/
├── .zed/tasks.json      # Zed editor tasks: build, test, fmt, fixtures, receiver
├── build.zig / build.zig.zon
├── src/
│   ├── main.zig
│   ├── collectors/      # os, cpu, memory, storage, dmi, network, power, packages
│   ├── transport/       # stdout, http, backoff
│   └── diff.zig
├── testdata/fixtures/   # captured /proc, /sys, /etc snapshots for golden tests
├── tools/
│   ├── capture-fixture.sh
│   └── receiver/        # throwaway Ruby (Sinatra) receiver for dev/testing
├── packaging/           # PKGBUILD, systemd unit (later milestone)
└── docs/schema-v1.md
```

## Milestones

| # | Scope |
|---|---|
| M1 | Local snapshot to stdout: `os`, `cpu`, `memory`, `storage.filesystems`; SysRoot + golden tests |
| M2 | Full inventory: devices, DMI, network, power, packages, device id; unprivileged-safe |
| M3 | Ship over HTTP to the Ruby receiver; retry with exponential backoff + jitter |
| M4 | Daemon mode, hourly interval, section-digest diffing for change detection |
| M5 | Config precedence, logging, systemd unit, PKGBUILD, packaging |

Tracked as GitHub milestones/issues, one issue per collector.

## Testing

- **Golden tests**: real `/proc`/`/sys` captures under `testdata/fixtures/`,
  parsed and compared against expected JSON — runs identically in CI since
  collectors never touch the real filesystem in tests.
- **Fuzzing**: Zig's built-in fuzzer targets every text parser with hostile
  input (truncated files, missing trailing newline, huge lines).
- **Oracle checks**: manual comparison against `lscpu`, `lsblk -J`, `free`,
  `df` on real hardware during development.

## Contributing / working on this

This is a personal learning project first; issues and PRs following the
milestone breakdown above are welcome regardless.

## License

TBD.
