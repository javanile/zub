---
title: ogg-on-zig
description: The OGG container library wrapped with Zig's build system
license: 0BSD
author: lateleite
author_github: lateleite
repository: https://github.com/lateleite/ogg-on-zig
category: tooling
topics:
  - ogg
  - zig
date: 2026-04-09
permalink: /packages/lateleite/ogg-on-zig/
---

# Ogg on Zig

This repository wraps the upstream OGG container library source code with Zig's build system.

Zig 0.15.2 is required.

## Installing as a `build.zig.zon` package

Run in your Zig project:
```sh
zig fetch --save-exact=ogg git+https://github.com/lateleite/ogg-on-zig.git
```

Then in your `build.zig` file:
```zig
pub fn build(b: *std.Build) !void {
    // ...

    // Add a reference to the package you've just fetched...
    const dep_ogg = b.dependency("ogg", .{
        .target = target,
        .optimize = optimize,
    });
    const lib_ogg = dep_ogg.artifact("ogg");

    // ...then link the library to your module
    your_module.linkLibrary(lib_ogg);

    // ...
}
```

After that, you may use Ogg's header files in your module.

## License

All (build) code here is released to public domain or under the BSD Zero Clause license, choose whichever you prefer.

You may find Ogg's license at [https://github.com/xiph/ogg/blob/06a5e0262cdc28aa4ae6797627a783b5010440f0/COPYING](https://github.com/xiph/ogg/blob/06a5e0262cdc28aa4ae6797627a783b5010440f0/COPYING).
