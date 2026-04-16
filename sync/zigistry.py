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

import configparser
import json
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlencode

from package_sync import (
    CLASSIFICATION_KEYS,
    PACKAGES_DIR,
    ROOT_DIR,
    SYNC_METADATA_KEYS,
    classify_zig_package,
    fetch_readme,
    github_request,
    is_repo_synced,
    strip_emoji,
    write_package_file,
    yaml_str,
)


TOPIC = "zig-package"
BATCH_SIZE = 10
DEFAULT_CATEGORY = ""

LOCK_FILE = os.path.join(os.path.dirname(__file__), "zigistry.lock")
CONF_FILE = os.path.join(os.path.dirname(__file__), "zigistry.conf")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
DESCRIPTION_LINE_RE = re.compile(r"^(description:\s*)(.+)$", re.MULTILINE)

NORMAL_SYNC_FRONTMATTER = {
    "is_sponsor": False,
    "sync_priority": "normal",
    "sync_source": "zigistry",
}

REQUIRED_FRONTMATTER_KEYS = CLASSIFICATION_KEYS + SYNC_METADATA_KEYS


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


def fetch_batch(cursor=None, token=None):
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
    url = f"https://api.github.com/search/repositories?{params}"
    data, remaining, reset_ts = github_request(url, token)
    return data.get("items", []), data.get("total_count", 0), remaining, reset_ts


def resolve_category(topics):
    for topic in topics:
        cat = TOPIC_MAP.get(topic.lower().strip())
        if cat:
            return cat
    return DEFAULT_CATEGORY


def write_repo_package(repo, token=None):
    keywords = [t for t in repo.get("topics", []) if t not in IGNORE_TOPICS]
    category = resolve_category(keywords)
    repo_copy = dict(repo)
    repo_copy["topics"] = keywords
    readme = fetch_readme(repo, token=token)
    classification = classify_zig_package(repo, token=token)
    path = write_package_file(
        repo_copy,
        readme=readme,
        classification=classification,
        category=category,
        extra_frontmatter=NORMAL_SYNC_FRONTMATTER,
    )
    status = "with README" if readme else "no README"
    print(f"  wrote {os.path.relpath(path, ROOT_DIR)}  ({repo['full_name']}, {status})", file=sys.stderr)


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


def sync_fresh(lock, token=None):
    items, total, remaining, _ = fetch_batch(cursor=None, token=token)
    print(f"[fresh] {len(items)}/{total} repos (rate limit remaining: {remaining})", file=sys.stderr)

    new_items = []
    skipped = []
    for repo in items:
        if is_repo_synced(
            repo,
            required_keys=REQUIRED_FRONTMATTER_KEYS,
            expected_frontmatter=NORMAL_SYNC_FRONTMATTER,
        ):
            skipped.append(repo)
            print(f"  skip    {repo['full_name']}  (already synced)", file=sys.stderr)
        else:
            new_items.append(repo)

    free_slots = len(skipped)
    if free_slots > 0 and len(new_items) > 0:
        recovery_cursor = items[-1]["updated_at"]
        print(f"[fresh] {free_slots} free slot(s) — recovery round from cursor {recovery_cursor}", file=sys.stderr)
        extra, _, remaining, _ = fetch_batch(cursor=recovery_cursor, token=token)
        for repo in extra[:free_slots]:
            if not is_repo_synced(
                repo,
                required_keys=REQUIRED_FRONTMATTER_KEYS,
                expected_frontmatter=NORMAL_SYNC_FRONTMATTER,
            ):
                new_items.append(repo)
                print(f"  recovered {repo['full_name']}", file=sys.stderr)
    elif free_slots == len(items):
        print(f"[fresh] All {len(items)} repos already synced — index is current, no recovery needed.", file=sys.stderr)

    for repo in new_items:
        write_repo_package(repo, token=token)

    lock["fresh"] = {"last_run": now_iso()}
    save_lock(lock)
    print(f"[fresh] Done. {len(new_items)} written, {len(skipped)} skipped.", file=sys.stderr)


def sync_backlog(lock, token=None):
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
        write_repo_package(repo, token=token)

    new_cursor = items[-1]["updated_at"]
    lock["backlog"] = {"cursor": new_cursor, "last_run": now_iso()}
    save_lock(lock)
    print(f"[backlog] Cursor advanced to: {new_cursor}", file=sys.stderr)


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
