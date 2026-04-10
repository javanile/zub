#!/usr/bin/env python3
"""
unsafe-status.py - Analyze _packages/ and mark unsafe packages in their frontmatter.

Rules are evaluated in order. A package is marked unsafe: true as soon as any
rule matches. Rules can be extended over time without changing the core logic.

Current rules:
  - zip_url: package file contains any URL ending in .zip
"""

import os
import re
import sys
from urllib.parse import urlparse


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGES_DIR = os.path.join(ROOT_DIR, "_packages")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
URL_RE = re.compile(r'https?://[^\s\)\]"\']+')


# ── Rules ─────────────────────────────────────────────────────────────────────

def url_path_ends_with(url, ext):
    """Check if the path component of a URL ends with `ext`, ignoring query params and fragments."""
    try:
        path = urlparse(url).path.rstrip(".,;)>\"'").lower()
        return path.endswith(ext)
    except Exception:
        return False


def rule_zip_url(content, frontmatter, body):
    """Flag any package whose file contains a URL whose path ends in .zip,
    regardless of query parameters or fragments (e.g. .zip?ts=1000 is still caught)."""
    for url in URL_RE.findall(content):
        if url_path_ends_with(url, ".zip"):
            return True, "contains a URL pointing to a .zip file"
    return False, None


RULES = [
    rule_zip_url,
    # add more rules here over time
]


# ── Frontmatter helpers ────────────────────────────────────────────────────────

def parse_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    m = FRONTMATTER_RE.match(content)
    if not m:
        return content, "", content
    frontmatter = m.group(1)
    body = content[m.end():]
    return content, frontmatter, body


def set_unsafe_flag(frontmatter, unsafe, reason):
    """Set or remove the unsafe flag and reason in the frontmatter string."""
    # Remove any existing unsafe/unsafe_reason lines
    lines = [
        l for l in frontmatter.splitlines()
        if not l.startswith("unsafe:") and not l.startswith("unsafe_reason:")
    ]
    if unsafe:
        lines.append(f"unsafe: true")
        lines.append(f'unsafe_reason: "{reason}"')
    return "\n".join(lines)


def rewrite_file(path, frontmatter, body):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"---\n{frontmatter}\n---{body}")


# ── Main ───────────────────────────────────────────────────────────────────────

def scan_packages():
    marked = []
    cleared = []
    skipped = []
    total = 0

    for dirpath, dirs, filenames in os.walk(PACKAGES_DIR):
        dirs.sort()  # visit subdirectories in alphabetical order
        for filename in sorted(filenames):
            if not filename.endswith(".md"):
                continue
            total += 1
            path = os.path.join(dirpath, filename)
            rel = os.path.relpath(path, ROOT_DIR)

            content, frontmatter, body = parse_file(path)
            if not frontmatter:
                skipped.append(rel)
                print(f"  SKIP    {rel}  — no frontmatter", file=sys.stderr)
                continue

            unsafe = False
            reason = None
            for rule in RULES:
                matched, rule_reason = rule(content, frontmatter, body)
                if matched:
                    unsafe = True
                    reason = rule_reason
                    break

            currently_unsafe = re.search(r"^unsafe:\s*true", frontmatter, re.MULTILINE) is not None
            if unsafe == currently_unsafe:
                print(f"  ok      {rel}", file=sys.stderr)
                continue  # nothing changed

            new_frontmatter = set_unsafe_flag(frontmatter, unsafe, reason)
            rewrite_file(path, new_frontmatter, body)

            if unsafe:
                marked.append((rel, reason))
                print(f"  UNSAFE  {rel}  — {reason}")
            else:
                cleared.append(rel)
                print(f"  CLEARED {rel}")

    return total, marked, cleared, skipped


def main():
    print(f"Scanning {PACKAGES_DIR} ...\n", file=sys.stderr)
    total, marked, cleared, skipped = scan_packages()
    print(f"\nScanned {total} packages — {len(marked)} marked unsafe, {len(cleared)} cleared, {len(skipped)} skipped.", file=sys.stderr)


if __name__ == "__main__":
    main()
