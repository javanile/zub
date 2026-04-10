#!/usr/bin/env python3
"""
zigistry.py - Crawl GitHub for zig-package topic repos and write _packages/*.md

Uses the "Around the Time" mechanism for stable, complete, drift-free crawling.
See README.md for a full explanation.
"""

import base64
import configparser
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from urllib.parse import urlencode


GITHUB_API = "https://api.github.com"
TOPIC = "zig-package"
BATCH_SIZE = 10
DEFAULT_CATEGORY = "tooling"

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGES_DIR = os.path.join(ROOT_DIR, "_packages")
LOCK_FILE = os.path.join(os.path.dirname(__file__), "zigistry.lock")
CONF_FILE = os.path.join(os.path.dirname(__file__), "zigistry.conf")


def load_topic_map():
    """Load topic → category mapping from zigistry.conf."""
    cfg = configparser.ConfigParser(strict=False)
    cfg.read(CONF_FILE)
    if not cfg.has_section("topics"):
        return {}
    return {k.strip(): v.strip() for k, v in cfg.items("topics")}


TOPIC_MAP = load_topic_map()


def github_request(url, token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "zub-zigistry/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            rate_remaining = resp.headers.get("X-RateLimit-Remaining", "?")
            rate_reset = resp.headers.get("X-RateLimit-Reset", None)
            return data, int(rate_remaining) if rate_remaining != "?" else None, rate_reset
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        if e.code == 403:
            reset = e.headers.get("X-RateLimit-Reset")
            if reset:
                wait = int(reset) - int(time.time()) + 1
                print(f"Rate limited. Waiting {wait}s...", file=sys.stderr)
                time.sleep(max(wait, 1))
                return github_request(url, token)
        raise


def load_lock():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            return json.load(f)
    return None


def save_lock(cursor):
    lock = {
        "cursor": cursor,
        "last_run": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(LOCK_FILE, "w") as f:
        json.dump(lock, f, indent=2)


def delete_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


def fetch_readme(full_name, token=None):
    """Fetch and decode the README for a repo. Returns plain text or None."""
    url = f"{GITHUB_API}/repos/{full_name}/readme"
    try:
        data, _, _ = github_request(url, token)
        content = data.get("content", "")
        encoding = data.get("encoding", "base64")
        if encoding == "base64":
            return base64.b64decode(content).decode("utf-8", errors="replace")
        return content
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def fetch_batch(cursor, token=None):
    """
    Fetch one batch of BATCH_SIZE repos updated before `cursor`.
    Always requests page=1 of the filtered window — no page drift possible.
    """
    query = f"topic:{TOPIC}"
    if cursor:
        query += f" pushed:<{cursor}"

    params = urlencode({
        "q": query,
        "sort": "updated",
        "order": "desc",
        "per_page": BATCH_SIZE,
        "page": 1,
    })
    url = f"{GITHUB_API}/search/repositories?{params}"
    data, remaining, reset_ts = github_request(url, token)
    return data.get("items", []), data.get("total_count", 0), remaining, reset_ts


def repo_slug(full_name):
    """'owner/repo-name' → 'owner-repo-name'"""
    return re.sub(r"[^a-zA-Z0-9\-]", "-", full_name).strip("-").lower()


def yaml_str(value):
    """Quote a YAML string value if it contains characters that break plain scalars."""
    if not value:
        return '""'
    if any(c in value for c in (':', '#', '[', ']', '{', '}', '&', '*', '!', '|', '>', "'", '"', '%', '@', '`')):
        return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return value


def resolve_category(topics):
    """Return the best category for a list of topics using the conf mapping."""
    for topic in topics:
        cat = TOPIC_MAP.get(topic.lower().strip())
        if cat:
            return cat
    return DEFAULT_CATEGORY


def repo_to_markdown(repo, readme=None):
    owner, name = repo["full_name"].split("/", 1)
    topics = repo.get("topics", [])
    keywords = [t for t in topics if t != TOPIC]
    category = resolve_category(keywords)
    license_name = ""
    if repo.get("license"):
        license_name = repo["license"].get("spdx_id") or repo["license"].get("name", "")
    date = (repo.get("updated_at") or "")[:10]
    description = repo.get("description") or ""

    # YAML frontmatter
    kw_lines = "".join(f"\n  - {k}" for k in keywords) if keywords else ""
    frontmatter = f"""---
title: {yaml_str(name)}
description: {yaml_str(description)}
license: {yaml_str(license_name)}
author: {yaml_str(owner)}
author_github: {yaml_str(owner)}
repository: {repo["html_url"]}
category: {category}
topics:{kw_lines}
date: {date}
permalink: /packages/{owner}/{name}/
---"""

    # Body: use real README if available, otherwise fallback to a minimal stub
    if readme:
        body = readme.strip() + "\n"
    else:
        body = f"# {name}\n\n"
        if description:
            body += f"{description}\n\n"
        body += f"""## Installation

Add to your `build.zig.zon`:

```zig
.dependencies = .{{
    .{re.sub(r"[^a-zA-Z0-9_]", "_", name)} = .{{
        .url = "https://github.com/{repo["full_name"]}/archive/refs/heads/{repo.get("default_branch", "main")}.tar.gz",
    }},
}},
```
"""

    return frontmatter + "\n\n" + body


def write_package_file(repo, readme=None):
    slug = repo_slug(repo["full_name"])
    letter = slug[0] if slug else "_"
    subdir = os.path.join(PACKAGES_DIR, letter)
    os.makedirs(subdir, exist_ok=True)
    path = os.path.join(subdir, f"{slug}.md")
    content = repo_to_markdown(repo, readme=readme)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Crawl GitHub zig-package topic using the Around the Time mechanism."
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub token (or set GITHUB_TOKEN env var)",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the lock file and restart from the most recent repos",
    )
    args = parser.parse_args()

    if not args.token:
        print("Warning: no GitHub token. Rate limits will be strict (10 req/min).", file=sys.stderr)
        print("Set GITHUB_TOKEN env var or use --token.", file=sys.stderr)

    if args.reset:
        delete_lock()
        print("Lock deleted. Will restart from the most recent repos.", file=sys.stderr)

    os.makedirs(PACKAGES_DIR, exist_ok=True)

    lock = load_lock()
    cursor = lock["cursor"] if lock else None

    if cursor:
        print(f"Resuming from cursor: {cursor}", file=sys.stderr)
    else:
        print("No lock found. Starting from the most recently updated repos.", file=sys.stderr)

    items, total, remaining, _ = fetch_batch(cursor, token=args.token)

    print(f"Fetched {len(items)}/{total} repos in this window (rate limit remaining: {remaining})", file=sys.stderr)

    if not items:
        delete_lock()
        print("Full cycle complete. Lock deleted. Next run will restart from the top.", file=sys.stderr)
    else:
        for repo in items:
            readme = fetch_readme(repo["full_name"], token=args.token)
            path = write_package_file(repo, readme=readme)
            readme_status = "with README" if readme else "no README"
            print(f"  wrote {os.path.relpath(path, ROOT_DIR)}  ({repo['full_name']}, {readme_status})", file=sys.stderr)

        new_cursor = items[-1]["updated_at"]
        save_lock(new_cursor)
        print(f"Lock updated. New cursor: {new_cursor}", file=sys.stderr)

    print(f"Done.", file=sys.stderr)


if __name__ == "__main__":
    main()