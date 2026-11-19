---
title: premiumize.zig
description: A library around the premiumize.me API
license: ""
author: chip-davis
author_github: chip-davis
repository: https://github.com/chip-davis/premiumize.zig
keywords:
date: 2026-11-13
updated_at: 2026-11-13T20:36:17+00:00
last_sync: 2026-11-13T20:36:17Z
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
permalink: /packages/chip-davis/premiumize.zig/
---

# premiumize.zig

A Zig client for the [premiumize.me](https://www.premiumize.me) REST API.

It covers the whole public API (account, folders, items, transfers, cache, services, zip) plus a few helpers for things like waiting for a transfer to finish and getting every file it produced with a download link.

No dependencies. HTTP goes through `std.http.Client`.

Requires Zig 0.17.1.

## Install

```sh
zig fetch --save git+https://github.com/<you>/premiumize.zig
```

Then in `build.zig`:

```zig
const premiumize = b.dependency("premiumize_zig", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("premiumize", premiumize.module("premiumize_zig"));
```

## Quick start

```zig
const std = @import("std");
const premiumize = @import("premiumize");
const Client = premiumize.Client;

pub fn main(init: std.process.Init) !void {
    const api_key = init.environ_map.get("PREMIUMIZE_API_KEY") orelse return error.NoApiKey;

    var pm = Client.init(init.gpa, init.io, .{ .auth = .{ .api_key = api_key } });
    defer pm.deinit();

    const info = try pm.account().info(.{});
    defer info.deinit();

    std.debug.print("customer {s}, {d:.1}% of fair use\n", .{
        info.value.customer_id,
        info.value.limit_used * 100,
    });
}
```

Your API key is on the [account page](https://www.premiumize.me/account). If you have an OAuth token instead, use `.auth = .{ .access_token = token }` and it's sent as a bearer header.

## How calls work

Endpoints are grouped the same way the API groups them, and every call takes an options struct:

```zig
pm.folder().list(.{ .id = folder_id });
pm.transfer().create(.{ .src = magnet, .folder_id = folder_id });
pm.item().details(.{ .id = file_id });
pm.services().list(.{});
```

Calls that return data give you a `std.json.Parsed(T)`. The response is yours until you call `deinit()`, and every string in it lives in that arena. If you need an ID after `deinit`, copy it first:

```zig
const res = try pm.folder().create(.{ .name = "downloads" });
defer res.deinit();
const id = try allocator.dupe(u8, res.value.id);
```

Calls that only return `{"status":"success"}` (rename, delete, paste, retry, ...) return `!void`.

Unknown JSON fields are ignored.

## Errors

Everything goes through `Client.Error`:

| Error | Meaning |
| --- | --- |
| `ApiError` | The API answered with `"status":"error"` |
| `BadStatus` | Non-2xx response that wasn't JSON (usually a 500) |
| `InvalidResponse` | JSON didn't match the expected type |
| `InvalidArgument` | Caught before sending, e.g. an empty `items` list |
| `Timeout`, `TransferNotFound`, `TransferNotFinished` | From the transfer helpers |

For details, pass a `Diagnostics`. It's reset at the start of the call and only filled on failure:

```zig
var d: Client.Diagnostics = .{};
const res = pm.item().details(.{ .id = id, .diag = &d }) catch |err| {
    std.debug.print("{t}: {s} ({?t})\n", .{ err, d.message() orelse "", d.code });
    return err;
};
defer res.deinit();
```

`d.code` is the API's `code` field as an `ErrorCode` enum. `d.code.?.retry()` gives you the category from the API docs (`transient`, `semi_permanent`, `permanent`, `unknown`). 

The client itself holds no per-call state, so give each thread its own `Diagnostics`.

When the response doesn't parse, the message says where:

```
UnexpectedToken at byte 812: ...,"progress":null,"message":...
```

## Transfers

Create a transfer, wait for it, then list what it produced:

```zig
const created = try pm.transfer().create(.{ .src = magnet });
defer created.deinit();

const t = try pm.transfer().wait(.{ .id = created.value.id, .timeout_s = 600 });
defer t.deinit();

if (t.value.status == .@"error") {
    std.debug.print("transfer failed: {s}\n", .{t.value.message orelse ""});
    return;
}

const files = try pm.transfer().files(.{ .transfer = t.value });
defer files.deinit();

for (files.value) |f| {
    std.debug.print("{s}  {d} bytes  {s}\n", .{ f.path, f.size, f.link orelse "-" });
}
```

The API has no "get one transfer" endpoint, so `get` and `wait` read `/transfer/list` and pick yours out of it.

`wait` polls every `interval_s` (default 3) until the transfer is `finished`, `seeding` or `error`, or `timeout_s` runs out. A failed transfer comes back as a value, not an error, so you can read its `message`. Rate limits and other retryable API errors don't end the wait; it sleeps and tries again. An ID that doesn't show up in the list gets a couple of polls of grace (`not_found_grace`) before `TransferNotFound`.

`files` uses `file_id` if the transfer has one (single file) and walks `folder_id` otherwise. It's checked in that order because a single-file transfer's `folder_id` can be the folder it was saved into, not a folder of its own.

If you're polling from a UI loop, skip `wait` and call `list` on your own timer instead.

## Downloading a folder

`folder().walk()` returns every file under a folder, recursively, with paths relative to it:

```zig
const files = try pm.folder().walk(.{ .id = folder_id });
defer files.deinit();

for (files.value) |f| {
    // f.path:  "Season 1/ep01.mkv"
    // f.name:  "ep01.mkv"
    // f.link:  direct download URL
    _ = f;
}
```

It makes one `/folder/list` request per folder and returns files only, sorted by path. Leave out `id` to walk from the root, but for the whole account `item().listAll()` is a single request. It doesn't include download links, though.

The library doesn't download files for you. `link` is a plain HTTPS URL, so stream it with `std.http.Client` or whatever you like.

## Cached content

Check the cache before adding something. If it's cached, `directDl` gives you links straight away without storing anything in your cloud:

```zig
const check = try pm.cache().check(.{ .items = &.{magnet} });
defer check.deinit();

if (check.value.response[0]) {
    const dl = try pm.transfer().directDl(.{ .src = magnet });
    defer dl.deinit();
    for (dl.value.content) |f| std.debug.print("{s}  {s}\n", .{ f.path, f.link });
}
```

`cache().check` takes a list. The response is three parallel arrays (`response`, `filename`, `filesize`) in the same order as your input.

## Endpoints

| Namespace | Calls |
| --- | --- |
| `account()` | `info` |
| `folder()` | `list`, `create`, `rename`, `delete`, `paste`, `uploadInfo`, `search`, `walk`* |
| `item()` | `details`, `rename`, `delete`, `listAll` |
| `transfer()` | `create`, `directDl`, `list`, `retry`, `delete`, `clearFinished`, `get`*, `wait`*, `files`* |
| `cache()` | `check` |
| `services()` | `list` |
| `zip()` | `generate` |

\* Helpers built on top of the API, not endpoints of their own.

`clearFinished` removes **all** finished transfers on the account, not just ones you created.

Response types are in `premiumize.types`.

## Development

```sh
zig build test --summary all
```

The tests run against a small local HTTP server (`src/testing.zig`) that answers with canned JSON and records each request, so they check both the request sent and how the response is parsed. Nothing touches the real API.

There's also an end-to-end run against your real account:

```sh
PREMIUMIZE_API_KEY=... zig build run
```

It calls every endpoint, but works inside a scratch folder (`pmzig-e2e-<timestamp>`) and deletes it at the end. The test transfer is the Big Buck Bunny magnet. Set `PREMIUMIZE_TEST_SRC` to use something else. `clearFinished` only runs if you pass `-- --clear-finished`, for the reason above.

## Not done yet

- No request timeout.
- No upload helper. `folder().uploadInfo()` gives you the URL and token, and the upload itself is up to you.
- No OAuth flow. Bring your own token.
