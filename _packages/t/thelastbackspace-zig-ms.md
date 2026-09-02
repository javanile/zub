---
title: zig-ms
description: "Convert duration strings like \"2 days\" to milliseconds and back — a small Zig library"
license: MIT
author: thelastbackspace
author_github: thelastbackspace
repository: https://github.com/thelastbackspace/zig-ms
keywords:
  - duration
  - time
date: 2026-08-27
updated_at: 2026-08-27T21:44:02+00:00
last_sync: 2026-08-27T21:44:02Z
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
permalink: /packages/thelastbackspace/zig-ms/
---

# ms

[![CI](https://github.com/thelastbackspace/zig-ms/actions/workflows/ci.yml/badge.svg)](https://github.com/thelastbackspace/zig-ms/actions/workflows/ci.yml)

Convert human-readable duration strings to milliseconds, and milliseconds
back to human-readable strings.

```zig
const ms = @import("ms");

const two_days = try ms.parse("2 days"); // 172800000
const short = try ms.format(allocator, 2000, .{}); // "2s"
const long = try ms.format(allocator, 2000, .{ .long = true }); // "2 seconds"
// `short` and `long` are caller-owned; free them when done.
```

## Installation

Requires Zig 0.16.0.

```sh
zig fetch --save git+https://github.com/thelastbackspace/zig-ms#v1.0.0
```

Or pinned to the release archive:

```sh
zig fetch --save ms https://github.com/thelastbackspace/zig-ms/archive/refs/tags/v1.0.0.tar.gz
```

Then in `build.zig`:

```zig
const ms = b.dependency("ms", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("ms", ms.module("ms"));
```

## API

### `parse(str: []const u8) ParseError!f64`

Parse `"2 days"`, `"1.5h"`, `"100"`, ... into milliseconds.

Units are case-insensitive: `y/yr/yrs/year/years`, `mo/month/months`,
`w/week/weeks`, `d/day/days`, `h/hr/hrs/hour/hours`,
`m/min/mins/minute/minutes`, `s/sec/secs/second/seconds`,
`ms/msec/msecs/millisecond/milliseconds`. The unit is optional, so
`"100"` is 100 ms. Spaces between the number and the unit are allowed
(`"1   s"`); trailing spaces after the unit are not. A year is 365.25
days; a month is one twelfth of a year.

Strings that do not match the grammar return NaN. Empty input is
`error.EmptyInput`; input over 100 characters is `error.InputTooLong`
(counted in Unicode code points).

### `format(allocator: Allocator, value: f64, options: FormatOptions) FormatError![]u8`

Render milliseconds with the largest unit that fits: `"3d"` for
234234234. Values are rounded to the nearest integer, halves toward
positive infinity, so `-1500` is `"-1s"`, not `"-2s"`. Pass
`.long = true` for verbose, pluralized output (`"3 days"`). The caller
owns the returned memory. NaN and infinities yield
`error.NonFiniteNumber`.

## Notes

- Rounding replicates JavaScript's `Math.round` (`@floor(x + 0.5)`), so
  results line up with the many libraries sharing those semantics.
- The 100-character limit counts Unicode code points.
- Values below one unit print as plain decimals; there is no exponent
  notation for very large inputs.

## Testing

```sh
zig build test
```

## Contributing

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The CI gate
(, tests, build) must pass.

## Credits

Behavior and the test suite follow the npm package
[`ms`](https://github.com/vercel/ms) v4.0.0 (MIT, © Vercel, Inc.);
semantics are reimplemented, not copied. Zig implementation
© 2026 thelastbackspace, MIT — see [LICENSE](LICENSE).
