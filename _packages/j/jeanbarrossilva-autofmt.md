---
title: autofmt
description: A configurable, multi-language file formatter.
license: GPL-3.0
author: jeanbarrossilva
author_github: jeanbarrossilva
repository: https://github.com/jeanbarrossilva/autofmt
keywords:
  - cli
  - cli-tool
  - formatter
  - formatters
date: 2026-08-01
category: tooling
updated_at: 2026-08-01T21:56:07+00:00
last_sync: 2026-08-01T21:56:07Z
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
permalink: /packages/jeanbarrossilva/autofmt/
---

<div align="center">
  <h1>autofmt</h1>
  <div>A configurable, multi-language file formatter.</div>
  <br>
  <a href="https://github.com/jeanbarrossilva/autofmt/actions/workflows/test.yml">
    <img src="https://github.com/jeanbarrossilva/autofmt/actions/workflows/test.yml/badge.svg" />
  </a>
</div>
<br>

<mark>autofmt allows you to, in one go, format multiple files using a formatter of your choosing for each of them.</mark> This comes in handy when your project contains files written in various programming languages, where each of these files is formatted differently. In an Android project, for example, you may have:
<div align="center">
  <table>
    <thead>
      <tr>
        <th>Language</th>
        <th>Formatter</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Kotlin</td>
        <td><code>ktlint</code> <a href="https://ktlint.github.io/ktlint">[website]</a></td>
      </tr>
      <tr>
        <td>Java</td>
        <td><code>google-java-format</code> <a href="https://github.com/google/google-java-format">[source]</a></td>
      </tr>
      <tr>
        <td>XML</td>
        <td><code>xmllint</code> <a href="https://man.freebsd.org/cgi/man.cgi?query=xmllint&sektion=1&manpath=FreeBSD+13.2-RELEASE+and+Ports">[manual]</a></td>
      </tr>
      <tr>
        <td>C++</td>
        <td><code>clang-format</code> <a href="https://clang.llvm.org/docs/ClangFormat.html">[documentation]</a></td>
      </tr>
    </tbody>
  </table>
</div>

Ensuring that every file is formatted according to the style of your project by running every formatter can be a laborious task; autofmt groups these formatters into one, runnable with a single command. This can be done by including a configuration file in your project, `.autofmt.json`, in which the formatters to be run by autofmt are specified:

```json
[
  {
    "identifier": "kt",
    "arguments": ["ktlint", "--format"],
    "extensions": [".kt", ".kts"]
  },
  {
    "identifier": "java",
    "arguments": ["google-java-format", "--replace"],
    "extensions": [".java"]
  },
  {
    "identifier": "xml",
    "arguments": ["xmllint", "--format"],
    "extensions": [".xml"]
  },
  {
    "identifier": "c",
    "arguments": ["clang-format", "-i"],
    "extensions": [".c", ".cpp", ".h"]
  }
]
```

> [!NOTE]
> These formatters should be installed in your system before autofmt is run.

After having installed autofmt and written the configuration file, running

```zsh
autofmt
```

will format every file with their respective formatter.
