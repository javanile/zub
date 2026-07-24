---
title: zigqr
description: "High-Performance, Single-Binary, Zero-Dependency QR & Barcode Generator"
license: MIT
author: sudo-su-coffee
author_github: sudo-su-coffee
repository: https://github.com/sudo-su-coffee/zigqr
keywords:
date: 2026-07-24
updated_at: 2026-07-24T08:05:58+00:00
last_sync: 2026-07-24T08:05:58Z
package_kind: binary
has_library: false
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/sudo-su-coffee/zigqr/
---

# ⚡ ZigQR V2

**High-Performance, Single-Binary, Zero-Dependency QR & Barcode Generator.**

ZigQR V2 is a complete rewrite of the original ZigQR, engineered for maximum performance, minimal memory footprint, and zero runtime dependencies. Designed as a lightweight primitive for data pipelines, microservices, and CLI automation, it compiles into a tiny, standalone executable that runs everywhere.

---

## ✨ Key Features

- 🚀 **Sub-Millisecond Generation**: Blazing-fast matrix calculations and encoding built in pure Zig.
- 📦 **Zero External Dependencies**: Pure Zig implementation — no C libraries (`libpng`, `zlib`, etc.) required.
- 📐 **Configurable Quiet Zones**: ISO/IEC 18004 compliant margins (`--margin`) to guarantee camera scanning reliability.
- 🛠️ **Multi-Format Support**:
  - **QR Codes**: Full Version 1–40 support.
  - **Barcodes**: Code 128, EAN-13, EAN-8 (*Coming soon in V2 stable*).
- 🖼️ **Flexible Output Formats**:
  - **PNG**: Crisp raster output using native `std.compress.zlib`.
  - **SVG**: Clean, scalable vector output.
  - **Terminal**: Direct ANSI/Unicode block rendering in your stdout stream.
- 📂 **High-Throughput Batch Processing**: Process thousands of codes per second via NDJSON streams.

---

## ⚙️ CLI Reference & Parameters

### Command-Line Flags

| Flag | Long Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| `-o` | `--output` | `stdout` | Destination file path (`.png`, `.svg`) or terminal output. |
| `-s` | `--size` | `10` | Pixel multiplier per QR module (e.g., `-s 10` = 10px per square). |
| `-m` | `--margin` | `4` | Quiet zone padding in modules (ISO standard is `4`). |
| `-e` | `--ec` | `M` | Error correction level: `L` (7%), `M` (15%), `Q` (25%), `H` (30%). |

---

## 📏 Quiet Zone & Sizing Guidelines

### Quiet Zone (`--margin`)
The ISO/IEC 18004 standard requires a **4-module quiet zone** around all four sides so camera scanners can detect boundaries against dark or patterned backgrounds.

- `--margin 4` *(Default)*: Full ISO standard compliance for maximum scanner compatibility.
- `--margin 2`: Compact margin for clean, minimalist digital UIs.
- `--margin 0`: No margin (use only if wrapped in external CSS padding or on light backgrounds).
- `--margin 6`+: Extra padding for print media, curved bottles, or dark surfaces.

### 📊 Size Calculation & Version Scaling

The final PNG resolution is determined by the formula:

$$\text{Final Width (px)} = (\text{Base Modules} + [2 \times \text{Margin}]) \times \text{Size}$$

Because the QR code Version (1 to 40) automatically increases based on data length, the base module grid grows from $21 \times 21$ up to $177 \times 177$.

#### Quick Comparison: Smallest vs. Largest Version (`--margin 4`)

| QR Version | Base Modules | Total Grid Modules (+8 margin) | Final Pixels at `--size 4` | Final Pixels at `--size 10` |
| :---: | :---: | :---: | :---: | :---: |
| **Version 1** | 21 × 21 | 29 × 29 | **116 × 116 px** | **290 × 290 px** |
| **Version 5** | 37 × 37 | 45 × 45 | **180 × 180 px** | **450 × 450 px** |
| **Version 10** | 57 × 57 | 65 × 65 | **260 × 260 px** | **650 × 650 px** |
| **Version 20** | 97 × 97 | 105 × 105 | **420 × 420 px** | **1,050 × 1,050 px** |
| **Version 40** | 177 × 177 | 185 × 185 | **740 × 740 px** | **1,850 × 1,850 px** |

---

### ⚡ Output File Size & Benchmarks

Because ZigQR uses native, optimized `std.compress.zlib` compression, generated PNGs are exceptionally lightweight and optimized for storage and web delivery:

