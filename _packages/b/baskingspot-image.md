---
title: image
description: "Image decoders and encoders in Zig with no C: PNG, JPEG, GIF, WebP, TIFF, JPEG XL, and more."
license: MIT
author: baskingspot
author_github: baskingspot
repository: https://github.com/baskingspot/image
keywords:
date: 2026-11-03
updated_at: 2026-11-03T16:52:21+00:00
last_sync: 2026-11-03T16:52:21Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 3
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/baskingspot/image/
---

# image

Image decoders and encoders in Zig with no C: PNG, JPEG, GIF, WebP, TIFF, JPEG XL, and more.

This project is incubating. It is unstable, its API will change, and it is not ready to depend on.

## Work on it

`nix develop` provides the toolchain, the reference libraries, and the
comparison arms, and `just ci` runs what CI runs: the tests in Debug,
ReleaseSafe, and on a big-endian target, the linters, a bounded fuzz run, and
the differential comparison against the reference decoders. `just fuzz`,
`just oracle`, and `just bench-compare` run the longer versions; `just corpus`
fetches the conformance suites (see `corpus/README.md`, `bench/README.md`,
and `THIRD_PARTY.md`).

## License

MIT. See `LICENSE`.
