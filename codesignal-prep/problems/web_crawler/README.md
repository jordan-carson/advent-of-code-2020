# Web crawler

Implement `WebCrawler` in `starter.py`. Tests fetch/parse pipeline design,
rate limiting, and dedup at scale. To keep this runnable offline and
deterministic, `fetch` and link-extraction are injected as callables
rather than doing real HTTP/HTML parsing — the crawling *logic* is what's
under test, not networking or an HTML parser.

## Level 1 — fetch and parse
- Constructor takes `fetch: Callable[[str], str]` (returns page content
  for a URL) and `extract_links: Callable[[str, str], list[str]]` (given
  a URL and its content, returns absolute URLs found in it)
- `crawl(start_url: str, max_pages: int) -> list[str]` — BFS from
  `start_url`, visiting each unique URL at most once, up to `max_pages`
  pages, returning visited URLs in visit order

## Level 2 — rate limiting
- Constructor also takes `requests_per_second: float`
- `crawl` must not call `fetch` faster than that rate (use an injectable
  `sleep: Callable[[float], None] = time.sleep` and an injectable
  `now: Callable[[], float] = time.monotonic` so tests don't need to
  actually sleep)

## Level 3 — domain filtering and politeness
- `crawl(start_url, max_pages, allowed_domains: set[str] | None = None)`
  — only follows links whose domain is in `allowed_domains` (all domains
  allowed if `None`)
- Track and expose `skipped_count` for links filtered out this way

## Level 4 — distributed crawling (simulated)
- `crawl_distributed(start_urls: list[str], max_pages: int, num_workers:
  int) -> list[str]` — simulate `num_workers` workers pulling from one
  shared frontier queue (round-robin is fine for the simulation) with the
  same one-visit-per-URL guarantee as Level 1, now across multiple seeds

## Level 5 (stretch) — retry with backoff
- `fetch` may raise; retry with exponential backoff up to a max attempt
  count before giving up on that URL and continuing the crawl

## Level 6 (stretch) — content-based dedup
- Two different URLs whose fetched content is identical (or above a
  similarity threshold you define) should only be "processed" once, even
  though both get visited
