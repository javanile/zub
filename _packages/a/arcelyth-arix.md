---
title: arix
description: A HTML parser written in Zig.
license: MIT
author: Arcelyth
author_github: Arcelyth
repository: https://github.com/Arcelyth/arix
keywords:
  - dom
  - html
  - html-parser
date: 2026-08-30
updated_at: 2026-08-30T14:09:21+00:00
last_sync: 2026-08-30T14:09:21Z
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
permalink: /packages/Arcelyth/arix/
---

# Arix

Arix is an HTML parser written in Zig for the purpose of high performance and minimal memory usage. It currently includes an encoding
sniffer, an HTML tokenizer, a TreeBuilder for tree construction, and a small DOM implementation.
Parser behavior is tested against the [html5lib test suite](https://github.com/html5lib/html5lib-tests).

Build and run the test: 
```sh
zig build test
```

You can add `debug` flag to show the debug informations. <br>
Add `-- [test_name]` to filter tests. <br>
For example: `zig build test --summary all -- tokenizer`.
