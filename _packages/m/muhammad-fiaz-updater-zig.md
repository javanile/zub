---
title: updater.zig
description: A production-grade update checker and auto-updater for Zig applications, supporting multiple Git hosting providers and flexible configurations.
license: MIT
author: muhammad-fiaz
author_github: muhammad-fiaz
repository: https://github.com/muhammad-fiaz/updater.zig
keywords:
  - update-checker
  - update-checker-zig
  - update-package-zig
  - zig-updater
date: 2026-10-31
updated_at: 2026-10-31T14:21:52+00:00
last_sync: 2026-10-31T14:21:52Z
package_kind: hybrid
has_library: true
has_binary: true
has_distributable_binary: true
binary_count: 3
distributable_binary_count: 3
multiple_binaries: true
is_sponsor: false
sync_priority: normal
sync_source: zigistry
permalink: /packages/muhammad-fiaz/updater.zig/
---

<div align="center">

# updater.zig

<a href="https://muhammad-fiaz.github.io/updater.zig/"><img src="https://img.shields.io/badge/docs-muhammad--fiaz.github.io-blue" alt="Documentation"></a>
<a href="https://ziglang.org/"><img src="https://img.shields.io/badge/Zig-0.15.0+-orange.svg?logo=zig" alt="Zig Version"></a>
<a href="https://github.com/muhammad-fiaz/updater.zig"><img src="https://img.shields.io/github/stars/muhammad-fiaz/updater.zig" alt="GitHub stars"></a>
<a href="https://github.com/muhammad-fiaz/updater.zig/issues"><img src="https://img.shields.io/github/issues/muhammad-fiaz/updater.zig" alt="GitHub issues"></a>
<a href="https://github.com/muhammad-fiaz/updater.zig/pulls"><img src="https://img.shields.io/github/issues-pr/muhammad-fiaz/updater.zig" alt="GitHub pull requests"></a>
<a href="https://github.com/muhammad-fiaz/updater.zig"><img src="https://img.shields.io/github/last-commit/muhammad-fiaz/updater.zig" alt="GitHub last commit"></a>
<a href="https://github.com/muhammad-fiaz/updater.zig"><img src="https://img.shields.io/github/license/muhammad-fiaz/updater.zig" alt="License"></a>
<a href="https://github.com/muhammad-fiaz/updater.zig/actions/workflows/ci.yml"><img src="https://github.com/muhammad-fiaz/updater.zig/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
<img src="https://img.shields.io/badge/platforms-linux%20%7C%20windows%20%7C%20macos-blue" alt="Supported Platforms">
<a href="https://github.com/muhammad-fiaz/updater.zig/actions/workflows/release.yml"><img src="https://github.com/muhammad-fiaz/updater.zig/actions/workflows/release.yml/badge.svg" alt="Release"></a>
<a href="https://github.com/muhammad-fiaz/updater.zig/releases/latest"><img src="https://img.shields.io/github/v/release/muhammad-fiaz/updater.zig?label=Latest%20Release&style=flat-square" alt="Latest Release"></a>
<a href="https://pay.muhammadfiaz.com"><img src="https://img.shields.io/badge/Sponsor-pay.muhammadfiaz.com-ff69b4?style=flat&logo=heart" alt="Sponsor"></a>
<a href="https://github.com/sponsors/muhammad-fiaz"><img src="https://img.shields.io/badge/Sponsor-💖-pink?style=social&logo=github" alt="GitHub Sponsors"></a>
<a href="https://github.com/muhammad-fiaz/updater.zig/releases"><img src="https://img.shields.io/github/downloads/muhammad-fiaz/updater.zig/total?label=Downloads&logo=github" alt="Downloads"></a>
<a href="https://hits.sh/muhammad-fiaz/updater.zig/"><img src="https://hits.sh/muhammad-fiaz/updater.zig.svg?label=Visitors&extraCount=0&color=green" alt="Repo Visitors"></a>

<p><em>A production-ready Zig library for automatic update checking with multi-provider support.</em></p>

<b>📚 <a href="https://muhammad-fiaz.github.io/updater.zig/">Documentation</a> |
<a href="https://muhammad-fiaz.github.io/updater.zig/api/">API Reference</a> |
<a href="https://muhammad-fiaz.github.io/updater.zig/guide/getting-started">Quick Start</a> |
<a href="CONTRIBUTING.md">Contributing</a></b>

</div>

---

