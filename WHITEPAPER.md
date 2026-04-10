# ZÜB: A Distributed Package Index for Zig
## Whitepaper v0.1 — April 2026

---

## Abstract

ZÜB is a distributed, federated package index for the Zig programming language. Unlike traditional centralized registries, ZÜB treats every deployed instance as a first-class node in a network. Package authors declare their canonical host directly inside their package metadata; all other nodes act as mirrors. This document describes the architecture, the federation model, the synchronization protocol, and the rationale for why this design should serve as a reference implementation for the next generation of package managers in any language ecosystem.

---

## 1. Problem Statement

### 1.1 The Centralization Trap

Every major package registry today is a single point of failure:

- **npm** — the `left-pad` incident (2016) took down thousands of projects worldwide with a single unpublish.
- **crates.io** — Rust's official registry is operated by a non-profit but remains architecturally centralized.
- **PyPI** — outages directly block CI/CD pipelines globally.
- **GitHub Packages** — tied to a single corporate entity and subject to geopolitical access restrictions.

The community response has historically been to add CDN layers or read replicas, which mitigates latency but does not address the fundamental governance and resilience problem: **the canonical truth lives in one place**.

### 1.2 The Zig Opportunity

Zig is a young language (pre-1.0 as of 2026) with a small but technically sophisticated community. Its package manager is built into the toolchain (`zig build` / `build.zig.zon`) and already embraces a decentralized model at the dependency-resolution level: packages are referenced by URL and hash, not by a registry name. This makes Zig's ecosystem a uniquely fertile ground for experimenting with a truly distributed registry architecture.

### 1.3 Existing Alternatives and Their Limits

| Registry | Model | Limitation |
|---|---|---|
| zigistry.dev | Centralized index, GitHub-sourced | Single operator, no federation |
| zig-central | Centralized | Inactive / experimental |
| x-cmd zig | Aggregator | Read-only, no publish flow |
| ZÜB | **Distributed, federated** | This paper |

---

## 2. Core Concepts

### 2.1 The Node

A ZÜB **node** is any deployment of the ZÜB codebase. Deploying ZÜB means becoming part of the network. Nodes can be:

- **Public nodes** — reachable from the internet, serving packages to any client.
- **Private nodes** — internal to an organization, accessible only within a VPN or local network.
- **Mirror nodes** — nodes that replicate a subset (or all) of another node's package index.

Any developer, company, or community can run a node. The reference node is `zub.javanile.org`.

### 2.2 Canonical Host Declaration

Every Zig package contains a `build.zig.zon` file. ZÜB extends the semantics of this file with an optional `registry` field:

```zon
.{
    .name = "httpz.zig",
    .version = "0.3.1",
    .registry = "https://zub.javanile.org",   // canonical host
    .mirrors = .{
        "https://zub.mycompany.internal",
        "https://community-node.example.org",
    },
    .dependencies = .{},
}
```

The `registry` field declares which ZÜB node is the **authoritative source** for this package. All other nodes that carry this package are mirrors. This is a per-package declaration, not a per-node policy — different packages on the same node can have different canonical hosts.

### 2.3 The Mirror Contract

When a node mirrors a package, it commits to:

1. Periodically polling the canonical host for new versions.
2. Serving the package tarball with an `X-ZUB-Origin` header pointing to the canonical host.
3. Refusing to accept publish operations for packages where it is not the canonical host.
4. Reporting its mirror status in the package metadata it serves.

This means **write operations always flow to the canonical host**, while **read operations can be satisfied by any mirror**. There is no eventual-consistency conflict for writes because write authority is declared in the package itself.

### 2.4 The Federation Graph

The set of all ZÜB nodes forms a directed graph:

- **Edges** represent mirror relationships (node A mirrors packages from node B).
- **Nodes** are ZÜB deployments.
- **Authority** is per-package, not per-node.

There is no central coordinator, no root-of-trust node, no blockchain. The graph is self-describing: every node publishes a `/api/nodes` endpoint listing the nodes it knows about, enabling organic discovery.

```
[zub.javanile.org]  ←→  [zub.mycompany.com]  ←→  [zub.community.dev]
        ↑                        ↑
  canonical for             canonical for
  httpz, serde              internal-sdk
```

