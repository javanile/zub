---
title: zig-hiae
description: HiAE - A High-Throughput Authenticated Encryption Algorithm for Cross-Platform Efficiency.
license: ""
author: hiae-aead
author_github: hiae-aead
repository: https://github.com/hiae-aead/zig-hiae
keywords:
  - aead
  - aes
  - encryption
  - hiae
date: 2026-05-27
updated_at: 2026-05-27T12:05:14+00:00
last_sync: 2026-05-27T12:05:14Z
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
permalink: /packages/hiae-aead/zig-hiae/
---

# HiAE: A High-Throughput Authenticated Encryption Algorithm for Cross-Platform Efficiency

A Zig implementation of HiAE, along with support for parallel variants.

## Benchmarks

### Encryption

#### Zen4

| Variant | Throughput |
| :------ | ---------: |
| HiAE    | 252.0 Gb/s |
| HiAEX2  | 449.9 Gb/s |
| HiAEX4  | 472.8 Gb/s |

#### Apple M1

| Variant | Throughput |
| :------ | ---------: |
| HiAE    | 169.5 Gb/s |
| HiAEX2  | 133.9 Gb/s |
| HiAEX4  |  98.3 Gb/s |

#### WebAssembly (lime1+simd128)

| Variant | Throughput |
| :------ | ---------: |
| HiAE    |   9.2 Gb/s |
| HiAEX2  |  11.0 Gb/s |
| HiAEX4  |   7.7 Gb/s |

#### MAC

#### Zen4 (likely limited by the memory bandwidth)

| Variant    | Throughput |
| :--------- | ---------: |
| HiAE-MAC   | 315.8 Gb/s |
| HiAEX2-MAC | 530.4 Gb/s |
| HiAEX4-MAC | 522.2 Gb/s |
| LeMAC      | 345.0 Gb/s |

#### Apple M1

| Variant    | Throughput |
| :--------- | ---------: |
| HiAE-MAC   | 163.1 Gb/s |
| HiAEX2-MAC | 182.9 Gb/s |
| HiAEX4-MAC | 138.8 Gb/s |
| LeMAC      | 219.2 Gb/s |

#### WebAssembly (lime1+simd128)

| Variant | Throughput |
| :------ | ---------: |
| HiAE    |   9.8 Gb/s |
| HiAEX2  |  12.0 Gb/s |
| HiAEX4  |   7.7 Gb/s |
| LeMAC   |  10.0 Gb/s |


## Circuits

### Absorption

![Absorption in HiAE](.media/s1.png)

### Encryption

![Encryption in HiAE](.media/s2.png)

### Inversion

![Inversion in HiAE](.media/s3.png)
