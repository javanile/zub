#!/usr/bin/env python3

import os
import re
import sys

from package_sync import (
    CLASSIFICATION_KEYS,
    PACKAGES_DIR,
    ROOT_DIR,
    SYNC_METADATA_KEYS,
    classify_zig_package,
    fetch_readme,
    fetch_repo,
    is_repo_synced,
    write_package_file,
)


SPONSORS_LIST = os.path.join(os.path.dirname(__file__), "sponsors.list")
SPONSOR_FRONTMATTER = {
    "is_sponsor": True,
    "sync_priority": "sponsor",
    "sync_source": "sponsors",
}
REQUIRED_FRONTMATTER_KEYS = CLASSIFICATION_KEYS + SYNC_METADATA_KEYS
GITHUB_REPO_RE = re.compile(r"^https://github\.com/([^/\s]+)/([^/\s#?]+?)(?:\.git)?/?$")


def iter_sponsor_urls():
    if not os.path.exists(SPONSORS_LIST):
        return []
    urls = []
    with open(SPONSORS_LIST, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
    return urls


def parse_github_full_name(url):
    match = GITHUB_REPO_RE.match(url.strip())
    if not match:
        raise ValueError(f"Unsupported sponsor URL: {url}")
    owner = match.group(1)
    repo = match.group(2)
    return f"{owner}/{repo}"


def sync_sponsors(token=None):
    os.makedirs(PACKAGES_DIR, exist_ok=True)
    sponsor_urls = iter_sponsor_urls()
    print(f"[sponsors] verifying {len(sponsor_urls)} sponsor repo(s)", file=sys.stderr)

    written = 0
    skipped = 0
    failed = 0

    for url in sponsor_urls:
        try:
            full_name = parse_github_full_name(url)
            repo = fetch_repo(full_name, token=token)
            if is_repo_synced(
                repo,
                required_keys=REQUIRED_FRONTMATTER_KEYS,
                expected_frontmatter=SPONSOR_FRONTMATTER,
            ):
                skipped += 1
                print(f"  skip    {repo['full_name']}  (already synced sponsor)", file=sys.stderr)
                continue

            readme = fetch_readme(repo, token=token)
            classification = classify_zig_package(repo, token=token)
            path = write_package_file(
                repo,
                readme=readme,
                classification=classification,
                extra_frontmatter=SPONSOR_FRONTMATTER,
            )
            written += 1
            status = "with README" if readme else "no README"
            print(f"  wrote {os.path.relpath(path, ROOT_DIR)}  ({repo['full_name']}, {status})", file=sys.stderr)
        except Exception as e:
            failed += 1
            print(f"  error   {url}  ({e})", file=sys.stderr)

    print(f"[sponsors] Done. {written} written, {skipped} skipped, {failed} failed.", file=sys.stderr)
    return 1 if failed else 0


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Sync sponsor repositories listed in sync/sponsors.list into _packages/*.md"
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub token (or set GITHUB_TOKEN env var)",
    )
    args = parser.parse_args()

    if not args.token:
        print("Warning: no GitHub token. Rate limits will be strict (10 req/min).", file=sys.stderr)
        print("Set GITHUB_TOKEN env var or use --token.", file=sys.stderr)

    raise SystemExit(sync_sponsors(token=args.token))


if __name__ == "__main__":
    main()
