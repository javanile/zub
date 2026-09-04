---
title: zigar
description: Toolkit enabling the use of Zig code in JavaScript and PHP projects
license: MIT
author: chung-leong
author_github: chung-leong
repository: https://github.com/chung-leong/zigar
keywords:
  - bunjs
  - electron
  - javascript
  - nodejs
  - nwjs
  - php
  - php8
  - phpextension
  - rollup-plugin
  - wasm
  - webpack-plugin
date: 2026-09-04
category: systems
updated_at: 2026-09-04T12:28:33+00:00
last_sync: 2026-09-04T12:28:33Z
package_kind: library
has_library: false
has_binary: false
has_distributable_binary: false
binary_count: 0
distributable_binary_count: 0
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/chung-leong/zigar/
---

# Zigar

![Logo](./logo.png)

A software tool set that lets you utilize [Zig](https://ziglang.org/) code in your JavaScript or
PHP projects.

Consult the [project wiki](https://github.com/chung-leong/zigar/wiki) for installation instructions
and tutorials.

## Features

* Access to all Zig data types in JavaScript/PHP
* Zig-to-JavaScript/PHP, JavaScript/PHP-to-Zig call marshalling
* Async task management
* Threads in native code and WebAssembly (with support for pthread)
* Emulating of file system operations
* Support for MacOS, Linux, and Windows (both 64-bit and 32-bit)
* Support for Node.js, Bun.js, Electron, and NW.js (native code execution)
* Support for Webpack, Rollup, and Vite (WebAssembly)

## Versioning

The major and minor version numbers of Zigar correspond to the version of the Zig compiler
it's designed for. The current version is 0.15.3. It works with Zig 0.15.x.

## Technical support

If you have questions concerning this project, please post them at this project's
[discussion section](https://github.com/chung-leong/zigar/discussions). I can also be contacted at
[ziggit.dev](https://ziggit.dev/), which also happens to be an excellent forum for finding help on
all matters related to the Zig language.
