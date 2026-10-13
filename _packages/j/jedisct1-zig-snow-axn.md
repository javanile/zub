---
title: zig-snow-axn
description: An implementation of the SNOW-Axn cipher.
license: ""
author: jedisct1
author_github: jedisct1
repository: https://github.com/jedisct1/zig-snow-axn
keywords:
  - aead
  - cipher
  - encryption
  - snow-axn
  - snow-v
  - ziglan
date: 2026-09-17
updated_at: 2026-09-17T18:34:29+00:00
last_sync: 2026-09-17T18:34:29Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/jedisct1/zig-snow-axn/
---

# SNOW-Axn: A Fast AEAD Stream Cipher in Aggregated Mode

A Zig implementation of the [SNOW-Axn](https://doi.org/10.62056/a6y7qj5vt) cipher.

## Usage

```zig
const SnowAx4 = @import("snow_axn").SnowAx4;

// key: [SnowAx4.key_length]u8; nonce: [SnowAx4.nonce_length]u8, unique for this key.
const plaintext = "Hello, SNOW-Axn!";
var ciphertext: [plaintext.len]u8 = undefined;
const tag = SnowAx4.encrypt(&ciphertext, plaintext, "header", key, nonce);

var decrypted: [plaintext.len]u8 = undefined;
try SnowAx4.decrypt(&decrypted, &ciphertext, tag, "header", key, nonce);
```

[The example program](src/example.zig) also makes the key and the nonce.

Encryption and decryption accept unaligned slices, and they can work in place. The input and the output must have the same length.

Other overlaps between the input and the output are not supported.

For encryption without authentication, use a variant with a zero-length tag and call `xor`. The same call with the same key and nonce decrypts the ciphertext.

```zig
const Stream = @import("snow_axn").SnowAxn(.{ .streams = 4, .tag_length = 0 });
Stream.xor(&ciphertext, plaintext, key, nonce);
```

For integrity only, use `const tag = SnowAx4.mac(data, key, nonce)` and `try SnowAx4.verify(tag, data, key, nonce)`.

The tag is the same as the AEAD tag of an empty message with `data` as associated data. These functions need a nonzero tag length.

Never use a nonce two times with the same key and the same parameters. Each message and each associated data must be shorter than 2^61 bytes.

The paper also limits one key to 2^64 invocations.

## Parameters

`SnowAx1`, `SnowAx2` and `SnowAx4` use 32-byte keys, 16-byte nonces and 16-byte tags.

`SnowAxn(options)` accepts every parameter value that the IV encoding of the paper defines:

| Option         | Range       | Default |
| :------------- | :---------- | ------: |
| `streams`      | 1–16        |       4 |
| `key_length`   | 16–32 bytes |      32 |
| `nonce_length` | 4–28 bytes  |      16 |
| `tag_length`   | 0–16 bytes  |      16 |

You select these parameters at compile time.

The IV encodes them, so a different parameter gives a different ciphertext and tag. Thus a shorter `tag_length` is not the same as a truncated 16-byte tag.
