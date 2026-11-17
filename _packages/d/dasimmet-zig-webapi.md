---
title: zig-webapi
description: ""
license: MIT
author: dasimmet
author_github: dasimmet
repository: https://github.com/dasimmet/zig-webapi
keywords:
date: 2026-11-16
updated_at: 2026-11-16T08:12:12+00:00
last_sync: 2026-11-16T08:12:12Z
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
permalink: /packages/dasimmet/zig-webapi/
---

# webapi

Type-safe Zig WebAssembly browser and WASI API wrappers around [`zig-javascript-bridge`](https://github.com/scottredig/zig-javascript-bridge) (`zjb`).

- **Landing Page**: <https://dasimmet.github.io/zig-webapi/>
- **API Documentation**: <https://dasimmet.github.io/zig-webapi/docs/>
- **Live Example**: <https://dasimmet.github.io/zig-webapi/example/>

`webapi` lets Zig WebAssembly applications interact with DOM APIs, events, WebGL, Fetch, Promises, IndexedDB, WebRTC, WebSockets, BroadcastChannel, WebAssembly/JSPI, and a pure-Zig WASI Snapshot Preview 1 runtime without writing custom JavaScript glue or relying on global callback singletons.

## Requirements

- **Zig**: `0.17.1` (see `minimum_zig_version` in [`build.zig.zon`](build.zig.zon))
- **Targets**: `wasm32-freestanding` or `wasm64-freestanding` in the browser; host target (`b.graph.host`) for unit tests via the built-in in-memory `zjb` mock.

## Modules

All modules are re-exported from [`src/webapi.zig`](src/webapi.zig):

| Module / Symbol | Purpose |
| --- | --- |
| [`webapi`](src/webapi.zig) (root) | Zero-allocation string extraction (`stringFromHandle`, `stringFromHandles`), allocating helpers (`stringFromHandleAlloc`, `bytesFromHandleAlloc`, `createStandaloneUint8Array`), context-bound callbacks (`boundFunction`, `boundEventListener`, `boundEventListenerTyped`), Web Crypto PRNG (`PseudoRandomNumberGenerator`), `constTagName`, `getUri`, `retainHandle`, `hasProperty`, `callAsync`. |
| [`webapi.zjb`](src/webapi.zig) | Resolves to `@import("zjb")` on WASM targets and [`src/testing/zjb.zig`](src/testing/zjb.zig) on host targets. |
| [`webapi.codec`](src/codec.zig) | Cached singleton JS `TextEncoder` / `TextDecoder` helpers (`encode`, `decode`). |
| [`webapi.CompressionStream`](src/CompressionStream.zig) | Compression Streams API `CompressionStream` (`gzip`, `deflate`, `deflate-raw`). |
| [`webapi.console`](src/console.zig) | Browser console logging (`log`, `debug`, `@"error"`) and `rootLogFn` for `std.Options.logFn`. |
| [`webapi.Crypto`](src/Crypto.zig) / [`webapi.crypto`](src/Crypto.zig) | Web Crypto API (`window.crypto`, `getRandomValues`, `randomUUID`, `SubtleCrypto`, `CryptoKey`). |
| [`webapi.DecompressionStream`](src/DecompressionStream.zig) | Compression Streams API `DecompressionStream`, `ReadableStream`, `WritableStream`, and `WritableStreamDefaultWriter`. |
| [`webapi.dom`](src/dom.zig) | Typed DOM wrappers: `Document`, `Window`, `Element`, `CSSStyleDeclaration`, `TokenList`, `DOMRect`, `Location`, `History`, `Navigator`, `Clipboard`, `Performance`, `MediaQueryList`, `VisualViewport`, `DataTransfer`, `HTMLIFrameElement`, `ServiceWorker`, `ServiceWorkerContainer`, `ServiceWorkerRegistration`. |
| [`webapi.Event`](src/Event.zig) | Base `Event` wrapper and compile-time `EventFor(name)` mapping to `KeyboardEvent`, `PointerEvent`, `MouseEvent`, `WheelEvent`, `InputEvent`, `ClipboardEvent`, `FocusEvent`, `SubmitEvent`, `TouchEvent`, `HashChangeEvent`, `PopStateEvent`, `MediaQueryListEvent`, and `BeforeInstallPromptEvent`. |
| [`webapi.Promise`](src/Promise.zig) | `Promise` and `Promise.Typed(T)` wrappers with context-bound `.thenFn(...)`. |
| [`webapi.Fetch`](src/Fetch.zig) / [`webapi.fetch`](src/Fetch.zig) | Browser Fetch API: `fetch`, `Headers`, `RequestInit`, and `Response`. |
| [`webapi.download`](src/download.zig) | Trigger browser file downloads from raw byte slices (`download.bytes`). |
| [`webapi.WebGL`](src/WebGL.zig) | WebGL2 / WebGL rendering context, buffers, textures, shaders/programs (`createProgramFromSource`), uniforms (`uploadMat4`, etc.), framebuffers, VAOs, and draw calls. |
| [`webapi.IndexedDb`](src/IndexedDb.zig) | Context-bound async `IndexedDB` wrapper (`open`, `Database`, `Transaction`, `ObjectStore`, `loadAllEntries`) using detached `Uint8Array` copies safe across WASM memory growth. |
| [`webapi.WebRTC`](src/WebRTC.zig) | `RTCPeerConnection`, `RTCDataChannel`, `RTCSessionDescription`, `RTCIceCandidate`, `RTCConfiguration`, and `RTCIceServer`. |
| [`webapi.WebSocket`](src/WebSocket.zig) | `WebSocket` wrapper with `ReadyState` and typed listener attachment. |
| [`webapi.BroadcastChannel`](src/BroadcastChannel.zig) | Cross-tab / worker `BroadcastChannel` wrapper. |
| [`webapi.Worker`](src/Worker.zig) | Web Workers API: `Worker`, `SharedWorker`, `MessagePort`, `MessageChannel`, `DedicatedWorkerGlobalScope`, `SharedWorkerGlobalScope`, `WorkerNavigator`, `WorkerLocation`. |
| [`webapi.WebAssembly`](src/WebAssembly.zig) | `Module`, `Instance`, `Memory`, `validate`, `compile`, `instantiate`, `instantiateAsync`, and JSPI (`Suspending`, `isJspiSupported`, `promising`). |
| [`webapi.Wasi`](src/Wasi.zig) | Pure-Zig WASI Snapshot Preview 1 runtime for running WASM binaries in the browser with in-memory, `.tar`, and `IndexedDb`-backed filesystems ([`src/Wasi/FileSystem.zig`](src/Wasi/FileSystem.zig)). |
| [`webapi.testing`](src/testing.zig) | Host-side unit tests and handle-leak checks powered by [`src/testing/zjb.zig`](src/testing/zjb.zig). |

## Quick Start

### 1. Add `webapi` to `build.zig.zon`

Fetch `webapi` with `zig fetch`:

```bash
zig fetch --save=webapi git+https://github.com/dasimmet/zig-webapi
```

Or add it directly to `build.zig.zon` (for local checkouts, use `.path = "../zig-webapi"` instead of `.url`/`.hash`):

```zig
.{
    .name = .my_wasm_app,
    .version = "0.0.1",
    .minimum_zig_version = "0.17.1",
    .fingerprint = 0x...,
    .dependencies = .{
        .webapi = .{
            .url = "git+https://github.com/dasimmet/zig-webapi#f9fd8468a3031a25985eefdf10b9f922e8138835",
            .hash = "webapi-0.0.1-fgeJxBcHBwBJNu2Zqi32OMNc8lfee1cW0wNFgs1PoOFx",
        },
    },
    .paths = .{ "build.zig", "build.zig.zon", "src", "static" },
}
```

### 2. Configure `build.zig`

`webapi` exports both the `"webapi"` Zig module (with `"zjb"` already wired in) and a `bindgen` helper that generates the matching JavaScript `Zjb` class from your compiled `.wasm` binary:

```zig
const std = @import("std");
const webapi_pkg = @import("webapi");

pub fn build(b: *std.Build) void {
    const optimize = b.standardOptimizeOption(.{});
    const wasm_target = b.standardTargetOptions(.{
        .default_target = .{
            .cpu_arch = .wasm32,
            .os_tag = .freestanding,
        },
    });

    const webapi_mod = b.dependency("webapi", .{}).module("webapi");

    const exe = b.addExecutable(.{
        .name = "app",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = wasm_target,
            .optimize = optimize,
            .strip = false,
            .imports = &.{
                .{ .name = "webapi", .module = webapi_mod },
            },
        }),
    });
    exe.rdynamic = true;

    const zjb_bindings = webapi_pkg.bindgen(b, .{
        .wasm = exe.getEmittedBin(),
        .basename = "zjb_bindings.js",
        .classname = "Zjb",
        .module_style = .es6,
        .minify = optimize != .debug,
    });

    b.default_step.dependOn(&b.addInstallFile(exe.getEmittedBin(), "www/app.wasm").step);
    b.default_step.dependOn(&b.addInstallFile(zjb_bindings, "www/zjb_bindings.js").step);
}
```

### 3. Write Zig Application Code

```zig
const std = @import("std");
const webapi = @import("webapi");

const dom = webapi.dom;
const Event = webapi.Event;
const zjb = webapi.zjb;

pub const std_options: std.Options = .{
    .logFn = webapi.console.rootLogFn,
    .log_level = .debug,
};

pub const panic = zjb.panic;

const App = struct {
    clicks: u32 = 0,

    fn onClick(self: *App, ev: Event.PointerEvent) void {
        _ = ev;
        self.clicks += 1;
        var buf: [64]u8 = undefined;
        const msg = std.fmt.bufPrint(&buf, "Clicked {d} times", .{self.clicks}) catch return;
        dom.document().setElemText("status", msg);
    }
};

pub fn main(init: std.process.Init.Minimal) !void {
    _ = init;
    const app = try std.heap.wasm_allocator.create(App);
    app.* = .{};

    if (dom.document().getElementById("my-btn")) |btn| {
        defer btn.release();
        btn.addEventListener("click", App, app, App.onClick);
    }

    std.log.info("App ready", .{});
}
```

### 4. Bootstrap in JavaScript

```javascript
import { Zjb } from "./zjb_bindings.js";

const zjb = new Zjb();
const { instance } = await WebAssembly.instantiateStreaming(fetch("app.wasm"), {
  env: {
    memory: new WebAssembly.Memory({ initial: 16 }),
    __stack_pointer: 0,
  },
  zjb: zjb.imports,
});

zjb.setInstance(instance);
instance.exports._start();
```

## Handle Ownership Rules

`zjb.Handle` values reference JavaScript objects stored in `Zjb._handles`:

- **Release owned handles**: Any wrapper or `zjb.Handle` returned by constructors or getters (`getElementById`, `getUniformLocation`, `createBuffer`, `fetch`, `response.text()`, `event.target()`, etc.) must be released with `.release()` when no longer needed.
- **Callback & listener views**: Handles passed into `boundFunction`, `addEventListener`, and `Promise.thenFn` callbacks are non-owning views and are automatically released when the callback returns. Use `boundFunctionOwned` / `addEventListenerOwned` / `boundEventListenerTypedOwned` if you need to keep the handle past callback return.
- **Global singletons**: `dom.document()` and `dom.window()` wrap `zjb.ConstHandle` values and do not need to be released.

## Running Unit Tests, Formatting & Docs

Host-side unit tests use the in-memory mock in [`src/testing/zjb.zig`](src/testing/zjb.zig) to verify wrapper behavior and detect handle leaks or double-frees without a browser:

```bash
# Run unit tests
zig build test

# Check Zig source formatting (omit -Dfmtcheck=true to format in place)
zig build fmt -Dfmtcheck=true

# Emit API documentation (zig-out/www/docs/), landing page (zig-out/www/), and example (zig-out/www/example/)
zig build docs
```

On pushes to `main`, [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs formatting checks, unit tests, and `zig build docs`, and deploys `zig-out/www` to [GitHub Pages](https://dasimmet.github.io/zig-webapi/).

## Example Project

A complete interactive browser example lives in [`example/`](example/):

- [`example/build.zig`](example/build.zig) & [`example/build.zig.zon`](example/build.zig.zon) — standalone package configuration consuming `webapi` via `.path = ".."`.
- [`example/src/main.zig`](example/src/main.zig) — demonstrates `console.rootLogFn`, `PseudoRandomNumberGenerator`, `WebGL`, `requestAnimationFrame` with `boundFunction`, typed `PointerEvent` / `InputEvent` / `KeyboardEvent` listeners, `fetch` + `Promise.Typed(Response)`, `Location.getHref`, and `download.bytes`.
- [`example/static/`](example/static/) — HTML, CSS, ES6 module bootstrap, and `data.json`.

Build and serve it locally:

```bash
cd example
zig build serve
```

Then open <http://127.0.0.1:8080> in a WebGL-capable browser. To build `example/zig-out/www/` without starting the HTTP server, run `zig build` inside `example/`.
