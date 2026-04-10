#!/usr/bin/env python3
"""
zigistry.py - Crawl GitHub for zig-package topic repos and write _packages/*.md

Two sync modes, one lock file:

  --mode fresh    Always fetches the most recently updated repos (no cursor).
                  Runs fast, keeps the index current with the GitHub activity stream.

  --mode backlog  Walks the full repo list oldest-to-newest using a time cursor.
                  Guarantees every package is eventually indexed. Auto-resets when
                  the list is exhausted and starts over from the top.

See README.md for a full explanation of the sync architecture.
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
DEFAULT_CATEGORY = ""

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGES_DIR = os.path.join(ROOT_DIR, "_packages")
LOCK_FILE = os.path.join(os.path.dirname(__file__), "zigistry.lock")
CONF_FILE = os.path.join(os.path.dirname(__file__), "zigistry.conf")

EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "\U0000FE00-\U0000FE0F"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U0000200D"
    "\U0000FE0F"
    "]+",
    flags=re.UNICODE,
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
DESCRIPTION_LINE_RE = re.compile(r"^(description:\s*)(.+)$", re.MULTILINE)


# ── Config ─────────────────────────────────────────────────────────────────────

def load_conf():
    cfg = configparser.ConfigParser(strict=False)
    cfg.read(CONF_FILE)
    topic_map = {}
    if cfg.has_section("topics"):
        topic_map = {k.strip(): v.strip() for k, v in cfg.items("topics")}
    ignore = set()
    if cfg.has_section("ignore_topics"):
        ignore = {k.strip() for k, _ in cfg.items("ignore_topics")}
    return topic_map, ignore


TOPIC_MAP, IGNORE_TOPICS = load_conf()


# ── Lock file ──────────────────────────────────────────────────────────────────

def load_lock():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            return json.load(f)
    return {}


def save_lock(lock):
    with open(LOCK_FILE, "w") as f:
        json.dump(lock, f, indent=2)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── GitHub API ─────────────────────────────────────────────────────────────────

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
            remaining = resp.headers.get("X-RateLimit-Remaining", "?")
            reset_ts = resp.headers.get("X-RateLimit-Reset", None)
            return data, int(remaining) if remaining != "?" else None, reset_ts
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


def fetch_batch(cursor=None, token=None):
    """
    Fetch one batch of BATCH_SIZE repos.
    If cursor is given, only repos updated strictly before that timestamp are returned.
    Always requests page=1 — no page drift possible.
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


def fetch_readme(full_name, token=None):
    url = f"{GITHUB_API}/repos/{full_name}/readme"
    try:
        data, _, _ = github_request(url, token)
        content = data.get("content", "")
        if data.get("encoding") == "base64":
            return base64.b64decode(content).decode("utf-8", errors="replace")
        return content
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


# ── Text helpers ───────────────────────────────────────────────────────────────

def strip_emoji(text):
    return re.sub(r" {2,}", " ", EMOJI_RE.sub("", text)).strip()


def yaml_str(value):
    if not value:
        return '""'
    if any(c in value for c in (':', '#', '[', ']', '{', '}', '&', '*', '!', '|', '>', "'", '"', '%', '@', '`')):
        return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return value


def repo_slug(full_name):
    return re.sub(r"[^a-zA-Z0-9\-]", "-", full_name).strip("-").lower()


def resolve_category(topics):
    for topic in topics:
        cat = TOPIC_MAP.get(topic.lower().strip())
        if cat:
            return cat
    return DEFAULT_CATEGORY


# ── Package file generation ────────────────────────────────────────────────────

