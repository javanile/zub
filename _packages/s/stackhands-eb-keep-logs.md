---
title: eb-keep-logs
description: Keep the logs of failed EasyBuild builds that a pipeline would lose, and rotate the log tree
license: MIT
author: stackhands
author_github: stackhands
repository: https://github.com/stackhands/eb-keep-logs
keywords:
  - easybuild
  - hpc
  - logging
  - slurm
date: 2026-11-13
category: tooling
updated_at: 2026-11-13T17:22:48+00:00
last_sync: 2026-11-13T17:22:48Z
package_kind: binary
has_library: false
has_binary: true
has_distributable_binary: true
binary_count: 1
distributable_binary_count: 1
multiple_binaries: false
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/stackhands/eb-keep-logs/
---

# eb-keep-logs

Keep the logs of EasyBuild builds that a build pipeline would otherwise lose, and keep the pipeline's log tree bounded.

A failed build's EasyBuild log stays in EasyBuild's tmpdir on the build node, which disappears with the job.
Parsing EasyBuild's stdout for the log path is unreliable, because EasyBuild wraps the "Results of the build can be found in the log file(s)" line.
`eb-keep-logs failed` asks `eb --last-log` for the path and keeps a copy.

## Install

Copy `eb-keep-logs` onto `PATH`, or install it with its EasyBuild recipe.
It needs `bash`, coreutils, `find`, `gzip`, `awk` and, for `failed`, `eb`.

A static Zig build of the same tool needs nothing but `eb`.
Build it with Zig 0.17.1:

```bash
zig build -Drelease=true
zig-out/bin/eb-keep-logs --version
```

`zig build test` runs its unit tests, the shell test suite against the
binary, and `tests/differential.sh`, which runs the shell script and the
binary on the same invocations.
[COMPAT.md](COMPAT.md) lists what the two share and where they differ on
purpose.

## Keep a failed build's logs

Run `eb` with `--tmp-logdir` pointing at a durable directory, then pass its exit status:

```bash
eb Foo-1.0.eb --tmp-logdir="$LOGDIR/easybuild-logs/Foo-1.0" 2>&1 | tee "$LOGDIR/Foo-1.0.stdout.log"
eb-keep-logs failed "${PIPESTATUS[0]}" Foo-1.0 "$LOGDIR" "$LOGDIR/easybuild-logs/Foo-1.0"
```

On a non-zero status this writes, next to `Foo-1.0.stdout.log`:

- `Foo-1.0.failed.ebout.log`, the EasyBuild log;
- `Foo-1.0.failed.command-out.txt` and `-err.txt`, the failing command's own output, when it lies under `EASYBUILD_TMPDIR` and belongs to the build account;
- `Foo-1.0.failed.meson-testlog.txt`, the full meson test log, when a meson test step failed.

Each kept file is closed to others and listed in `$LOGDIR/.licensed-logs`, because a failed compile line of licensed software can print the licence number.
On status 0 it keeps nothing.

## Rotate a log tree

```bash
eb-keep-logs rotate /srv/build-logs --compress-after 30 --delete-after 365
```

`rotate` looks only at run directories named `YYYYMMDD_HHMMSS` directly under the root, and dates each run by its name.
It gzips the `*.log` and `*.txt` files of runs older than `--compress-after` days, keeps each file's mode, and updates the run's `.licensed-logs`.
It removes whole runs older than `--delete-after` days only when that option is given.

## Tests

```bash
bash tests/test_eb_keep_logs.sh
```

## License

MIT
