---
title: zig-totp
description: A TOTP and HOTP library for zig.
license: Apache-2.0
author: deatil
author_github: deatil
repository: https://github.com/deatil/zig-totp
keywords:
  - hotp
  - otp
  - otp-generator
  - otp-verification
  - otpauth
  - totp
  - zig-hotp
  - zig-otp
  - zig-totp
date: 2026-07-08
updated_at: 2026-07-08T05:56:18+00:00
last_sync: 2026-07-08T05:56:18Z
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
permalink: /packages/deatil/zig-totp/
---

## Zig-totp 

A TOTP and HOTP library for zig.


### Why One Time Passwords?

One Time Passwords (OTPs) are an mechanism to  improve security over passwords alone. When a Time-based OTP (TOTP) is stored on a user's phone, and combined with something the user knows (Password), you have an easy on-ramp to [Multi-factor authentication](http://en.wikipedia.org/wiki/Multi-factor_authentication) without adding a dependency on a SMS provider.  This Password and TOTP combination is used by many popular websites including Google, GitHub, Facebook, Salesforce and many others.

The `zig-totp` library enables you to easily add TOTPs to your own application, increasing your user's security against mass-password breaches and malware.

Because TOTP is standardized and widely deployed, there are many [mobile clients and software implementations](http://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm#Client_implementations).


### Env

 - Zig >= 0.16.0


### Adding zig-totp as a dependency

Add the dependency to your project:

```sh
zig fetch --save=zig-totp git+https://github.com/deatil/zig-totp#main
```

or use local path to add dependency at `build.zig.zon` file

```zig
.{
    .dependencies = .{
        .@"zig-totp" = .{
            .path = "./lib/zig-totp",
        },
        ...
    }
}
```

And the following to your `build.zig` file:

```zig
const zig_totp_dep = b.dependency("zig-totp", .{});
exe.root_module.addImport("zig-totp", zig_totp_dep.module("zig-totp"));
```

The `zig-totp` structure can be imported in your application with:

```zig
const totp = @import("zig-totp");
```


### Get Starting

~~~zig
const std = @import("std");
const totp = @import("zig-totp");

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    const alloc = init.arena.allocator();

    const secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ";
    // const n = totp.time.now(io).utc();
    // const passcode = try totp.generateCodeAt(alloc, secret, n);
    const passcode = try totp.generateCode(alloc, io, secret);

    defer alloc.free(passcode);

    // output: 
    // generateCode: 906939
    std.debug.print("generateCode: {s} \n", .{passcode});

    // const valid = totp.validateAt(alloc, passcode, secret, n);
    const valid = totp.validate(alloc, io, passcode, secret);
    
    // output: 
    // validate: true
    std.debug.print("validate: {} \n", .{valid});
}
~~~


### Generate Qrcode Url

~~~zig
const std = @import("std");
const totp = @import("zig-totp");

pub fn main(init: std.process.Init) !void {
    const alloc = init.arena.allocator();

    const secret = "test-data";

    var key = try totp.generate(alloc, .{
        .issuer = "Example",
        .account_name = "accountName",
        .period = 30,
        // .secret_size = 20,
        // use secret if secret not empty, or use secret_size to generate secret
        .secret = secret,
        .digits = .Six,
        .algorithm = .SHA1,
    });
    defer key.deinit();

    const qrcode_url = key.urlString();
    defer alloc.free(qrcode_url);

    // output: 
    // qrcode_url: otpauth://totp/Example:accountName?issuer=Example&period=30&digits=6&secret=ORSXG5BNMRQXIYI&algorithm=SHA1
    std.debug.print("qrcode_url: {} \n", .{qrcode_url});
}
~~~


### LICENSE

*  The library LICENSE is `Apache2`, using the library need keep the LICENSE.


### Copyright

*  Copyright deatil(https://github.com/deatil).
