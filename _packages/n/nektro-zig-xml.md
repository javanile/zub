---
title: zig-xml
description: A pure-Zig fully spec-compliant XML parser.
license: MPL-2.0
author: nektro
author_github: nektro
repository: https://github.com/nektro/zig-xml
keywords:
date: 2026-11-04
updated_at: 2026-11-04T03:18:37+00:00
last_sync: 2026-11-04T03:18:37Z
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
permalink: /packages/nektro/zig-xml/
---

# zig-xml

![loc](https://sloc.xyz/github/nektro/zig-xml)
[![license](https://img.shields.io/github/license/nektro/zig-xml.svg)](https://github.com/nektro/zig-xml/blob/master/LICENSE)
[![nektro @ github sponsors](https://img.shields.io/badge/sponsors-nektro-purple?logo=github)](https://github.com/sponsors/nektro)
[![Zig](https://img.shields.io/badge/Zig-0.17-f7a41d)](https://ziglang.org/)
[![Zigmod](https://img.shields.io/badge/Zigmod-latest-f7a41d)](https://github.com/nektro/zigmod)

A pure-zig spec-compliant XML parser.

https://www.w3.org/TR/xml/

Passes all standalone tests from https://www.w3.org/XML/Test/xmlconf-20020606.htm, even more coverage coming soon.

One caveat is that this parser expects UTF-8.

```
Build Summary: 3/3 steps succeeded; 120/120 tests passed
test success
└─ run test 120 passed 5ms MaxRSS:1M
   └─ zig test Debug native success 1s MaxRSS:247M
```
