---
title: md4z
description: Zig bindings of md4c markdown parser
license: GPL-3.0
author: a-marigold
author_github: a-marigold
repository: https://github.com/a-marigold/md4z
keywords:
  - markdown
  - markdown-parser
  - md4c
date: 2026-11-20
updated_at: 2026-11-20T19:12:49+00:00
last_sync: 2026-11-20T19:12:49Z
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
permalink: /packages/a-marigold/md4z/
---

### About

Zig bindings of [md4c](https://github.com/mity/md4c) Markdown parser.

- Zig version - 0.17.1
- `md4c` version - 0.6.0
- `md4c-html` isn't supported

### Usage

The only APIs of this library:
1. `Parser(comptime Visitor: type)`.
2. `Parser(Visitor).init(visitor: Visitor, flags: u32)`.
3. `Parser(Visitor).parse(input: []const u8)`.

#### Flags (`FLAG_*`)

Flags specify features and extensions of Markdown to support.

`DIALECT_COMMONMARK` and `DIALECT_GITHUB` can also be used as flags,
because they're compounds of features of `FLAG_*` declarations.

#### Visitor

`Visitor` is a namespace (struct, enum, etc).

`Visitor` can have any fields, any public variable or fn declarations,
but it must have at least the 5 callbacks as `pub fn`.

Parameters of callbacks: 
- A mutable pointer to the visitor.
- `enterBlock`, `leaveBlock`, `enterSpan` and `leaveSpan` also receive:
  1. `block_type` or `span_type`, which is an enum.
  2. `*const Block` or `*const Span`, which a pointer to bare union, 
     active field of which corresponds to the active field of the `_type` enum
- `text` also receives:
  1. `text_type`, which is an enum.
  2. `data`, which is a **non**-null-terminated slice of the text.

Callbacks can return errors. 
If a callback returns an error, `parse` stops and returns that error.

There are 5 callbacks in `md4c` library:
```zig
// Can be any namespace (struct, enum, union, opaque)
const Visitor = struct {
    user_field: SomeType,
    user_field1: SomeType1,

    // Callbacks can or can not return errors

    // It's guaranteed that `leaveBlock` is called
    // for every span that appears in `enterBlock`
    // (if there are no errors)
    pub fn enterBlock(self: *@This(), block_type: BlockType, block: *const Block) SomeError!void {}
    pub fn leaveBlock(self: *@This(), block_type: BlockType, block: *const Block) !void {}

    // It's guaranteed that `leaveSpan` is called
    // for every span that appears in `enterSpan`
    // (if there are no errors)
    pub fn enterSpan(self: *@This(), span_type: SpanType, block: *const Span) void {}
    pub fn leaveSpan(self: *@This(), span_type: SpanType, block: *const Span) void {}

    // Isn't called for the whole content of a block or span at once.
    // Instead, textual contents of blocks and spans can be
    // sliced into parts so `text` is called multiple times for it
    pub fn text(self: *@This(), text_type: TextType, data: []const u8) void {}
};

const parser: Parser(Visitor) = .init(.{ .user_field = ... }, flags);

// May return an error from a callback,
// which stops the parsing completely
try parser.parse("# *Hello*");
```
