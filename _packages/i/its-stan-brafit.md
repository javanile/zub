---
title: Brafit
description: Brainfuck interpreter written in Zig
license: MIT
author: its-Stan
author_github: its-Stan
repository: https://github.com/its-Stan/Brafit
keywords:
  - brainfuck
  - brainfuck-interpreter
  - interpreter
date: 2026-06-24
category: systems
updated_at: 2026-06-24T23:38:24+00:00
last_sync: 2026-06-24T23:38:24Z
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
permalink: /packages/its-Stan/Brafit/
---

# Brafit

Zig written BRAinFuck InTerpreter.
The build is done using the zig cli with `zig build [--release]`.
The executable output take a filepath pointing to the source file as input.
The output of the executable is the execution of the Brainfuck source code, using stdin as input, and stdout as output.
