---
title: zjolt
description: Zig bindings for Jolt Physics — vendored upstream Jolt, real C ABI with plain function-pointer callbacks, host allocator injection, ABI drift guarded by tests
license: MIT
author: pedronaugusto
author_github: pedronaugusto
repository: https://github.com/pedronaugusto/zjolt
keywords:
  - zig-gamedev
date: 2026-09-14
updated_at: 2026-09-14T03:30:52+00:00
last_sync: 2026-09-14T03:30:52Z
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
permalink: /packages/pedronaugusto/zjolt/
---

# zjolt

[![CI](https://github.com/pedronaugusto/zjolt/actions/workflows/ci.yml/badge.svg)](https://github.com/pedronaugusto/zjolt/actions/workflows/ci.yml)

Zig bindings for [Jolt Physics](https://github.com/jrouwe/JoltPhysics),
vendored at 5.6.0. Every Jolt subsystem is bound — shapes, bodies, the step,
queries, constraints, characters, vehicles, ragdolls, soft bodies and hair —
through a C ABI (`ffi/zjolt.h`) that a C or C++ host can link on its own, and
a Zig wrapper over it.

Status: **v0.2.1.** Pre-1.0, so naming and shape can change between minor
versions. There are no compatibility aliases, so there is one spelling of
everything.

## Usage

Every line below is quoted from `tests/consumer/src/main.zig`, which
`ci/run.sh` builds through `b.dependency` and runs. `ci/check-examples.sh`
fails if this block and that file stop matching character for character.

`tests/consumer/src/main.zig`
```zig
pub fn main() !void {
    var gpa_state = std.heap.DebugAllocator(.{}){};
    defer std.debug.assert(gpa_state.deinit() == .ok);
    const gpa = gpa_state.allocator();

    try zjolt.init(.{ .allocator = gpa });
    defer zjolt.deinit();

    const jobs = try zjolt.JobSystem.initThreadPool(.{});
    defer jobs.deinit();

    const system = try zjolt.PhysicsSystem.init(.{ .layers = zjolt.layersFromType(Layers) });
    defer system.deinit();

    const shape = try zjolt.Shape.initSphere(0.5, .{});
    defer shape.release();

    const ball = try system.bodies().createAndAdd(.{
        .shape = shape,
        .object_layer = Layers.moving,
        .position = zjolt.rvec3(0, 10, 0),
    }, .activate);

    // Per frame:
    var frame: usize = 0;
    while (frame < 60) : (frame += 1) {
        const update_error = try system.step(1.0 / 60.0, 1, jobs);
        if (update_error.contact_constraints_full) return error.ContactConstraintsFull;
    }

    // The ball began at y = 10 and gravity is the whole point, so this is
    // what says the library linked here really stepped.
    const transform = system.bodies().getTransform(ball);
    if (!(transform.position.y < 10)) return error.BallDidNotFall;

    try reportBuild();
}
```

`Layers` is a plain Zig struct in the same file: two object layers, two
broad-phase layers, and the four functions that map and filter them, which
`zjolt.layersFromType` turns into Jolt's three interfaces at comptime.
`reportBuild` is that file's last line and not part of the recipe: it checks
that the build options crossed the module boundary.

## Install

```sh
zig fetch --save git+https://github.com/pedronaugusto/zjolt#v0.2.1
```

Import the Zig module:

```zig
const zjolt_dep = b.dependency("zjolt", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("zjolt", zjolt_dep.module("zjolt"));
```

Or link the C library, from Zig or from a C or C++ host:

```zig
exe.root_module.linkLibrary(zjolt_dep.artifact("zjolt"));
```

Both are exercised by `tests/consumer`. Jolt is vendored in
`libs/JoltPhysics` and compiled from source: nothing else to fetch, no system
package to find. [UPSTREAM.md](UPSTREAM.md) has the pinned commit.

## The API

Every entry point is named after the Jolt method it calls:

    JPH::BodyInterface::GetLinearVelocity   ->  zjoltBodyGetLinearVelocity
    JPH::Shape::GetSubType                  ->  zjoltShapeGetSubType
    JPH::HingeConstraint::SetTargetAngle    ->  zjoltHingeConstraintSetTargetAngle
    JPH::CharacterVirtual::ExtendedUpdate   ->  zjoltCharacterUpdate

The rule is `zjolt` + the type + the method, and `src/abi_check.zig` pairs the
two sides of the ABI by name with no hand-written list, so a name that breaks
it fails the build. Two departures: the interface is dropped where Jolt has
only one, so `BodyInterface`'s methods are `zjoltBody*`; and overloads become
distinct names, with a `Locked` suffix on the form that requires you to
already hold the body lock.

The Zig wrapper drops the prefix and the type, because the receiver supplies
both: `system.bodies().getLinearVelocity(body)`. Anything it does not wrap is
reachable through `zjolt.c`, one namespace per header — `zjolt.c.body`,
`zjolt.c.constraint`, `zjolt.c.query`. [BINDING.md](BINDING.md) is the recipe
new surface follows, and records the decisions that stay settled.

## Scope

The scope is Jolt 5.6.0. **1459 C entry points** across **25 headers** cover:

| Subsystem | Bound |
|---|---|
| Shapes | The convex primitives (box, sphere, capsule, cylinder, triangle, tapered capsule, tapered cylinder, convex hull), mesh, height field, plane, empty, both compounds, and the decorated shapes (scaled, rotated-translated, offset-centre-of-mass). A mutable compound's children move, are added and are removed at run time. Introspection, mesh and height-field read-back, and binary save and restore for a collision cook. |
| Materials | Per triangle on a mesh and per quad on a height field, resolved into every query hit. |
| The world | Broad-phase and object layers and their filters, the step with a job-system seam, contact and activation listeners, step listeners, and the combine callbacks for friction and restitution. |
| Bodies | Create, destroy, add, remove, motion type, teleport, kinematic move, activate, velocities, forces and impulses, shape swap, user data, collision groups, read/write body locks, and batched add and remove. |
| Queries | Ray casts, shape casts, overlap and point tests, in closest-hit, all-hits and streaming forms, each with broad-phase layer, object layer, body and shape filters. `TransformedShape` runs the same queries against a single placed shape, with no physics system at all. |
| Constraints | All twelve kinds (fixed, point, hinge, slider, distance, cone, swing-twist, six-DOF, gear, rack and pinion, pulley, path), with their motors, limits, springs and run-time state. |
| Characters | `CharacterVirtual` with ground state, stair walking, shape swapping, contact listeners and character-versus-character collision; and the rigid `Character`. |
| Vehicles | Wheeled and tracked, with the drivetrain (engine, transmission, differentials), wheel pose and force read-back, and manual or automatic gears. |
| Ragdolls | Skeletons, poses, settings and instances, driving to a pose kinematically or with motors, and the body ids that map a contact back to a limb. |
| Soft bodies, hair | Both, including the compute-backend seam hair needs. |
| State | Save and restore, whole-system or one body at a time, for rollback, replay and determinism checks. |
| Debug draw | Arrays of lines, triangles and text for the host to render. Jolt's geometry collection behind it is compiled under `-Ddebug_renderer`. |
| Scenes | A whole world described as data, saved and restored. |
| Custom shapes | A Zig host implements Jolt's own shape interface, convex or general, without writing C++. |
| Geometry | GJK and EPA against any two support functions, convex hull building, polygon clipping, triangle indexing, and the AABB tree builder and splitters `MeshShape` is packed from. Usable without a physics system. |
| Triangle collision | Collide or cast a convex shape or a sphere against triangles fed one at a time, with active-edge normals and internal-edge removal. |
| Reflection | Jolt's RTTI over its own registered types, and the ObjectStream text and binary formats, which are compiled under `-Dobject_stream`, on by default. |
| Constraint parts | All fourteen, ported to Zig rather than bound, so a custom constraint's inner loop makes no foreign call. |
| Deterministic maths | Jolt's own trigonometry, matrix inversion and half-float conversions, bit-for-bit, for a build that has to agree with a C++ one. |

Every entry point has a Zig caller: `tools/zig_surface_exceptions.txt` is
empty, and `ci/check-coverage.sh` fails both when an entry point loses its Zig
caller and when an excuse is written for one that has a caller after all.
**13 entry points are native rather than wrapped** — a quaternion product, a
matrix transform, a lerp — because a cross-TU call cannot be inlined. Each has
a line in `tools/zig_native.txt` naming the declaration that computes it and
the test that compares the two answers.

Every public Jolt name in `libs/JoltPhysics/Jolt` carries a verdict and none
is a gap. The claimed areas hold **2682 public Jolt names** — every method,
every free function, and every public data member of a `*Settings` type.
**1367 are spelled out by an entry point** of a matching name. The other
**1315 carry a recorded verdict** in `tools/verdicts_*.txt`, one line each
naming what makes the name reachable: **600 `BOUND`**, **195 `EXTENSION`**,
**214 `INTERNAL`**, **190 `LANGUAGE`**, **116 `ZIG`** and **0 `GAP`**.
`ci/check-coverage.sh` fails the build on a gap;
[docs/coverage.md](docs/coverage.md) defines the other five verdicts.

Matching is by name, not by behaviour, and `BOUND` means the effect is
reachable through the entry points the line names, not that the upstream
symbol itself crosses the ABI:
`BodyInterface::ActivateBodiesInAABox` is `BOUND` because
`zjoltBodyActivateInBox` does the same thing under another name, not because
it is callable.

Not bound: Jolt's DX12, Vulkan and Metal compute backends, which need those
SDKs and are not compiled — a host with a device implements
`ZJoltComputeInterface` and passes it to `zjoltComputeSystemCreate`. The CPU
backend is compiled and bound.

## Design

What a caller has to know. The reasoning is in
[docs/design.md](docs/design.md).

- **Callbacks cross as C function pointers, not C++ vtables.** Every Jolt
  interface — the two layer filters, `ContactListener`,
  `BodyActivationListener`, the four query filters — is a function-pointer
  table with a `user` pointer. `zjolt.layersFromType` builds the tables from a
  Zig struct at comptime, `zjolt.layersFromInstance` from a value, so a host
  writes no `callconv(.c)` and no per-ABI variant.
- **Queries stream.** The collector is what the ABI exposes; closest-hit and
  count-then-fill are sinks over the same traversal. `onHit` returns an enum
  rather than an early-out fraction, and it runs with a broad-phase read lock
  held: a failure is stashed, the query stopped, and the error raised once the
  locks are dropped, so a caller writes `try`.
- **The frame loop has its own path.** `getActiveBodies` then `getTransforms`
  reads what moved in two ABI crossings, walking the ids in chunks under
  `BodyLockMultiRead` rather than taking one body lock each. An id whose body
  was destroyed since the step is reported through a count, not a failed
  batch. Bit masks arrive as Zig types: `update_error` is a
  `packed struct(u32)`, degrees of freedom are `.allowed_dofs = .plane_2d`.
- **Preconditions return instead of aborting.** Failure is a returned value
  throughout: **777 entry points return a `ZJoltResult`** and
  **385 return `void`**, the rest a value of their own, and `zjolt.lastError`
  carries the detail Jolt reports as a string. Jolt itself asserts where a
  library for a service would return, and several of those assertions sit on
  paths an ordinary caller reaches. Each one this ABI can reach is a returned
  error with a test behind it: a rotation is renormalised as it crosses the
  boundary, a setter Jolt asserts on for a static body does nothing, a trace
  thunk is installed unconditionally so a missing hook costs a line on stderr
  rather than the process. One is left alone, because the judgement is
  upstream's: `PhysicsSystem::Update` asserts its error mask is empty one line
  before returning it.
- **A saved shape carries its own container.** Jolt's shape restore indexes a
  table with a type read from the stream before checking that read, so
  `zjoltShapeRestore` wraps the payload in a 32-byte header — magic tag,
  container version, config id, Jolt version, length, CRC-32 — and validates
  it first. It is not a defence against a crafted payload whose checksum
  matches.
- **The header and the Zig externs are compared by reflection.** A test
  `@cImport`s `zjolt.h` and pairs every struct field by name with its offset,
  every function's parameters, every enumerator and every constant, comparing
  size, alignment, signedness and int-versus-float.
  13 kinds of deliberate drift are verified to fail it, and
  20 mutations for the other guards do the same — 33 mutations in all. `zjoltAbiLayout()` and `ZJOLT_CONFIG_ID` catch
  a library and a caller compiled with different options. See
  [docs/abi.md](docs/abi.md).

## Allocators

`init(.{ .allocator = gpa })` routes every Jolt allocation through a
`std.mem.Allocator`. It is process-wide, because
[Jolt's own allocator is](https://github.com/jrouwe/JoltPhysics/blob/v5.6.0/Jolt/Core/Memory.h)
— five global function pointers — and a per-system parameter would be one this
package could not honour. A C host passes `malloc`/`free` in a few lines, as
`tests/c_smoke.c` does.

Jolt frees with `free(block)` and `aligned_free(block)`, with no size and no
alignment, while Zig requires both, so `src/memory.zig` stores a header ahead
of each block. Jolt's plain `allocate` takes no alignment argument yet puts
SIMD types in what it returns: the minimum it needs is read from
`zjoltDefaultAllocateAlignment()` rather than assumed to be 16, because on a
32-bit target it is 8. Static and thread-local storage exists before any hook
can be installed and is not covered.

## Build options

| Option | Default | Effect |
|---|---|---|
| `-Ddouble_precision` | `false` | World positions become `f64` (`JPH_DOUBLE_PRECISION`), for worlds too large for float precision. Changes the ABI. |
| `-Dobject_layer_bits` | `16` | Width of an object layer, 16 or 32. Changes the ABI. |
| `-Dcross_platform_deterministic` | `false` | Trades speed for bit-identical results across platforms. |
| `-Denable_asserts` | on in Debug | Keeps Jolt's internal assertions. |
| `-Dsanitize_c` | `false` | Compiles the C and C++ with Zig's undefined-behaviour sanitizer. Off by default so the sanitizer runtime is never forced into a consumer's link; zjolt's own Debug runs turn it on. |
| `-Dshared` | `false` | Builds the C library as a shared object. |
| `-Ddebug_renderer` | `false` | Compiles Jolt's debug-draw geometry collection (`JPH_DEBUG_RENDERER`). |
| `-Dprofile` | `false` | Compiles Jolt's profiler (`JPH_PROFILE_ENABLED`), which instruments every `JPH_PROFILE` scope in Jolt's own source. |
| `-Dcpu_compute` | `true` | Compiles Jolt's CPU compute backend — what the hair solver runs on when the host lends no device. |
| `-Dobject_stream` | `true` | Compiles Jolt's reflective object stream (`JPH_OBJECT_STREAM`) and its text and binary editor format. |
| `-Dtrack_simulation_stats` | `false` | Tracks Jolt's per-body simulation stats (`JPH_TRACK_SIMULATION_STATS`). |
| `-Dtrack_broadphase_stats` | `false` | Tracks Jolt's broad-phase query stats (`JPH_TRACK_BROADPHASE_STATS`). |
| `-Dtrack_narrowphase_stats` | `false` | Tracks Jolt's per-shape-pair narrow-phase timing stats (`JPH_TRACK_NARROWPHASE_STATS`). |
| `-Dexternal_profile` | `false` | Routes Jolt's profile scopes to a host profiler (`JPH_EXTERNAL_PROFILE`) instead of Jolt's own. Mutually exclusive with `-Dprofile`, and wins over it. |

Exactly 2 rows change the ABI — the two marked "Changes the ABI." above — and
each contributes one bit to `ZJOLT_CONFIG_ID`. The symbol names are identical
either way, so a consumer built against a differently configured header links
cleanly and then reads a different set of types than the library writes.
`zjoltInit` compares the two ids and returns `ZJOLT_RESULT_CONFIG_MISMATCH`
first, which is why the header's `zjoltInit` is a `static inline` wrapper
passing the caller's id rather than the library's.

The rest are compile-time scope. Every entry point is declared in every build:
one a flag turns off still exists and returns `ZJOLT_RESULT_UNSUPPORTED`, so a
caller never has to `#ifdef` around a declaration.

There is no `-Dsimd` option: Jolt derives every `JPH_USE_*` from the
compiler's own predefines, so the lever is the Zig target's CPU model. A cross
build resolves to the baseline model and compiles Jolt's AVX2 paths out, a
native build takes the host CPU, and `-Dcpu=x86_64_v3` raises either.
`zjolt.cpuFeatures()` reports the set the library was compiled with.

## Platforms

| | Suite executed by CI | Also compiled by CI |
|---|---|---|
| Linux | x86_64, glibc | aarch64 glibc; x86_64 and aarch64 musl |
| macOS | aarch64 | x86_64 |
| Windows | x86_64, both the gnu and the MSVC ABI | aarch64, gnu ABI |

Every job in that matrix passed on run
[`34779640943`](https://github.com/pedronaugusto/zjolt/actions/runs/34779640943).
The runners are `ubuntu-24.04`, `macos-26-arm64` and `windows-2025`.

`-Dtarget=x86_64-windows-msvc` needs the Microsoft C++ standard library, so it
is built on a Windows host and skipped elsewhere. Every other target above is
a plain `zig build -Dtarget=...` from any host. Nothing here has been
benchmarked.

## Testing

```sh
zig build test                       # the Zig suite, and the C smoke test with it
zig build test-c                     # the C smoke test alone
zig build --build-file tests/consumer/build.zig run   # as a downstream dependency

ci/run.sh            # the inner loop: hygiene, native Debug, the C test
ci/run.sh --full     # everything CI runs, minus the jobs that need network
ci/install-hooks.sh  # run the inner loop automatically before every push
```

Every Zig test runs the library through `std.testing.allocator`, which fails
on a leak; `zig build test-c` drives the exposed surface through the header
alone with a counting `malloc`/`free`. Every fixture is built in code, so the
suite ships no third-party assets. The bar is one characteristic test per
subsystem, never one per entry point, and
[docs/testing.md](docs/testing.md) lists what they assert.

3 reflective sweeps run alongside them, each finding its list by reflection:
one calls every entry point with nulls, one calls every entry point before
`init`, and one hands every enum parameter a value no enumerator names.

CI runs that suite in four optimize modes with the sanitizer on and off, plus
the standalone C test, on each of the three hosts above; separately it
executes five build configurations and builds a sixth, runs the ABI-drift
mutations, and re-fetches the pinned upstream commit to prove `libs/` is
unmodified. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

`ci/run.sh` is that matrix locally, and `ci/check-mirror.sh` fails when the
two rosters differ. The default is trimmed, because Jolt is
179 translation units per configuration; `ci/run.sh --full` is 38 checks —
30 of them run on this host, 8 cross-compiling. `ci/measurements.sh` recomputes
every number this README states, and `ci/check-numbers.sh` fails the build
when one disagrees with the tree.

## Requirements

Zig 0.16.0, which is what `build.zig.zon` asks for and what CI pins. Jolt is
compiled by Zig's own clang, so there is no separate C++ toolchain, SDK or
system library to install.

## Contributing

Issues and pull requests are welcome. Four things to know first:

- **`libs/JoltPhysics` is vendored verbatim and must not be edited.** Changes
  there are lost at the next re-vendor. If upstream needs fixing, fix it
  upstream; if zjolt needs to work around upstream, do it in `ffi/` and record
  it in [UPSTREAM.md](UPSTREAM.md).
- **Run `ci/run.sh` before pushing** — or `ci/install-hooks.sh` once, and it
  runs itself. Run `ci/run.sh --full` for anything structural.
- **Comments state a contract, not a narrative**, and `ci/check-comments.sh`
  fails a pull request over either half of that. A block above one declaration
  is at most six lines, a file header or a block under a `//===---===//` banner
  at most fourteen, and the register is documentation rather than
  conversation. The cap never justifies dropping a fact: units, ownership,
  lifetime, nullability, error conditions and ordering constraints come first.
- **New source files go in the explicit lists in `build.zig`.** There are no
  globs, so nothing starts compiling by accident.

## Licence

MIT, see [LICENSE](LICENSE), which covers this package's own code. Vendored
Jolt Physics is MIT, copyright Jorrit Rouwe and contributors; its licence text
ships with the package at `libs/JoltPhysics/LICENSE`.
