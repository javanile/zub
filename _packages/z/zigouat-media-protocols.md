---
title: media-protocols
description: Media protocols implementation in zig
license: MIT
author: zigouat
author_github: zigouat
repository: https://github.com/zigouat/media-protocols
keywords:
  - ice
  - rfc8445
  - rfc8489
  - rtcp
  - rtp
  - rtsp
  - sdp
  - srtp
  - stun
date: 2026-07-16
updated_at: 2026-07-16T15:53:35+00:00
last_sync: 2026-07-16T15:53:35Z
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
permalink: /packages/zigouat/media-protocols/
---

# Media Protocols

Zig implementations of various protocols related to media processing and streaming.

The projects is structured into modules, each module is a separate library that can be used independently. The modules are:

* `rtp/rtcp` - implementation of the real-time transport protocol (RTP) and real-time transport control protocol (RTCP).
    
    The following RFCs are also implemented as part of the `rtp/rtcp` module:
    * [RFC 3550](https://datatracker.ietf.org/doc/html/rfc3550) - RTP: A Transport Protocol for Real-Time Applications.
    * [RFC 4585](https://datatracker.ietf.org/doc/html/rfc4585) - Extended RTP Profile for Real-time Transport Control Protocol (RTCP)-Based Feedback (RTP/AVPF).
    * [RFC 8285](https://datatracker.ietf.org/doc/html/rfc8285) - A General Mechanism for RTP Header Extensions.

* `srtp` - [SRTP (Secure Real-time Transport Protocol)](https://datatracker.ietf.org/doc/html/rfc3711) implementation of the secure real-time transport protocol based on RFC 3711.
* `sdp` - [SDP (Session Description Protocol)](https://datatracker.ietf.org/doc/html/rfc4566) implementation for describing multimedia sessions based on RFC 4566.
* `rtsp` - [RTSP (Real Time Streaming Protocol)](https://datatracker.ietf.org/doc/html/rfc2326) implementation for controlling streaming media servers based on RFC 2326.
* `stun` - [STUN (Session Traversal Utilities for NAT)](https://datatracker.ietf.org/doc/html/rfc8489) implementation for NAT traversal based on RFC 8489.
* `ice` - [ICE (Interactive Connectivity Establishment)](https://datatracker.ietf.org/doc/html/rfc8445) implementation of the interactive connectivity establishment (ICE) protocol for Network Address Translator (NAT) Traversal.

## Status

This repo is under active development, and the implementations are not yet complete. Breaking changes may occur frequently.

## Installation
Add `media_protocols` as a dependency in your `build.zig.zon` file:

```bash
zig fetch --save git+https://github.com/zigouat/media-protocols.git#v0.1.0
```

Then, in your `build.zig` file, add the following:

```zig
const media_protocols = b.dependecy("media_protocols", .{ .target = .target, .optimize = optimize });

/// You can all the whole module:
exe.root_module.addImportPath("media_protocols", media_protocols.module("protocols"));

/// Or you can import only the modules you need:
exe.root_module.addImportPath("rtp", media_protocols.module("rtp"));
exe.root_module.addImportPath("ice", media_protocols.module("ice"));
```
