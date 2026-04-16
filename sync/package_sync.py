#!/usr/bin/env python3

import base64
import json
import os
import re
import hashlib
import sys
import time
import urllib.error
import urllib.request


GITHUB_API = "https://api.github.com"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGES_DIR = os.path.join(ROOT_DIR, "_packages")
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache", "github")

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
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.+)$", re.MULTILINE)

CLASSIFICATION_KEYS = (
    "package_kind",
    "has_library",
    "has_binary",
    "has_distributable_binary",
    "binary_count",
    "distributable_binary_count",
    "multiple_binaries",
)

SYNC_METADATA_KEYS = (
    "is_sponsor",
    "sync_priority",
    "sync_source",
)


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


def fetch_repo(full_name, token=None):
    url = f"{GITHUB_API}/repos/{full_name}"
    data, _, _ = github_request(url, token)
    return data


def repo_full_name(repo_or_full_name):
    if isinstance(repo_or_full_name, dict):
        return repo_or_full_name["full_name"]
    return repo_or_full_name


def repo_updated_at(repo_or_full_name):
    if isinstance(repo_or_full_name, dict):
        return repo_or_full_name.get("updated_at", "")
    return ""


def cache_file_path(repo_or_full_name, resource_name):
    full_name = repo_full_name(repo_or_full_name)
    updated_at = repo_updated_at(repo_or_full_name) or "no-updated-at"
    cache_key = hashlib.sha256(f"{full_name}\n{updated_at}\n{resource_name}".encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{cache_key}.txt")


def read_cached_text(repo_or_full_name, resource_name):
    path = cache_file_path(repo_or_full_name, resource_name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_cached_text(repo_or_full_name, resource_name, content):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = cache_file_path(repo_or_full_name, resource_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("" if content is None else content)


def fetch_readme(repo_or_full_name, token=None):
    cached = read_cached_text(repo_or_full_name, "README")
    if cached is not None:
        return cached or None

    full_name = repo_full_name(repo_or_full_name)
    url = f"{GITHUB_API}/repos/{full_name}/readme"
    try:
        data, _, _ = github_request(url, token)
        content = data.get("content", "")
        if data.get("encoding") == "base64":
            content = base64.b64decode(content).decode("utf-8", errors="replace")
        write_cached_text(repo_or_full_name, "README", content)
        return content
    except urllib.error.HTTPError as e:
        if e.code == 404:
            write_cached_text(repo_or_full_name, "README", "")
            return None
        raise


def fetch_repo_file(repo_or_full_name, path, token=None):
    cached = read_cached_text(repo_or_full_name, path)
    if cached is not None:
        return cached or None

    full_name = repo_full_name(repo_or_full_name)
    url = f"{GITHUB_API}/repos/{full_name}/contents/{path}"
    try:
        data, _, _ = github_request(url, token)
        content = data.get("content", "")
        if data.get("encoding") == "base64":
            content = base64.b64decode(content).decode("utf-8", errors="replace")
        write_cached_text(repo_or_full_name, path, content)
        return content
    except urllib.error.HTTPError as e:
        if e.code == 404:
            write_cached_text(repo_or_full_name, path, "")
            return None
        raise


def strip_emoji(text):
    return re.sub(r" {2,}", " ", EMOJI_RE.sub("", text)).strip()


def yaml_str(value):
    if not value:
        return '""'
    if any(c in value for c in (':', '#', '[', ']', '{', '}', '&', '*', '!', '|', '>', "'", '"', '%', '@', '`')):
        return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return value


def yaml_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return '""'
    if isinstance(value, int):
        return str(value)
    return yaml_str(str(value))


def repo_slug(full_name):
    return re.sub(r"[^a-zA-Z0-9\-]", "-", full_name).strip("-").lower()


def package_file_path(full_name):
    slug = repo_slug(full_name)
    letter = slug[0] if slug else "_"
    return os.path.join(PACKAGES_DIR, letter, f"{slug}.md")


def format_updated_at(github_ts):
    if not github_ts:
        return ""
    if github_ts.endswith("Z"):
        return github_ts[:-1] + "+00:00"
    return github_ts


def extract_declared_artifacts(build_text, kind_names):
    pattern = re.compile(
        r"const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*.*?\.(%s)\s*\((.*?)\);"
        % "|".join(re.escape(name) for name in kind_names),
        re.DOTALL,
    )
    artifacts = []
    for match in pattern.finditer(build_text or ""):
        var_name = match.group(1)
        body = match.group(3)
        name_match = re.search(r'\.name\s*=\s*"([^"]+)"', body)
        if not name_match:
            name_match = re.search(r'^\s*"([^"]+)"', body)
        artifacts.append({
            "var_name": var_name,
            "name": name_match.group(1) if name_match else "",
        })
    return artifacts


def classify_zig_package(repo_or_full_name, token=None):
    build_zig = fetch_repo_file(repo_or_full_name, "build.zig", token=token)
    build_zig_zon = fetch_repo_file(repo_or_full_name, "build.zig.zon", token=token)
    main_zig = fetch_repo_file(repo_or_full_name, "src/main.zig", token=token)

    executables = extract_declared_artifacts(build_zig, ("addExecutable",)) if build_zig else []
    libraries = extract_declared_artifacts(
        build_zig,
        ("addLibrary", "addStaticLibrary", "addSharedLibrary", "addModule"),
    ) if build_zig else []

    executable_vars = {artifact["var_name"] for artifact in executables}
    distributable_executable_vars = set()
    if build_zig:
        for match in re.finditer(r"\.installArtifact\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)", build_zig):
            var_name = match.group(1)
            if var_name in executable_vars:
                distributable_executable_vars.add(var_name)

    binary_count = len(executables)
    distributable_binary_count = len(distributable_executable_vars)
    has_binary = binary_count > 0
    has_library_signal = len(libraries) > 0
    has_main = bool(main_zig and re.search(r"\bpub\s+fn\s+main\s*\(", main_zig))

    if not has_binary and has_main:
        binary_count = 1
        distributable_binary_count = max(distributable_binary_count, 1)
        has_binary = True

    has_library = has_library_signal or (build_zig is not None or build_zig_zon is not None) and not has_binary

    if has_binary and has_library:
        package_kind = "hybrid"
    elif has_binary:
        package_kind = "binary"
    else:
        package_kind = "library"

    has_distributable_binary = distributable_binary_count > 0
    if has_binary and not has_distributable_binary:
        has_distributable_binary = True
        distributable_binary_count = max(distributable_binary_count, binary_count)

    return {
        "package_kind": package_kind,
        "has_library": has_library,
        "has_binary": has_binary,
        "has_distributable_binary": has_distributable_binary,
        "binary_count": binary_count,
        "distributable_binary_count": distributable_binary_count,
        "multiple_binaries": binary_count > 1,
    }


def repo_to_markdown(repo, readme=None, classification=None, category="", extra_frontmatter=None):
    owner, name = repo["full_name"].split("/", 1)
    topics = repo.get("topics", [])
    keywords = topics
    license_name = ""
    if repo.get("license"):
        license_name = repo["license"].get("spdx_id") or repo["license"].get("name", "")
    date = (repo.get("updated_at") or "")[:10]
    updated_at = format_updated_at(repo.get("updated_at", ""))
    description = strip_emoji(repo.get("description") or "")
    classification = classification or {
        "package_kind": "library",
        "has_library": True,
        "has_binary": False,
        "has_distributable_binary": False,
        "binary_count": 0,
        "distributable_binary_count": 0,
        "multiple_binaries": False,
    }
    extra_frontmatter = extra_frontmatter or {}

    kw_lines = "".join(f"\n  - {k}" for k in keywords) if keywords else ""
    category_line = f"\ncategory: {category}" if category else ""
    extra_lines = "".join(f"\n{key}: {yaml_scalar(value)}" for key, value in extra_frontmatter.items())
    frontmatter = f"""---
title: {yaml_str(name)}
description: {yaml_str(description)}
license: {yaml_str(license_name)}
author: {yaml_str(owner)}
author_github: {yaml_str(owner)}
repository: {repo["html_url"]}
keywords:{kw_lines}
date: {date}{category_line}
updated_at: {updated_at}
last_sync: {repo.get("updated_at", "")}
package_kind: {classification["package_kind"]}
has_library: {"true" if classification["has_library"] else "false"}
has_binary: {"true" if classification["has_binary"] else "false"}
has_distributable_binary: {"true" if classification["has_distributable_binary"] else "false"}
binary_count: {classification["binary_count"]}
distributable_binary_count: {classification["distributable_binary_count"]}
multiple_binaries: {"true" if classification["multiple_binaries"] else "false"}{extra_lines}
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


def write_package_file(repo, readme=None, classification=None, category="", extra_frontmatter=None):
    path = package_file_path(repo["full_name"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    content = repo_to_markdown(
        repo,
        readme=readme,
        classification=classification,
        category=category,
        extra_frontmatter=extra_frontmatter,
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def read_package_frontmatter(full_name):
    path = package_file_path(full_name)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    m = FRONTMATTER_RE.match(content)
    if not m:
        return {}
    data = {}
    for match in FRONTMATTER_KEY_RE.finditer(m.group(1)):
        data[match.group(1)] = match.group(2).strip()
    return data


def read_package_date(full_name):
    frontmatter = read_package_frontmatter(full_name)
    return frontmatter.get("date")


def is_repo_synced(repo, required_keys=(), expected_frontmatter=None):
    stored_date = read_package_date(repo["full_name"])
    if stored_date is None:
        return False
    if stored_date != (repo.get("updated_at") or "")[:10]:
        return False
    frontmatter = read_package_frontmatter(repo["full_name"])
    if not all(key in frontmatter for key in required_keys):
        return False
    expected_frontmatter = expected_frontmatter or {}
    return all(frontmatter.get(key) == yaml_scalar(value) for key, value in expected_frontmatter.items())
