---
title: jbsh
description: "The JSON Bourne Shell. A shell for JSON you don't understand yet. cd, ls, and grep your way through any blob. Pipe out."
license: MIT
author: justinGrosvenor
author_github: justinGrosvenor
repository: https://github.com/justinGrosvenor/jbsh
keywords:
  - cli
  - developer-tools
  - json
  - repl
  - shell
  - terminal
  - wasm
date: 2026-07-12
category: tooling
updated_at: 2026-07-12T16:38:55+00:00
last_sync: 2026-07-12T16:38:55Z
package_kind: binary
has_library: false
has_binary: true
has_distributable_binary: true
binary_count: 2
distributable_binary_count: 2
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/justinGrosvenor/jbsh/
---

# jbsh — JSON Bourne Shell

> A shell for JSON you don't understand yet. `cd`, `ls`, and `grep` your way through any blob — it never chokes and never lies.

![CI](https://github.com/justinGrosvenor/jbsh/actions/workflows/ci.yml/badge.svg)

You've got a big, unfamiliar JSON response and no idea what's in it. `jq` makes you already know the path. `jless` lets you look but you can't pipe out of it. `gron` floods you. **jbsh** lets you *walk* it like a filesystem — and pipe what you find into the next command.

```
$ jbsh response.json
jbsh › / ❯ ls
metadata/
count
users/
tags/
jbsh › / ❯ cd users/0
jbsh › /users/0 ❯ ls -l
TYPE    SIZE  VALUE              NAME
number  -     1                  id
string  3     "Ada"              name
string  15    "ada@example.com"  email
jbsh › /users/0 ❯ cat name
"Ada"
```

Hit **Tab** and you see the keys that are actually there. That's the whole point: **you don't have to know the shape in advance.**

## Why

- **Explore, don't query.** Unix verbs you already know — `cd` / `ls` / `cat` / `grep` — and zero DSL to learn.
- **Composable.** Every action also runs non-interactively and pipes cleanly — JSON in, plain text out:
  ```
  curl -s https://api.example.com/users | jbsh -c "cat -r users/0/email"
  jbsh users.json -c "find -v @example.com" | wc -l   # how many example.com addresses?
  token=$(jbsh creds.json -c "cat -r access_token")    # capture a value in a script
  ```
- **Never chokes.** Bounded before allocation — a 2 GB log line or pathological nesting becomes a clear error, never a crash or a hang.
- **Never lies.** Surfaces duplicate keys, preserves big-integer / high-precision numbers verbatim, rejects malformed UTF-8. What it shows you is the truth about the bytes.
- **Tiny & portable.** One ~210 KiB static binary. Linux, macOS, Windows — and the core compiles to WebAssembly.

## Install

**Homebrew** (macOS/Linux; builds from source, pulls `zig` as a build dep — if prompted, `brew trust justinGrosvenor/tap` first):

```
brew install justinGrosvenor/tap/jbsh
```

**Prebuilt binaries** — Linux (x86_64/aarch64), macOS (x86_64/aarch64), Windows — on the [releases page](https://github.com/justinGrosvenor/jbsh/releases). Each archive holds the binary, man page, and license:

```
curl -sL https://github.com/justinGrosvenor/jbsh/releases/latest/download/jbsh-aarch64-macos.tar.gz | tar -xz
sudo install jbsh-aarch64-macos/jbsh /usr/local/bin/
```

**From source** — needs [Zig 0.16](https://ziglang.org/download/):

```
git clone https://github.com/justinGrosvenor/jbsh
cd jbsh
zig build -Doptimize=ReleaseSmall
# → zig-out/bin/jbsh
```

The Homebrew formula is maintained in [`packaging/homebrew/`](packaging/homebrew/) and published via [justinGrosvenor/homebrew-tap](https://github.com/justinGrosvenor/homebrew-tap).

## Usage

```
jbsh <file.json>               # interactive REPL
jbsh <file.json> -c "<cmds>"   # run commands and exit
cat data.json | jbsh -c "ls"   # read JSON from stdin
```

Commands chain with `&&` (stop on error) and `;` (continue):

| Command | Does |
|---|---|
| `cd <path>` | move — `cd users/0`, `cd ..`, `cd /` |
| `ls [-l] [path]` | list children; `-l` adds type, size, and a value preview |
| `cat [-r] [path]` | print a value as JSON; `-r` prints it raw (unquoted scalar / compact) for piping |
| `tree [path]` | nested structural overview with box-drawing connectors |
| `pwd` · `type [path]` · `len [path]` | current path · value type · length |
| `find <pat>` · `find -v <pat>` · `grep <pat>` | find keys · find values · search string values (each shows the match's path) |
| `help [cmd]` · `info` · `limits` · `version` | help · document stats · active limits · version |

Paths use `/`, `..`, `.`, `key`, `[i]`, and compounds like `a/b/0`. Flags: `--color=auto|always|never`, `--max-lines=N`, `--max-width=N`, and `--max-{size,depth,string,members}=N`.

## What it isn't

- **Not a transformer** — use `jq`. jbsh is read-only by doctrine.
- **Not a query language** — precise `SELECT`-style querying is a planned sequel.
- **Not a viewer** — `fx` and `jless` are great for *looking*; jbsh is a shell, so the value you find flows into your next command.

## The franchise

"JSON Bourne Shell" is act one — *The Identity* (`sh`): figure out what this JSON is. The names are a roadmap *and* a scope-fence — each installment has to earn its place:

- **The Identity** — this shell. **(now)**
- **The Sequel** — SQL-over-JSON, read-only. (yes, "SQL" is pronounced *sequel*)
- **Bourne Again** — mutation (`bash`). (far future)

## Status

Early (v0.1), but the explorer works end to end and is gated on every push by **191 tests + the full [JSONTestSuite](https://github.com/nst/JSONTestSuite) conformance corpus** across Linux, macOS, and Windows. The interactive REPL is POSIX for now; Windows has full `-c` / pipe support (console raw-mode is a fast-follow). Built in [Zig](https://ziglang.org).

## License

MIT — see [LICENSE](LICENSE).
