---
title: texzel
description: A pure Zig library for BCn texture encoding/decoding.
license: MIT
author: asgardkat
author_github: asgardkat
repository: https://github.com/asgardkat/texzel
keywords:
  - bc1
  - bc6h
  - bc7
  - bcn
  - compression
  - dxt
  - dxt1
  - dxt3
  - dxt5
  - encoding
  - rgtc
  - s3tc
  - texture
date: 2026-03-08
category: systems
updated_at: 2026-03-08T03:54:15+00:00
last_sync: 2026-03-08T03:54:15Z
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
permalink: /packages/asgardkat/texzel/
---

# Texzel

[![CI](https://img.shields.io/github/actions/workflow/status/asgardkat/texzel/main_ci.yml?branch=main&label=CI)](https://github.com/asgardkat/texzel/actions/workflows/main_ci.yml)
[![License](https://img.shields.io/github/license/asgardkat/texzel)](https://github.com/asgardkat/texzel/blob/main/LICENSE)
[![Zig](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Fasgardkat%2Ftexzel%2Fmain%2Fbuild.zig.zon&search=minimum_zig_version%5Cs%2A%3D%5Cs%2A%22%28%5B%5E%22%2B%5D%2B%29&replace=%241&label=zig&color=f7a41d&logo=zig&logoColor=white)](https://github.com/asgardkat/texzel/blob/main/build.zig.zon)

Texzel is a pure Zig library for texture encoding/decoding (compression/decompression) with no dependencies.

It is currently focused on the BCn, ETC2/EAC and ASTC codecs as well as converting between different raw pixel formats.

## Supported Formats
| Format | Decode | Encode | Notes |
|---|---|---|---|
| Raw | ✅ | ✅ | Supports any arbitrary pixel layout and can swizzle when converting. Some common ones are defined for convenience, including the packed 5:6:5, 4:4:4:4, 5:5:5:1, 10:10:10:2, 11:11:10 float and RGB9E5 shared exponent formats. |
| BC1 (S3TC DXT1) | ✅ | ✅ | BC1a is supported, any texel with alpha < 255 will be treated as fully transparent |
| BC2 (S3TC DXT3) | ✅ | ✅ | |
| BC3 (S3TC DXT5) | ✅ | ✅ | |
| BC4 (RGTC1) | ✅ | ✅ | |
| BC5 (RGTC2) | ✅ | ✅ | |
| BC6 (BPTC_FLOAT) | ✅ | ✅ | |
| BC7 (BPTC)  | ✅ | ✅ | |
| ETC1 | ✅ | ✅ | |
| ETC2 RGB | ✅ | ✅ | Includes the T, H and planar modes |
| ETC2 RGBA1 (punchthrough) | ✅ | ✅ | Alpha below 128 is encoded as transparent, transparent texels decode as all zeros |
| ETC2 RGBA8 | ✅ | ✅ | |
| EAC R11 | ✅ | ✅ | Unsigned only for now, decodes to 16 bits |
| EAC RG11 | ✅ | ✅ | Unsigned only for now, decodes to 16 bits |
| ASTC | ✅ | ❌ | All 2D block sizes from 4x4 to 12x12. `astc_4x4` and friends are the LDR profile and decode to 8 bits, set `.srgb = true` for sRGB textures, which round slightly differently. `astc_hdr_4x4` and friends are the HDR profile and decode to half floats. |

## Current State
Texzel is still very early in development and the API is not stable, the code is not particularly clean or efficient.

It works with textures I've tested but it's possible there are bugs in specific modes of specific codecs. Please open an issue if you find one!

Texzel does not currently support file formats, as such you must provide raw buffers to compress/decompress. I'm still uncertain if adding support for DDS/KTX2 etc should be in scope for this project or not.

Contributions are very welcome!

## Benchmarks
`zig build bench -Doptimize=ReleaseFast` times texzel against other libraries on the same files:

| Library | Decodes | Encodes |
|---|---|---|
| [bcdec](https://github.com/iOrange/bcdec) | BC1 to BC7 | |
| [etcdec](https://github.com/iOrange/etcdec) | ETC1, ETC2, EAC | |
| [stb_dxt](https://github.com/nothings/stb) | | BC1, BC3, BC4, BC5 |
| [bc7enc](https://github.com/richgel999/bc7enc) (rgbcx, bc7decomp) | BC1, BC3, BC4, BC5, BC7 | BC1, BC3, BC4, BC5, BC7 |
| [etcpak](https://github.com/wolfpld/etcpak) | BC3, BC4, BC7, ETC1, ETC2, EAC | BC1, BC3, BC4, BC5, BC7, ETC1, ETC2, EAC |
| [astcenc](https://github.com/ARM-software/astc-encoder) | ASTC | |

Decoders are checked against texzel's output. Every encoder, texzel included, is scored by decoding its output with bcdec or etcdec and comparing that to the source, so the quality numbers don't rely on texzel's decoder. Times are per image, single threaded, with every library writing into an output buffer it reuses, so allocating memory and faulting in fresh pages isn't counted. The ratio is texzel's time divided by the other library's, so lower is better for texzel and 1.0x means the same speed.

Arguments filter the rows, and `--min-ms` sets how long each measurement runs (300 by default):
```
zig build bench -Doptimize=ReleaseFast -- etc2 "decode bc7" --min-ms=100
```

The libraries are only fetched when you run the bench, so they aren't dependencies of the library. etcpak's BC1 and BC5 decoders aren't timed because they don't write every row of each block.

Decoding, measured on a Ryzen 9 9950X3D. Output is compared with bcdec for BCn, etcdec for ETC2/EAC and astcenc for ASTC.

| Decode | Output | texzel vs bcdec / etcdec / astcenc |
|---|---|---|
| BC1 | within 1 | 1.05x to 1.25x |
| BC2 | within 1 | ~1.2x |
| BC3 | within 1 | 1.35x |
| BC4 | identical | ~1.45x |
| BC5 | identical | ~1.05x |
| BC6 | identical | 1.15x to 1.2x |
| BC7 | identical | 0.8x to 0.85x |
| ETC1 | identical | 1.05x to 1.2x |
| ETC2 RGB | identical | ~1.2x |
| ETC2 RGBA1 | identical | ~1.5x |
| ETC2 RGBA8 | identical | 1.1x |
| EAC R11 | within 1 | ~0.95x |
| EAC RG11 | within 1 | ~0.7x |
| ASTC, mostly simple blocks | identical | 0.4x to 0.75x |
| ASTC, detailed images | identical | 1.1x to 1.3x |
| ASTC HDR | identical | 1.3x to 1.5x |

BC1 to BC3 can be off by 1 because texzel widens the 5:6:5 endpoints to 8 bits before blending the in-between colors, and bcdec blends first. Both are within what the format allows. EAC is off by 1 from etcdec because the two round 11 bits to 16 differently.

Encoding, same machine. Quality is RGB PSNR as decoded by bcdec or etcdec, higher is better. Best and worst are the other encoders with the highest and lowest quality. The last column is texzel's time over each other encoder's, from its best case to its worst.

| Encode | Image | texzel | Best other | Worst other | texzel vs others |
|---|---|---|---|---|---|
| BC1 | night | 5.9 ms, 39.7 dB | rgbcx level 18: 524 ms, 40.4 dB | etcpak: 0.10 ms, 37.5 dB | 0.01x to 58x |
| BC3 | alpha_gradient | 5.2 ms, 48.8 dB | rgbcx level 18: 281 ms, 50.3 dB | etcpak: 0.30 ms, 43.3 dB | 0.02x to 17x |
| BC4 | ziggy | 0.39 ms, 57.8 dB | rgbcx: 0.23 ms, 56.6 dB | etcpak: 0.03 ms, 50.8 dB | 0.54x to 13x |
| BC5 | ziggy | 0.67 ms, 60.4 dB | rgbcx: 0.36 ms, 59.3 dB | etcpak: 0.05 ms, 52.2 dB | 0.48x to 15x |
| BC7 | night, opaque_fast | 835 ms, 47.0 dB | bc7enc uber 4: 774 ms, 45.4 dB | bc7enc uber 0: 203 ms, 45.3 dB | 1.1x to 11x |
| BC7 | ziggy, alpha_fast | 682 ms, 65.1 dB | bc7enc uber 4: 108 ms, 64.9 dB | etcpak: 8.4 ms, 62.4 dB | 6.3x to 81x |
| ETC1 | night | 33 ms, 39.0 dB | etcpak: 1.5 ms, 37.8 dB | | 22x |
| ETC2 RGB | night | 59 ms, 39.4 dB | etcpak: 1.8 ms, 38.0 dB | etcpak, no heuristics: 2.4 ms, 37.9 dB | 25x to 33x |
| ETC2 RGBA8 | alpha_gradient | 57 ms, 48.3 dB | etcpak, no heuristics: 2.8 ms, 45.7 dB | etcpak: 1.8 ms, 45.6 dB | 20x to 31x |
| EAC R11 | ziggy | 2.8 ms, 56.0 dB | etcpak: 0.73 ms, 48.4 dB | | 3.8x |
| EAC RG11 | ziggy | 6.1 ms, 58.7 dB | etcpak: 1.3 ms, 50.6 dB | | 4.7x |

BC2, BC6 and ETC2 RGBA1 have nothing to compare against yet. BC1's quality only counts color on texels that aren't transparent in the source, since texzel uses BC1's transparent mode and the others don't. BC1 takes a `refinement_passes` option, three passes gets night to 39.9 dB for about 20% more time.

## Adding to your project
Texzel tracks Zig master, see `minimum_zig_version` in [build.zig.zon](build.zig.zon) for the version it's tested against.

1. Add texzel to your build.zig.zon
```
zig fetch --save git+https://github.com/asgardkat/texzel
```

2. Add the dependency to your project, for example:
```zig
const texzel_dependency = b.dependency("texzel", .{
  .target = target,
  .optimize = optimize,
});

exe_mod.addImport("texzel", texzel_dependency.module("texzel"));
```

## Usage Example
```zig
const allocator = ...;
const io = ...;

// Import Texzel
const texzel = @import("texzel");

// Load a raw rgba image
const raw_buffer = try std.Io.Dir.cwd().readFileAlloc(io, "resources/ziggy.rgba", allocator, .limited(16 << 20));
defer allocator.free(raw_buffer);

// Image dimensions
const dimensions = texzel.core.Dimensions{
    .width = 512,
    .height = 512,
};

// Create a raw image data instance from the buffer
const raw_image = try texzel.rawImageFromBuffer(
    allocator,
    texzel.pixel_formats.RGBA8U,
    dimensions,
    raw_buffer,
);
defer raw_image.deinit();

// Compress to BC1
const compressed_buffer = try texzel.encode(
    allocator,
    .bc1,
    texzel.pixel_formats.RGBA8U,
    raw_image,
    .{},
);
defer allocator.free(compressed_buffer);

// Decompress to RawImage but in BGRA8U this time
const new_raw_image = try texzel.decode(
    allocator,
    .bc1,
    texzel.pixel_formats.BGRA8U,
    dimensions,
    compressed_buffer,
    .{},
);
defer new_raw_image.deinit();

// Access the new raw buffer
const new_raw_buffer = new_raw_image.asBuffer();
_ = new_raw_buffer; // Do something
```

## Third Party
The BC6 and BC7 code is based on [bcdec](https://github.com/iOrange/bcdec) and [block_compression](https://github.com/hasenbanck/block_compression), and the bench builds bcdec to compare against. The test images are listed with their licenses too.

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for the full notices.

## License
Texzel is licensed under the [MIT License](LICENSE).

Licenses for third-party software and assets can be found [here](THIRD_PARTY_LICENSES.md).
