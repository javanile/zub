---
title: opus-on-zig
description: "Opus codec wrapped with Zig's build system"
license: 0BSD
author: lateleite
author_github: lateleite
repository: https://github.com/lateleite/opus-on-zig
category: tooling
topics:
  - opus
  - opus-codec
  - zig
date: 2026-04-09
permalink: /packages/lateleite/opus-on-zig/
---

# Opus on Zig

This repository wraps the upstream Opus codec library source code with Zig's build system.

Zig 0.15.2 is required.

## Installing as a `build.zig.zon` package

Run in your Zig project:
```sh
zig fetch --save-exact=opus git+https://github.com/lateleite/opus-on-zig.git
```

Then in your `build.zig` file:
```zig
pub fn build(b: *std.Build) !void {
    // ...

    // Add a reference to the package you've just fetched...
    const dep_opus = b.dependency("opus", .{
        .target = target,
        .optimize = optimize,
    });
    const lib_opus = dep_opus.artifact("opus");

    // ...then link the library to your module
    your_module.linkLibrary(lib_opus);

    // ...
}
```

After that, you may use Opus' header files in your module.

## License

All (build) code here is released to public domain or under the BSD Zero Clause license, choose whichever you prefer.

You may find Opus' license at [https://github.com/xiph/opus/blob/788cc89ce4f2c42025d8c70ec1b4457dc89cd50f/LICENSE_PLEASE_READ.txt](https://github.com/xiph/opus/blob/788cc89ce4f2c42025d8c70ec1b4457dc89cd50f/LICENSE_PLEASE_READ.txt).
