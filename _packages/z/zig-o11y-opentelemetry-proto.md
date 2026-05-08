---
title: opentelemetry-proto
description: "Zig type definitions generated from https://github.com/open-telemetry/opentelemetry-proto"
license: MIT
author: zig-o11y
author_github: zig-o11y
repository: https://github.com/zig-o11y/opentelemetry-proto
keywords:
  - opentelemetry
  - protobuf
date: 2026-04-18
category: data-formats
updated_at: 2026-04-18T12:48:20+00:00
last_sync: 2026-04-18T12:48:20Z
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
permalink: /packages/zig-o11y/opentelemetry-proto/
---

## OpenTelemetry Protobuf Zig

[OpenTelemetry Protobuf definitions](https://github.com/open-telemetry/opentelemetry-proto) packaged for Zig.

---

This repository checks out the official OpenTelemetry Protobuf definitions in a submodule and contains a Zig build to expose the generated Zig code as a package.

### Import the package

The following command will checkout the latest avaiable commit on `main`, which _should_ also be the latest tagged version.

```bash
zig fetch --save "git+https://github.com/zig-o11y/opentelemetry-proto"
```

To specify a tag, add the ref (e.g. `v1.6.0` tag).

```bash
zig fetch --save "git+https://github.com/zig-o11y/opentelemetry-proto#v1.6.0"
```

Tags in this repository will mirror the tags in the OpenTelemetry official repository.

### Generate the code for a new release

When a new tag is added in the upstream repository, there is a build step we can use to update the generated code.
Pick a tag from the upstream repo, say <vX.Y.Z>, and run:

```zig
zig build update-tag -Dtag=<vX.Y.Z>
```

### Dependencies

The marvellous [`zig-protobuf`](https://github.com/Arwalk/zig-protobuf/) library from @Arwalk.
