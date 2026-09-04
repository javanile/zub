---
title: pixelsculp_anim
description: "Typed, deterministic animation engine for Zig UIs: physical springs, CSS-style tweens with the full Penner set, decay flings, keyframes and choreographed sequences. Zero dependencies, headless-testable."
license: Apache-2.0
author: cstffx
author_github: cstffx
repository: https://github.com/cstffx/pixelsculp_anim
keywords:
  - animation
  - easing
  - game-development
  - keyframes
  - springs
  - tween
  - ui
date: 2026-08-26
category: game-development
updated_at: 2026-08-26T08:59:22+00:00
last_sync: 2026-08-26T08:59:22Z
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
permalink: /packages/cstffx/pixelsculp_anim/
---

# pixelsculp_anim

Typed, deterministic animation engine for Zig UIs: physical springs, CSS-style tweens with the full Penner set, decay flings, keyframes and choreographed sequences.

Zero dependencies. No GL, no libc, no threads, no globals — you feed it time, it feeds back values.

```zig
const anim = @import("pixelsculp_anim");

var animator: anim.Animator = try .init(allocator);
defer animator.deinit();

var x: f32 = 0;
_ = try animator.spring_to(f32, &x, 100.0, .{ .response_s = 0.35, .bounce = 0.4 });

// your render loop:
try animator.update(dt); // writes value() straight into every registered field
```

## Features

**Deterministic by construction**
- Time is injected by the caller (`animator.update(dt)`): record the `dt`s, replay them, get bit-identical motion. Headless-testable, replayable, seed-free.
- Springs integrate with semi-implicit Euler at fixed 1/240 substeps; settle is checked *per substep* and reported as consumed time.
- Infinite repeats clamp their internal clock to two cycles, so hour-long pulses stay precise in `f32`.

**Springs with real physics**
- Parametrize physically (`stiffness`, `damping`, `mass`) or descriptively (`SpringParams.duration_bounce(response_s, bounce)`).
- Non-physical inputs are validated and saturated instead of exploding.
- `retarget()` mid-flight keeps current velocity — no hitch, no restart.
- Presets: `anim.snappy`, `anim.bouncy`, `anim.gentle`.

**Tweens with a complete easing vocabulary**
- Full Penner set (`quad`…`bounce` × in/out/in_out) with mathematically exact endpoints, plus `smoothstep`/`smootherstep`.
- CSS-style cubic-bezier curves with a Newton + bisection solver; `eval_seed(x, t_hint, &t_out)` warm-starts across frames (~1.6× faster than cold evaluation).
- `linear`, `hold`, `steps(n)` and composable adapters: `time_flip`, `value_flip`, `pair`, `blend`.

**Motion beyond A-to-B**
- `decay_from(ptr, velocity)` — exponential friction for fling gestures; always comes to rest exactly at `v0/λ`.
- `Track(T)` keyframes: normalized stop offsets with per-segment easing, sampled by binary search, zero allocation.
- `sequence_to()` choreographs multiple segments through one field, honoring each segment's `delay_s` and rolling leftover `dt` between segments without frame hitches.
- `Repeat` (finite/count/infinite, reverse mode) and `FillMode` (.forwards default).

**Animate anything made of floats**
- `mix(T, a, b, t)` is a compile-time recursive interpolator: `Vec2`, `Color`, your own structs — if it's built from floats, it animates. No traits, no boilerplate.
- Utilities included: `clamp01`, `ilerp`, `remap`, `eerp` (exponential lerp for zooms/scales), `damp` (framerate-independent smoothing toward a target).

**Ergonomic runtime**
- One type-erased `Animator` registry keyed by destination field: `animate_to` / `spring_to` / `tween_to` retarget transparently instead of stacking conflicting nodes.
- Two-phase update makes callbacks safe: a callback may cancel *other* fields mid-pump; paused nodes survive; nested `update()` calls are ignored.
- Playback controls everywhere: `pause`, `resume_anim`, `cancel`, `finish_now`, global `time_scale` (slow motion), `max_dt` clamp, `pause_all` / `resume_all`.
- Optional update/complete callbacks per animation.

**Plays well with UI code**
- Designed for immediate-mode-ish render loops: values land directly in your fields, you draw whatever you want.
- `pixelsculp_widgets` integration: `WidgetContext.anim` accepts an optional `*Animator`; when null, widgets jump straight to final state.

## Installation

```bash
zig fetch --save git+https://github.com/cstffx/pixelsculp_anim
```

```zig
// build.zig
const anim = b.dependency("pixelsculp_anim", .{});
exe.root_module.addImport("pixelsculp_anim", anim.module("pixelsculp_anim"));
```

Requires Zig 0.16.0.

## Testing

Pure CPU logic — the whole suite runs headless:

```bash
zig build test
```

## Repository layout

| Module | Responsibility |
|---|---|
| `mix.zig` | Comptime recursive interpolation + range utilities |
| `curve.zig` | Easing curves, bézier solver, Penner set, adapters |
| `spring.zig` | Damped oscillator (physical & descriptive params) |
| `decay.zig` | Exponential friction for flings |
| `keyframes.zig` | `Track(T)` multi-stop timelines |
| `motion.zig` | `MotionSpec` union, `Repeat`, `FillMode` |
| `animation.zig` | `Animation(T)` playback, progress springs, retargeting |
| `animator.zig` | Field-keyed registry, sequencing, global controls |

Documentation site: <https://cstffx.github.io/pixelsculp_anim/> (English · Español).
