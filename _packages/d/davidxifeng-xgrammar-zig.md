---
title: xgrammar-zig
description: "Pure-Zig port of xgrammar-rs for grammar-constrained LLM decoding (JSON Schema / EBNF / Regex / Lark / Structural Tag -> token bitmask & logit masking), with idiomatic Zig APIs and full bit-for-bit parity against the Rust reference oracle."
license: ""
author: davidxifeng
author_github: davidxifeng
repository: https://github.com/davidxifeng/xgrammar-zig
keywords:
  - zig-package-manager
  - zig-packages
date: 2026-11-24
updated_at: 2026-11-24T09:40:08+00:00
last_sync: 2026-11-24T09:40:08Z
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
permalink: /packages/davidxifeng/xgrammar-zig/
---

# xgrammar-zig

**English** | [中文](README.zh-CN.md) | [日本語](README.ja.md)

Pure-Zig (**Zig 0.17.1**, zero external dependencies) port of **xgrammar-rs 0.2.8** (with v0.2.9 correctness fixes) for grammar-constrained LLM decoding (JSON Schema / EBNF / Regex / Lark / Structural Tag -> token bitmask & logit masking), designed around idiomatic Zig 0.17 value handles, explicit allocators, and bit-for-bit Rust oracle parity.

## Features

- **Zero-dependency pure Zig 0.17.1** layered module architecture (`src/<subsystem>.zig` + `src/<subsystem>/`: `support -> tokenizer -> fsm -> grammar -> parser -> functor -> converter -> compiler -> matcher`).
- **Bit-for-bit Rust oracle parity**: verified via `tools/oracle.zig` (`zig-out/bin/xgrammar-oracle`) against `tools/oracle-rs/target/release/oracle` across `json_schema`, `ebnf`, `raw` / `byte_fallback` vocabularies, padded `vocab_size`, multi-byte UTF-8, multi-word bitmasks, and whole-codepoint jump-forward strings.
- **Idiomatic Zig 0.17 API**:
  - Atomic ref-counted value handles (`TokenizerInfo`, `CompactFsm`, `CompiledGrammar`), arena-backed `Grammar` value handles with zero-copy `GrammarBuilder`, and unified `Diagnostic` (`{f}` formatting).
  - High-level static constructors (`Grammar.fromEbnf`, `Grammar.builtinJson`, `Grammar.fromJsonSchema`, `Grammar.fromRegex`, `Grammar.fromLark`, `Grammar.fromStructuralTag`, `Grammar.unionOf`, `Grammar.concatOf`).
  - Owned `TokenBitmask` and non-owning `TokenBitmaskView` with `@Vector(8, f32)` SIMD `applyToLogits` / `applyBatchToLogits` and `@popCount` + `@ctz` bit queries (`countAllowed`, `singleAllowedToken`, `maskedTokens`).
  - Zero-allocation `fillNextTokenBitmask` hot path after warmup, parallel `BatchMatcher` (`max_threads`), and zero-DOM streaming `v16` JSON serialization (`Grammar.format` via `{f}`).
- **Concurrency & caching**:
  - Sharded mutex-guarded `RuleLevelCache` and `GrammarCompiler` cache backed by O(1) intrusive `LruCache` ([`src/support/lru_cache.zig`](src/support/lru_cache.zig)).
  - Multi-threaded `buildAdaptiveTokenMaskCache` reusing one value-embedded `EarleyParser` per worker backed by caller-owned `ThreadSafeAllocator` (zero hidden `page_allocator`).

## Quickstart (Zig 0.17)

