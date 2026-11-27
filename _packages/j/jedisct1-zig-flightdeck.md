---
title: zig-flightdeck
description: "FlightDeck-DeckBO: Parallelizable, session-supporting, nonce-misuse resistant and committing authenticated encryption."
license: MIT
author: jedisct1
author_github: jedisct1
repository: https://github.com/jedisct1/zig-flightdeck
keywords:
  - aead
  - authenticated-encryption
  - cryptography
  - deck-bo
  - deckbo
  - flighdeck
  - flightdeck
  - kangarootwelv
  - keccak
  - sponge
  - turboshake
  - turboshake128-bo
  - turboshake256-bo
date: 2026-11-27
updated_at: 2026-11-27T16:55:00+00:00
last_sync: 2026-11-27T16:55:00Z
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
permalink: /packages/jedisct1/zig-flightdeck/
---

# FlightDeck for Zig

A Zig implementation of FlightDeck and Deck-BO for encrypting and authenticating data.
Written entirely in Zig, with no dependencies beyond the standard library.

This is the original implementation.
It was ported to [Rust](https://github.com/jedisct1/rust-flightdeck) and [C](https://github.com/jedisct1/c-flightdeck), and all three give the same results, byte for byte.

## What's in there

- Duplex cipher: `Shake128Duplex`, `Shake256Duplex`, `TurboShake128Duplex`, `TurboShake256Duplex`.
- Deck cipher: `Shake128FlightDeck`, `Shake256FlightDeck`, `TurboShake128FlightDeck`, `TurboShake256FlightDeck`.
- Authenticated encryption: `Shake128Bo(tag_length)`, `Shake256Bo(...)`, `TurboShake128Bo(...)`, `TurboShake256Bo(...)`.

Not sure which layer you need? Here's what each one does:

- Authenticated encryption is what you want to protect messages.
  You give it a key and a message, and it gives you back a ciphertext nobody can read, plus a tag that proves nobody tampered with it.
  If you just want to encrypt things, pick this one and ignore the rest.
- A deck cipher is the building block underneath.
  It mixes a key with any data you feed it, and gives you back as many random-looking bytes as you ask for.
  That's handy to authenticate data without encrypting it, to derive keys, or to build your own protocol.
- A duplex cipher does the same thing as a deck cipher, but only on small blocks, one at a time.
  The deck cipher is built with it, and unless you're building a mode of your own, you won't need it directly.

The generic constructions behind them are public too: `OverwriteDuplex`, `FlightDeck` and `DeckBo`.

So you can build your own:

- `FlightDeck` takes any duplex type that looks like `OverwriteDuplex`, a chunk length and a chaining value length.
- `DeckBo` takes any deck cipher and a tag length.

And SHAKE or TurboSHAKE?
The TurboSHAKE instances use 12 rounds of Keccak-p[1600] and are about twice as fast as the SHAKE ones, which use 24.
The 128 and 256 in the names are the security levels, in bits.

## Installing

Add the package to your `build.zig.zon`:

```sh
zig fetch --save git+https://github.com/jedisct1/zig-flightdeck
```

Then make the module available to your code, in `build.zig`:

```zig
const flightdeck = b.dependency("flightdeck", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("flightdeck", flightdeck.module("flightdeck"));
```

## Usage

A deck cipher takes strings of any length, and gives you back as many bytes as you want after each of them.
Those bytes depend on the key and on everything it was given so far.

```zig
const flightdeck = @import("flightdeck");

var deck: flightdeck.TurboShake128FlightDeck = .init(key);

// Absorb a string, get 32 bytes that depend on the key and on that string.
var mac: [32]u8 = undefined;
deck.duplex(&mac, message, 1);

// Get more output from the same call.
var more: [1000]u8 = undefined;
deck.squeeze(&more);

// Absorb another string. The output now depends on both strings.
// It can also be XORed into a buffer, to use it as a keystream.
deck.duplex(&.{}, nonce, 1);
deck.xor(ciphertext, plaintext);
```

That last argument of `duplex` is a trailer: a handful of bits you can use for domain separation.

It's an integer made of these bits, least significant first, followed by a final 1.
So `1` is the empty trailer, `0b10` is the single bit 0, and FlightDeck accepts values from 1 to 31.

Need a clone? Just copy the instance.
There's also `cloneCompact()`, which gives you a clone that can only be used to absorb the next string.

One thing to remember: call `duplex` before `squeeze` or `xor`.
There's nothing to squeeze before that, and you'll hit an assertion.

Authenticated encryption works on sessions:

```zig
const Aead = flightdeck.TurboShake128Bo(32);

var sender: Aead = .init(key);
var receiver: Aead = .init(key);

var tag: [Aead.tag_length]u8 = undefined;
sender.encrypt(ciphertext, &tag, message, associated_data);
try receiver.decrypt(decrypted, ciphertext, tag, associated_data);
```

Every message is authenticated along with all the messages that came before it in the session.

There's no nonce. So if you encrypt the same message twice, at the same point of two sessions with the same key, you get the same ciphertext.

Besides the length of the message, that's all it reveals, but if it matters to you, put a nonce or a counter in the associated data.

The tag length is a parameter, in bytes.

A tag of twice the security level, so 32 bytes for the 128-bit instances, also commits to the key, the associated data and the plaintext at that security level.

Keys are normally `key_length` random bytes: 16 for the 128-bit instances and 32 for the 256-bit ones.

That said, any byte string of at most `key_length_max` bytes is accepted, which is 160 and 128 bytes respectively.

## Sessions

A session is a value like any other.
`init()` starts it, everything you encrypt, decrypt or absorb moves it forward, and you keep it around for as long as the conversation lasts, one on each side.

Encrypting a message and decrypting it leave a session in the same state.
So a single session can carry both directions, as long as the two sides take turns:

```zig
const Aead = flightdeck.TurboShake128Bo(16);

var alice: Aead = .init(key);
var bob: Aead = .init(key);

var buffer: [4]u8 = undefined;
var tag: [Aead.tag_length]u8 = undefined;

alice.encrypt(&buffer, &tag, "ping", "");
try bob.decrypt(&buffer, &buffer, tag, "");

bob.encrypt(&buffer, &tag, "pong", "");
try alice.decrypt(&buffer, &buffer, tag, "");
```

If both sides can send whenever they want, their messages can cross and the two sessions stop matching.
In that case, use two sessions, one for each direction, each with its own key. There's an example below.

`absorb()` mixes something into a session without sending a ciphertext: a session identifier, a nonce, the transcript of a handshake.
Both sides have to absorb the same thing at the same point.

`squeeze()` gives you bytes that depend on the key and on everything that happened in the session so far.
Both sides get the same ones, so that's how you make new keys out of a session.

```zig
alice.absorb("session 1234");
bob.absorb("session 1234");

var alice_key: [32]u8 = undefined;
var bob_key: [32]u8 = undefined;
alice.squeeze(&alice_key);
bob.squeeze(&bob_key);
// alice_key and bob_key are the same.
```

All of this happens on the same state, in any order you like: encrypt, decrypt, absorb, squeeze.
The only rule is that the two sides go through the same messages and the same `absorb()` calls, in the same order.

Squeezing is not part of that, because it doesn't move the session: what comes next is the same whether you squeezed or not.
Squeeze again and you get the bytes that follow, not the same ones, until the next message or `absorb()`.
There has to be something in the session first: on a brand new one, `squeeze()` hits an assertion.

An `absorb()` is just an empty message, whose tag is thrown away.
If you'd rather have the other side check what it absorbed, send that tag instead:

```zig
alice.encrypt(&.{}, &tag, &.{}, "session 1234");
try bob.decrypt(&.{}, &.{}, tag, "session 1234");
```

What you squeeze comes after the tag of the last message, and never includes it.
So tags can travel in the clear and squeezed bytes can stay secret.

A few more things to know:

- A message that doesn't authenticate doesn't move the session.
  So a forged or damaged one does no harm: the real one still decrypts after it.
- A message that gets lost or comes out of order is another story: what was sent after it doesn't decrypt until it shows up.
  So sessions need a transport that delivers everything, in order.
- Copying the instance copies the session, to save it or to try something on the side.
- Messages and `absorb()` are Deck-BO as the paper specifies it.
  `squeeze()` is an addition, so don't expect it from other implementations.

Back to the two directions that don't take turns.
Squeeze two keys from a session both sides share, and start one session for each direction.
Here's the client. The server does the same thing with the two keys swapped:

```zig
var keys: [32]u8 = undefined;
handshake.squeeze(&keys);

const client_to_server = keys[0..16];
const server_to_client = keys[16..];
var sending: Aead = .init(client_to_server);
var receiving: Aead = .init(server_to_client);
```

## Hashing

A deck cipher doesn't need a secret key.
With an empty key, it's a hash function:

```zig
var hasher: flightdeck.TurboShake128FlightDeck = .init("");

var digest: [32]u8 = undefined;
hasher.duplex(&digest, message, 1);

// A longer digest? Keep squeezing.
var more: [32]u8 = undefined;
hasher.squeeze(&more);
```

Each call to `duplex()` adds a string, and the digest covers all of them, in order.
There's no way to mix up `"ab"` then `"c"` with `"a"` then `"bc"`, so you can hash a list of fields without length prefixes.

Ask for at least 32 bytes with the 128-bit instances, and 64 bytes with the 256-bit ones.
Finding two inputs with the same digest is then as hard as it is with SHAKE or TurboSHAKE: both papers prove it, even when the key is public.

A public string works as a key too.
Using the name of your application, for instance, keeps its digests apart from everybody else's.

Before you use it that way, know that:

- It's not a standard hash function. The digests don't match TurboSHAKE, KangarooTwelve or anything else, so use those if other software has to compute them.
- The FlightDeck paper mentions hashing without a key as future work.
  If that gets specified some day, the digests may not be the same as the ones you get here.
- Only collisions are covered by a proof.
- Authenticated encryption needs a secret key. Without one, anybody can decrypt.

## Performance

### x86-64, with AVX-512

AMD Ryzen 7 7700 (Zen 4)

| MiB/s   | Code   |  64 B | 1 KiB | 8 KiB | 64 KiB | 1 MiB |
| ------- | ------ | ----: | ----: | ----: | -----: | ----: |
| Hash    | Zig    |   509 |  1377 |  2319 |   4998 |  5952 |
|         | C      |   529 |  1421 |  2347 |   6148 |  6365 |
|         | Rust   |   498 |  1423 |  2306 |   6014 |  6286 |
|         | XKCP   |   178 |   731 |   878 |   2322 |  5124 |
|         | BLAKE3 |   825 |   958 |  4958 |   6340 |  6378 |
| Absorb  | Zig    |   506 |  1375 |  2318 |   4996 |  5951 |
|         | C      |   485 |  1398 |  2342 |   6131 |  6355 |
|         | Rust   |   534 |  1449 |  2317 |   6019 |  6283 |
|         | XKCP   |   176 |   728 |   876 |   2322 |  5123 |
|         | BLAKE3 |   820 |   946 |  4984 |   6335 |  6381 |
| Squeeze | Zig    |   510 |  2919 |  5473 |   6088 |  6171 |
|         | C      |   495 |  2796 |  5366 |   5980 |  6083 |
|         | Rust   |   530 |  2647 |  5351 |   6082 |  6162 |
|         | XKCP   |   178 |   830 |  3797 |   5567 |  5805 |
|         | BLAKE3 |   816 |  5831 |  6655 |   6745 |  6720 |
| Deck-BO | Zig    |   250 |   938 |  1622 |   2724 |  3010 |
|         | C      |   247 |   936 |  1625 |   2995 |  3082 |
|         | Rust   |   271 |   935 |  1611 |   2982 |  3069 |
|         | XKCP   |    87 |   384 |   708 |   1631 |  2700 |

### WebAssembly, Wasmer with Cranelift

| MiB/s   | Code   |  64 B | 1 KiB | 8 KiB | 64 KiB | 1 MiB |
| ------- | ------ | ----: | ----: | ----: | -----: | ----: |
| Hash    | Zig    |   246 |   760 |  1185 |   1358 |  1404 |
|         | C      |   207 |   648 |  1118 |   1377 |  1465 |
|         | Rust   |   266 |   711 |  1022 |   1348 |  1416 |
|         | XKCP   |   159 |   492 |   694 |    760 |   763 |
|         | BLAKE3 |   683 |   781 |  1715 |   1748 |  1748 |
| Absorb  | Zig    |   276 |   789 |  1186 |   1359 |  1406 |
|         | C      |   223 |   659 |  1121 |   1377 |  1464 |
|         | Rust   |   270 |   709 |  1029 |   1347 |  1415 |
|         | XKCP   |   154 |   492 |   694 |    760 |   763 |
|         | BLAKE3 |   666 |   789 |  1713 |   1749 |  1746 |
| Squeeze | Zig    |   288 |  1211 |  1438 |   1578 |  1593 |
|         | C      |   227 |  1027 |  1341 |   1425 |  1434 |
|         | Rust   |   264 |  1013 |  1360 |   1450 |  1448 |
|         | XKCP   |   161 |   337 |   355 |    359 |   359 |
|         | BLAKE3 |   596 |   722 |   730 |    732 |   731 |
| Deck-BO | Zig    |   133 |   463 |   641 |    726 |   744 |
|         | C      |   123 |   400 |   603 |    695 |   720 |
|         | Rust   |   138 |   403 |   572 |    693 |   714 |
|         | XKCP   |    83 |   205 |   249 |    264 |   262 |

### WebAssembly, Wasmer with LLVM

| MiB/s   | Code   |  64 B | 1 KiB | 8 KiB | 64 KiB | 1 MiB |
| ------- | ------ | ----: | ----: | ----: | -----: | ----: |
| Hash    | Zig    |   328 |   946 |   917 |    932 |   925 |
|         | C      |   359 |  1006 |   947 |    942 |   934 |
|         | Rust   |   316 |   826 |   733 |    964 |   971 |
|         | XKCP   |   288 |   834 |  1045 |   1085 |  1085 |
|         | BLAKE3 |   663 |   909 |  2290 |   2345 |  2353 |
| Absorb  | Zig    |   325 |   946 |   917 |    932 |   924 |
|         | C      |   326 |   988 |   945 |    942 |   933 |
|         | Rust   |   324 |   825 |   735 |    964 |   972 |
|         | XKCP   |   287 |   831 |  1044 |   1085 |  1084 |
|         | BLAKE3 |   660 |   908 |  2288 |   2348 |  2352 |
| Squeeze | Zig    |   327 |   830 |   918 |    939 |   939 |
|         | C      |   330 |   769 |   859 |    871 |   871 |
|         | Rust   |   319 |   818 |   954 |    973 |   974 |
|         | XKCP   |   289 |   701 |   761 |    773 |   772 |
|         | BLAKE3 |   672 |  1058 |  1094 |   1099 |  1097 |
| Deck-BO | Zig    |   163 |   433 |   455 |    466 |   465 |
|         | C      |   177 |   447 |   446 |    453 |   450 |
|         | Rust   |   168 |   408 |   414 |    484 |   487 |
|         | XKCP   |   137 |   371 |   444 |    455 |   454 |

## References

FlightDeck comes from ["Parallelizable modes for duplex-based authenticated encryption"](https://eprint.iacr.org/2026/2801) by Joan Daemen, Silvia Mella and Gilles Van Assche.

The overwrite duplex and Deck-BO come from ["Shaking up authenticated encryption"](https://eprint.iacr.org/2024/1618) by Joan Daemen, Seth Hoffert, Silvia Mella, Gilles Van Assche and Ronny Van Keer.
