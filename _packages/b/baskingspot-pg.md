---
title: pg
description: "PostgreSQL wire protocol in Zig: frontend and backend message codecs, with no IO and no allocator."
license: MIT
author: baskingspot
author_github: baskingspot
repository: https://github.com/baskingspot/pg
keywords:
  - postgresql
  - wire-protocol
date: 2026-11-16
category: data-formats
updated_at: 2026-11-16T04:44:59+00:00
last_sync: 2026-11-16T04:44:59Z
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
permalink: /packages/baskingspot/pg/
---

<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/static/logo-dark.svg">
    <img src="docs/static/logo.svg" alt="pg" height="48">
  </picture>
</h1>

PostgreSQL wire protocol in Zig: frontend and backend message codecs, with no IO and no allocator.

Postgres defines 42 messages and four more that open a connection, and each one is a byte layout in the manual. This library is those layouts. It turns bytes into messages and messages into bytes, and it has no opinion about what a connection does next: a client, a server, or a proxy built on it owns the socket, the buffers, and the policy.

## What is in it

- [Reading a stream](https://baskingspot.dev/pg/#reading-a-stream): `frame.Decoder` finds boundaries without holding a body, so a `DataRow` larger than the read buffer costs nothing.
- [Decoding a message](https://baskingspot.dev/pg/#decoding-a-message): `backend.Message.decode` takes a tag and a body, and every slice it returns points into that body.
- [Writing a message](https://baskingspot.dev/pg/#writing-a-message): `frontend.Message.encode` writes the tag from the union arm and the length after the body.
- [Opening a connection](https://baskingspot.dev/pg/#opening-a-connection): the four messages before the protocol has tags, and `startup.peek` for the first eight bytes.
- [Error codes](https://baskingspot.dev/pg/#error-codes): `sqlstate.SqlState` holds every SQLSTATE code, and the code is the enum tag.
- [Limits](https://baskingspot.dev/pg/#limits): no connection, no SCRAM, and one builder that is missing.

Not implemented:

- A connection: the startup, authentication, and ready-for-query cycle is a state machine above this library.
- SCRAM-SHA-256 and MD5: the messages they ride on are here, and the algorithms are not, so nothing here completes a login against PostgreSQL 10 or later on its own.
- Backend builders beyond `ErrorResponse`, `DataRow`, and `RowDescription`: a server composing a `ParameterStatus` writes those bytes itself.

## Install

```sh
zig fetch --save https://baskingspot.dev/pg/v0.1.0.tar.gz
```

Add the module to your build:

```zig
const pg = b.dependency("pg", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("pg", pg.module("pg"));
```

`pg` builds with Zig 0.17.

## Documentation

- The [guide](https://baskingspot.dev/pg/) covers reading a stream, decoding and writing messages, opening a connection, and the SQLSTATE vocabulary.
- The [API reference](https://baskingspot.dev/pg/api/) documents every public symbol. Every declaration in `src/` carries the doc comment the API entry renders.
- [`AGENTS.md`](AGENTS.md) has the working notes for the repository.

## Work on it

```sh
just ci
```

`nix develop` provides the toolchain. `just` lists the recipes, and `just ci` runs the tests, the lint, a benchmark smoke run, and the site build. `just fuzz 10M` runs the fuzzer with an iteration budget, and `just bench` measures the decoders.

## License

MIT. See `LICENSE`. The logo files in `docs/static/` are baskingspot marks and are not covered by it. See `docs/static/LICENSE`.

## How it's made

Built with LLM assistance. [How, in detail](https://github.com/baskingspot/.github/blob/main/docs/AI.md).

<a href="https://github.com/baskingspot"><img src="https://raw.githubusercontent.com/baskingspot/.github/main/brand/assets/badge.svg" alt="baskingspot" height="24"></a>
