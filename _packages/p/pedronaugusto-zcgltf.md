---
title: zcgltf
description: Zig bindings for cgltf — vendored upstream v1.15, complete surface enforced at compile time, std.mem.Allocator and std.Io adapters, ABI drift guarded by tests
license: MIT
author: pedronaugusto
author_github: pedronaugusto
repository: https://github.com/pedronaugusto/zcgltf
keywords:
  - zig-gamedev
date: 2026-09-14
updated_at: 2026-09-14T02:52:58+00:00
last_sync: 2026-09-14T02:52:58Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/pedronaugusto/zcgltf/
---

# zcgltf

[![CI](https://github.com/pedronaugusto/zcgltf/actions/workflows/ci.yml/badge.svg)](https://github.com/pedronaugusto/zcgltf/actions/workflows/ci.yml)

Zig bindings for [cgltf](https://github.com/jkuhlmann/cgltf). Parse glTF and
GLB from memory or from a file, load buffers, validate, read vertex data back
through the accessor API, and write documents out again.

## Usage

The block below is a region of [`examples/usage.zig`](examples/usage.zig),
which `zig build examples` builds and runs. `ci/readme_usage.sh` extracts it
and `ci/check-docs.sh` fails the build if this copy has drifted from it.

<!-- BEGIN GENERATED ci/readme_usage.sh -->
```zig
const zcgltf = @import("zcgltf");

var options = std.mem.zeroes(zcgltf.Options);
options.memory = zcgltf.memoryOptions(&gpa);

const path = "tests/data/triangle.gltf";
const data = try zcgltf.parseFile(&options, path);
defer zcgltf.free(data);
try zcgltf.loadBuffers(&options, data, path);
try zcgltf.validate(data);

const prim = &data.meshes.?[0].primitives.?[0];
const positions = zcgltf.findAccessor(prim, .position, 0) orelse
    return error.MissingPositions;
const indices = prim.indices orelse return error.MissingIndices;

var corners: [9]f32 = undefined;
const floats = zcgltf.unpackFloats(positions, &corners);
var index_values: [3]u32 = undefined;
const idx = zcgltf.unpackIndices(indices, u32, &index_values);
```
<!-- END GENERATED -->

## Install

```sh
zig fetch --save git+https://github.com/pedronaugusto/zcgltf#v0.1.2
```

Then in `build.zig`:

```zig
const zcgltf_dep = b.dependency("zcgltf", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("zcgltf", zcgltf_dep.module("zcgltf"));
```

A C or C++ host links the library and includes upstream's own headers, which
the artifact installs:

```zig
exe.root_module.linkLibrary(zcgltf_dep.artifact("zcgltf"));  // then #include <cgltf.h>
```

zcgltf fetches no dependencies: cgltf is vendored in `libs/cgltf`, pinned by
commit and byte-identical to upstream — see [UPSTREAM.md](UPSTREAM.md).
Forward `optimize` as shown; a Debug library inside a release executable is
not what you meant.

## The API

Vendored upstream is cgltf `v1.15`. Every function `cgltf.h` and
`cgltf_write.h` declare is bound as an extern, and every struct and enum they
declare is mirrored field by field; the test `ABI: src/c/ agrees with cgltf's
headers, and binds all of them` in `src/abi_check.zig` fails the build if a
header function is not bound. The idiomatic layer wraps all of them but
`cgltf_copy_extras_json`, which upstream deprecates in favour of reading
`Extras.data` directly; it stays reachable as
`zcgltf.c.access.cgltf_copy_extras_json`.

| | |
|---|---|
| Document lifecycle | `parse`, `parseFile`, `loadBuffers`, `loadBufferBase64`, `validate`, `free` |
| Strings | `decodeString`, `decodeUri` |
| Accessor reading | `findAccessor`, `readFloat`, `readUint`, `readIndex`, `unpackFloats`, `unpackIndices`, `unpackFloatsCount`, `unpackIndicesCount`, `bufferViewData` |
| Element sizing | `numComponents`, `componentSize`, `calcSize` |
| Node transforms | `nodeTransformLocal`, `nodeTransformWorld` |
| Object to index | `indexOf`, `animationIndexOf` |
| Writing | `writeFile`, `writeAlloc` |
| Adapters | `memoryOptions`, `freeThrough`, `fileOptions` |
| The raw C surface | `zcgltf.c` |

The document model is re-exported under Zig names — `cgltf_buffer_view` is
`BufferView` — with optionals where upstream documents a field as omittable,
so reading a parsed document is `orelse` rather than a null check remembered
or forgotten. Enums keep upstream's values, the GL-valued sampler constants
included, and the API's one anonymous union is a named `CameraData`.

`cgltf_result` folds into one `Error` set; values that are answers — a count,
an index — stay plain values. Wrappers take and return slices and derive
counts from `len`, so no wrapper asks for a length a slice already knows.
`indexOf` is one comptime-dispatched entry point for all of upstream's
per-type index helpers. `version()` reports `build.zig.zon`'s version, which
is the only place it is written.

## Design

### Allocators

`memoryOptions(allocator)` fills cgltf's per-call `MemoryOptions` from a
`std.mem.Allocator`. Per-call, not process-global: two documents can use two
allocators.

It covers everything the parser allocates — cgltf routes all of that through
`options->memory`. It does not cover `cgltf_write_file`, which allocates its
serialization buffer with plain `malloc` and opens the file with `fopen`
(`cgltf_write.h:1248`, `cgltf_write.h:1253`), reaching neither hook. To write
through a Zig allocator, use `writeAlloc`.

cgltf frees with `free(ptr)` and passes no size, while a Zig allocator needs
the length back, so the adapter stores a size header ahead of each block
(16-byte aligned, so any alignment upstream's structs assume still holds);
[BINDING.md](BINDING.md) has the shape. That header is why a block cgltf hands
back for the caller to own — the one `loadBufferBase64` returns — must be
released with `freeThrough(&options.memory, buf.ptr)` and never with the
allocator directly: the pointer cgltf sees is past the header, so
`allocator.free(buf)` would pass the wrong base and the wrong length.
`freeThrough` falls back to `std.c.free` when no hooks are installed, so it is
correct for either kind of options.

### File I/O

`fileOptions(io)` replaces the fopen-based default reader with `std.Io`. That
closes two portability holes rather than adding a convenience: upstream's
default cannot open a path outside the ANSI code page on Windows, and,
compiled by anything but MSVC, it sizes files with a 32-bit `ftell`, so a
`.glb` over 2 GiB fails as `io_error`. [UPSTREAM.md](UPSTREAM.md) has the
file:line for both, and `FileOptions.read` is upstream's own documented escape
hatch for exactly this. It covers reading; upstream offers no write hook.

### The ABI guard

The externs and the document-model mirror are hand-written, not produced by
translate-c, so the wrapper gets the types it wants and the shipped module
never compiles C. Nothing in either compiler then checks that
those declarations still agree with the headers, and a `cgltf_size` narrowed
to `c_int` links cleanly and corrupts. `src/abi_check.zig` closes that: a
comptime `@cImport` of the vendored headers, in the test module only, compared
against `src/c/*.zig` by reflection — every field by name and by offset, every
signature, every enumerator's value, the union member by member. Drift is a
compile error rather than a memory-corruption bug, and the same sweep run
backwards is what makes completeness a build property.

`ci/check-abi-drift.sh` proves the guard fires, by applying deliberate drifts
one at a time and requiring each to be refused. CI runs it on the
x86_64-linux-gnu ABI and on MSVC's, because the headers are compared as
preprocessed and laid out for a target. [docs/abi-guard.md](docs/abi-guard.md)
has the detail.

### Build options

- `-Dsanitize_c=true` compiles the C with Zig's undefined-behaviour sanitizer.
  It is off by default, and deliberately not tied to `optimize`: the sanitizer
  emits calls into a runtime linked only into a compilation that is itself
  sanitized, so a consumer who forgot to forward `optimize` would get an
  `undefined symbol: __ubsan_handle_*` link failure naming nothing they can
  act on. zcgltf's own CI runs Debug both ways.
- Options are declared once and mirrored into a Zig module, re-exported as
  `zcgltf.options`, so the wrapper cannot disagree with how the C was
  compiled.
- One translation unit compiles — `src/cgltf_impl.c`, which instantiates the
  implementation-in-header parser and writer exactly once — and it is listed
  explicitly, never globbed.

## Scope

- Vendored cgltf is `v1.15`. A later upstream release is a re-vendor;
  [UPSTREAM.md](UPSTREAM.md) has the procedure.
- Static library only: cgltf declares no export macro, so a shared build would
  export nothing.
- `cgltf_copy_extras_json` is bound but not wrapped; `Extras.data` carries the
  same span.
- cgltf parses `EXT_meshopt_compression` and does not decode it. Decoding is a
  call the host makes into meshoptimizer —
  [docs/meshopt-pairing.md](docs/meshopt-pairing.md) is the contract, and
  `tests/interop/` runs it end to end.
- The writer does not emit `EXT_meshopt_compression`: `cgltf_write.h` has no
  handling for it, so a document parsed from a compressed asset writes back
  without the extension.
- Draco is parsed as metadata only; upstream ships no Draco decoder.

## Platforms

| | Suite executed by CI | Compile-checked by CI |
|---|---|---|
| Linux | x86_64 glibc | aarch64 glibc, x86_64 musl |
| macOS | aarch64 | x86_64 |
| Windows | x86_64, both the gnu and the MSVC ABI | aarch64 gnu |

Every job in that matrix passed on [run
`34780059981`](https://github.com/pedronaugusto/zcgltf/actions/runs/34780059981).

## Testing

```sh
zig build test
```

runs the ABI cross-check, the behavioural tests — vertex data read back
through accessors, node transforms, error mapping, a write-and-reparse round
trip, and both adapters against `std.testing.allocator`, so an unbalanced
allocation seam is a leak-check failure — the C smoke test (`zig build
test-c`), which proves the installed headers and library stand alone with no
Zig in the picture, and the examples, which are built and run.

```sh
zig build --build-file tests/consumer/build.zig run
```

builds zcgltf the way a downstream package does, through `b.dependency`. That
path resolves the artifact by scanning the dependency's install step and the
headers by their installed spelling; nothing in `src/` exercises either, so
both can break while the whole suite stays green.

```sh
ci/run.sh            # the full matrix
ci/run.sh --quick    # native Debug only, for the inner loop
ci/install-hooks.sh  # run the matrix automatically before every push
```

`ci/run.sh` mirrors [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and
reports every failure rather than stopping at the first. The drift proof runs
on this host's ABI; the second arm is
`ci/run.sh --drift-target=x86_64-windows-msvc`, kept out of the default
because it rebuilds once per mutation. CI runs both on every push, and a
release should run both here.

### By the numbers

<!-- BEGIN GENERATED ci/measurements.sh --markdown -->
| | |
|---:|---|
| **0.1.2** | version (one home: `build.zig.zon`) |
| **39** | upstream C entry points (declared in the vendored `cgltf.h` + `cgltf_write.h`) |
| **39** | Zig externs (`pub extern fn` in `src/c/*.zig`) |
| **49** | structs mirrored field-by-field (`src/c/types.zig`) |
| **17** | enums mirrored enumerator-by-enumerator |
| **15** | Zig tests `zig build test` executes |
| **2332** | Zig source lines (`src/`) |
| **19** | deliberate drifts `ci/check-abi-drift.sh` must refuse |
| **23** | steps `ci/run.sh` runs |
| **7** | further targets `ci/run.sh` cross-compiles |
<!-- END GENERATED -->

Not one of those is typed into this file. `ci/measurements.sh` recomputes them
from the tree and `ci/check-docs.sh` fails the build if what is committed
differs, or if a top-level document states any other multi-digit number by
hand without a line in `tools/doc_numbers.txt` saying why it cannot go stale.
[docs/contributing.md](docs/contributing.md) records what that gate cannot
catch.

## Requirements

Zig 0.16.0, and libc, which the library links. Nothing else.

## Contributing

Issues and pull requests are welcome.
[docs/contributing.md](docs/contributing.md) has what a pull request has to
satisfy, and [BINDING.md](BINDING.md) is the contract for how surface is
shaped.

## Licence

MIT, see [LICENSE](LICENSE). Vendored cgltf is MIT, copyright Johannes
Kuhlmann; its inlined jsmn JSON tokenizer is MIT, copyright Serge Zaitsev.
