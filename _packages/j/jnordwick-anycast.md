---
title: anycast
description: One cast to rule them all
license: BSD-2-Clause
author: jnordwick
author_github: jnordwick
repository: https://github.com/jnordwick/anycast
keywords:
date: 2026-05-22
updated_at: 2026-05-22T18:53:33+00:00
last_sync: 2026-05-22T18:53:33Z
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
permalink: /packages/jnordwick/anycast/
---

** Future Direction

There is no direction. I just add them as I need them, and if you want me to add something either post a PR or message me on reddit and I'll see what I can do.

I do want to add zero-cost lvalue casts though since I find it quite annoying.

More to come... maybe... or not... but likely... kinda likely.


* Anycast
version 0.0 (this will never need versioning so don't worry about it). This works for 0.16.

I got tired of the endless casting in zig especially after the type arguemnts was removed from the casting functions in favor of using the expected return type. This can often lead to this string of verbose unnecessary casts, so I have slowly beed adding casting to this single casting function.

Will this cause bugs? Probably. It is a "do what I say and don't questions my authority" kind of thing. If you want to cast that bool into a float, it will trust you.

It will make it easier to do pointer and bit manipulation.

** Future Direction

There is no direction. I just add them as I need them, and if you want me to add something either post a PR or message me on reddit and I'll see what I can do.

I do want to add zero-cost lvalue casts though since I find it quite annoying.

More to come... maybe... or not... but likely... kinda likely.

** Currently Supported

#+begin_src
int, float, bool, enum -> int, float, bool, enum
int, ptr -> int, ptr
struct, union -> struct, union, int, float, enum, ptr
optional -> optional
#+end_src

** Examples

#+begin_src
cast(u32, 1243.4)
cast(bool, 123)
cast([*]u32, "asfd")
cast(f32, true) -> 1.0
#+end_src
