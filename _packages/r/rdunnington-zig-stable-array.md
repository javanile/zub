---
title: zig-stable-array
description: Address-stable array with a max size that allocates directly from virtual memory.
license: NOASSERTION
author: rdunnington
author_github: rdunnington
repository: https://github.com/rdunnington/zig-stable-array
keywords:
date: 2026-05-22
updated_at: 2026-05-22T02:23:12+00:00
last_sync: 2026-05-22T02:23:12Z
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
permalink: /packages/rdunnington/zig-stable-array/
---

# zig-stable-array
Address-stable array with a max size that allocates directly from virtual memory. Memory is only committed when actually used, and virtual page table mappings are relatively cheap, so you only pay for the memory that you're actually using. Additionally, since all memory remains inplace, and new memory is committed incrementally at the end of the array, there are no additional recopies of data made when the array is enlarged.

Ideal use cases are for large arrays that potentially grow over time. When reallocating a dynamic array with a high upper bound would be a waste of memory, and depending on dynamic resizing may incur high recopy costs due to the size of the array, consider using this array type. Another good use case is when stable pointers or slices to the array contents are desired; since the memory is never moved, pointers to the contents of the array will not be invalidated when growing. Not recommended for small arrays, since the minimum allocation size is the platform's minimum page size. Also not for use with platforms that don't support virtual memory, such as WASM.

Typical usage is to specify a large size up-front that the array should not encounter, such as 2GB+. Then use the array as usual. If freeing memory is desired, `shrinkAndFree()` will decommit memory at the end of the array. Total memory usage can be calculated with `calcTotalUsedBytes()`. The interface is very similar to ArrayList, except for the allocator semantics. Since typical heap semantics don't apply to this array, the memory is manually managed using mmap/munmap and VirtualAlloc/VirtualFree on nix and Windows platforms, respectively.

Usage:
```zig
var array = StableArray(u8).init(1024 * 1024 * 1024 * 128); // virtual address reservation of 128 GB
try array.appendSlice(&[_]u8{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 });
assert(array.calcTotalUsedBytes() == mem.page_size);
for (array.items) |v, i| {
    assert(v == i);
}
array.shrinkAndFree(5);
assert(array.calcTotalUsedBytes() == mem.page_size);
array.deinit();
```
