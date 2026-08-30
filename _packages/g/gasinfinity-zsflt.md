---
title: zsflt
description: "Mirror of https://codeberg.org/GasInfinity/zsflt"
license: MIT
author: GasInfinity
author_github: GasInfinity
repository: https://github.com/GasInfinity/zsflt
keywords:
date: 2026-08-17
updated_at: 2026-08-17T22:54:23+00:00
last_sync: 2026-08-17T22:54:23Z
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
permalink: /packages/GasInfinity/zsflt/
---

# zsflt

An IEEE soft-float + fixed point library, used extensively in [zitrus](https://github.com/GasInfinity/zitrus/tree/main).

## Coverage:
- Conversion between arbitrary IEEE754 floating point values with nearest-even rounding handling almost all denormal cases (except denormal -> normal where DAZ currently).
- Arbitrary Fixed-point values and conversion between floating point and fixed.
