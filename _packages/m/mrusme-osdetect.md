---
title: osdetect
description: "Runtime operating system and distribution detection for Zig. (https://tty.fail/mrus/osdetect)"
license: NOASSERTION
author: mrusme
author_github: mrusme
repository: https://github.com/mrusme/osdetect
keywords:
  - detection
  - discovery
  - distribution
  - operating-system
  - os
date: 2026-08-09
category: systems
updated_at: 2026-08-09T10:56:17+00:00
last_sync: 2026-08-09T10:56:17Z
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
permalink: /packages/mrusme/osdetect/
---

# osdetect

Runtime operating system and distribution detection for Zig.

The library reads what the system publishes about itself and reports it, along
with where each fact came from and how much it can be trusted. It does not
decide what you should do with that.

It knows approximately 120 distributions by name, roundabout 110 Linux and
around 10 BSD, and compiles for every target Zig can build `std.Io` for, where
it returns the compile time facts and nulls for the rest.

## Installation

```sh
zig fetch --save git+https://tty.fail/mrus/osdetect
```

Then in `build.zig`:

```zig
const osdetect = b.dependency("osdetect", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("osdetect", osdetect.module("osdetect"));
```

## Usage

```zig
const std = @import("std");
const osdetect = @import("osdetect");

pub fn main(init: std.process.Init) !void {
    var env = try osdetect.detectInit(init);
    defer env.deinit();

    std.debug.print("{s}\n", .{env.osName()});
    std.debug.print("{s}\n", .{env.distroName()});
}
```

`detectInit` is a wrapper, alternatively `detect` can be used more explicitly:

```zig
var env = try osdetect.detect(gpa, io, .{ .environ = init.minimal.environ });
defer env.deinit();
```

The information in `env` can be used as follows:

```zig
switch (env.os.value) {
    .linux => {
        if (env.distro) |d| switch (d.id) {
            .ubuntu, .debian => {},
            .arch, .omarchy => {},
            else => {},
        };
    },
    .windows => {},
    .macos => {},
    else => {},
}
```

## Facts

`Environment` contains the information that was found, with absent fields being
`null`:

```zig
pub const Environment = struct {
    target_os: std.Target.Os.Tag,        // comptime, builtin.os.tag
    target_arch: std.Target.Cpu.Arch,    // comptime, builtin.cpu.arch
    os: Detection(std.Target.Os.Tag),    // confirmed at runtime
    android: bool,

    version: ?Detection(Version),
    release_name: ?[]const u8,           // "Tahoe", "24H2", "noble"
    build_id: ?[]const u8,               // "25B78", "26100.2314"
    kernel: ?Kernel,
    hardware_model: ?[]const u8,

    distro: ?DistroInfo,
    desktop: ?Detection(Desktop),
    session: ?Detection(Session),
    init_system: ?Detection(InitSystem),
    libc: ?Detection(LibC),
    compat: Compat,
};
```

The operating system field is `std.Target.Os.Tag` and compares directly against
`builtin.os.tag`.

**Note:** That tag set has no `android`, since Android is `.linux` with an
`.android` ABI.

### Provenance

Probes are wrapped in a `Detection`:

```zig
pub fn Detection(comptime T: type) type {
    return struct {
        value: T,
        source: Source,          // os_release, registry, sysctl, proc, ...
        confidence: Confidence,  // definitive or inferred
    };
}
```

The `confidence` `definitive` means the system said so, `inferred` means a
heuristic produced it and a different heuristic could disagree. You can check
the demo CLI, as it prints both for every field:

```
distro
  id              kubuntu
  base            ubuntu
  family          debian
  source          marker_path (inferred)
```

### Distribution

`DistroInfo` contains the resolved enum and the exact text:

```zig
pub const DistroInfo = struct {
    id: Distribution,        // resolved, may be a flavor such as .kubuntu
    base: Distribution,      // what the system itself named
    family: Family,          // package ecosystem
    source: Source,
    confidence: Confidence,

    id_raw: []const u8,      // the ID verbatim, even when unrecognized
    id_like: []const []const u8,
    name: []const u8,
    pretty_name: []const u8,
    version_id: ?[]const u8,
    version: ?[]const u8,
    version_codename: ?[]const u8,
    build_id: ?[]const u8,
    variant: ?[]const u8,
    variant_id: ?[]const u8,
    home_url: ?[]const u8,
    raw: []const KeyValue,   // every pair, including uninterpreted ones
};
```

A distribution missing from the enum is not a detection failure. `id_raw`,
`name` and `pretty_name` always contain what the system reported, and `raw`
contains every key.

`Family` is the package ecosystem: `debian`, `rhel`, `suse`, `arch`, `gentoo`,
`slackware`, `mandriva`, `alpine`, `void`, `nix`, `guix`, `puppy`,
`independent`, `bsd`, `darwin`, `windows`.

### Flavors

Kubuntu, Xubuntu, Lubuntu, Edubuntu and the Ubuntu MATE, Budgie, Cinnamon and
Unity flavors all ship Ubuntu's `/etc/os-release` verbatim, so os-release alone
cannot tell them apart. They are identified by the dpkg record of the desktop
metapackage that defines them, with the settings directory as a second opinion.
MX Linux AHS is MX Linux with an `ahs` marker in `/etc/mx-version`, and Void
Linux Musl is Void with musl as the detected libc.

