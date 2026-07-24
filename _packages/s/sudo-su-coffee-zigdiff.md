---
title: zigdiff
description: high-performance CLI utility and library for structural, semantic comparison of JSON documents
license: MIT
author: sudo-su-coffee
author_github: sudo-su-coffee
repository: https://github.com/sudo-su-coffee/zigdiff
keywords:
date: 2026-07-24
updated_at: 2026-07-24T08:36:03+00:00
last_sync: 2026-07-24T08:36:03Z
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
permalink: /packages/sudo-su-coffee/zigdiff/
---

# ⚡ zigdiff

**Sub-Millisecond, Zero-Dependency Semantic JSON Diff Engine.**

`zigdiff` is a high-performance CLI tool and embeddable Zig package for structural, semantic comparison of JSON documents. Unlike line-based diff tools (`diff`, `git diff`), `zigdiff` compares underlying tree structures—ignoring whitespace, key ordering, and formatting variations.

Think of `zigdiff` as a **lightweight, internal Git engine for JSON state trees**. It tracks structural evolution, powers automated state auditing, and enables instant drift detection across your internal microservices and DevOps pipelines.

Designed as both a standalone, single-binary CLI tool for CI/CD pipelines and a native, zero-dependency library importable into any Zig project.

---

## 🎯 Primary & Enterprise Use Cases

* **Terraform & Pulumi State Drift Detection**: Compare live infrastructure state against declared state files to detect configuration drift before applying updates.
* **Kubernetes Manifest Auditing**: Detect structural changes across raw or rendered Kubernetes manifests in GitOps pipelines.
* **API Contract & Payload Testing**: Verify that API mock payloads match expected production responses without failing on key reordering.
* **Internal State Versioning & Audit Logging**: Store concise JSON delta reports in internal audit trails (e.g., PostgreSQL JSONB, VaultS3, or event streams) instead of saving duplicate full snapshots.
* **Automated Control Planes & Rollback Triggers**: Use programmatically in internal daemons to evaluate state changes and trigger automatic rollbacks if unsafe structural fields are mutated.
* **Embedded Zig Applications**: Import directly as a native Zig module to compute JSON structural deltas in custom microservices, agents, or CLI engines.

---

## ✨ Key Features

- 🚀 **Sub-Millisecond Execution**: Instant tree traversal written in pure Zig.
- 📦 **Zero External Dependencies**: Pure Zig implementation—no external C/system libraries required.
- 🧠 **Semantic Awareness**: Treats `{ "a": 1, "b": 2 }` and `{ "b": 2, "a": 1 }` as identical.
- 📊 **Path-Based Reports**: Displays clear dot-notation change paths (`.spec.replicas: 3 -> 5`).
- 🤖 **Machine & Human Friendly**: Supports ANSI color terminal output and structured JSON output.
- 🚦 **CI/CD & Language Agnostic**: Strict exit codes designed specifically for build pipeline gating.

---

## 🛠️ Usage for All Developers (CLI)

### 1. Basic File Comparison
Compare two JSON files from your terminal:
```bash
zigdiff base.json target.json

```

**Output:**

```text
~ .spec.replicas: 3 -> 5
- .metadata.labels.legacy (was true)
+ .metadata.annotations.updated_by: "ci-bot"

```

---

### 2. Machine-Readable JSON Output

Output structural changes as JSON for downstream consumption in Python, Node, Go, or Rust scripts:

```bash
zigdiff base.json target.json --format json

```

**Output:**

```json
[
  { "type": "modified", "path": ".spec.replicas", "old": 3, "new": 5 },
  { "type": "removed", "path": ".metadata.labels.legacy", "old": true },
  { "type": "added", "path": ".metadata.annotations.updated_by", "new": "ci-bot" }
]

```

---

### 3. Piping via Stdin

Stream input directly into `zigdiff` using the `-` alias:

```bash
kubectl get deployment my-app -o json | zigdiff expected.json -

```

---

## ⚡ Usage for Zig Developers (Library Import)

You can import `zigdiff` directly into your Zig projects as a native module.

### Step 1: Add to `build.zig.zon`

```zig
.{
    .name = "my-app",
    .version = "0.1.0",
    .dependencies = .{
        .zigdiff = .{
            .url = "[https://github.com/blacklovertech/zigdiff/archive/refs/tags/v1.0.0.tar.gz](https://github.com/blacklovertech/zigdiff/archive/refs/tags/v1.0.0.tar.gz)",
            // .hash = "...", // Auto-generated on `zig build`
        },
    },
    .paths = .{"."},
}

```

### Step 2: Link in `build.zig`

```zig
const zigdiff_dep = b.dependency("zigdiff", .{
    .target = target,
    .optimize = optimize,
});

exe.root_module.addImport("zigdiff", zigdiff_dep.module("zigdiff"));

```

### Step 3: Use in Zig Code (`main.zig`)

```zig
const std = @import("std");
const zigdiff = @import("zigdiff");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const base_json = "{\"a\": 1, \"b\": 2}";
    const target_json = "{\"b\": 2, \"a\": 5}";

    var result = try zigdiff.diffJsonStrings(allocator, base_json, target_json);
    defer result.deinit();

    // Work with structural changes programmatically
    for (result.changes.items) |change| {
        std.debug.print("Path: {s}, Type: {}\n", .{ change.path, change.change_type });
    }
}

```

---

## 🚦 Exit Codes for CI/CD Pipelines

| Exit Code | Meaning | Description |
| --- | --- | --- |
| **`0`** | **No Drift** | Documents are structurally identical. |
| **`1`** | **Drift Detected** | Structural differences were found. |
| **`2`** | **Error** | File not found, invalid JSON syntax, or CLI error. |

---

## 🔮 Future Roadmap & Version Plans

### 📍 v1.1.0 (YAML & Multi-Document Support)

* Native YAML parsing (`.yaml` / `.yml`) for direct comparison of raw Kubernetes manifests.
* Multi-document YAML stream support (`---` separator).

### 📍 v1.2.0 (Path Exclusion & Filtering)

* Key exclusion flags (`--ignore-keys .metadata.managedFields`).
* JSONPath-based wildcard matching (`--ignore-keys "spec.template.metadata.*"`).

### 📍 v1.3.0 (Array Comparison Strategies)

* Configurable array diffing rules:
* Strict index-based ordering (Default).
* Unordered set comparison (`--array-mode set`).
* Key-by ID matching for arrays of objects (`--array-key id`).

### 📍 v2.0.0 (Embedded State Tracker & Snapshot Engine)
* **`zigdiff init`**: Initialize local structural tracking (`.zigdiff/` repository).
* **`zigdiff snapshot -m "msg"`**: Store compressed, semantic JSON tree snapshots.
* **`zigdiff status`**: Report live configuration drift relative to the last snapshot.
* **`zigdiff log`**: View structural change history across snapshots.
* **`zigdiff rollback`**: Revert disk state to a previous structural revision.


---

## 📜 License

[MIT License](https://www.google.com/search?q=LICENSE)
