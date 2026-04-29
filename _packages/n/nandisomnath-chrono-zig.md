---
title: chrono-zig
description: The chrono library for zig
license: MIT
author: nandisomnath
author_github: nandisomnath
repository: https://github.com/nandisomnath/chrono-zig
keywords:
  - chrono
date: 2026-04-29
updated_at: 2026-04-29T11:55:46+00:00
last_sync: 2026-04-29T11:55:46Z
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
permalink: /packages/nandisomnath/chrono-zig/
---

Chrono: Timezone-aware date and time handling
========================================



Chrono aims to provide all functionality needed to do correct operations on dates and times in the
[proleptic Gregorian calendar](https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar):

* The `DateTime` type is timezone-aware
  by default, with separate timezone-naive types.
* Operations that may produce an invalid or ambiguous date and time return `Option` or `MappedLocalTime`
* Configurable parsing and formatting with an `strftime` inspired date and time formatting syntax.
* The `Local` timezone works with the current timezone of the OS.
* Types and operations are implemented to be reasonably efficient.

Timezone data is not shipped with chrono by default to limit binary sizes. Use the companion crate
[Chrono-TZ](https://crates.io/crates/chrono-tz) or [`tzfile`](https://crates.io/crates/tzfile) for
full timezone support.

## Documentation

[`Experimental`](https://nandisomnath.github.io/chrono-zig),  Documentation is not fully prepared.

<!-- See [docs.rs](https://docs.rs/chrono/latest/chrono/) for the API reference. -->

## Limitations

* Only the proleptic Gregorian calendar (i.e. extended to support older dates) is supported.
* Date types are limited to about +/- 262,000 years from the common epoch.
* Time types are limited to nanosecond accuracy.
* Leap seconds can be represented, but Chrono does not fully support them.
* No `deprecated` functions are no longer maintained.

## Module features



## Zig version requirements

The Minimum Supported Zig Version is currently **Zig 0.14.0**.


## License

This project is licensed under 
* [MIT License](https://opensource.org/licenses/MIT)


## Disclaimer

This project is a port of the rust version of
[`Chrono`](https://github.com/chronotope/chrono).  
If the rust version have any bug that can have in this project.
