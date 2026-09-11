---
title: zig-base91
description: Base91 encoding for Zig.
license: MIT
author: jedisct1
author_github: jedisct1
repository: https://github.com/jedisct1/zig-base91
keywords:
  - base64
  - base91
  - codec
date: 2026-09-10
updated_at: 2026-09-10T00:54:44+00:00
last_sync: 2026-09-10T00:54:44Z
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
permalink: /packages/jedisct1/zig-base91/
---

# Base91 for Zig

An implementation of the Base91 encoding scheme written in Zig.

It enables you to convert binary data to a Base91-encoded string and vice versa.

## Overview

- **Space Efficiency:** Base91 produces shorter encoded strings compared to Base64, which can be advantageous when minimizing data size is a priority.
- **Performance Trade-Off:** Although Base91 is more space-efficient, its encoding/decoding operations are generally slower than those of Base64. This trade-off should be considered based on your application’s requirements.

## Considerations

- **When to Use:** Opt for Base91 when reducing the size of encoded data is critical, such as in bandwidth-constrained environments or when storing large volumes of encoded data.
- **When to Avoid:** If your application is performance-sensitive and the encoding/decoding speed is paramount, Base64 might be a more suitable alternative.
