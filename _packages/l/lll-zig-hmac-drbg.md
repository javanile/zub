---
title: zig-hmac-drbg
description: Deterministic random bit generator using hmac/sha256 as per NIST 800-90A
license: MIT
author: lll
author_github: lll
repository: https://github.com/lll/zig-hmac-drbg
keywords:
date: 2026-05-27
updated_at: 2026-05-27T02:07:32+00:00
last_sync: 2026-05-27T02:07:32Z
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
permalink: /packages/lll/zig-hmac-drbg/
---

# zig-hmac-drbg
[![zig version](https://img.shields.io/badge/0.15.2-orange?style=flat&logo=zig&label=Zig&color=%23eba742)](https://ziglang.org/download/)
[![zig doc](https://img.shields.io/badge/zigdoc%20-pages-orange?color=%23eba742)](https://lll.github.io/zig-hmac-drbg/)
[![reference Zig](https://img.shields.io/badge/deps%20-0-orange?color=%23eba742)](https://github.com/lll/zig-hmac-drbg/blob/main/build.zig.zon)
[![build](https://github.com/lll/zig-hmac-drbg/actions/workflows/build.yml/badge.svg)](https://github.com/lll/zig-hmac-drbg/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Deterministic random bit generator using hmac/sha256 as per NIST 800-90A.

## Usage

```zig
const std = @import("std");
const hmacdrbg = @import("hmac_drbg");

pub fn main() !void {
    var seed: [48]u8 = undefined;
    std.crypto.random.bytes(&seed);

    var rng = hmacdrbg.HmacDrbg.init(256, &seed, null);

    var out: [32]u8 = undefined;
    _ = rng.generate(&out);

    // Re-seeding is required every 10,000 generate calls
    var new_seed: [48]u8 = undefined;
    std.crypto.random.bytes(&new_seed);
    try rng.reseed(&new_seed);
}
```
