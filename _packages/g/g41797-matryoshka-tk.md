---
title: matryoshka-tk
description: Toolkit for Building Multitasking Systems in Zig
license: MIT
author: g41797
author_github: g41797
repository: https://github.com/g41797/matryoshka-tk
keywords:
  - building-block
  - concurrent-programming
  - modular-monolith
  - multitasking
  - std-io
  - toolkit
date: 2026-08-13
updated_at: 2026-08-13T06:02:15+00:00
last_sync: 2026-08-13T06:02:15Z
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
permalink: /packages/g41797/matryoshka-tk/
---

![](kitchen/_logo/matryoshka-tk-logo.png)

---

# Toolkit for Building Multitasking Systems

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Linux](https://github.com/g41797/matryoshka-tk/actions/workflows/linux.yml/badge.svg)](https://github.com/g41797/matryoshka-tk/actions/workflows/linux.yml)
[![Windows](https://github.com/g41797/matryoshka-tk/actions/workflows/windows.yml/badge.svg)](https://github.com/g41797/matryoshka-tk/actions/workflows/windows.yml)
[![macOS](https://github.com/g41797/matryoshka-tk/actions/workflows/mac.yml/badge.svg)](https://github.com/g41797/matryoshka-tk/actions/workflows/mac.yml)
[![Deploy Documentation](https://github.com/g41797/matryoshka-tk/actions/workflows/docs.yml/badge.svg)](https://github.com/g41797/matryoshka-tk/actions/workflows/docs.yml)


---


Software has two worlds.

- The first moves data.
- The second processes data.

Matryoshka-Tk is a _toolkit_ for the second world.


---

## What Matryoshka-Tk Is For

---

Matryoshka-Tk provides

- tools for the code that runs
  - **after** data enters the system
  - **before** data leaves the system
  - **within** long-running _tasks_

Typical example of such system - Image processing pipeline.

Goal of Matryoshka:

- to let developers think in terms of
  - processing
  - inter-tasks communication
  - reusing
  - workflows
- instead of low-level details

---

## NAQ (Never Asked Questions)

---


<details>  
<summary>On the landing page, I saw the Matryoshka LOC count. How do you calculate it?</summary>

- Only src/*.zig files
- Comments, imports and empty lines are excluded 

Today (11 Aug 2026) - **722** LOC

</details>

---



## Want to understand it?

---


Read this <a href="https://g41797.github.io/matryoshka-tk/" target="_blank" rel="noopener noreferrer">beautiful documentation</a>

---
