---
title: ggml-zig
description: Pure-zig ggml library port
license: MPL-2.0
author: zillama
author_github: zillama
repository: https://github.com/zillama/ggml-zig
keywords:
  - machine-learning
date: 2026-04-09
updated_at: 2026-04-09T09:46:58+00:00
last_sync: 2026-04-09T09:46:58Z
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
permalink: /packages/zillama/ggml-zig/
---

# ggml-zig

A pure Zig port of [ggml](https://github.com/ggml-org/ggml) — the tensor library powering llama.cpp and similar LLM inference engines.

> **Status**: Vulkan backend only. Works with real models. Not that performant yet.

---

## Why Zig?

Porting ggml to Zig isn't about novelty. It's about what Zig forces into the open that C++ hides:

- **Explicit memory management** — no GC, no hidden allocations, no surprises. Every allocation is visible at the call site. Staging-buffer policies and lifetimes are clear rather than implicit.
- **Explicit error handling** — GPU and driver failures are normal control flow via error unions, not exceptions or silent side-channels. No unchecked return codes.
- **Comptime type safety** — push constants, specialization constants, and descriptor layouts are validated at compile time, catching ABI mismatches before they reach the driver.
- **C-level performance** — no runtime overhead, no GC pauses, direct control over data layout and memory placement.
- **No hidden control flow** — `defer`, `errdefer`, and explicit allocators make resource cleanup auditable and predictable.
- **Better refactoring safety** — ownership is explicit, so backend refactors (sync, pipeline, multi-GPU) are less likely to silently break lifetime invariants.

Simply: I like Zig, and Vulkan backend development is exactly where these properties matter most.

---

## Vulkan Backend

The Vulkan backend is organized into clear domains:

| Domain | Responsibility |
|--------|---------------|
| `core` | Context, device bindings, constants |
| `device` | Instance, device selection, queues |
| `memory` | Buffers, staging, transfers |
| `pipeline` | SPIR-V shader registry, descriptors, push constants |
| `compute` | Graph dispatch, op routing, fusion |

### Supported Operations

- **Binary**: `add`, `sub`, `mul`, `div`
- **Unary**: `sqr`, `sqrt`, `sin`, `cos`, `log`, `scale`, `clamp`, and more
- **Normalization**: `rms_norm`, `norm`, `l2_norm`, `group_norm`
- **Attention**: `softmax`, `rope`, `flash_attn`, `diag_mask_inf`
- **Matrix multiply**: `mul_mat`, `mul_mat_id`
- **Tensor/Shape**: `repeat`, `concat`, `cpy`, `get_rows`, `set_rows`
- **Misc**: `sum`, `argsort`, `im2col`, `pool`

Fusion support is included for multi-add and attention-adjacent patterns, reducing dispatch overhead and memory traffic.

---

## Requirements

- Zig `0.16.0-dev.3121+d34b868bc` or newer master
- Vulkan-capable GPU and driver

---

## Building

```sh
# Compile-only check (fast, no GPU required)
zig build check

# Full build
zig build
```

`zig build check` compiles the public `ggml` module through a dependency smoke test — a quick way to confirm your toolchain and dependencies resolve correctly.

---

## Usage

Fetch the dependency (this writes the URL and hash into `build.zig.zon` automatically):

```sh
zig fetch --save git+https://github.com/zillama/ggml-zig#0.0.1
```

Then wire it in `build.zig`:

```zig
const ggml_dep = b.dependency("ggml", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("ggml", ggml_dep.module("ggml"));
```

Then in your code:

```zig
const ggml = @import("ggml");
const vk = ggml.backends.vulkan;

// Access backend context, device, memory, pipeline, compute domains:
// vk.context, vk.device, vk.buffer, vk.pipeline_registry, vk.graph ...
```

The public API surface is rooted at `src/ggml.zig`. Backends are accessed via `ggml.backends.vulkan.*`.

---

## Testing

Tests are split into three tiers:

| Step | Command | Requires GPU |
|------|---------|--------------|
| Compile check | `zig build check` | No |
| Unit + integration | `zig build test` | No (hermetic) |
| End-to-end (real GPU) | `zig build test-e2e` | Yes |

### Unit & integration tests

```sh
zig build test
```

Covers:
- Operation support tables, offload heuristics, shape/stride math
- Vulkan device creation and queue initialization
- Shader dispatch with real tensor data and result verification
- Pipeline/descriptor/push-constant wiring
- SPIR-V validation and generated shader compilation
- All backend modules exercised via `comptime` import checks

### End-to-end tests

```sh
zig build test-e2e
```

Runs actual tensor operations on a Vulkan GPU and verifies numeric results. The inference smoke test checks model file loading when a path is provided:

```sh
GGML_TEST_MODEL_PATH=/path/to/model.gguf zig build test-e2e
```

Set `GGML_E2E_VERBOSE=1` for detailed per-operation output.

### Coverage summary

| Area | Tier |
|------|------|
| Backend registration and device selection | unit |
| Tensor type math and stride correctness | unit |
| Vulkan pipeline creation and descriptor sets | integration |
| SPIR-V shader compilation and validation | integration |
| Binary/unary/norm op dispatch on GPU | e2e |
| Matrix multiply on GPU | e2e |
| Attention ops (softmax, rope, flash_attn) | e2e |
| Full graph execution with result readback | e2e |
| Model file loading smoke | e2e (opt-in via env) |

---

## License

[MIT](LICENSE)
