---
title: Zig-ROM-Compress
description: mirror of codeberg.org/bcrist/zig-rom-compress
license: NOASSERTION
author: bcrist
author_github: bcrist
repository: https://github.com/bcrist/Zig-ROM-Compress
keywords:
  - compression
  - compression-algorithm
  - embedded
  - encoding
  - rom
date: 2026-04-18
category: systems
updated_at: 2026-04-18T16:20:56+00:00
last_sync: 2026-04-18T16:20:56Z
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
permalink: /packages/bcrist/Zig-ROM-Compress/
---

# Zig-Rom-Compress

A simple algorithm for in-storage compression of potentially sparse data where the data will be fully uncompressed before usage.

The motivating use case is when using a microcontroller to bootstrap an SRAM at reset, which will thereafter function as a lookup table/ROM.
Often times such lookup tables may contain several megabytes of highly patterned data, but you'd like to initialize it with just a small/cheap microcontroller, and typically these will have much less than 1MB of flash memory.

Note for most data, an LZ-based compressor like DEFLATE will achieve a better compression ratio, but doesn't support sparse data without adding additional metadata.
The decompressor for this scheme is also very simple and requires only a few bytes of working RAM.

## Algorithm

The key insight that we make use of is that many data words are likely to be repeated many times,
and there may be many "don't care" addresses that we need not initialize at all.
Furthermore, the data need not be reconstructed in linear order.

The compressor begins by partitioning the data into lists of addresses which point to the same data value.
Then it sorts the addresses within those lists, and sorts the partitions based on the data value.
It can then use delta compression and RLE on the transformed data.

The algorithm works well in most real-world cases where there are many addresses with the same data value,
and even better if those addresses appear in contiguous blocks.
It is possible, however, (particularly with encrypted or random-like data) that the compressed version may actually be larger.