---

## 3. Architecture

### 3.1 Node Components

Each ZÜB node consists of:

| Component | Responsibility |
|---|---|
| **Index** | Stores package metadata (name, versions, description, canonical host, mirrors) |
| **Sync Engine** | GitHub Actions-based poller that discovers and imports packages from known sources |
| **API Layer** | REST API serving package search, package detail, version list |
| **Web UI** | Human-readable frontend for browsing the index |
| **Node Registry** | List of known peer nodes, used for discovery and mirror coordination |

### 3.2 Sync Protocol (Current Implementation)

The current ZÜB implementation uses GitHub Actions as its sync engine:

1. A scheduled workflow runs periodically (e.g., every 6 hours).
2. The workflow queries known upstream sources (GitHub topics, other ZÜB nodes, community-maintained lists).
3. For each discovered package, it fetches `build.zig.zon` to extract metadata.
4. It upserts the package record into the local index.
5. If a `registry` field is present in `build.zig.zon`, it records the canonical host.

This design means **no persistent server process is required** for synchronization. A ZÜB node can run entirely on static hosting with GitHub Actions doing all the heavy lifting.

### 3.3 Sync Protocol (Target Implementation)

The target architecture adds a lightweight daemon for real-time federation:

```
[Canonical Node]
    │
    ├─ POST /api/publish  ← package author pushes new version
    │
    └─ broadcasts to known mirrors via webhook
            │
            ▼
    [Mirror Node]
        ├─ validates signature
        ├─ fetches tarball
        └─ updates local index
```

Webhooks are signed with the canonical node's keypair. Mirror nodes maintain a list of trusted public keys.

### 3.4 Package Identity

A package in ZÜB is uniquely identified by:

```
{canonical_host}/{namespace}/{name}@{version}
```

Example: `zub.javanile.org/community/httpz.zig@0.3.1`

The canonical host is part of the identity. This prevents namespace collisions between nodes and makes the authority relationship explicit in every reference.

---

## 4. Use Cases

### 4.1 Corporate Air-Gap Mirror

A company using Zig internally wants to ensure their builds never depend on external network access. They deploy a private ZÜB node, configure it to mirror all packages from `zub.javanile.org`, and point their `build.zig.zon` files at the internal node. If the external network goes down, builds continue uninterrupted.

### 4.2 Community-Owned Packages

A Zig community in a region with unreliable connectivity to European/US servers deploys a regional ZÜB node. Package authors in that community declare the regional node as their canonical host. Their packages are mirrored globally but the write authority remains local.

### 4.3 Organization-Scoped Packages

A company publishes internal Zig packages on their own ZÜB node. These packages are not listed on `zub.javanile.org`. The company's developers use the internal node; external developers cannot access these packages. No special access control mechanism is needed beyond standard network-level isolation.

### 4.4 Offline Development

A developer forks ZÜB, deploys it locally (e.g., via Docker), and uses it as a personal package cache. All dependencies are mirrored locally. This is functionally equivalent to `verdaccio` for npm but with a fully federated design.

---

## 5. The General Model

ZÜB is a case study, but the underlying design is language-agnostic. The key principles that other package managers should adopt:

### 5.1 Authority is a Package Property, Not a Registry Property

The canonical host of a package should be declared by the package author in the package metadata, not imposed by the registry operator. This shifts power from registry operators to package authors.

### 5.2 Forkability as a Feature

A registry that cannot be forked and self-hosted is a registry that cannot be trusted long-term. ZÜB is designed so that `git clone && deploy` produces a fully functional, independent node that can participate in the network immediately.

### 5.3 GitHub Actions as Infrastructure

For small-to-medium ecosystems, scheduled GitHub Actions workflows are a viable and cost-effective synchronization mechanism. They eliminate the need for dedicated server infrastructure for the sync layer, making it accessible to community operators with minimal resources.

### 5.4 No Central Coordinator

The network must function without any single node having special authority over others. Discovery is achieved through peer lists. Conflict resolution is achieved through the canonical host declaration. There is no "main" ZÜB node — `zub.javanile.org` is the reference implementation, not the root of trust.

