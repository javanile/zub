---
title: zig.rb
description: 🧩 Create type-safe Ruby native extensions effortlessly with zig.rb, offering automatic memory management and high performance using Zig.
license: 
author: GC-RIP
author_github: GC-RIP
repository: https://github.com/GC-RIP/zig.rb
topics:
  - embedded-zig
  - microzig
  - ring-buffer
  - stm32f103rb
  - zig
date: 2026-04-10
permalink: /packages/gc-rip-zig-rb/
---

# zig.rb

🧩 Create type-safe Ruby native extensions effortlessly with zig.rb, offering automatic memory management and high performance using Zig.

## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{
    .zig_rb = .{
        .url = "https://github.com/GC-RIP/zig.rb/archive/refs/heads/main.tar.gz",
    },
},
```