def repo_to_markdown(repo, readme=None):
    owner, name = repo["full_name"].split("/", 1)
    topics = repo.get("topics", [])
    keywords = [t for t in topics if t not in IGNORE_TOPICS]
    category = resolve_category(keywords)
    license_name = ""
    if repo.get("license"):
        license_name = repo["license"].get("spdx_id") or repo["license"].get("name", "")
    date = (repo.get("updated_at") or "")[:10]
    description = strip_emoji(repo.get("description") or "")

    kw_lines = "".join(f"\n  - {k}" for k in keywords) if keywords else ""
    category_line = f"\ncategory: {category}" if category else ""
    frontmatter = f"""---
title: {yaml_str(name)}
description: {yaml_str(description)}
license: {yaml_str(license_name)}
author: {yaml_str(owner)}
author_github: {yaml_str(owner)}
repository: {repo["html_url"]}
keywords:{kw_lines}
date: {date}{category_line}
last_sync: {repo.get("updated_at", "")}
permalink: /packages/{owner}/{name}/
---"""

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


def read_package_date(repo):
    """Return the `date` stored in an existing package file, or None if absent."""
    slug = repo_slug(repo["full_name"])
    path = os.path.join(PACKAGES_DIR, slug[0], f"{slug}.md")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None
    match = re.search(r"^date:\s*(.+)$", m.group(1), re.MULTILINE)
    return match.group(1).strip() if match else None


def is_already_synced(repo):
    """True if the package file exists and its date matches the repo's updated_at."""
    stored_date = read_package_date(repo)
    if stored_date is None:
        return False
    return stored_date == (repo.get("updated_at") or "")[:10]


# ── Sanitize ───────────────────────────────────────────────────────────────────

def sanitize_existing_packages():
    fixed = 0
    for dirpath, dirs, filenames in os.walk(PACKAGES_DIR):
        dirs.sort()
        for filename in sorted(filenames):
            if not filename.endswith(".md"):
                continue
            path = os.path.join(dirpath, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            m = FRONTMATTER_RE.match(content)
            if not m:
                continue

            frontmatter = m.group(1)
            rest = content[m.end():]

            def clean_description(match):
                prefix = match.group(1)
                raw = match.group(2)
                if (raw.startswith('"') and raw.endswith('"')) or \
                   (raw.startswith("'") and raw.endswith("'")):
                    unquoted = raw[1:-1].replace('\\"', '"')
                else:
                    unquoted = raw
                return prefix + yaml_str(strip_emoji(unquoted))

            new_frontmatter = DESCRIPTION_LINE_RE.sub(clean_description, frontmatter)

            if new_frontmatter != frontmatter:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"---\n{new_frontmatter}\n---{rest}")
                rel = os.path.relpath(path, ROOT_DIR)
                print(f"  sanitized {rel}", file=sys.stderr)
                fixed += 1

    print(f"\nDone. {fixed} files sanitized.", file=sys.stderr)


# ── Sync modes ─────────────────────────────────────────────────────────────────

def sync_fresh(lock, token=None):
    """
    Fetch the most recently updated repos — always page=1, no cursor.

    If some repos in the batch are already synced (date matches), those slots are
    freed up and a recovery round fetches more repos to fill them — unless ALL
    repos in the batch are already synced, in which case the index is current and
    no recovery is needed.
    """
    items, total, remaining, _ = fetch_batch(cursor=None, token=token)
    print(f"[fresh] {len(items)}/{total} repos (rate limit remaining: {remaining})", file=sys.stderr)

    new_items = []
    skipped = []
    for repo in items:
        if is_already_synced(repo):
            skipped.append(repo)
            print(f"  skip    {repo['full_name']}  (already synced)", file=sys.stderr)
        else:
            new_items.append(repo)

    # Recovery round: fill free slots if at least one repo was genuinely new.
    # If all were already synced we are in parity — no point going deeper.
    free_slots = len(skipped)
    if free_slots > 0 and len(new_items) > 0:
        recovery_cursor = items[-1]["updated_at"]
        print(f"[fresh] {free_slots} free slot(s) — recovery round from cursor {recovery_cursor}", file=sys.stderr)
        extra, _, remaining, _ = fetch_batch(cursor=recovery_cursor, token=token)
        # Only take as many as the free slots
        for repo in extra[:free_slots]:
            if not is_already_synced(repo):
                new_items.append(repo)
                print(f"  recovered {repo['full_name']}", file=sys.stderr)
    elif free_slots == len(items):
        print(f"[fresh] All {len(items)} repos already synced — index is current, no recovery needed.", file=sys.stderr)

    for repo in new_items:
        readme = fetch_readme(repo["full_name"], token=token)
        path = write_package_file(repo, readme=readme)
        status = "with README" if readme else "no README"
        print(f"  wrote {os.path.relpath(path, ROOT_DIR)}  ({repo['full_name']}, {status})", file=sys.stderr)

    lock["fresh"] = {"last_run": now_iso()}
    save_lock(lock)
    print(f"[fresh] Done. {len(new_items)} written, {len(skipped)} skipped.", file=sys.stderr)


