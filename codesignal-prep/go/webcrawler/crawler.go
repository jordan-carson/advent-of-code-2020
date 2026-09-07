// Package webcrawler is a starter for the web crawler problem.
// See ../../problems/web_crawler/README.md for the full spec.
//
// Fetch and link extraction are injected as functions rather than doing
// real HTTP/HTML parsing, so tests stay deterministic and offline -- the
// crawling logic is what's under test.
package webcrawler

import "time"

type Crawler struct {
	Fetch             func(url string) string
	ExtractLinks      func(url, content string) []string
	RequestsPerSecond float64 // 0 means unlimited
	Sleep             func(time.Duration)
	Now               func() time.Time
	SkippedCount      int // for Level 3
}

func New(fetch func(string) string, extractLinks func(string, string) []string) *Crawler {
	return &Crawler{
		Fetch:        fetch,
		ExtractLinks: extractLinks,
		Sleep:        time.Sleep,
		Now:          time.Now,
	}
}

// --- Level 1 ---

// Crawl does a BFS from startURL, visiting each unique URL at most once,
// up to maxPages pages, returning visited URLs in visit order.
// allowedDomains is optional (Level 3): nil means all domains allowed.
func (c *Crawler) Crawl(startURL string, maxPages int, allowedDomains map[string]bool) []string {
	panic("not implemented")
}

// --- Level 4 ---

// CrawlDistributed simulates numWorkers workers pulling from one shared
// frontier queue, with the same one-visit-per-URL guarantee as Level 1,
// now across multiple seeds.
func (c *Crawler) CrawlDistributed(startURLs []string, maxPages int, numWorkers int) []string {
	panic("not implemented")
}
