---
title: sdl3_mixer-on-zig
description: "SDL3_Mixer library wrapped with Zig's build system"
license: 0BSD
author: lateleite
author_github: lateleite
repository: https://github.com/lateleite/sdl3_mixer-on-zig
keywords:
  - sdl-mixer
  - sdl3
  - sdl3-mixer
date: 2026-04-09
updated_at: 2026-04-09T14:33:07+00:00
last_sync: 2026-04-09T14:33:07Z
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
permalink: /packages/lateleite/sdl3_mixer-on-zig/
---

# SDL3_Mixer on Zig

This repository wraps the upstream SDL3_Mixer library source code with Zig's build system.

Zig 0.15.2 is required.

The build setup support the following audio decoders:

- FLAC through dr_flac
- GME's formats
- MIDI through TiMidity
- Module/tracker music through XMP
- MP3 through dr_mp3
- Opus
- Vorbis

It also uses [castholm's SDL3 port by default](https://github.com/castholm/SDL).

## Installing as a `build.zig.zon` package

Run in your Zig project:
```sh
zig fetch --save-exact=sdl3_mixer git+https://github.com/lateleite/sdl3_mixer-on-zig.git
```

Then in your `build.zig` file:
```zig
pub fn build(b: *std.Build) !void {
    // ...

    // Add a reference to the package you've just fetched...
    const dep_mixer = b.dependency("sdl3_mixer", .{
        .target = target,
        .optimize = optimize,
        // you may choose to use your system's SDL3 library,
        // instead of building and statically linking another.
        //.@"use-system-sdl" = false,
    });
    const lib_mixer = dep_mixer.artifact("SDL_mixer");

    // ...then link the library to your module
    your_module.linkLibrary(lib_mixer);

    // ...
}
```

After that, you may use SDL3_Mixer's header files in your module.

## License

All (build) code here is released to public domain or under the BSD Zero Clause license, choose whichever you prefer.

You may find SDL3_Mixer's license at [https://github.com/libsdl-org/SDL_mixer/blob/8c52ef985c3c6495fcb5cf7a118aa544388c2765/LICENSE.txt](https://github.com/libsdl-org/SDL_mixer/blob/8c52ef985c3c6495fcb5cf7a118aa544388c2765/LICENSE.txt).