### 5.5 Graceful Degradation

A node that loses connectivity to its peers continues to serve the packages it has cached. A node that loses its canonical host continues to serve the last known version of each package. The network degrades gracefully rather than failing catastrophically.

---

## 6. Comparison with Existing Federation Models

| Model | Example | Authority | Write | Read |
|---|---|---|---|---|
| Centralized + CDN | npm + Cloudflare | Central registry | Central | Distributed |
| Mirrored | PyPI mirrors | Central registry | Central | Distributed |
| Federated social (ActivityPub) | Mastodon | Per-instance | Per-instance | Federated |
| **ZÜB model** | ZÜB nodes | **Per-package** | **Per-package canonical host** | **Any mirror** |
| Blockchain | (various) | Consensus | Consensus | Distributed |

The ZÜB model is closest to the ActivityPub federation model but applied to packages rather than social content. The key innovation is moving authority to the package level rather than the instance level.

---

## 7. Security Considerations

### 7.1 Package Tampering

Zig's native package manager already uses content-addressed hashing (`build.zig.zon` includes a `.hash` field). ZÜB mirrors must preserve and serve the original hash, allowing clients to verify integrity regardless of which node served the package.

### 7.2 Node Impersonation

Nodes should publish their public key at a well-known endpoint (`/.well-known/zub-pubkey`). Mirror attestations and webhook payloads should be signed. Client tooling should warn when a package's canonical host changes.

### 7.3 Namespace Squatting

Since package identity includes the canonical host, squatting is namespace-scoped. An attacker on a different node cannot claim `zub.javanile.org/community/httpz.zig` — they can only create `evilnode.example/community/httpz.zig`, which has a different identity.

---

## 8. Roadmap

### Phase 1 — Foundation (current)
- Static index synchronized via GitHub Actions
- Web UI with package browsing and search
- Basic REST API for package metadata

### Phase 2 — Federation
- Node discovery via `/api/nodes` endpoint
- Mirror relationship tracking per package
- Webhook-based real-time sync between nodes
- HTTPS enforcement across all nodes

### Phase 3 — Trust and Identity
- Node keypair registration
- Signed mirror attestations
- Package signature verification

### Phase 4 — Ecosystem
- CLI tooling for publishing to a ZÜB node
- Integration with `zig build` for ZÜB-hosted dependencies
- Documentation and onboarding for new node operators

---

## 9. Conclusion

ZÜB demonstrates that a useful, federated package registry can be built with minimal infrastructure, leveraging existing tools (GitHub Actions, static hosting) while encoding a principled federation model. The per-package canonical host declaration is the key architectural insight: it aligns write authority with package authorship, eliminates single points of failure, and enables a network of independently operated nodes to cooperate without coordination overhead.

The Zig ecosystem is small enough that experimentation is low-risk and fast. If the model proves sound, it should inform the design of future package registries in any language — particularly those that have learned the hard lessons of centralization.

---

## Appendix A — Minimal `build.zig.zon` with ZÜB metadata

```zon
.{
    .name = "my-package",
    .version = "1.0.0",
    .registry = "https://my-zub-node.example.org",
    .fingerprint = 0xdeadbeefcafebabe,
    .dependencies = .{},
    .paths = .{""},
}
```

## Appendix B — Node Discovery Endpoint

```json
GET /api/nodes

{
  "node": "https://zub.javanile.org",
  "version": "0.1.0",
  "peers": [
    {
      "url": "https://zub.community.dev",
      "last_seen": "2026-04-10T15:00:00Z",
      "package_count": 42
    }
  ]
}
```

## Appendix C — Mirror Attestation Header

```
HTTP/1.1 200 OK
Content-Type: application/octet-stream
X-ZUB-Origin: https://zub.javanile.org
X-ZUB-Canonical: https://zub.javanile.org/community/httpz.zig@0.3.1
X-ZUB-Mirror: https://zub.mycompany.com
X-ZUB-Hash: sha256:abc123...
```

---

*ZÜB is an open source project by Francesco Napoletano / javanile.org*
*This whitepaper is released under CC BY 4.0*