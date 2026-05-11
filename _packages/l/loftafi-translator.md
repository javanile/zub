---
title: translator
description: Translation table mapper for Zig
license: MIT
author: loftafi
author_github: loftafi
repository: https://github.com/loftafi/translator
keywords:
date: 2026-05-04
updated_at: 2026-05-04T23:31:30+00:00
last_sync: 2026-05-04T23:31:30Z
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
permalink: /packages/loftafi/translator/
---

# 🧹 Translation Table Mapper

Load translation data from a CSV file to that translations may be
served based on a translation key.

This library does not provide LLM or online automated translation of text.

# 📝 Usage

Tokenise your text into words and use `translator.translate("FIRST_NAME")` to
retrieve a translation of a keyword.

```zig
    const Translation = @import("translation").Translation;

    pub fn main() void {
        // Initialise a translator with a data file
        var translator: Translation = .empty;
        defer translator.deinit(allocator);
        try translator.loadTranslationData(allocator, "keys,en,el\nBREAD,bread,ἄρτος\n");

        try std.debug.assert(translator.maps.contains(Lang.english));

        translator.setLanguage(.english);
        std.log.info("FIRST_NAME={s}", .{translator.translate("FIRST_NAME")});
    }
```

## TODO

Store language information based on ISO 639 language and ISO 3166 country
information.

## 📨 Contributing

Contributions under the MIT license are welcome. Consider raising an issue
first to discuss the proposed change.

## 🔒 License

This code is released under the terms of the MIT license. This
code is useful for my purposes. No warrantee is given or implied
that this library will be suitable for your purpose and no warantee
is given or implied that this code is free from defects.