```zig
const std = @import("std");
const xgrammar = @import("xgrammar");

pub fn example(allocator: std.mem.Allocator) !void {
    const vocab = [_][]const u8{ "{\"ok\": ", "true", "false", "}", "</s>" };

    var tok = try xgrammar.TokenizerInfo.init(allocator, &vocab, .{
        .vocab_type = .raw,
        .stop_token_ids = &.{4},
    });
    defer tok.deinit();

    var compiler = try xgrammar.GrammarCompiler.init(allocator, &tok, .{
        .max_threads = 4,
    });
    defer compiler.deinit();

    const schema =
        \\{"type":"object","properties":{"ok":{"type":"boolean"}},"required":["ok"],"additionalProperties":false}
    ;
    var compiled = try compiler.compileJsonSchema(schema, .{
        .any_whitespace = false,
        .strict_mode = true,
    });
    defer compiled.deinit();

    var matcher = try xgrammar.GrammarMatcher.init(allocator, &compiled, .{});
    defer matcher.deinit();

    var bitmask = try xgrammar.TokenBitmask.initSingle(allocator, tok.vocabSize());
    defer bitmask.deinit();

    _ = try matcher.fillNextTokenBitmask(&bitmask, 0, null);
    var logits = [_]f32{ 1.0, 2.0, 3.0, 4.0, 5.0 };
    bitmask.applyToLogits(&logits);
    _ = try matcher.acceptToken(0, null); // `{"ok": `
}
```

## Layout

- `src/xgrammar.zig` — Public API root (`pub const internal = ...;` exposes internal subsystem namespaces)
- `src/{support,tokenizer,fsm,grammar,parser,functor,converter,compiler,matcher}.zig` — Subsystem entry modules and consolidated submodules (`87` files total under `src/`)
- `src/Diagnostic.zig` — Unified zero-value-safe diagnostic carrier (`{f}` formatted output)
- `src/oracle_parity_test.zig`, `src/idiomatic_api_test.zig`, `src/upstream_v029_test.zig` — Parity, API/regression, and v0.2.9 test suites
- `tools/oracle.zig` & `tools/bench.zig` — Oracle CLI (`zig-out/bin/xgrammar-oracle`) and benchmark CLI (`zig-out/bin/xgrammar-bench`)
- `tools/oracle-rs/` — Reference Rust oracle & benchmark binaries for side-by-side verification

## Build, Test & Oracle Parity

```sh
# Build library, zig-out/bin/xgrammar-oracle, and zig-out/bin/xgrammar-bench
zig build

# Run full test suite (all unit + parity + v0.2.9 + regression tests, 0 leaks)
zig build test
zig test src/xgrammar.zig

# Side-by-side oracle check
tools/oracle-rs/target/release/oracle < case.json > expected.json
zig-out/bin/xgrammar-oracle < case.json > actual.json
```

## Benchmarks (Zig vs Rust)

Measured side-by-side on Apple M3 (`arm64`, Zig `0.17.1 -Doptimize=ReleaseFast` vs `xgrammar-rs 0.2.8 --release`) over a 32K vocab, nested JSON Schema, 4-rule EBNF, and 33-token decode trace with identical output checksums (`bitmask_checksum = 9170455314173489972`):

- **Per-token decode (`fill + apply + accept`)**: Zig **`2.12 µs/tok`** vs Rust `13.55 µs/tok` (**6.39x faster**), with mask fill **`1.39 µs/tok`** vs Rust `1.42 µs/tok` (zero heap allocations after warmup) and `@Vector(8, f32)` SIMD logit masking **7.42x–8.02x faster** (`1.68 µs` b=1, `7.10 µs` b=4).
- **Init & compilation**: 256-bucket radix vocab partitioning cuts 32K `TokenizerInfo.init` to **`4.43 ms`** (down 16.3% from Stage 2 `5.30 ms`), reused `EarleyParser` mask builders cut cold JSON Schema compilation to **`4.88 ms` (1t) / `3.22 ms` (4t)**, and cold 1t EBNF compilation runs in **`43.00 µs`** (`35.00 µs` min) vs Rust `58.42 µs` (**1.36x faster**).

See [docs/BENCHMARKS.md](docs/BENCHMARKS.md) for full Stage 0 → Stage 3 tables, methodology, and reproduction commands.

## For AI Agents (Agent Skill)

This repository includes self-contained agent documentation and tested Zig examples so AI coding agents can use `xgrammar` correctly without reading `src/`:

- **Repository instructions**: [AGENTS.md](AGENTS.md)
- **Skill entry point**: [.agents/skills/xgrammar-zig/SKILL.md](.agents/skills/xgrammar-zig/SKILL.md)
- **Complete API reference**: [.agents/skills/xgrammar-zig/references/api-reference.md](.agents/skills/xgrammar-zig/references/api-reference.md)
- **Supported grammar formats**: [.agents/skills/xgrammar-zig/references/grammar-formats.md](.agents/skills/xgrammar-zig/references/grammar-formats.md)
- **Runnable Zig recipes**: [.agents/skills/xgrammar-zig/examples/recipes.zig](.agents/skills/xgrammar-zig/examples/recipes.zig)

To give agents in a downstream project the same knowledge automatically:

```sh
cp -r .agents/skills/xgrammar-zig /path/to/your-project/.agents/skills/
```
