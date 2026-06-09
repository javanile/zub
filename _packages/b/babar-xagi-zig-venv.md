---
title: zig-venv
description: Zig virtual environment and package manager foundation — Python venv-style workflows for Zig projects.
license: ""
author: babar-xagi
author_github: babar-xagi
repository: https://github.com/babar-xagi/zig-venv
keywords:
  - cli
  - package-manager
  - registry
  - tooling
  - venv
date: 2026-06-01
category: tooling
updated_at: 2026-06-01T06:09:39+00:00
last_sync: 2026-06-01T06:09:39Z
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
permalink: /packages/babar-xagi/zig-venv/
---

# zigenv ⚡

**Virtual environment manager for Zig** — pin, install, and switch Zig compiler versions per project, just like Python's `.venv`.

```
$ zigenv init 0.16.0
initialized .zig-env/ for zig 0.16.0

  activate:   source .zig-env/activate
  fish:       source .zig-env/activate.fish
  powershell: . .\.zig-env\Activate.ps1

run 'zigenv install 0.16.0' to download the compiler

$ zigenv install 0.16.0
downloading https://ziglang.org/download/0.16.0/zig-linux-x86_64-0.16.0.tar.xz
[##################################################] 100%
installed zig 0.16.0 → /home/user/.zigenv/versions/0.16.0

$ source .zig-env/activate
activated zig 0.16.0

(zig-0.16.0) $ zig version
0.16.0
```

---

## Why zigenv?

Zig's release cadence is fast and breaking changes happen between versions. Different projects need different compiler versions. Without a virtual environment tool, teams either:

- Pin a system-wide Zig version (breaks other projects), or
- Manually download and symlink compilers (tedious and error-prone).

zigenv solves this by giving each project its own isolated compiler reference, with automatic shell integration and a shared download cache so disk space is never wasted.

---

## Requirements

| Requirement | Version     |
|-------------|-------------|
| Zig         | 0.16.0 stable for current development |
| OS          | Linux, macOS, Windows, FreeBSD |
| curl or wget | For downloading compiler tarballs |
| tar         | For extracting `.tar.xz` (Linux/macOS) |
| unzip       | For extracting `.zip` (Windows) |

---

## Installation

### From source (recommended)

```sh
git clone https://github.com/your-org/zigenv
cd zigenv
zig build -Doptimize=ReleaseSafe
sudo cp zig-out/bin/zigenv /usr/local/bin/
```

### Verify

```sh
zigenv --version
# zigenv 0.1.0
```

---

## Commands

| Command                  | Description                                       |
|--------------------------|---------------------------------------------------|
| `zigenv init <version>`  | Create `.zig-env/` pinned to `<version>`          |
| `zigenv install <version>` | Download & cache a Zig compiler version         |
| `zigenv remove`          | Delete `.zig-env/` and `.zig-version`             |
| `zigenv list`            | List all cached Zig versions                      |
| `zigenv which`           | Print path to the active `zig` binary             |
| `zigenv current`         | Print the pinned version for this project         |
| `zigenv status`          | Show full environment health                      |
| `zigenv help`            | Print help message                                |
| `zigenv version`         | Print zigenv version                              |

### Version formats

```
0.16.0                   Stable release
master                   Latest nightly build
0.17.0-dev.123+ab12cd    Specific nightly build
```

---

## Workflow

### 1 — Initialise a project

```sh
cd ~/my-project
zigenv init 0.16.0
```

This creates two things:

```
my-project/
├── .zig-version          ← "0.16.0"
└── .zig-env/
    ├── activate          ← POSIX sh / bash / zsh
    ├── activate.fish     ← Fish shell
    ├── Activate.ps1      ← PowerShell
    └── config.json       ← metadata
```

### 2 — Download the compiler

```sh
zigenv install 0.16.0
```

The tarball is downloaded once and cached globally at `~/.zigenv/versions/0.16.0/`. Every project that pins the same version reuses this cache — no duplicate downloads.

### 3 — Activate

```sh
# bash / zsh / sh
source .zig-env/activate

# Fish
source .zig-env/activate.fish

# PowerShell
. .\.zig-env\Activate.ps1
```

Activation prepends the cached binary directory to `$PATH` and changes your prompt to show the active version. Your system Zig is untouched.

### 4 — Work normally

```sh
zig version          # 0.16.0
zig build            # uses pinned version
zig build test       # same
```

### 5 — Deactivate

```sh
deactivate
```

`$PATH` and `$PS1` are restored to their original values.

---

## Global cache layout

```
~/.zigenv/
└── versions/
    ├── 0.14.0/
    │   ├── zig           ← the compiler binary
    │   ├── lib/
    │   └── ...
    ├── 0.15.2/
    ├── 0.16.0/
    └── master/           ← latest nightly, updated on each 'zigenv install master'
```

Override the cache location with `$ZIGENV_HOME`:

```sh
export ZIGENV_HOME=/opt/zigenv
zigenv install 0.16.0   # goes to /opt/zigenv/versions/0.16.0
```

