---
title: velox-sdk
description: The SDK for Velox.
license: MIT
author: skzidev
author_github: skzidev
repository: https://github.com/skzidev/velox-sdk
keywords:
date: 2026-08-21
updated_at: 2026-08-21T06:24:20+00:00
last_sync: 2026-08-21T06:24:20Z
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
permalink: /packages/skzidev/velox-sdk/
---

# Velox SDK

This repository lays out the programmatic interface for working with Velox and the V5 brain hardware.

Concurrency is handled through the VEXos task scheduler. You can use a `velox_sdk.V5Io` (which should ideally be aliased as `velox.Io`) instance which **should** hopefully let you use other Zig 0.16 dependencies out of the box (although that has not bene fully tested).
