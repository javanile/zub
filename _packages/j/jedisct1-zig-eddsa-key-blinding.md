---
title: zig-eddsa-key-blinding
description: A Zig implementation of EdDSA signatures with blind keys.
license: MIT
author: jedisct1
author_github: jedisct1
repository: https://github.com/jedisct1/zig-eddsa-key-blinding
keywords:
  - blinding
  - ed25519
  - eddsa
date: 2026-04-11
updated_at: 2026-04-11T12:39:08+00:00
last_sync: 2026-04-11T12:39:08Z
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
permalink: /packages/jedisct1/zig-eddsa-key-blinding/
---

# EdDSA signatures with blind keys

A Zig implementation of the [EdDSA key blinding](https://chris-wood.github.io/draft-wood-cfrg-eddsa-blinding/draft-wood-cfrg-eddsa-blinding.html) proposal.

```zig
    // Create a standard Ed25519 key pair
    const kp = try Ed25519.KeyPair.create(null);

    // Create a random blinding seed
    var blind: [32]u8 = undefined;
    crypto.random.bytes(&blind);

    // Blind the key pair
    const blind_kp = try BlindEd25519.blind(kp, blind);

    // Sign a message and check that it can be verified with the blind public key
    const msg = "test";
    const sig = try BlindEd25519.sign(msg, blind_kp, null);
    try Ed25519.verify(sig, msg, blind_kp.blind_public_key);

    // Unblind the public key
    const pk = try BlindEd25519.unblind_public_key(blind_kp.blind_public_key, blind);
    try std.testing.expectEqualSlices(u8, &pk, &kp.public_key);
```