---

## Automatic activation with direnv

Install [direnv](https://direnv.net/) and add this to your project's `.envrc`:

```sh
source_up_if_exists
if [ -f .zig-env/activate ]; then
    . .zig-env/activate
fi
```

Then run `direnv allow` once. From that point, entering the directory activates the environment automatically and leaving it deactivates.

---

## CI / GitHub Actions

```yaml
- name: Install zigenv
  run: |
    zig build -Doptimize=ReleaseFast
    echo "$PWD/zig-out/bin" >> $GITHUB_PATH

- name: Install pinned Zig
  run: zigenv install "$(cat .zig-version)"

- name: Build & Test
  run: |
    source .zig-env/activate
    zig build test
```

See [`examples/ci_workflow.yml`](examples/ci_workflow.yml) for a full matrix example.

---

## Project structure

```
zigenv/
├── build.zig            ← build configuration (Zig 0.16.0 stable)
├── build.zig.zon        ← package manifest
├── src/
│   ├── main.zig         ← entry point (std.process.Init.Minimal)
│   ├── cli.zig          ← command parsing and dispatch
│   ├── version.zig      ← version string parsing, comparison, URL generation
│   ├── env.zig          ← per-project .zig-env/ lifecycle
│   ├── fetch.zig        ← download and extract Zig tarballs
│   └── shell.zig        ← activation script generation (sh/fish/ps1)
├── tests/
│   ├── version_test.zig ← 30+ tests: parsing, formatting, ordering, URLs
│   ├── cli_test.zig     ← argument routing, version round-trips
│   └── env_test.zig     ← full lifecycle: init → status → remove
├── examples/
│   ├── basic_usage.sh   ← annotated shell walkthrough
│   ├── ci_workflow.yml  ← GitHub Actions integration
│   └── direnv_integration.sh
└── README.md
```

---

## Architecture

```
main.zig
  └─ cli.zig (parse args, dispatch)
       ├─ env.zig  (init / status / remove per-project .zig-env/)
       │    ├─ version.zig  (parse, compare, URL generation)
       │    └─ shell.zig    (write activate scripts)
       └─ fetch.zig  (download tarball, extract to ~/.zigenv/versions/)
            └─ version.zig
```

### Key design decisions

**No HTTP client dependency.** zigenv delegates downloads to the system `curl` (or `wget` as fallback) via `std.process.run`. This sidesteps `std.http.Client`'s rapidly-changing API while remaining zero-dependency — curl ships on every major OS and is already used by Zig's own package manager.

**Zig 0.16.0 std.Io.Threaded.** The entry point uses `pub fn main(init: std.process.Init.Minimal) !void`, `std.process.Args.Iterator`, `std.process.Environ`, and `std.Io.Threaded` for sequential CLI I/O.

**Shared global cache, per-project activation.** Compiler binaries live in `~/.zigenv/versions/<ver>/` and are shared across all projects. The `.zig-env/` directory in each project only contains activation scripts and metadata — no binary duplication.

**Shell-native activation.** Rather than wrapping `zig` in a shim binary (like `rbenv` does), zigenv prepends the cache directory to `$PATH` at shell level. This is simpler, faster, and works transparently with any tool that calls `zig`.

---

## Running tests

```sh
zig build test
```

All tests run without network access. `env_test.zig` uses `testing.tmpDir` for fully isolated filesystem operations that are cleaned up automatically.

```sh
# Run only version tests
zig build test -- version-tests

# Check formatting
zig build fmt
```

---

## Compatibility

### Zig 0.16.0 stable

Current development is validated on Zig `0.16.0` stable.

The project uses the stable Zig APIs available in 0.16.0:

- `build.zig` uses module-based `.root_module` setup,
- filesystem code uses `std.Io.Dir`,
- CLI argv uses `std.process.Args.Iterator`,
- environment access uses `std.process.Environ`,
- child process execution uses `std.process.run`.

`zigenv` can still manage `master` and `0.17.0-dev...` compiler versions for user projects; the tool itself is now developed and validated with `0.16.0` stable.

See [`doc/phase0/`](doc/phase0/) for the validation notes.

---

## Contributing

1. Fork and clone the repository.
2. Run `zig build test` — all tests must pass.
3. Run `zig build fmt` — code must be correctly formatted.
4. Open a pull request with a clear description.

Please open an issue before starting large features. The project roadmap includes:

- [ ] `zigenv upgrade` — bump `.zig-version` to the latest stable and re-download
- [ ] `zigenv run <version> -- <command>` — run a command under any version without activating
- [ ] Shell hook for automatic activation on `cd` (like `rbenv`)
- [ ] Windows ZIP extraction without requiring `unzip` (use `std.zip`)
- [ ] Checksum verification against `ziglang.org/download/index.json`

---

## License

MIT — see [LICENSE](LICENSE).

---

## Acknowledgements

Inspired by Python's `venv`, Ruby's `rbenv`, and Node's `nvm`. Built for the Zig community.
