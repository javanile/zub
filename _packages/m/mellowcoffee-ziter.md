---
title: ziter
description: lazy, composable iterators for zig
license: MIT
author: mellowcoffee
author_github: mellowcoffee
repository: https://github.com/mellowcoffee/ziter
keywords:
  - iterator
date: 2026-08-28
updated_at: 2026-08-28T19:01:57+00:00
last_sync: 2026-08-28T19:01:57Z
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
permalink: /packages/mellowcoffee/ziter/
---

## 📼 ziter

Lazy, composable iterators for Zig.

Any container type may be an iterator as long as it declares the following:

```zig
pub const Item = T;
pub fn next(self: *@This()) ?Item;
```

`next` must return `null` when the iterator is exhausted, and must not return
an error union.

Iterators may be created via `slice`, `range`, `adapt`, or `from`, from slices,
intervals, std-style iterators, or hand-written implementations respectively.

Check `src/main.zig` for more details until a proper documentation is written.

### Todo

- [ ] Unit tests.
- [ ] Filters and maps with context, as Zig lacks closures. :(
- [ ] Mayyybe remove `Item` and just require `next` as `Item` can probably always be inferred from `next`?
- [ ] Write actual documentation.