Every answer from that stage is `.inferred` with `.marker_path` as the source,
and `base` contains what the operating system reported. A caller that distrusts
the heuristic can read `base` and ignore `id`.

### Compatibility layers

`target_os` and `os` can only differ under a compatibility layer, since e.g. a
Linux ELF cannot execute on e.g. an NT kernel otherwise. This difference is in
`Compat`:

```zig
pub const Compat = struct {
    wsl: ?Detection(WslVersion),      // wsl1 or wsl2
    wine: ?Detection(?[]const u8),    // the Wine version string
    container: ?Detection(Container), // docker, podman, lxc, nspawn, jail, ...
    virtualization: ?Detection(Virtualization),
    translation: ?Detection(Translation), // rosetta2, wow64, qemu_user, ...
    termux: bool,
};
```

`env.compat.isNative()` is true when none of them fired.

## Convenience

Convenience methods over the resolved fields:

```zig
env.isLinux()      env.isWindows()     env.isMacOS()      env.isDarwin()
env.isFreeBSD()    env.isOpenBSD()     env.isNetBSD()     env.isDragonFly()
env.isBSD()        env.isIllumos()     env.isAndroid()    env.isIOS()

env.isDebianLinux()  env.isUbuntuLinux()   env.isArchLinux()
env.isFedoraLinux()  env.isGentooLinux()   env.isOmarchyLinux()
env.isAlpineLinux()  env.isNixOS()         env.isVoidLinux()

env.isDebianLike()   env.isRedHatLike()   env.isArchLike()    env.isSuseLike()

env.isWSL()          env.isContainer()    env.isVirtualMachine()
env.isWine()         env.isTranslated()   env.isTermux()      env.isForeign()

env.isDistro(.pop_os)   // matches id, base, or an ID_LIKE entry
env.isFamily(.arch)
```

## Detection

On Linux the resolver runs in stages and stops at the first definitive answer:

- Stage one reads `/etc/os-release`, falling back to `/usr/lib/os-release`.
- Stage two maps `ID` through an exact table.
- Stage three, for an `ID` not in the table, walks `ID_LIKE` for the family and
  matches `NAME` and `PRETTY_NAME` against a substring table.
- Stage four reads the legacy files, from `/etc/lsb-release` and
  `/etc/slackware-version` through to `/etc/debian_version` last, since that one
  is present on every Debian derivative.
- Stage five is the flavor refinement described above.

The desktop comes from `XDG_CURRENT_DESKTOP`, `DESKTOP_SESSION` and the
compositor specific variables. The init system comes from `/proc/1/comm`, with
`/run/systemd/system` and the other runtime directories as the fallback. The
libc comes from `/proc/self/maps`, which names the interpreter this process
loaded. Where that says nothing (e.g. the binary is statically linked), it comes
from the dynamic loader on disk.

Windows calls `RtlGetVersion`. Edition and release names come from the registry
through `NtOpenKey` and `NtQueryValueKey`. Coverage runs from Windows NT 3.51
through Windows 11 25H2 and Server 2025, with the feature update names resolved
by build number.

**Note:** Windows 11 retains the NT `10.0` kernel version, therefore it's the
build number that separates it from Windows 10.

Darwin reads `kern.osproductversion`, `kern.osrelease`, `kern.osversion`,
`hw.machine`, `hw.model`, `sysctl.proc_translated` for Rosetta 2 and
`kern.hv_vmm_present` for virtualization. `kern.osproductversion` only exists
from 10.13.4, so older systems fall back to `SystemVersion.plist`, and it
reports `10.16` on macOS 11 and later when the caller was linked against an old
SDK, which is corrected against the Darwin major version. Names run from 10.0
Cheetah through macOS 26 Tahoe.

The BSDs read `kern.ostype`, `kern.osrelease`, `kern.version` and `hw.machine`
through `sysctl`. FreeBSD and the systems built on it also ship
`/etc/os-release` and get the same treatment as Linux. OpenBSD, NetBSD and
DragonFly publish no such file. OpenBSD has no `sysctlbyname` at all.

## Testing

`Options.root` redirects every path lookup into a directory, which makes the
whole Linux and BSD path testable without a matching machine. It also lets a
caller inspect a mounted image:

```zig
var env = try osdetect.detect(gpa, io, .{ .root = mounted_image });
defer env.deinit();
```

`classify` goes further and takes os-release content directly, with no allocator
and no filesystem:

```zig
const c = osdetect.classify(text);
// c.id, c.base, c.family, c.confidence
```

## Build

```sh
zig build test    # unit tests, table regressions and fixture tree tests
zig build check   # compile the library for 26 targets
zig build run     # print the detected environment with sources
zig build fmt     # check formatting
```

`zig build check` covers x86_64, aarch64, riscv64, arm, x86, powerpc64le, s390x,
loongarch64 and wasm32 against linux-gnu, linux-musl, linux-android,
windows-gnu, windows-msvc, macos, ios, freebsd, openbsd, netbsd, dragonfly, wasi
and freestanding.

## Zig version

Built for 0.16. A nightly CI job builds against Zig master.

## License

Copyright © 2026 [マリウス](https://xn--gckvb8fzb.com) and the osdetect Authors

osdetect is released under Version 1.1 of the
[SEGV License](https://xn--gckvb8fzb.com/segv/), whose full text is included in
the [LICENSE](LICENSE) file. Go read it, there will be a test on it on Monday.
