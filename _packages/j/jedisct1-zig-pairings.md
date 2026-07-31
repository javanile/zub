---
title: zig-pairings
description: Pairing-friendly curves in pure Zig (BLS12-381, BN462).
license: ""
author: jedisct1
author_github: jedisct1
repository: https://github.com/jedisct1/zig-pairings
keywords:
  - bn381
  - bn462
  - pairing
  - pairing-cryptography
  - pairings
date: 2026-07-30
updated_at: 2026-07-30T04:26:27+00:00
last_sync: 2026-07-30T04:26:27Z
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
permalink: /packages/jedisct1/zig-pairings/
---

# Pairings for Zig

A pairing-friendly elliptic curve library for Zig, implementing BLS12-381 and BN462 at the 128-bit security level.

Useful for BLS signatures, zero-knowledge proofs, etc.

This work is based on the [`draft-irtf-cfrg-pairing-friendly-curves`](https://datatracker.ietf.org/doc/draft-irtf-cfrg-pairing-friendly-curves/) draft.

## Curves

### BLS12-381

The primary curve, widely used in Ethereum 2.0, Zcash, and other systems.

- G1: Points on E(Fp): y^2 = x^3 + 4 (projective coordinates)
- G2: Points on the sextic twist E'(Fp2): y^2 = x^3 + 4(u+1) (projective coordinates)
- GT: Target group in Fp12, reached via optimal Ate pairing

### BN462

A Barreto-Naehrig curve at the 128-bit security level.

## Usage

Add the package to your `build.zig.zon` dependencies, then:

```zig
const bls = @import("pairings").bls12_381;

const g1 = bls.G1.basePoint;
const g2 = bls.G2.basePoint;

// Compute a pairing
const gt = bls.pairing.pair(g1, g2);

// Scalar multiplication
const s: bls.scalar.CompressedScalar = ...; // 32-byte little-endian scalar
const p = g1.mul(s, .little) catch unreachable;

// Random points (requires std.Io)
const random_g1 = bls.G1.random(io);
const random_g2 = bls.G2.random(io);

// Serialization
const compressed = g1.toCompressed();
const restored = try bls.G1.fromCompressed(compressed);
```
