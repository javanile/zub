---
title: arix
description: A web browser engine written in Zig.
license: MIT
author: Arcelyth
author_github: Arcelyth
repository: https://github.com/Arcelyth/arix
keywords:
  - browser
  - css-parser
  - dom
  - html-parser
  - web
  - webbrowser
  - webengine
date: 2026-09-05
updated_at: 2026-09-05T13:25:30+00:00
last_sync: 2026-09-05T13:25:30Z
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

Arix is a web browser engine written in Zig for the purpose of high performance and minimal memory usage.  <br>

The project currently includes:

- HTML parser
- CSS parser
- A small DOM implementation

**Arix is still under active development. Networking, style engine, layout engine, painting and the browser user interface are not complete yet.**

## Testing

HTML parser's behavior is tested against the [html5lib test suite](https://github.com/html5lib/html5lib-tests).

Build and run the test: 
```sh
zig build test
```

You can add `debug` flag to show the debug informations. <br>
Add `-- [test_name]` to filter tests. <br>

For example: 
```sh
zig build test --summary all -- tokenizer
```
