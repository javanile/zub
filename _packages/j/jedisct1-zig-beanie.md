---
title: zig-beanie
description: BEANIE tweakable block cipher for Zig.
license: ""
author: jedisct1
author_github: jedisct1
repository: https://github.com/jedisct1/zig-beanie
keywords:
  - beanie
  - block
  - block-cipher
  - cipher
  - tbc
  - tweakable-block-cipher
date: 2026-07-13
updated_at: 2026-07-13T12:50:11+00:00
last_sync: 2026-07-13T12:50:11Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 1
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/jedisct1/zig-beanie/
---

# zig-beanie

`zig-beanie` is a Zig implementation of BEANIE, the 32-bit tweakable block cipher.

BEANIE was designed for low-latency memory encryption on microcontrollers, where 32-bit words are common and software attacks are a primary concern. This repository provides a small Zig library in `src/root.zig`, a simple CLI example in `src/main.zig`, and in-source tests for the core cipher operations.

But is can have many other applications, especially since it's a perfect match for SIMD implementations.

## Cipher at a glance

- 32-bit block cipher
- tweakable design for memory-encryption style contexts
- 128-bit key and 128-bit tweak in this implementation

## Reference

Simon Gerhalter, Samir Hodzic, Marcel Medwed, Marcel Nageler, Artur Folwarczny, Ventzi Nikov, Jan Hoogerbrugge, Tobias Schneider, Gary McConville, and Maria Eichlseder, "BEANIE - A 32-bit Cipher for Cryptographic Mitigations Against Software Attacks," IACR Transactions on Symmetric Cryptology, 2025(4), pp. 31-69.
