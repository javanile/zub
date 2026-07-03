---
title: zig-silithium
description: "Silithium: Compact, Efficient and Non-separable Hybrid Signatures."
license: MIT
author: jedisct1
author_github: jedisct1
repository: https://github.com/jedisct1/zig-silithium
keywords:
  - combiner
  - hybrid
  - post-quantum
  - pq
  - signatures
  - silithium
date: 2026-07-01
updated_at: 2026-07-01T10:43:02+00:00
last_sync: 2026-07-01T10:43:02Z
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
permalink: /packages/jedisct1/zig-silithium/
---

# Silithium: Compact, Efficient and Non-separable Hybrid Signatures

An implementation of Silithium, from the paper "Compact, Efficient and Non-separable Hybrid Signatures" by Julien Devevey, Morgane Guerreau, and Maxime Romeas.

Silithium is a hybrid signature scheme built from a classical elliptic-curve signature and ML-DSA.

Istead of signing a message twice and concatenating the two signatures, Silithium makes both sides share one Fiat-Shamir challenge.

The resulting signature is smaller than a naive composite signature and is not separable into useful standalone classical or post-quantum signatures.
