import requests
import sys

url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {
    "query": "domain adaptation channel estimation wireless",
    "limit": 15,
    "fields": "title,year,citationCount,venue,authors,abstract,externalIds"
}

resp = requests.get(url, params=params, timeout=15)
if resp.status_code == 200:
    data = resp.json()
    papers = data.get("data", [])
    print(f"Semantic Scholar returned: {len(papers)}")
    for i, p in enumerate(papers):
        title = p.get("title")
        year = p.get("year")
        cites = p.get("citationCount")
        venue = p.get("venue")
        authors = ", ".join([a.get("name", "") for a in p.get("authors", [])][:3])
        safe_str = f"[{i+1}] ({year}) {title} | Cites: {cites} | {venue} | Authors: {authors}"
        sys.stdout.buffer.write((safe_str + "\n").encode("utf-8", errors="replace"))
else:
    print(f"Status: {resp.status_code}, {resp.text[:200]}")