A production-ready, developer-friendly update checker library for Zig applications. Check for updates from GitHub, GitLab, Codeberg, or custom providers with comprehensive version comparison and auto-update capabilities.

**⭐️ If you find `updater.zig` useful, please give it a star! ⭐️**

---

<details>
<summary><strong>✨ Features of updater.zig</strong> (click to expand)</summary>

| Feature                        | Description                                                 |
| ------------------------------ | ----------------------------------------------------------- |
| 🔄 **Update Checking**         | Check for updates from multiple Git hosting providers       |
| 🌐 **Multi-Provider Support**  | GitHub, GitLab, Codeberg, and custom providers              |
| 📊 **Version Comparison**      | SemVer, CalVer, numeric, custom formats with suffix support |
| 🔧 **Auto-Update**             | Download, install, backup, and rollback functionality       |
| 💬 **Custom Messages**         | Fully customizable update notifications and prompts         |
| 🔒 **Checksum Verification**   | SHA256 verification for secure downloads                    |
| 🏗️ **Build-Time Checks**       | Optional update checks during build process                 |
| ⏰ **Background Checking**     | Non-blocking periodic update checks                         |
| 🛡️ **CI-Aware**                | Auto-disables in CI environments                            |
| 📝 **Detailed Error Messages** | Human-readable errors with suggestions                      |
| 🖥️ **Cross-Platform**          | Windows, Linux, macOS (32-bit and 64-bit)                   |
| 📦 **Zero Dependencies**       | Built entirely on the Zig standard library                  |
| ⚡ **High Performance**        | Efficient HTTP requests with configurable timeouts          |
| 🔑 **Auth Token Support**      | Private repository access via auth tokens                   |

</details>

---

<details>
<summary><strong>📌 Prerequisites & Supported Platforms</strong> (click to expand)</summary>

<br>

## Prerequisites

