---
title: zigzvm
description: One script. Any Zig version. Instant switching.
license: MIT
author: sudo-su-coffee
author_github: sudo-su-coffee
repository: https://github.com/sudo-su-coffee/zigzvm
keywords:
date: 2026-07-27
updated_at: 2026-07-27T06:27:58+00:00
last_sync: 2026-07-27T06:27:58Z
package_kind: library
has_library: false
has_binary: false
has_distributable_binary: false
binary_count: 0
distributable_binary_count: 0
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/sudo-su-coffee/zigzvm/
---

# zig_zvm.sh – Simple Zig Version Manager

One script. Any Zig version. Instant switching.

`zig_zvm.sh` is a tiny, zero‑dependency Bash script that lets you download, install, and switch between any version of Zig — from `0.13.0` up through the latest release.

It auto-detects your OS (Linux/macOS) and architecture (x86_64/aarch64), handles the tarball-naming change Zig introduced at `0.14.1`, caches downloads so you never re-fetch the same version twice, and fixes your shell's `PATH` automatically.

## 🚀 Features

- **Three separate stages** — download, install, and switch are independent commands, so you always know exactly what's on disk vs what's active.
- **Version-agnostic** — works with any Zig release, old or new tarball-naming convention.
- **Auto-detection** — picks the right tarball for your OS/arch automatically.
- **Download caching** — tarballs are cached in `~/zig/.cache/`; a version is only ever downloaded from ziglang.org once, no matter how many times you install/switch/reinstall it.
- **Symlink-based switching** — the active version lives at `~/zig/current`, no `sudo` needed.
- **Self-healing PATH** — automatically detects and fixes a stale/incorrect PATH entry in your `.bashrc`/`.zshrc`, and adds one if it's missing. No manual copy-pasting.
- **Verified installs** — every install is checked for a working `zig` binary before being marked successful; broken/partial installs are cleaned up automatically instead of silently switching to a dead symlink.
- **Lightweight** — only needs `curl` or `wget`, `tar`, and `file` (all standard on Linux/macOS).

## 📦 Installation

```bash
curl -L https://raw.githubusercontent.com/sudo-su-coffee/zigzvm/main/zig_zvm.sh -o ~/bin/zig_zvm.sh
chmod +x ~/bin/zig_zvm.sh
export PATH="$HOME/bin:$PATH"   # add to your shell rc if not already there
```

Or manually: save the script, `chmod +x` it, and place it somewhere on your `PATH`.

## 🧪 Usage

```bash
# Show installed versions and which one is active
./zig_zvm.sh --list

# Download a version only — saves the tarball to ~/zig/.cache/, doesn't install it
./zig_zvm.sh --dl 0.15.2

# Install a version only — extracts from cache into ~/zig/<version>/
# If it isn't downloaded yet, this tells you to run --dl first instead of
# silently fetching it for you.
./zig_zvm.sh --install 0.15.2

# Download + install (if needed) + switch to it, all in one step
./zig_zvm.sh --switch 0.15.2

# Help
./zig_zvm.sh --help
```

Short single-dash aliases also work: `-list`, `-dl`, `-install`, `-switch`.

After switching, verify:

```bash
zig version   # should match the version you chose
which zig     # should point to ~/zig/current/zig
```

## 🧠 How it works

- Downloaded tarballs are cached in `~/zig/.cache/`.
- Each installed version is extracted to `~/zig/<version>/` (the `zig` binary sits at the top level of that folder — Zig's official tarballs do **not** use a `bin/` subdirectory).
- `~/zig/current` is a symlink pointing at whichever version is active.
- `--switch` adds `export PATH="$HOME/zig/current:$PATH"` to your shell rc file the first time it runs, and auto-corrects it if an old/wrong entry is already there.
- Because a script can never modify the PATH of the shell that launched it, the very first time you fix your rc file you'll need to run `source ~/.bashrc` (or open a new terminal) once — after that, every new terminal picks up the correct `zig` automatically, with zero manual steps.

### The three-stage workflow

| Stage | Command | Touches network? | Touches disk (install)? |
|---|---|---|---|
| 1. Download | `--dl <version>` | Yes, if not cached | No |
| 2. Install | `--install <version>` | Never | Yes, extracts from cache (fails with a clear message if step 1 hasn't run) |
| 3. Switch | `--switch <version>` | Only if steps 1–2 haven't happened yet | Yes, plus repoints `~/zig/current` |

This split is useful if you want to pre-fetch a version on a fast connection and install it later offline, or just want clear visibility into what's downloaded vs. what's actually installed.

## 🗑️ Uninstall

```bash
rm -f ~/bin/zig_zvm.sh   # or wherever you placed it
rm -rf ~/zig             # deletes all installed versions and the download cache
```

Optionally remove the `PATH` line from your `~/.bashrc` or `~/.zshrc`.

## 📄 License

MIT – do whatever you like with it.
