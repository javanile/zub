# Contributing to zub

zub is a distributed package index for Zig. Contributions are welcome in three main areas: adding packages manually, improving the sync pipeline, and improving the site itself.

## Ways to contribute

### 1. Add or fix a package entry

Package entries live in `_packages/{first_letter}/{slug}.md`. Each file is a Jekyll page with YAML frontmatter followed by a Markdown body.

To add a package manually:

1. Fork the repository
2. Create a file at `_packages/{first_letter_of_slug}/{owner}-{repo}.md`
3. Use the frontmatter structure below
4. Open a pull request

**Frontmatter structure:**

```yaml
---
title: zig-clap
description: Command line argument parsing for Zig
license: MIT
author: Hejsil
author_github: Hejsil
repository: https://github.com/Hejsil/zig-clap
topics:
  - cli
  - argument-parsing
date: 2026-01-15
permalink: /packages/hejsil-zig-clap/
---
```

After the frontmatter, add a short Markdown description and an installation snippet showing how to add the package to `build.zig.zon`.

**Rules for a valid entry:**

- The repository must have the `zig-package` topic on GitHub
- The package must be publicly accessible
- One file per repository — the filename must be `{owner}-{repo}.md` in lowercase with non-alphanumeric characters replaced by hyphens
- `permalink` must be `/packages/{slug}/` where slug matches the filename without `.md`

### 2. Improve the sync pipeline

The automated sync lives in `sync/zigistry.py`. It uses the **"Around the Time"** crawling mechanism (see [README.md](README.md) for a full explanation).

To run it locally:

```bash
# Requires Python 3.8+, no external dependencies
export GITHUB_TOKEN=ghp_...
make sync-zigistry
```

To reset the crawl cursor and restart from the most recently updated repos:

```bash
python3 sync/zigistry.py --reset
```

The lock file at `sync/zigistry.lock` tracks the current cursor. Delete it or use `--reset` to force a full re-crawl.

If you find a bug or want to improve the sync logic, please open an issue first to discuss the approach before submitting a PR.

### 3. Improve the site

The site is built with Jekyll and hosted on GitHub Pages. To run it locally:

```bash
make serve   # requires Docker
```

The site configuration is in `_config.yml`. The remote theme is `javanile/package-manager`.

## Pull request guidelines

- Keep each PR focused on a single concern
- For new packages added via sync, do not submit the generated files manually — let the sync pipeline handle them
- For manual package additions, verify the repository exists and is active before submitting
- Prefer editing existing files over creating new ones
- Do not include `sync/zigistry.lock` or `sync/zigistry.json` in your PR

## Reporting issues

Open an issue on GitHub if you find:

- A package entry with incorrect or outdated metadata
- A repository that should be indexed but is missing
- A bug in the sync pipeline
- A site rendering problem