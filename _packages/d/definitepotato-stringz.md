---
title: stringz
description: A growable UTF-8 string library for Zig, in one file with no dependencies.
license: NOASSERTION
author: definitepotato
author_github: definitepotato
repository: https://github.com/definitepotato/stringz
keywords:
date: 2026-11-25
updated_at: 2026-11-25T16:26:22+00:00
last_sync: 2026-11-25T16:26:22Z
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
permalink: /packages/definitepotato/stringz/
---

# stringz

A growable UTF-8 string library for Zig, in one file with no dependencies.

- **Two flavors, following the standard library.** `String` is unmanaged, like `std.ArrayList`: you pass the allocator to the calls that need it. `Managed` stores the allocator for you.
- **Byte offsets by default.** `len()` is O(1) and every index is a byte offset. Operations that count characters say so in their name (`codepointCount`, `codepointAt`).
- **No hidden allocations.** Splitting, searching and trimming never allocate. If a method can allocate, it takes an allocator (or is on `Managed`) and returns an error union.
- **Works with plain slices too.** The non-allocating helpers are also free functions on `[]const u8`.

The API style is inspired by [JakubSzark/zig-string](https://github.com/JakubSzark/zig-string).

## Contents

- [Install](#install)
- [Quick start](#quick-start)
- [Guide](#guide)
  - [Three things to know first](#three-things-to-know-first)
  - [Creating a string](#creating-a-string)
  - [Reading the contents](#reading-the-contents)
  - [Building](#building)
  - [Removing and trimming](#removing-and-trimming)
  - [Replacing and transforming](#replacing-and-transforming)
  - [Searching and comparing](#searching-and-comparing)
  - [Splitting](#splitting)
  - [Characters (codepoints)](#characters-codepoints)
  - [Parsing](#parsing)
  - [Formatting and writers](#formatting-and-writers)
  - [Handing memory in and out](#handing-memory-in-and-out)
  - [Capacity](#capacity)
  - [Hash map keys](#hash-map-keys)
  - [Using Managed](#using-managed)
  - [Free functions on slices](#free-functions-on-slices)
- [What is not included](#what-is-not-included)
- [Tests](#tests)
- [License](#license)

## Install

Requires Zig 0.17.0 or newer.

Add the package to your project:

```sh
zig fetch --save git+https://github.com/definitepotato/stringz
```

Then expose it to your code in `build.zig`:

```zig
const stringz = b.dependency("stringz", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("stringz", stringz.module("stringz"));
```

Because the library is a single file, you can also copy `src/stringz.zig` into your project and `@import` it directly.

## Quick start

```zig
const std = @import("std");
const stringz = @import("stringz");
const String = stringz.String;

pub fn main(init: std.process.Init) !void {
    const allocator = init.gpa;

    // Unmanaged: you pass the allocator to anything that may allocate.
    var greeting: String = .empty;
    defer greeting.deinit(allocator);

    try greeting.append(allocator, "  hello, world  ");
    greeting.trim();
    greeting.toCapitalized();
    try greeting.print(allocator, " (take {d})", .{2});
    _ = try greeting.replace(allocator, "World", "Zig");

    std.debug.print("{s}\n", .{greeting.str()}); // Hello, Zig (take 2)
    std.debug.print("{d} bytes, starts with Hello: {}\n", .{
        greeting.len(),
        greeting.startsWith("Hello"),
    });

    // Managed: the string remembers the allocator for you.
    var csv: stringz.Managed = try .fromSlice(allocator, "name,age,city");
    defer csv.deinit();

    var columns = csv.split(",");
    while (columns.next()) |column| std.debug.print("column: {s}\n", .{column});
}
```

This exact program lives in `examples/quickstart.zig`. Run it with `zig build example`.

## Guide

The examples below use the unmanaged `String` and assume this at the top of the file:

```zig
const std = @import("std");
const stringz = @import("stringz");
const String = stringz.String;
const Managed = stringz.Managed;
```

`allocator` is any `std.mem.Allocator`. In tests, use `std.testing.allocator`, which reports leaks.

### Three things to know first

**1. There are two flavors with the same methods.**

```zig
// Unmanaged: no allocator stored, 24 bytes on a 64-bit target.
var a: String = .empty;
defer a.deinit(allocator);
try a.append(allocator, "hi");

// Managed: stores the allocator, so calls are shorter.
var b: Managed = .init(allocator);
defer b.deinit();
try b.append("hi");
```

Pick `String` when you hold many strings (in a struct, a list, a map) or already have an allocator at hand. Pick `Managed` when one string is passed around on its own. You can convert at any time:

```zig
var m = a.toManaged(allocator);   // `a` is now empty
var u = b.moveToUnmanaged();      // `b` is now empty
```

With `String`, always pass the same allocator to every call on the same string.

**2. Indexes are byte offsets.**

UTF-8 characters take one to four bytes, so the byte length and the character count differ:

```zig
var s: String = try .fromSlice(allocator, "aé🔥");
defer s.deinit(allocator);

s.len();              // 7  (bytes: 1 + 2 + 4), O(1)
s.codepointCount();   // 3  (characters), O(n)
s.codepointAt(1).?;   // "é"
s.byteOffset(2).?;    // 3  (the emoji starts at byte 3)
```

`find`, `insert`, `removeRange`, `substr` and friends all speak byte offsets. The offsets returned by `find` can be passed straight to the others. If you have a character index instead, convert it with `byteOffset`.

Passing an out-of-range offset is a bug in the caller, checked by an assertion in Debug and ReleaseSafe builds, the same as indexing a slice or a `std.ArrayList`.

**3. Returned slices are borrowed.**

Methods that return `[]const u8` (`str`, `cut`, `split`, `codepointAt`, ...) return views into the string's own memory. They stay valid until you next modify the string. Copy what you want to keep:

```zig
var s: String = try .fromSlice(allocator, "key=value");
defer s.deinit(allocator);

const key, const value = s.cut("=").?;   // both point into `s`

var kept: String = try .fromSlice(allocator, value);
defer kept.deinit(allocator);
try s.set(allocator, "something else");   // `key` and `value` are now invalid
```

For the same reason, do not pass a slice of a string to a method that modifies that same string.

### Creating a string

| Call                                     | Result                                                |
| ---------------------------------------- | ----------------------------------------------------- |
| `String.empty`                           | Empty string. No allocation.                          |
| `String.fromSlice(allocator, bytes)`     | Copy of `bytes`.                                      |
| `String.fromUtf8(allocator, bytes)`      | Copy of `bytes`, or `error.InvalidUtf8` if malformed. |
| `String.fromPrint(allocator, fmt, args)` | Formatted text, like `std.fmt.allocPrint`.            |
| `String.initCapacity(allocator, n)`      | Empty string with room for `n` bytes.                 |
| `String.fromOwnedSlice(slice)`           | Takes over an allocated slice without copying.        |
| `stringz.join(allocator, sep, parts)`    | `parts` joined with `sep` between them.               |
| `s.clone(allocator)`                     | Independent copy of `s`.                              |
| `s.substr(allocator, start, end)`        | New string from bytes `start..end`.                   |

```zig
var a: String = .empty;
defer a.deinit(allocator);

var b: String = try .fromSlice(allocator, "copied");
defer b.deinit(allocator);

var c: String = try .fromPrint(allocator, "{s}-{d}", .{ "id", 7 });   // "id-7"
defer c.deinit(allocator);

var e = try stringz.join(allocator, ", ", &.{ "a", "b", "c" });   // "a, b, c"
defer e.deinit(allocator);
```

Every string you create needs a matching `deinit(allocator)`, including the ones returned by `clone`, `substr` and `join`. Calling `deinit` on an empty string is fine.

`fromSlice` accepts any bytes. Use `fromUtf8` at the edges of your program (file contents, network input) if you want to reject malformed text up front.

### Reading the contents

| Call          | Returns                       |
| ------------- | ----------------------------- |
| `s.str()`     | The contents as `[]const u8`. |
| `s.len()`     | Length in bytes.              |
| `s.isEmpty()` | `true` if the length is zero. |

`str()` is the bridge to everything else in Zig that takes a slice:

```zig
std.debug.print("{s}\n", .{s.str()});
const first_three = s.str()[0..3];
```

### Building

| Call                                 | Effect                                               |
| ------------------------------------ | ---------------------------------------------------- |
| `s.append(allocator, bytes)`         | Adds `bytes` to the end.                             |
| `s.appendByte(allocator, byte)`      | Adds one byte.                                       |
| `s.appendCodepoint(allocator, cp)`   | Adds one character given as a `u21`.                 |
| `s.print(allocator, fmt, args)`      | Adds formatted text.                                 |
| `s.insert(allocator, index, bytes)`  | Inserts `bytes` at a byte offset.                    |
| `s.set(allocator, bytes)`            | Replaces the whole contents.                         |
| `s.repeat(allocator, n)`             | Makes the string hold `n` copies of itself in total. |
| `s.padStart(allocator, width, fill)` | Pads on the left to `width` characters.              |
| `s.padEnd(allocator, width, fill)`   | Pads on the right to `width` characters.             |
| `s.center(allocator, width, fill)`   | Pads on both sides to `width` characters.            |

```zig
var s: String = .empty;
defer s.deinit(allocator);

try s.append(allocator, "world");
try s.insert(allocator, 0, "hello ");
try s.appendByte(allocator, '!');
try s.appendCodepoint(allocator, 0x1F525);
try s.print(allocator, " x{d}", .{3});
// "hello world!🔥 x3"

try s.set(allocator, "ab");
try s.repeat(allocator, 3);   // "ababab"

try s.set(allocator, "7");
try s.padStart(allocator, 3, '0');   // "007"
try s.padEnd(allocator, 6, '.');     // "007..."

try s.set(allocator, "hi");
try s.center(allocator, 6, '*');   // "**hi**"
```

Notes:

- `repeat(allocator, 1)` changes nothing and `repeat(allocator, 0)` empties the string.
- Padding widths are measured in characters, and `fill` is a single byte such as `' '` or `'0'`. A string already at or over the width is left alone. When `center` cannot split the padding evenly, the extra byte goes on the right.

### Removing and trimming

None of these allocate, except `replaceRange` when the replacement is longer than what it replaces.

| Call                                           | Effect                                                        |
| ---------------------------------------------- | ------------------------------------------------------------- |
| `s.pop()`                                      | Removes the last character and returns it as `?u21`.          |
| `s.removeRange(start, end)`                    | Removes bytes `start..end`.                                   |
| `s.replaceRange(allocator, start, end, bytes)` | Replaces bytes `start..end` with `bytes`.                     |
| `s.truncate(max_bytes)`                        | Shortens to at most `max_bytes`, never splitting a character. |
| `s.trim()`                                     | Removes whitespace from both ends.                            |
| `s.trimStart()` / `s.trimEnd()`                | Removes whitespace from one end.                              |
| `s.trimChars(chars)`                           | Removes any of the bytes in `chars` from both ends.           |
| `s.clearRetainingCapacity()`                   | Empties the string, keeps the memory for reuse.               |
| `s.clearAndFree(allocator)`                    | Empties the string and frees the memory.                      |

```zig
var s: String = try .fromSlice(allocator, "hello cruel world");
defer s.deinit(allocator);

s.removeRange(5, 11);                             // "hello world"
try s.replaceRange(allocator, 0, 5, "goodbye");   // "goodbye world"

try s.set(allocator, "héllo");
_ = s.pop();     // returns 'o', leaves "héll"
s.truncate(2);   // byte 2 is inside "é", so it backs up: "h"

try s.set(allocator, "  padded\t\n");
s.trim();   // "padded"

try s.set(allocator, "--=value=--");
s.trimChars("-=");   // "value"
```

Whitespace means space, tab, `\n`, `\r`, vertical tab and form feed (`stringz.whitespace`).

`pop` returns `null` on an empty string. If the string ends in bytes that are not valid UTF-8, it removes one byte and returns U+FFFD.

### Replacing and transforming

| Call                                              | Effect                                                                      |
| ------------------------------------------------- | --------------------------------------------------------------------------- |
| `s.replace(allocator, needle, replacement)`       | Replaces every match. Returns the number replaced.                          |
| `s.replaceFirst(allocator, needle, replacement)`  | Replaces the first match. Returns `true` if there was one.                  |
| `s.replaceN(allocator, needle, replacement, max)` | Replaces at most `max` matches, left to right. Returns the number replaced. |
| `s.toLowercase()` / `s.toUppercase()`             | Changes the case of ASCII letters.                                          |
| `s.toCapitalized()`                               | Uppercases the first letter of each word.                                   |
| `s.reverse()`                                     | Reverses the order of the characters.                                       |

```zig
var s: String = try .fromSlice(allocator, "a-b-c-d");
defer s.deinit(allocator);

const n = try s.replace(allocator, "-", "+");       // n == 3, "a+b+c+d"
_ = try s.replaceFirst(allocator, "+", " plus ");   // "a plus b+c+d"
_ = try s.replaceN(allocator, "+", "", 1);          // "a plus bc+d"

try s.set(allocator, "the quick fox");
s.toCapitalized();   // "The Quick Fox"
s.toUppercase();     // "THE QUICK FOX"
s.toLowercase();     // "the quick fox"

try s.set(allocator, "aé🔥");
s.reverse();   // "🔥éa"
```

Notes:

- An empty `needle` matches nothing and returns 0.
- If a replace call fails with `error.OutOfMemory`, the string is left exactly as it was.
- Case conversion only touches ASCII letters `a-z` and `A-Z`. `"É"` stays `"É"`. See [What is not included](#what-is-not-included).
- `reverse` keeps each character intact but does not know about combining marks or multi-codepoint emoji.

### Searching and comparing

Nothing here allocates. Positions are byte offsets, and "not found" is `null`.

| Call                                          | Returns                                          |
| --------------------------------------------- | ------------------------------------------------ |
| `s.find(needle)`                              | `?usize` offset of the first match.              |
| `s.findFrom(start, needle)`                   | First match at or after byte `start`.            |
| `s.rfind(needle)`                             | Offset of the last match.                        |
| `s.findAny(chars)`                            | Offset of the first byte that is any of `chars`. |
| `s.contains(needle)`                          | `bool`                                           |
| `s.count(needle)`                             | Number of non-overlapping matches.               |
| `s.startsWith(prefix)` / `s.endsWith(suffix)` | `bool`                                           |
| `s.eql(other)`                                | `true` if the contents equal the slice `other`.  |
| `s.eqlIgnoreCase(other)`                      | Same, ignoring ASCII case.                       |
| `s.order(other)`                              | `.lt`, `.eq` or `.gt`, byte-wise, for sorting.   |

```zig
var s: String = try .fromSlice(allocator, "foo bar foo");
defer s.deinit(allocator);

s.find("foo");          // 0
s.rfind("foo");         // 8
s.findFrom(1, "foo");   // 8
s.findAny(" \t");       // 3
s.find("baz");          // null
s.contains("bar");      // true
s.count("foo");         // 2

s.eql("foo bar foo");             // true
s.eqlIgnoreCase("FOO BAR FOO");   // true
s.order("zebra");                 // .lt
```

The comparison methods take a slice. To compare two strings, pass `other.str()`.

### Splitting

Splitting gives you an iterator of slices into the original string. Nothing is copied or allocated, so there is nothing to free.

| Call                     | Yields                                                  |
| ------------------------ | ------------------------------------------------------- |
| `s.split(separator)`     | Pieces between each `separator`. Empty pieces are kept. |
| `s.splitAny(separators)` | Same, where any one byte of `separators` separates.     |
| `s.rsplit(separator)`    | Like `split`, from the end backwards.                   |
| `s.tokenize(separators)` | Like `splitAny`, but empty pieces are skipped.          |
| `s.fields()`             | Whitespace-separated words.                             |
| `s.lines()`              | Lines, handling both `\n` and `\r\n`.                   |

```zig
var s: String = try .fromSlice(allocator, "a,b,,c");
defer s.deinit(allocator);

var parts = s.split(",");   // "a", "b", "", "c"
while (parts.next()) |part| std.debug.print("[{s}]\n", .{part});

var tokens = s.tokenize(",");   // "a", "b", "c"

try s.set(allocator, "one\r\ntwo\nthree\n");
var lines = s.lines();   // "one", "two", "three"

try s.set(allocator, "  the quick\tbrown fox ");
var words = s.fields();   // "the", "quick", "brown", "fox"
```

`split` accepts a separator of any length, such as `", "` or `"::"`. `lines` does not produce an extra empty line for a trailing newline, but blank lines in the middle are kept.

When you only want two halves, `cut` is simpler than an iterator:

| Call                   | Returns                                                 |
| ---------------------- | ------------------------------------------------------- |
| `s.cut(separator)`     | `?{ before, after }` around the first `separator`.      |
| `s.cutLast(separator)` | `?{ before, after }` around the last `separator`.       |
| `s.cutPrefix(prefix)`  | The rest after `prefix`, or `null` if it is not there.  |
| `s.cutSuffix(suffix)`  | The rest before `suffix`, or `null` if it is not there. |

```zig
try s.set(allocator, "host=example.com:8080");

const key, const rest = s.cut("=").?;
// key == "host", rest == "example.com:8080"

// `rest` is a plain slice, so std.mem takes over from here.
const host, const port = std.mem.cutLast(u8, rest, ":").?;
// host == "example.com", port == "8080"

try s.set(allocator, "v1.2.3");
s.cutPrefix("v");      // "1.2.3"
s.cutSuffix(".zip");   // null
```

To collect the pieces into a list, append them yourself. Copy each piece if it needs to outlive the string.

### Characters (codepoints)

A codepoint is one Unicode character number, such as `U+00E9` for `é`. These methods walk the string from the start, so they are O(n).

| Call                      | Returns                                                      |
| ------------------------- | ------------------------------------------------------------ |
| `s.codepointCount()`      | Number of characters.                                        |
| `s.codepointAt(n)`        | The bytes of the `n`th character, as `?[]const u8`.          |
| `s.byteOffset(n)`         | The byte offset where the `n`th character starts.            |
| `s.codepoints()`          | An iterator over the characters.                             |
| `s.isCharBoundary(index)` | `false` if the byte offset is inside a multi-byte character. |
| `s.isValidUtf8()`         | `true` if the contents are well-formed UTF-8.                |
| `s.isAscii()`             | `true` if every byte is below 128.                           |

To visit every character, use the iterator instead of calling `codepointAt` in a loop:

```zig
var s: String = try .fromSlice(allocator, "aé🔥");
defer s.deinit(allocator);

var it = s.codepoints();
while (it.next()) |char| {
    // char is a []const u8: "a", then "é", then "🔥"
    std.debug.print("{s}\n", .{char});
}

var numbers = s.codepoints();
numbers.nextCodepoint();   // 'a' as a u21
numbers.nextCodepoint();   // 0xE9

s.isCharBoundary(1);   // true
s.isCharBoundary(2);   // false, inside "é"
```

To remove characters 1 up to 3 by character index, convert first:

```zig
s.removeRange(s.byteOffset(1).?, s.byteOffset(3).?);
```

`byteOffset(n)` returns `len()` when `n` equals the character count, so it works as the end of a range, and `null` beyond that.

Malformed UTF-8 never crashes these functions. An invalid byte counts as one character, and `nextCodepoint` reports it as U+FFFD.

### Parsing

| Call               | Returns                                                       |
| ------------------ | ------------------------------------------------------------- |
| `s.toInt(T, base)` | The whole string as an integer of type `T`.                   |
| `s.toFloat(T)`     | The whole string as a float of type `T`.                      |
| `s.toBool()`       | `?bool` for true/false, yes/no, on/off, 1/0 (any ASCII case). |
| `s.isBlank()`      | `true` if empty or whitespace only.                           |

```zig
var s: String = try .fromSlice(allocator, "42");
defer s.deinit(allocator);

try s.toInt(u32, 10);   // 42

try s.set(allocator, "0xff");
try s.toInt(u8, 0);   // 255, base 0 reads the 0x / 0o / 0b prefix

try s.set(allocator, "2.5");
try s.toFloat(f64);   // 2.5

try s.set(allocator, "yes");
s.toBool();   // true
```

`toInt` and `toFloat` return the same errors as `std.fmt.parseInt` and `std.fmt.parseFloat` (`error.InvalidCharacter`, `error.Overflow`). They do not skip whitespace, so `trim()` first when parsing user input.

### Formatting and writers

A string can be printed two ways: `{s}` with `s.str()`, or `{f}` with the string itself.

```zig
var name: String = try .fromSlice(allocator, "Ziggy");
defer name.deinit(allocator);

var line: String = try .fromPrint(allocator, "hello {f}, aka {s}", .{ name, name.str() });
defer line.deinit(allocator);
// "hello Ziggy, aka Ziggy"
```

Some APIs write their output to a `*std.Io.Writer` (JSON serializers, for example). To have them append to a string, lend it out as a writer and take it back afterwards:

```zig
var aw = line.toWriter(allocator);   // `line` is empty while `aw` holds the bytes
try aw.writer.writeAll("!");         // pass &aw.writer to any writer-based API
line = .fromWriter(&aw);             // "hello Ziggy, aka Ziggy!"
```

`toWriter` returns a `std.Io.Writer.Allocating`. If you return early between `toWriter` and `fromWriter`, call `aw.deinit()` to free the bytes.

### Handing memory in and out

These move bytes between a string and plain slices without copying.

| Call                           | Effect                                                         |
| ------------------------------ | -------------------------------------------------------------- |
| `s.toOwnedSlice(allocator)`    | Returns the bytes as `[]u8`. You free them. `s` becomes empty. |
| `s.toOwnedSliceZ(allocator)`   | Same, as a zero-terminated `[:0]u8` for C APIs.                |
| `String.fromOwnedSlice(slice)` | Wraps a slice you allocated. The string frees it on `deinit`.  |

```zig
var s: String = try .fromSlice(allocator, "payload");

const bytes: []u8 = try s.toOwnedSlice(allocator);   // `s` is now empty
defer allocator.free(bytes);

const raw = try allocator.dupe(u8, "adopted");
var adopted: String = .fromOwnedSlice(raw);   // no copy
defer adopted.deinit(allocator);
```

After `toOwnedSlice` the string is empty and can be reused or dropped. A slice given to `fromOwnedSlice` must come from the same allocator you later pass to the string's methods.

### Capacity

A string usually has more memory reserved than it is using, so that appending does not reallocate every time. You rarely need these, but they help in hot loops.

| Call                                   | Effect                                         |
| -------------------------------------- | ---------------------------------------------- |
| `s.capacity()`                         | Bytes that fit without reallocating.           |
| `s.ensureTotalCapacity(allocator, n)`  | Reserves room for at least `n` bytes in total. |
| `s.ensureUnusedCapacity(allocator, n)` | Reserves room for at least `n` more bytes.     |
| `s.shrinkToFit(allocator)`             | Gives back unused memory.                      |

To reuse one string as a scratch buffer, call `clearRetainingCapacity()` between uses.

### Hash map keys

The simplest way to key a map by text is `std.StringHashMap` with `s.str()`. The map borrows the bytes, so the string must outlive the entry and must not be modified while it is a key.

```zig
var by_slice: std.StringHashMap(u32) = .init(allocator);
defer by_slice.deinit();

var key: String = try .fromSlice(allocator, "apples");
defer key.deinit(allocator);

try by_slice.put(key.str(), 3);
by_slice.get("apples");   // 3
```

To use the `String` itself as the key, pass `String.HashContext`. Two strings with the same contents are the same key:

```zig
var by_string: std.HashMap(
    String,
    u32,
    String.HashContext,
    std.hash_map.default_max_load_percentage,
) = .init(allocator);
defer by_string.deinit();

try by_string.put(key, 3);
```

`Managed.HashContext` does the same for `Managed` keys.

### Using Managed

`Managed` has every method `String` has. The only differences:

- Drop the allocator argument: `s.append("x")` and not `s.append(allocator, "x")`.
- Constructors take the allocator once: `Managed.init(allocator)`, `Managed.fromSlice(allocator, "x")`, `Managed.fromOwnedSlice(allocator, slice)`, and so on.
- `deinit()` takes no argument.
- `clone()` and `substr()` return a `Managed` using the same allocator.
- There is no `Managed.empty`. Use `Managed.init(allocator)`, which does not allocate.

```zig
var s: Managed = .init(allocator);
defer s.deinit();

try s.append("  hello, world  ");
s.trim();
s.toCapitalized();
_ = try s.replace("World", "Zig");   // "Hello, Zig"
```

The allocator is available as `s.allocator`, and the wrapped unmanaged string as `s.unmanaged`.

### Free functions on slices

You do not need a `String` for read-only work. These take any `[]const u8`, including string literals, and never allocate:

| Function                                             | Returns                             |
| ---------------------------------------------------- | ----------------------------------- |
| `stringz.trim(s)`, `trimStart(s)`, `trimEnd(s)`      | A sub-slice without the whitespace. |
| `stringz.lines(s)`                                   | Line iterator.                      |
| `stringz.fields(s)`                                  | Word iterator.                      |
| `stringz.codepoints(s)`                              | Character iterator.                 |
| `stringz.codepointCount(s)`                          | Number of characters.               |
| `stringz.codepointAt(s, n)`                          | The `n`th character.                |
| `stringz.byteOffset(s, n)`                           | Byte offset of the `n`th character. |
| `stringz.isCharBoundary(s, i)`                       | `bool`                              |
| `stringz.isValidUtf8(s)`, `isAscii(s)`, `isBlank(s)` | `bool`                              |
| `stringz.toBool(s)`                                  | `?bool`                             |

```zig
const raw = "  Name: Ziggy \r\n";

stringz.trim(raw);               // "Name: Ziggy"
stringz.isBlank("   ");          // true
stringz.codepointCount("aé🔥");   // 3
stringz.toBool("off");           // false
```

Note the difference from the method: `stringz.trim(slice)` returns a shorter view and changes nothing, while `s.trim()` modifies the string in place.

Searching, comparing and cutting plain slices is already covered by `std.mem` (`find`, `findLast`, `startsWith`, `cut`, `splitSequence`, ...) and `std.ascii` (`eqlIgnoreCase`), so stringz does not duplicate them.

## What is not included

stringz understands UTF-8 encoding, but it does not ship Unicode data tables. That means:

- **No Unicode case mapping.** `toUppercase`, `toLowercase`, `toCapitalized` and `eqlIgnoreCase` handle ASCII letters only.
- **No grapheme clusters.** A "character" here is a codepoint. Some things a reader sees as one character are several codepoints, such as `é` written as `e` plus a combining accent, flags, and family emoji. `codepointCount`, `reverse`, `pop`, `truncate` and the pad functions treat those as separate characters.
- **No normalization or locale-aware sorting.** `eql` and `order` compare bytes.
- **No display width.** Padding counts codepoints, so text with wide CJK characters or emoji will not line up in a terminal.

If you need any of these, pair stringz with a dedicated Unicode library.

## Tests

```sh
zig build test      # run everything
zig build example   # run the quick start
```

`zig build test` runs two files:

- `src/test_stringz.zig` tests every method on `String` and `Managed`, and the free functions. It also throws random valid text and random garbage bytes at the character functions, fails every allocation one at a time to check nothing leaks, and breaks the build if `Managed` is ever missing a method that `String` has.
- `examples/guide.zig` holds the snippets from this README as tests. If you change an example here, change it there too.

## License

MIT, see [LICENSE](LICENSE).
