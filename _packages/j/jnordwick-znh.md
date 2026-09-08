---
title: znh
description: "Zig Microbenchmarking Harness: for generating microbenchmarks in zig, but way inferior to JMH"
license: BSD-2-Clause
author: jnordwick
author_github: jnordwick
repository: https://github.com/jnordwick/znh
keywords:
date: 2026-09-08
updated_at: 2026-09-08T14:35:48+00:00
last_sync: 2026-09-08T14:35:48Z
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
permalink: /packages/jnordwick/znh/
---

* zayin -- zig benchmarking harness

I'm ripping everything up and chanding the way it runs.

The new Io interface requires deep changes already and
there has been some changes in std and the compiler, so
I'm using this as a reason to make the other changes I
wanted.

Also renaming it to zayin and will change the repo name
when soon-ish.