def sync_backlog(lock, token=None):
    """
    Walk the full repo list using a time cursor (pushed:<cursor).
    Advances BATCH_SIZE repos per run. When exhausted, resets and starts over.
    Guarantees every package is eventually indexed.
    """
    state = lock.get("backlog", {})
    cursor = state.get("cursor")

    if cursor:
        print(f"[backlog] Resuming from cursor: {cursor}", file=sys.stderr)
    else:
        print(f"[backlog] Starting new cycle from the most recently updated repos.", file=sys.stderr)

    items, total, remaining, _ = fetch_batch(cursor=cursor, token=token)
    print(f"[backlog] {len(items)}/{total} repos in window (rate limit remaining: {remaining})", file=sys.stderr)

    if not items:
        lock["backlog"] = {"cursor": None, "last_run": now_iso(), "last_cycle": now_iso()}
        save_lock(lock)
        print(f"[backlog] Full cycle complete. Cursor reset. Next run restarts from the top.", file=sys.stderr)
        return

    for repo in items:
        readme = fetch_readme(repo["full_name"], token=token)
        path = write_package_file(repo, readme=readme)
        status = "with README" if readme else "no README"
        print(f"  wrote {os.path.relpath(path, ROOT_DIR)}  ({repo['full_name']}, {status})", file=sys.stderr)

    new_cursor = items[-1]["updated_at"]
    lock["backlog"] = {"cursor": new_cursor, "last_run": now_iso()}
    save_lock(lock)
    print(f"[backlog] Cursor advanced to: {new_cursor}", file=sys.stderr)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Crawl GitHub zig-package topic repos and write _packages/*.md"
    )
    parser.add_argument(
        "--mode",
        choices=["fresh", "backlog"],
        help="Sync mode: 'fresh' captures recently updated repos, 'backlog' walks the full list",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub token (or set GITHUB_TOKEN env var)",
    )
    parser.add_argument(
        "--reset",
        metavar="MODE",
        help="Reset the cursor for a specific mode (fresh|backlog|all)",
    )
    parser.add_argument(
        "--sanitize",
        action="store_true",
        help="Strip emojis and fix YAML quoting in all existing package files, then exit",
    )
    args = parser.parse_args()

    if args.sanitize:
        sanitize_existing_packages()
        return

    if args.reset:
        lock = load_lock()
        targets = ["fresh", "backlog"] if args.reset == "all" else [args.reset]
        for t in targets:
            lock.pop(t, None)
            print(f"Reset: cleared state for mode '{t}'.", file=sys.stderr)
        save_lock(lock)
        return

    if not args.mode:
        parser.error("--mode is required (choose: fresh, backlog)")

    if not args.token:
        print("Warning: no GitHub token. Rate limits will be strict (10 req/min).", file=sys.stderr)
        print("Set GITHUB_TOKEN env var or use --token.", file=sys.stderr)

    os.makedirs(PACKAGES_DIR, exist_ok=True)
    lock = load_lock()

    if args.mode == "fresh":
        sync_fresh(lock, token=args.token)
    elif args.mode == "backlog":
        sync_backlog(lock, token=args.token)


if __name__ == "__main__":
    main()
