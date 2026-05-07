---
title: Zig-BitHelper
description: mirror of codeberg.org/bcrist/zig-bithelper
license: NOASSERTION
author: bcrist
author_github: bcrist
repository: https://github.com/bcrist/Zig-BitHelper
keywords:
  - util
  - utilities
  - utility-library
  - utils
date: 2026-04-18
updated_at: 2026-04-18T16:13:15+00:00
last_sync: 2026-04-18T16:13:15Z
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
permalink: /packages/bcrist/Zig-BitHelper/
---

# Zig-BitHelper

Provides some helper functions for dealing with integers as bit fields:

  - bits.as: Similar to @bitCast, but works with enums as well
  - bits.zx: Casts as unsigned and zero-extends to the requested size
  - bits._1x: Casts as unsigned and one-extends to the requested size
  - bits.sx: Casts as signed and then extends to the requested size
  - bits.concat: Concatenates unsigned integers (little endian)
  - bits.swapHalves: Swaps the high and low halves of an integer with event bit count
