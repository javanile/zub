# ZÜB

A distributed package index for Zig.

## Package sync architecture

The sync pipeline uses a single lock file (`sync/zigistry.lock`) with independent state for each sync mode. Two modes run on every scheduled execution, each with a different purpose.

```json
{
  "fresh": {
    "last_run": "2026-04-10T10:30:00Z"
  },
  "backlog": {
    "cursor": "2026-03-15T10:32:00Z",
    "last_run": "2026-04-10T10:30:00Z"
  }
}
```

---

### Mode: `fresh`

**Purpose:** capture packages that were updated recently.

Every run fetches `page=1` of `topic:zig-package sort=updated_at desc` — no cursor, no state beyond `last_run`. This mode runs fast and keeps the index current with the GitHub activity stream. A package updated an hour ago will appear in the index after the next scheduled run.

```
Every run → fetch 10 most recently updated repos → write/overwrite _packages/*.md
```

---

### Mode: `backlog`

**Purpose:** guarantee that every package is eventually indexed, including repos that have never been updated since creation.

Uses a time-based cursor (`pushed:<cursor`) that advances backward through the timeline. Each run fetches `page=1` of the filtered window — this eliminates **page drift** (the problem that occurs when repos get updated mid-crawl and shift the page boundaries).

```
Run 1: no cursor     → 10 most recent repos   → cursor = T[10]
Run 2: cursor=T[10]  → next 10 repos          → cursor = T[20]
Run 3: cursor=T[20]  → next 10 repos          → cursor = T[30]
...
Run N: cursor=T[end] → 0 results              → cursor reset → cycle restarts
```

When a run returns zero results the full cycle is complete: the cursor is cleared and the next run starts over from the top.

A package that gets updated while the backlog cursor is below it will be picked up by `fresh` mode immediately, and by `backlog` again in the next full cycle.

---

### Why two modes?

| Need | Mode |
|---|---|
| New or recently updated package appears quickly | `fresh` |
| Package created years ago and never updated gets indexed | `backlog` |
| Package updated mid-backlog-cycle is not missed | `fresh` catches it; `backlog` re-syncs next cycle |

Both modes write to the same `_packages/` directory and are safe to run in sequence in the same CI job.

---

### Running

```bash
# One batch of fresh packages
make sync-zigistry mode=fresh

# One batch from the backlog
make sync-zigistry mode=backlog

# Fix emoji and YAML quoting in existing files
python3 sync/zigistry.py --sanitize

# Reset backlog cursor (restart full crawl)
python3 sync/zigistry.py --reset backlog

# Reset everything
python3 sync/zigistry.py --reset all
```

Set `GITHUB_TOKEN` to avoid strict unauthenticated rate limits (10 req/min).

### Lock file semaphores

Each mode has its own independent state inside `zigistry.lock`. Adding a new mode in the future requires only a new function in `sync/zigistry.py` and a new key in the lock file — existing modes are unaffected.

| Key | Description |
|---|---|
| `fresh.last_run` | Timestamp of last fresh run |
| `backlog.cursor` | `updated_at` of last processed repo; `null` means start of new cycle |
| `backlog.last_run` | Timestamp of last backlog run |
| `backlog.last_cycle` | Timestamp of last completed full cycle |
