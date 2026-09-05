"""Implement WebCrawler level by level. See README.md for the spec."""
from __future__ import annotations

import time
from typing import Callable


class WebCrawler:
    def __init__(
        self,
        fetch: Callable[[str], str],
        extract_links: Callable[[str, str], list[str]],
        requests_per_second: float | None = None,
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], float] = time.monotonic,
    ) -> None:
        self.fetch = fetch
        self.extract_links = extract_links
        self.requests_per_second = requests_per_second
        self.sleep = sleep
        self.now = now
        self.skipped_count = 0  # for Level 3

    # --- Level 1 ---
    def crawl(self, start_url: str, max_pages: int, allowed_domains: set[str] | None = None) -> list[str]:
        raise NotImplementedError

    # --- Level 4 ---
    def crawl_distributed(self, start_urls: list[str], max_pages: int, num_workers: int) -> list[str]:
        raise NotImplementedError


def _fake_site() -> dict[str, list[str]]:
    return {
        "http://a.com": ["http://a.com/1", "http://a.com/2"],
        "http://a.com/1": ["http://a.com/2", "http://a.com/3"],
        "http://a.com/2": [],
        "http://a.com/3": ["http://external.com"],
        "http://external.com": [],
    }


def test_level_1() -> None:
    site = _fake_site()

    def fetch(url: str) -> str:
        return url  # content is irrelevant here, links come from the map

    def extract_links(url: str, content: str) -> list[str]:
        return site.get(url, [])

    crawler = WebCrawler(fetch=fetch, extract_links=extract_links)
    visited = crawler.crawl("http://a.com", max_pages=10)
    assert visited[0] == "http://a.com"
    assert len(visited) == len(set(visited))  # no URL visited twice
    assert set(visited) == set(site.keys())


def test_level_1_max_pages() -> None:
    site = _fake_site()
    crawler = WebCrawler(fetch=lambda u: u, extract_links=lambda u, c: site.get(u, []))
    visited = crawler.crawl("http://a.com", max_pages=2)
    assert len(visited) == 2


def test_level_3_domain_filter() -> None:
    site = _fake_site()
    crawler = WebCrawler(fetch=lambda u: u, extract_links=lambda u, c: site.get(u, []))
    visited = crawler.crawl("http://a.com", max_pages=10, allowed_domains={"a.com"})
    assert "http://external.com" not in visited
    assert crawler.skipped_count >= 1


if __name__ == "__main__":
    test_level_1()
    test_level_1_max_pages()
    print("Level 1 OK")
    test_level_3_domain_filter()
    print("Level 3 domain filter OK")
