# ZÜB

A distributed package index for Zig.

## Package sync: the "Around the Time" mechanism

The `sync-zigistry` process does not download all GitHub repositories in a single shot. Instead it uses a crawling strategy called **"Around the Time"**: each run fetches only 10 repositories, advances a time-based cursor, and on the next run continues exactly where it left off — with no drift and no missed packages.

### How it works

A lock file (`sync/zigistry.lock`) stores the current cursor — the `updated_at` timestamp of the last repo processed:

```json
{
  "cursor": "2026-03-15T10:32:00Z",
  "last_run": "2026-04-10T12:00:00Z"
}
```

Each run issues a single GitHub query anchored to that cursor:

```
topic:zig-package pushed:<{cursor}  sort=updated_at desc  page=1
```

By always requesting `page=1` of the filtered window — instead of advancing the page number — the result set is always stable and deterministic.

```
lock exists?
  ├── YES → query with cursor → fetch 10 repos → update cursor to oldest in batch
  └── NO  → query without filter → fetch 10 most recent repos → create lock
```

When a run returns zero results the full cycle is complete: the lock is automatically deleted and the next run restarts from the most recently updated repos.

The lock can also be reset manually by deleting `sync/zigistry.lock` or running:

```bash
python3 sync/zigistry.py --reset
```

### Why a timestamp cursor instead of a page number

A page-number approach suffers from **page drift**: if a repo gets updated between two runs it moves up in the list, causing every other repo to shift down by one position. Some repos get skipped, others get processed twice.

The cursor solves this by filtering the dataset at query time:

```
Run 1: cursor=NOW          → repos updated before NOW         (10 most recent)
Run 2: cursor=T[10]        → repos updated before T[10]       (next 10)
Run 3: cursor=T[20]        → repos updated before T[20]       (next 10)
...
Run N: cursor=T[(N-1)*10]  → 0 results → lock deleted → cycle complete
```

No matter how many repos get updated between runs, the window below the cursor never shifts. Each batch is always a stable `page=1` of a narrower and narrower slice of the timeline.

### Advantages of "Around the Time"

| Property | Benefit |
|---|---|
| **Complete coverage** | Every repo is processed exactly once per cycle, including repos that have never been updated since creation |
| **No page drift** | Repos that get updated mid-cycle move above the cursor and are picked up at the start of the next cycle, not skipped |
| **Incremental by design** | Each run is one lightweight API call (10 results). Friendly to cron, rate limits, and CI pipelines |
| **Self-healing** | A repo updated after it was processed will resurface at the top of the next cycle automatically |
| **Safe reset** | Deleting the lock file restarts from the top with no side effects on the accumulated index |

### Running

```bash
make sync-zigistry
```

Set `GITHUB_TOKEN` to avoid strict unauthenticated rate limits (10 req/min).