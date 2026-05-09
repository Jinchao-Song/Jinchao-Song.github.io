import requests
import re
import sys

AUTHOR_ID = "28394161"  # semanticscholar.org/author/Jinchao-Song/28394161

def get_scholar_stats(author_id):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}"
    params = {"fields": "citationCount,hIndex,paperCount,name"}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    citations = data.get("citationCount", 0)
    h_index = data.get("hIndex", 0)
    name = data.get("name", "")
    print(f"Fetched: {name} | Citations={citations} | h-index={h_index}")
    return citations, h_index

def update_html(citations, h_index):
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update animateCounter JS call
    html = re.sub(
        r"(animateCounter\(document\.getElementById\('citationCounter'\),\s*)\d+",
        rf"\g<1>{citations}",
        html
    )

    # 2. Update h-index stat-num span
    html = re.sub(
        r'(<span class="stat-num">)\d+(</span>\s*<span class="stat-label">h-index)',
        rf'\g<1>{h_index}\2',
        html
    )

    # 3. Update i10-index stat-num span
    html = re.sub(
        r'(<span class="stat-num">)\d+(</span>\s*<span class="stat-label">i10-index)',
        rf'\g<1>{h_index}\2',
        html
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done: citations={citations}, h-index={h_index}")

if __name__ == "__main__":
    try:
        citations, h_index = get_scholar_stats(AUTHOR_ID)
        update_html(citations, h_index)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