| `--size` Flag | Resolution Range | Approx. PNG File Size | Ideal Target |
| :---: | :---: | :---: | :--- |
| `-s 4` | ~116 × 116 px | **~14 KB** | Micro UI icons & inline badges |
| `-s 6` | ~174 × 174 px | **~30 KB** | Lightweight web widgets |
| `-s 8` | ~232 × 232 px | **~53 KB** | Standard mobile/app displays |
| `-s 10` | ~290 × 290 px | **~83 KB** | High-DPI screens & receipts |
| `-s 12` | ~348 × 348 px | **~119 KB** | Desktop UIs & dynamic cards |
| `-s 16` | ~464 × 464 px | **~211 KB** | Print media (300 DPI) |
| `-s 20` | ~580 × 580 px | **~330 KB** | High-resolution signage & posters |

---

## 🚀 Quick Start

### Installation

```bash
git clone [https://gitlab.com/blacklovertech/zigqr](https://gitlab.com/blacklovertech/zigqr)
cd zigqr
zig build -Doptimize=ReleaseSmall

```

### Basic Usage

**Generate a Standard PNG with Custom Margin and Size:**

```bash
./zig-out/bin/zigqr gen "[https://ziglang.org](https://ziglang.org)" --output my_qr.png --size 12 --margin 4 --ec M

```

**Generate Scalable SVG Vector:**

```bash
./zig-out/bin/zigqr gen "Hello World" --output my_qr.svg

```

**Batch Mode (Streaming via NDJSON):**

```bash
cat data.ndjson | ./zig-out/bin/zigqr batch --output ./output_dir/

```

---

## 🧪 Testing & Verification

Run the comprehensive test script to generate multiple sizes, verify PNG structures, and test NDJSON batch streaming:

```bash
#!/bin/bash
# test_zigqr.sh - Comprehensive test runner

set -e

echo "=== Building ZigQR ==="
zig build -Doptimize=ReleaseSmall

echo -e "\n=== Testing Single Generation ==="
./zig-out/bin/zigqr gen "Hello World" --output test_single.png --size 10 --margin 4 --ec H

echo -e "\n=== Testing Various Module Sizes & Margins ==="
for size in 4 6 8 10 12 16 20; do
    echo "--- Module Size: $size ---"
    ./zig-out/bin/zigqr gen "Test QR $size" --output test_${size}.png --size ${size} --margin 4 --ec M
    # Silence zlib version mismatch warnings from pngcheck via stderr redirection
    pngcheck test_${size}.png 2>/dev/null
done

echo -e "\n=== Creating Batch Test Data ==="
cat > test_data.ndjson << 'EOF'
{"text": "[https://github.com](https://github.com)", "label": "github", "ec": "H", "size": 10, "margin": 4}
{"text": "mailto:test@example.com", "label": "email", "ec": "M", "size": 8, "margin": 4}
{"text": "BEGIN:VCARD\nVERSION:3.0\nFN:John Doe\nTEL:+1234567890\nEND:VCARD", "label": "contact", "ec": "Q", "size": 12, "margin": 4}
{"text": "WIFI:T:WPA;S:MyNetwork;P:password123;;", "label": "wifi", "ec": "M", "size": 8, "margin": 4}
{"text": "Hello World! This is a test message", "label": "text", "ec": "L", "size": 8, "margin": 4}
EOF

echo -e "\n=== Running Batch Stream Processing ==="
mkdir -p qr_output
./zig-out/bin/zigqr batch --output ./qr_output/ < test_data.ndjson

echo -e "\n=== All tests complete successfully! ==="

```

---

## 🔗 Cross-Language Integration

ZigQR functions as a standalone binary and integrates into any language runtime by calling the CLI or piping NDJSON streams.

### 🐍 Python

```python
import subprocess
import json

def generate_qr(text, output_path, margin=4, size=10):
    subprocess.run([
        "./zigqr", "gen", text, 
        "--output", output_path,
        "--size", str(size),
        "--margin", str(margin)
    ], check=True)

# Batch mode via NDJSON stdin stream
data = [{"text": "[https://ziglang.org](https://ziglang.org)", "label": "zig", "margin": 4, "size": 10}]
p = subprocess.Popen(["./zigqr", "batch", "--output", "./out/"], stdin=subprocess.PIPE)
p.communicate(input="\n".join(map(json.dumps, data)).encode())

```

### 🐹 Go

```go
package main

import (
    "os/exec"
)

func main() {
    cmd := exec.Command("./zigqr", "gen", "Hello from Go", "--output", "go_qr.svg", "--margin", "4")
    if err := cmd.Run(); err != nil {
        panic(err)
    }
}

```

### 🦀 Rust

```rust
use std::process::Command;

fn main() {
    let status = Command::new("./zigqr")
        .arg("gen")
        .arg("Hello from Rust")
        .arg("--output")
        .arg("rust_qr.svg")
        .arg("--margin")
        .arg("4")
        .status()
        .expect("Failed to execute ZigQR process");
    
    assert!(status.success());
}

```

---

## 📖 Documentation

For the complete API reference, advanced build flags, and architecture guides, visit our [Mintlify Documentation](https://zigqr.blacklovertech.im).

---

## ⚖️ License

[MIT License](https://www.google.com/search?q=LICENSE)
