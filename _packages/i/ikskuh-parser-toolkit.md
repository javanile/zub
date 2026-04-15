---
title: parser-toolkit
description: A toolkit that makes it easier to write recursive-descent parsers in Zig.
license: MIT
author: ikskuh
author_github: ikskuh
repository: https://github.com/ikskuh/parser-toolkit
keywords:
  - compiler
  - compiler-frontend
  - parser
  - recursive-descent-parser
  - tokenizer
  - tokenizer-parser
date: 2026-04-15
category: data-formats
updated_at: 2026-04-15T10:01:18+00:00
last_sync: 2026-04-15T10:01:18Z
permalink: /packages/ikskuh/parser-toolkit/
---

# A parser toolkit

![Project Logo](design/logo.png)

This repo contains a tiny parser toolkit that can be used to build new parsers and programming languages.

It provides:
- [x] Configurable tokenizer
- [x] Parser core (accept functions with state restoration)
- [ ] Compiler error management (emission, rendering, source locations)


## Demo

Invoke `zig build run` to run a tiny command line calculator that can evaluate basic expressions, parens and invoke functions:
```
$ zig build run
? 10
= 10
? 10 + 10
= 20
? 5 * 3
= 15
? a = 10
= 10
? sqrt(a)
= 3.1622776601683795
? sin(3.14)
= 0.0015926529164868282
? a = a + 1
= 11
? a = a + 1
= 12
? ^D
```

Available functions are:
```zig
fn sin(v: f64) f64
fn cos(v: f64) f64
fn tan(v: f64) f64
fn sqrt(v: f64) f64
fn pow(a: f64, b: f64) f64
fn ln(v: f64) f64
fn ln10(v: f64) f64
fn ln2(v: f64) f64
fn log(b: f64, v: f64) f64
```
