---
title: media-formats
description: Media formats implementation in zig
license: MIT
author: zigouat
author_github: zigouat
repository: https://github.com/zigouat/media-formats
keywords:
  - demuxer
  - isobmff
  - ivf
  - media-format
  - mp4
  - muxer
date: 2026-07-16
updated_at: 2026-07-16T17:23:34+00:00
last_sync: 2026-07-16T17:23:34Z
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
permalink: /packages/zigouat/media-formats/
---

# Protocols

Zig implementations of media formats (muxers/demuxers).

The projects is structured into modules, each module is a separate library that can be used independently. The modules are:

* `mp4` - implementation of the MP4 format.
* `ivf` - implementation of the IVF format.

## Installation

Add `media_formats` as a dependency in your `build.zig.zon` file:

```bash
zig fetch --save git+https://github.com/zigouat/media-formats.git#v0.1.0
```

Then, in your `build.zig` file, add the following:

```zig
const media_formats = b.dependency("media_formats", .{
    .target = target,
    .optimize = optimize,
});

// You can add the whole module:
exe.root_module.addImportPath("media_formats", media_formats.module("media-formats"));

// Or you can import only the modules you need:
exe.root_module.addImportPath("mp4", media_formats.module("mp4"));
```
