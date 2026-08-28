---
title: babel
description: A library for building language servers in Zig
license: MIT
author: MKindberg
author_github: MKindberg
repository: https://github.com/MKindberg/babel
keywords:
date: 2026-08-19
updated_at: 2026-08-19T20:48:48+00:00
last_sync: 2026-08-19T20:48:48Z
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
permalink: /packages/MKindberg/babel/
---

# babel
A framework for writing, or at least prototyping, language servers in Zig.
It allows you to register callbacks that will be called when notifications or
requests are received. In addition to this it will also keep track of and automatically
update the documents being edited.

## Usage

### Creating the server
```zig
const std = @import("std");
const lsp = @import("lsp");

// Set the global log function to lsp.log in order to use the lsp protocol
// for logging
pub const std_options = std.Options{ .log_level = .info, .logFn = lsp.log };

// File specific state
const State = struct {
    fn init() State {
        return .{};
    }
    fn deinit(self: State) void {
        _ = self;
    }
};
// Create an alias for the server type. An instance of State will be available
// in each callback.
const Lsp = lsp.Lsp(.{ .state_type = State });

pub fn main(init: std.process.Init) !u8 {
    // Information about the server that will be passed to the client.
    const server_info = lsp.types.ServerInfo{ .name = "server_name", .version = "0.1.0" };

    var in_buffer: [1024]u8 = undefined;
    var out_buffer: [1024]u8 = undefined;
    var stdin = std.Io.File.stdin().reader(std.Options.debug_io, &in_buffer);
    var stdout = std.Io.File.stdout().writer(std.Options.debug_io, &out_buffer);

    var server = Lsp.init(init.gpa, init.io, &stdin.interface, &stdout.interface, server_info);
    defer server.deinit();

    // Start the server, it will run until it gets a shutdown signal from the
    // client. Callbacks need to be registered before the server starts, so
    // that's done in the setup function which is called once the client's
    // `initialize` request has been received.
    return try server.start(setup);
}

fn setup(p: Lsp.SetupParameters) void {
    p.server.registerCallback(.{ .@"textDocument/didOpen" = handleOpenDoc });
    p.server.registerCallback(.{ .@"textDocument/didClose" = handleCloseDoc });
    p.server.registerCallback(.{ .@"textDocument/didChange" = handleChangeDoc });
    p.server.registerCallback(.{ .@"textDocument/hover" = handleHover });
}

// All callbacks take one parameter which is a struct containing an arena
// allocator that's freed when the callback returns, the current document
// and state, and any additional data that might be useful.
// The return values are just aliases for regular types and it doesn't matter
// if the alias or real type is used.
fn handleOpenDoc(p: Lsp.OpenDocumentParameters) Lsp.OpenDocumentReturn {
    std.log.info("Opened {s}", .{p.context.document.uri});
    // The file local state should be initialized when a document is opened.
    p.context.state = State.init();
}

// Most resources related to the document will be freed automatically, but the
// user provided state needs to be handled manually.
fn handleCloseDoc(p: Lsp.CloseDocumentParameters) Lsp.CloseDocumentReturn {
    // Deinitialize the state when the file is closed.
    p.context.state.?.deinit();
}

// An example of additional data that can be included in the parameters struct
// is the changes that triggered a changeDocument event.
fn handleChangeDoc(p: Lsp.ChangeDocumentParameters) Lsp.ChangeDocumentReturn {
    for (p.params.contentChanges) |change| {
        std.log.info("New text: {s}", .{change.text});
    }
}

// Callbacks handling requests will have a non-void return value that will
// be sent back to the client after the callback returns.
fn handleHover(p: Lsp.HoverParameters) Lsp.HoverReturn {
    // A document provides some helper function that can be useful.
    const word = p.context.document.getWord(p.params.position, "\n .,") orelse return null;
    std.log.info("Hovering the word {s} at {d}:{d}", .{ word, p.params.position.line, p.params.position.character });
    return .{ .contents = word };
}
```

### Build the server
```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Build the server
    const exe = b.addExecutable(.{
        .name = "server_name",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });

    // Add the dependency towards babel
    const babel = b.dependency("babel", .{ .target = target, .optimize = optimize });

    // Allow the server to import the lsp module from babel
    const lsp = babel.module("lsp");
    exe.root_module.addImport("lsp", lsp);

    b.installArtifact(exe);
}
```
