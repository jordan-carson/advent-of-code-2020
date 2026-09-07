package webcrawler

import "testing"

func fakeSite() map[string][]string {
	return map[string][]string{
		"http://a.com":        {"http://a.com/1", "http://a.com/2"},
		"http://a.com/1":      {"http://a.com/2", "http://a.com/3"},
		"http://a.com/2":      {},
		"http://a.com/3":      {"http://external.com"},
		"http://external.com": {},
	}
}

func TestLevel1(t *testing.T) {
	site := fakeSite()
	c := New(
		func(url string) string { return url },
		func(url, content string) []string { return site[url] },
	)
	visited := c.Crawl("http://a.com", 10, nil)
	if len(visited) == 0 || visited[0] != "http://a.com" {
		t.Fatalf("Crawl start = %v; want first element http://a.com", visited)
	}
	seen := map[string]bool{}
	for _, u := range visited {
		if seen[u] {
			t.Fatalf("Crawl visited %q twice: %v", u, visited)
		}
		seen[u] = true
	}
	if len(seen) != len(site) {
		t.Fatalf("Crawl visited %d urls; want all %d in the fake site", len(seen), len(site))
	}
}

func TestLevel1MaxPages(t *testing.T) {
	site := fakeSite()
	c := New(
		func(url string) string { return url },
		func(url, content string) []string { return site[url] },
	)
	visited := c.Crawl("http://a.com", 2, nil)
	if len(visited) != 2 {
		t.Fatalf("Crawl with maxPages=2 visited %d; want 2", len(visited))
	}
}

func TestLevel3DomainFilter(t *testing.T) {
	site := fakeSite()
	c := New(
		func(url string) string { return url },
		func(url, content string) []string { return site[url] },
	)
	visited := c.Crawl("http://a.com", 10, map[string]bool{"a.com": true})
	for _, u := range visited {
		if u == "http://external.com" {
			t.Fatalf("Crawl with allowedDomains={a.com} visited external.com: %v", visited)
		}
	}
	if c.SkippedCount < 1 {
		t.Fatalf("SkippedCount = %d; want at least 1 (external.com link filtered out)", c.SkippedCount)
	}
}
