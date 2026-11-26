---
title: sigv4
description: "AWS Signature Version 4 request signing in Zig: the canonical request, the string to sign, and the HMAC-SHA256 signing key, with no I/O."
license: MIT
author: baskingspot
author_github: baskingspot
repository: https://github.com/baskingspot/sigv4
keywords:
date: 2026-11-26
updated_at: 2026-11-26T19:30:42+00:00
last_sync: 2026-11-26T19:30:42Z
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
permalink: /packages/baskingspot/sigv4/
---

<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/static/logo-dark.svg">
    <img src="docs/static/logo.svg" alt="sigv4" height="48">
  </picture>
</h1>

AWS Signature Version 4 request signing in Zig: the canonical request, the
string to sign, and the HMAC-SHA256 signing key, with no I/O.

Every request to an AWS API carries a signature over its method, path, headers,
and body hash. The algorithm is fixed and small. The failures are in the
strings: a header list that sorts case-folded and joins its duplicates, a query
that sorts by its encoded bytes, a path escaped a second time for every service
except S3, and a scope date that has to agree with the timestamp.

This package builds those strings and the chain. It writes the `Authorization`
field value, or a presigned query, into a buffer you own. There is no
allocator, no clock, no credentials store, and no HTTP client: the timestamp is
a string you supply.

```zig
const value = try sigv4.signing.writeAuthorization(&field, &creq, request, credentials);
```

The AWS signing test suite is vendored unmodified, and `just test` runs every
case through the same code: the canonical request, the string to sign, the
signature, and the field value, for both the header and the query form.

## What is in it

- [The request](https://baskingspot.dev/sigv4/#the-request): `canonical.Request` is the signature's view of a request, with a wire `path` and a `PathMode` of `.service`, `.unnormalized`, or `.s3`.
- [The canonical request](https://baskingspot.dev/sigv4/#the-canonical-request): `writeRequest` writes the six parts and sorts the caller's header and query slices in place; the parts are public on their own.
- [The string to sign](https://baskingspot.dev/sigv4/#the-string-to-sign): `Scope.init` takes the date from the timestamp so the two cannot disagree, and `writeStringToSign` covers the canonical request's hash.
- [The signing key](https://baskingspot.dev/sigv4/#the-signing-key): `signingKey` is the four-round HMAC chain, and it zeroes the intermediate keys before it returns.
- [The Authorization field](https://baskingspot.dev/sigv4/#the-authorization-field): `writeAuthorization` checks the timestamp, merges a session token, and refuses an S3 request it knows AWS will reject.
- [Presigning](https://baskingspot.dev/sigv4/#presigning): `presign` builds the `X-Amz-*` query and the signature for a URL that carries its own credentials.
- [Limits](https://baskingspot.dev/sigv4/#limits): no clock, no HTTP, no SigV4a, no streaming chunk signatures.

Not implemented:

- SigV4a: `sigv4.algorithm` is `AWS4-HMAC-SHA256`, and the `AWS4-ECDSA-P256-SHA256` chain needs a signing curve and a different key format.
- Streaming signatures: nothing writes `STREAMING-AWS4-HMAC-SHA256-PAYLOAD` or the chunk chain below it. A streaming hash arrives as a string in `Request.payload_hash`.
- A credentials store: no profile file, no IMDS, no STS call, and no refresh. `Credentials` holds strings.
- An HTTP client: no request type and no header parsing. A folded header line is the parser's job.

## Install

```sh
zig fetch --save https://baskingspot.dev/sigv4/v0.1.0.tar.gz
```

Add the module in `build.zig`:

```zig
const sigv4 = b.dependency("sigv4", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("sigv4", sigv4.module("sigv4"));
```

`sigv4` builds with Zig 0.17.

## Documentation

- The [guide](https://baskingspot.dev/sigv4/) covers the request, the canonical form, the key chain, the field, presigning, and the limits, with examples that compile.
- The [API reference](https://baskingspot.dev/sigv4/api/) documents every public symbol.
- [`docs/examples/`](docs/examples/) is the code the guide shows, compiled by `just test`.
- [`test/fixtures/`](test/fixtures/) is the vendored AWS signing test suite and the botocore-signed vectors; [`THIRD_PARTY.md`](THIRD_PARTY.md) records where they came from.
- [`AGENTS.md`](AGENTS.md) has the working notes for the repository.

## Work on it

```sh
just ci
```

`nix develop` provides the toolchain and the site tools. `just` lists the
recipes, and `just ci` runs what CI runs: the tests, lint, and the site build.
`just guide` serves the guide with live reload, and `just doc` builds the whole
site into `zig-out/site/sigv4/`.

## License

MIT. See [`LICENSE`](LICENSE). The AWS signing test suite in
`test/fixtures/aws-signing-suite/` is Apache-2.0, and its `LICENSE` and
`NOTICE` travel with it. See [`THIRD_PARTY.md`](THIRD_PARTY.md). The logo
files in `docs/static/` are baskingspot marks and are not covered by the
license; see [`docs/static/LICENSE`](docs/static/LICENSE).

## How it's made

Built with LLM assistance. [How, in detail](https://github.com/baskingspot/.github/blob/main/docs/AI.md).

<a href="https://github.com/baskingspot"><img src="https://raw.githubusercontent.com/baskingspot/.github/main/brand/assets/badge.svg" alt="baskingspot" height="24"></a>
