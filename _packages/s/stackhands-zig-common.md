---
title: zig-common
description: "Shared Zig library for the stackhands tools: Linux system calls with named errors, descriptor-checked file handling, child processes, gzip in place"
license: MIT
author: stackhands
author_github: stackhands
repository: https://github.com/stackhands/zig-common
keywords:
  - easybuild
  - hpc
  - linux
date: 2026-11-14
category: systems
updated_at: 2026-11-14T06:05:52+00:00
last_sync: 2026-11-14T06:05:52Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 3
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/stackhands/zig-common/
---

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="branding/logo/logo-dark.svg">
    <img src="branding/logo/logo-light.svg" alt="zig-common" width="420">
  </picture>
</p>

# zig-common

<!-- docs:start -->
The pieces the stackhands Zig tools share: Linux system calls with named
errors, file handling checked on the open descriptor, running a child
program, gzip in place and the `.licensed-logs` list, and command-line
plumbing.

Documentation: <https://stackhands.github.io/zig-common/>

It holds only what at least two tools need, or what one tool needs in a form
the next port will reuse. It is Linux only and needs Zig 0.17.1.

## Use it from a tool

```zig
// build.zig.zon
.dependencies = .{
    .zig_common = .{
        .url = "git+https://github.com/stackhands/zig-common#<commit>",
        .hash = "<hash zig fetch prints>",
    },
},
```

```zig
// build.zig
const common = b.dependency("zig_common", .{ .target = target, .optimize = optimize });
mod.addImport("zig_common", common.module("zig_common"));
```

`zig fetch --save git+https://github.com/stackhands/zig-common#<commit>` writes
the entry and its hash.

## Modules

| module | what it does |
|---|---|
| `sys` | `std.os.linux` calls with EINTR retried and errno mapped to a Zig error set |
| `fsx` | open without following a final symbolic link, checks on the descriptor (`fstat`), a copy that renames into place so a short write does not destroy the destination, line append, atomic replace keeping owner, mode and access ACLs, cross-filesystem move with strict or portable ACL handling, directory iteration, `rm -rf` that never follows links, `realpath` through `/proc/self/fd` |
| `proc` | run a program by absolute path with an empty signal mask, default handlers and no descriptors above 2, by default in its own session; stdin fed and stdout and stderr read at once, each with a cap; an optional deadline, SIGTERM, a grace period, SIGKILL to the process group; a cancel flag a signal handler can set; group members left after the child exits are killed before it is reaped; `which` looks a name up in an explicit PATH |
| `logs` | `gzip -9` in place with gzip's header (name, mtime, OS byte), owner, mode and times kept; rewrite of `.licensed-logs` entries |
| `env` | the environment as raw bytes with getenv's first-entry rule, duplicate names found, a child environment built with each name once, shell name check |
| `state` | private files in a shared directory: trusted only when the open file is a regular file of this user with one link and no group or other bits, a lock trusted the same way, atomic 0600 writes; `RootLock`, a flock gate plus a POSIX record lock on a sidecar, with a deadline read from the clock. The gate and the sidecar must each be a regular file of this user with one link |
| `json` | a JSON reader with Python's two string encodings (surrogateescape text, one byte per code point), Python values, and `json.dumps(indent=N, sort_keys=True)` byte for byte, float repr included |
| `pytext` | byte strings as Python text: the surrogateescape character, the 'replace' decoder, str.isspace, strip and split, shlex.quote |
| `atomic` | `atomic_write`: replace a file only after its bytes, owner, mode and every ACL form (GPFS NFSv4, NFSv4, POSIX access) are durable and read back; fault points before write, fsync and rename |
| `syslog` | events to a collector: a `unix:`, `journal:`, `udp:` or `tcp:` target, RFC 5424 and native journald framing for the `Identity` the caller names, and `send`, the transport alone, with a timeout; nothing here fails the caller |
| `cli` | messages to stdout and stderr that ignore a closed stream, exit code 2 for a refused invocation, the version line |

## Test

```bash
zig build test --summary all
```

## Compatibility

[COMPAT.md](https://github.com/stackhands/zig-common/blob/main/COMPAT.md) lists the library version, the Zig version, and the tool
versions built on each.

## License

MIT, see [LICENSE](https://github.com/stackhands/zig-common/blob/main/LICENSE).

<!-- stackhands:begin -->
## Part of stackhands

zig-common is one of the [stackhands](https://github.com/stackhands) tools for building, installing and maintaining an HPC software stack with EasyBuild on top of EESSI.

| Tool | Job | Docs |
|---|---|---|
| [eb-stack](https://github.com/stackhands/eb-stack) | Solve, shard and plan an EasyBuild build list; admit builds under a scratch inode budget | [docs](https://eb-stack.rgoswami.me/) |
| [eb-staged-rebuild](https://github.com/stackhands/eb-staged-rebuild) | Rebuild an installation in a staged tree and swap it in, so running jobs keep their paths | [docs](https://stackhands.github.io/eb-staged-rebuild/) |
| [eessi-arch-guard](https://github.com/stackhands/eessi-arch-guard) | Reload EESSI in a Slurm task that inherited it for another CPU or GPU | [docs](https://stackhands.github.io/eessi-arch-guard/) |
| [eb-local](https://github.com/stackhands/eb-local) | Install software with EasyBuild on top of EESSI into a directory a user or project owns | [docs](https://stackhands.github.io/eb-local/) |
| [eb-keep-logs](https://github.com/stackhands/eb-keep-logs) | Keep a failed build's EasyBuild log and command output; rotate a pipeline's log tree | [docs](https://stackhands.github.io/eb-keep-logs/) |
| [rfc9162](https://github.com/stackhands/rfc9162) | Append-only Merkle logs hashed as RFC 9162, with tiled storage and signed checkpoints | [docs](https://stackhands.github.io/rfc9162/) |
| **zig-common** | The shared Zig library under the Zig tools: system calls, checked files, child processes | [docs](https://stackhands.github.io/zig-common/) |
<!-- stackhands:end -->
