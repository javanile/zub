---
title: eth-p2p-z
description: Ethereum p2p implementation in Zig
license: ""
author: zen-eth
author_github: zen-eth
repository: https://github.com/zen-eth/eth-p2p-z
keywords:
  - beacon-chain
  - gossipsub
  - lean-ethereum
  - libp2p
  - libp2p-muxer
  - libp2p-pubsub
  - libp2p-security
  - libp2p-transport
  - multistream
  - quic
date: 2026-04-21
category: networking
updated_at: 2026-04-21T10:03:32+00:00
last_sync: 2026-04-21T10:03:32Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/zen-eth/eth-p2p-z/
---

# eth-p2p-z

Zig implementation of the Ethereum peer-to-peer stack, built on top of the [libp2p](https://libp2p.io/) architecture.

**Note**: This project is pre-release software. Expect rapid iteration and frequent breaking API changes while we carve out the Ethereum-focused feature set.

## Project scope

- Transport: QUIC (lsquic-backed) is the only supported transport. TCP, WebRTC, WebTransport, and other stacks are intentionally out of scope.
- PubSub: Gossipsub v1.0 router is available today; additional Ethereum networking protocols will be layered on top in subsequent milestones.
- Platform: Zig 0.15.2 toolchain targeting modern desktop/server environments. Browser runtimes are not supported.

If you are looking for a general-purpose libp2p implementation with multiple transports and protocol stacks, this project is not a drop-in replacement.

## Prerequisites

- Zig 0.15.2

## Building

To build the project, run the following command in the root directory of the project:

```bash
zig build -Doptimize=ReleaseSafe
```

## Running Tests

To run the tests, run the following command in the root directory of the project:

```bash
zig build test --summary all
```

## Usage

Update `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/zen-eth/zig-libp2p.git
```

In your `build.zig`:

```zig
const libp2p_dep = b.dependency("libp2p", .{
    .target = target,
    .optimize = optimize,
});
const libp2p_module = libp2p_dep.module("zig-libp2p");
root_module.addImport("libp2p", libp2p_module);
```
