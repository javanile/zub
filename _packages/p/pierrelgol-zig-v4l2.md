---
title: zig-v4l2
description: typed v4l2-bindings for Zig
license: MIT
author: pierrelgol
author_github: pierrelgol
repository: https://github.com/pierrelgol/zig-v4l2
keywords:
  - linux
  - v4l2
  - zig-libary
date: 2026-04-19
category: systems
updated_at: 2026-04-19T10:09:43+00:00
last_sync: 2026-04-19T10:09:43Z
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
permalink: /packages/pierrelgol/zig-v4l2/
---

# zig-v4l2

Typed [Video4Linux2](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/v4l2.html) bindings for Zig.

Provides idiomatic Zig types and constants for the full V4L2 API surface: capabilities, buffers, formats, controls, events, tuners, subdevices, media topology, and more.

> Linux only. Requires V4L2 kernel headers (`linux/videodev2.h`).

## Installation

### 1. Add the dependency

```sh
zig fetch --save git+https://github.com/pierrelgol/zig-v4l2#main
```

This adds `zig_v4l2` to your `build.zig.zon`.

### 2. Wire it up in `build.zig`

```zig
const zig_v4l2 = b.dependency("zig_v4l2", .{
    .target = target,
    .optimize = optimize,
});

// Import the module into your executable / library:
exe.root_module.addImport("z4l2", zig_v4l2.module("z4l2"));
```

### Cross-compilation / non-standard header location

If your V4L2 headers are not under `/usr/include/<linux-triple>/`, pass the
`header-path` option (relative to `/usr/include`):

```sh
zig build -Dheader-path=arm-linux-gnueabihf
```

## Usage

```zig
const z4l2 = @import("z4l2");

// Query device capabilities
var cap: z4l2.capability.Capability = undefined;
// ... fill via ioctl VIDIOC_QUERYCAP ...

// Work with pixel formats
const fmt: z4l2.pixel.PixelFormat = .yuyv;

// Work with controls — IDs are exported directly from z4l2.control
const brightness_id = z4l2.control.brightness;
```

See [`src/demo.zig`](src/demo.zig) for a working example that queries and prints
capability information for a V4L2 device.

```sh
zig build run                      # queries /dev/video0
zig build run -- /dev/video1       # queries a specific device
```

## API overview

| Module | Contents |
|---|---|
| `z4l2.capability` | `VIDIOC_QUERYCAP`, device capability flags |
| `z4l2.buffer` | buffer types, memory models, `v4l2_buffer` |
| `z4l2.pixel` | pixel formats (`V4L2_PIX_FMT_*`) |
| `z4l2.frame` | frame size / interval enumeration |
| `z4l2.stream` | streaming parameters |
| `z4l2.control` | generic control infrastructure |
| `z4l2.geometry` | crop / selection rectangles |
| `z4l2.format` | image format negotiation |
| `z4l2.input` / `z4l2.output` | input/output enumeration |
| `z4l2.tuner` | tuner / modulator |
| `z4l2.audio` | audio input/output |
| `z4l2.event` | event subscription and dequeuing |
| `z4l2.media` | Media Controller topology |
| `z4l2.mediabus` | media bus formats |
| `z4l2.subdev` | sub-device ioctls |
| `z4l2.standard` | video standards |
| `z4l2.timings` | DV timings |
| `z4l2.encoder` / `z4l2.decoder` | codec parameters |
| `z4l2.vbi` | VBI capture / output |
| `z4l2.debug` | chip register access |
| `z4l2.ioctl` | `Ioctl` enum and `IO`/`IOR`/`IOW`/`IOWR` helpers |
| `z4l2.abi` | raw ABI structs from the kernel headers |
| `z4l2.control.*` | per-class control IDs (camera, image, jpeg, mpeg, …) |
| `z4l2.control.stateless.*` | stateless codec controls (H.264, HEVC, VP8/9, AV1, …) |

## License

MIT — see [LICENSE](LICENSE).

## AI disclosure

Once the core bindings were hand-written and working, Claude and Codex were used as batch-processing tools for mechanical refactoring work: splitting the original monolithic binding file into the smaller, namespaced modules you see under `src/v4l2/`, batch-writing ABI-level tests, and drafting inline documentation for the generated types. All design decisions, the binding implementation itself, and review of the generated output were done by hand.

This library is still early. There are likely rough edges, missing coverage, and bugs. If you run into anything, feel free to open an issue or send a pull request — contributions are welcome.