| Requirement          | Version                   | Notes                                                      |
| -------------------- | ------------------------- | ---------------------------------------------------------- |
| **Zig**              | 0.15.0+                   | Download from [ziglang.org](https://ziglang.org/download/) |
| **Operating System** | Windows 10+, Linux, macOS | Cross-platform support                                     |

---

## Supported Platforms

| Platform         | 32-bit | 64-bit    | ARM                        | Status       |
| ---------------- | ------ | --------- | -------------------------- | ------------ |
| **Windows**      | ✅ x86 | ✅ x86_64 | -                          | Full support |
| **Linux**        | ✅ x86 | ✅ x86_64 | ✅ aarch64                 | Full support |
| **macOS**        | ✅ x86 | ✅ x86_64 | ✅ aarch64 (Apple Silicon) | Full support |
| **Freestanding** | ✅ x86 | ✅ x86_64 | ✅ aarch64, arm, riscv64   | Full support |

</details>

---

<details>
<summary><strong>🌐 Supported Providers</strong> (click to expand)</summary>

| Provider               | API          | Auth Support | Rate Limits               |
| ---------------------- | ------------ | ------------ | ------------------------- |
| **GitHub**             | REST API v3  | ✅ Token     | 60/hr (5000/hr with auth) |
| **GitLab**             | REST API v4  | ✅ Token     | Varies by instance        |
| **Codeberg**           | Gitea API v1 | ✅ Token     | Varies                    |
| **Self-Hosted Gitea**  | Gitea API v1 | ✅ Token     | Custom                    |
| **Self-Hosted GitLab** | REST API v4  | ✅ Token     | Custom                    |
| **Custom**             | User-defined | ✅ Custom    | Custom                    |

</details>

---

## Installation

```bash
zig fetch --save https://github.com/muhammad-fiaz/updater.zig/archive/refs/tags/0.0.1.tar.gz
```

Or for nightly installation:

```bash
zig fetch --save git+https://github.com/muhammad-fiaz/updater.zig.git
```

Then in your `build.zig`:

```zig
const updater_dep = b.dependency("updater", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("updater", updater_dep.module("updater"));
```

---

## Quick Start

```zig
const std = @import("std");
const updater = @import("updater");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Simple GitHub update check
    const result = try updater.checkGitHub(
        allocator,
        "muhammad-fiaz",    // owner
        "updater.zig",      // repo
        "0.0.1",            // current version
    );

    if (result.has_update) {
        std.debug.print("Update available: {s}\n", .{result.latest_version.?});
        std.debug.print("Download: {s}\n", .{result.release_url.?});
    } else {
        std.debug.print("You're running the latest version!\n", .{});
    }
}
```

---

## Version Comparison

updater.zig supports multiple version formats:

```zig
const updater = @import("updater");

// Semantic Versioning (default)
// 1.0.0, v1.2.3, 1.0.0-alpha, 1.0.0-beta+build
.comparator = updater.version.semantic,

// Custom Format (e.g., 0.01.1-release)
// Supports suffix ranking: release > stable > rc > beta > alpha > dev
.comparator = updater.version.custom_format,

// Numeric (e.g., 1.2, 1.10)
// Handles multi-digit components: 1.10 > 1.9
.comparator = updater.version.numeric,

// Date-Based (CalVer)
// 2024.01.15, 2024.12.31, 20240115
.comparator = updater.version.date_based,

// Lexical (string comparison)
.comparator = updater.version.lexical,
```

### Suffix Priority

For custom versions with suffixes:

| Suffix    | Priority |
| --------- | -------- |
| `release` | 100      |
| `stable`  | 99       |
| `final`   | 98       |
| `rc`      | 50       |
| `beta`    | 30       |
| `alpha`   | 20       |
| `dev`     | 10       |
| `nightly` | 5        |

---

## Auto-Update

```zig
const updater = @import("updater");

var auto_updater = updater.AutoUpdater.init(allocator, .{
    .provider = updater.providers.github,
    .owner = "muhammad-fiaz",
    .repo = "updater.zig",
    .current_version = "0.0.1",
    .auto_update = .{
        .enabled = true,
        .auto_download = true,
        .auto_install = false,
        .prompt_before_update = true,
        .backup_current = true,
        .verify_checksum = true,
        .install_command = "zig build install",
        .pre_update_command = "echo Backing up...",
        .post_update_command = "echo Done!",
    },
});
defer auto_updater.deinit();

const result = try auto_updater.checkAndUpdate();
```

### AutoUpdater Methods

| Method             | Description                 |
| ------------------ | --------------------------- |
| `checkAndUpdate()` | Check and optionally update |
| `download()`       | Download update file        |
| `install()`        | Install downloaded update   |
| `backupCurrent()`  | Backup current executable   |
| `rollback()`       | Restore from backup         |
| `cleanup()`        | Remove temporary files      |

---

## Custom Providers

```zig
const updater = @import("updater");

// Self-hosted Gitea
const gitea = updater.providers.gitea("https://git.mycompany.com");

// Self-hosted GitLab
const gitlab = updater.providers.selfHostedGitlab("https://gitlab.internal.com");

const result = try updater.checkForUpdates(allocator, .{
    .provider = gitea,
    .owner = "team",
    .repo = "myproject",
    .current_version = "1.0.0",
});
```

---

## Configuration

### Full Configuration Options

```zig
const config = updater.UpdateConfig{
    // Core settings
    .enabled = true,
    .provider = updater.providers.github,
    .owner = "username",
    .repo = "myproject",
    .current_version = "1.0.0",
    .auth_token = null,             // For private repos
    .timeout_ms = 10000,            // 10 seconds
    .comparator = updater.version.semantic,
    .include_prereleases = false,

    // Message customization
    .messages = .{
        .show_update_available = true,
        .show_up_to_date = true,
        .show_skipped = false,
        .show_errors = true,
        .silent = false,
        .update_available_message = "New version!",
        .up_to_date_message = "Latest version.",
        .message_prefix = "[MyApp]",
        .custom_download_url = "https://example.com/download",
        .update_command = "zig fetch --save <url>",
    },

    // Auto-update settings
    .auto_update = .{
        .enabled = false,
        .auto_download = false,
        .auto_install = false,
        .prompt_before_update = true,
        .backup_current = true,
        .verify_checksum = true,
        .install_command = "zig build install",
    },
};
```

### Config Builder (Fluent API)

```zig
var builder = updater.configBuilder();
const config = try builder
    .provider(updater.providers.github)
    .owner("muhammad-fiaz")
    .repo("updater.zig")
    .currentVersion("0.0.1")
    .customMessage("Update available!")
    .enableAutoUpdate()
    .silentMode()
    .build();
```

---

## Error Handling

updater.zig provides detailed error information:

```zig
const result = updater.checkForUpdates(allocator, config) catch |err| {
    const info = updater.core.getUpdateErrorInfo(err);
    std.debug.print("Error: {s}\n", .{info.message});
    std.debug.print("Details: {s}\n", .{info.details.?});
    std.debug.print("Suggestion: {s}\n", .{info.suggestion.?});
    return;
};
```

### Error Types

| Error              | Description                           | Suggestion                            |
| ------------------ | ------------------------------------- | ------------------------------------- |
| `ConnectionFailed` | Network connection failed             | Check internet connection             |
| `HttpNotFound`     | Repository or release not found (404) | Verify owner/repo and release exists  |
| `HttpUnauthorized` | Authentication required (401)         | Provide valid auth_token              |
| `HttpForbidden`    | Access denied (403)                   | Check repo visibility or token scopes |
| `HttpRateLimited`  | Too many requests (429)               | Wait or use auth_token                |
| `InvalidJson`      | Invalid API response                  | API may have changed                  |
| `MissingField`     | Required field missing                | Ensure release has proper metadata    |
| `ChecksumMismatch` | Download verification failed          | Re-download the file                  |

---

## Build-Time Integration

Add update checking to your build process:

```zig
const updater = @import("updater");

pub fn build(b: *std.Build) void {
    // ... your build setup ...

    updater.build_integration.addUpdateCheck(b, .{
        .owner = "muhammad-fiaz",
        .repo = "updater.zig",
        .current_version = "0.1.0",
        .provider = .github,
    });
}
```

---

## Environment Variables

| Variable                   | Effect                            |
| -------------------------- | --------------------------------- |
| `ZIG_UPDATE_CHECK_DISABLE` | Disables all update checks        |
| `CI`                       | Auto-disables checks in CI        |
| `GITHUB_ACTIONS`           | Auto-disables checks in GitHub CI |
| `GITLAB_CI`                | Auto-disables checks in GitLab CI |

---

## API Reference

### Module Functions

| Function                                         | Description                      |
| ------------------------------------------------ | -------------------------------- |
| `checkForUpdates(allocator, config)`             | Perform update check with config |
| `checkGitHub(allocator, owner, repo, version)`   | Quick GitHub check               |
| `checkGitLab(allocator, owner, repo, version)`   | Quick GitLab check               |
| `checkCodeberg(allocator, owner, repo, version)` | Quick Codeberg check             |
| `checkAndUpdate(allocator, config)`              | Check and auto-update            |
| `formatUpdateMessage(allocator, result, config)` | Format result message            |
| `printUpdateMessage(result, config)`             | Print formatted message          |
| `isGloballyDisabled()`                           | Check if updates are disabled    |
| `isCI()`                                         | Check if running in CI           |
| `configBuilder()`                                | Create fluent config builder     |

### Providers

| Provider                          | Description                   |
| --------------------------------- | ----------------------------- |
| `providers.github`                | GitHub API provider           |
| `providers.gitlab`                | GitLab API provider           |
| `providers.codeberg`              | Codeberg (Gitea) API provider |
| `providers.gitea(base_url)`       | Self-hosted Gitea provider    |
| `providers.selfHostedGitlab(url)` | Self-hosted GitLab provider   |
| `providers.custom(...)`           | Fully custom provider         |

### Version Comparators

| Comparator              | Description                         |
| ----------------------- | ----------------------------------- |
| `version.semantic`      | SemVer (1.2.3, v1.2.3-alpha)        |
| `version.custom_format` | Custom with suffix (0.01.1-release) |
| `version.numeric`       | Numeric (1.2, 1.10)                 |
| `version.date_based`    | CalVer (2024.01.15)                 |
| `version.lexical`       | String comparison                   |

---

## Examples Directory

The `examples/` directory contains comprehensive examples:

- **basic.zig** - Core operations and getting started
- **custom_provider.zig** - Self-hosted and custom providers
- **runtime_check.zig** - Runtime checking and auto-update
- **version_compare.zig** - Version comparison strategies
- **all_features.zig** - Complete feature demonstration

---

## Building

```bash
# Run tests
zig build test --summary all

# Build library
zig build

# Run basic example
zig build example

# Run all examples
zig build examples

# Run specific example
zig build run-basic
zig build run-version_compare
zig build run-all_features

# Format code
zig fmt src/ examples/
```

---

## Documentation

Full documentation: **https://muhammad-fiaz.github.io/updater.zig/**

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT License - see [LICENSE](LICENSE).

Copyright (c) 2025 Muhammad Fiaz

---

## Links

- **Documentation**: https://muhammad-fiaz.github.io/updater.zig/
- **Repository**: https://github.com/muhammad-fiaz/updater.zig
- **Issues**: https://github.com/muhammad-fiaz/updater.zig/issues
- **Releases**: https://github.com/muhammad-fiaz/updater.zig/releases
