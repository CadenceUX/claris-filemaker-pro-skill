#!/usr/bin/env python3
"""Harvest en/pro-help pages from help.claris.com and extract structured facts.

Deterministic: no model involvement. Pages are fetched verbatim and parsed with
regex against the fixed Claris markdown structure (YAML frontmatter, `# Title`,
`## Compatibility` table, `## Originated in version`).
"""
import re, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
os.makedirs(PAGES, exist_ok=True)

PRODUCTS = ["FileMaker Pro", "FileMaker Go", "FileMaker WebDirect",
            "FileMaker Server", "FileMaker Cloud", "FileMaker Data API",
            "Custom Web Publishing"]


def urls_from_sitemap(path):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.search(r'\((https://help\.claris\.com/markdown/en/pro-help/([^)]+)\.md)\)', line)
        if m:
            out.append((m.group(2), m.group(1)))
    return sorted(set(out))


def fetch(job, retries=3):
    slug, url = job
    dest = os.path.join(PAGES, slug.replace("/", "__") + ".md")
    if os.path.exists(dest) and os.path.getsize(dest) > 100:
        return slug, True
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "claris-filemaker-pro-skill-rebuild/2.0"})
            data = urllib.request.urlopen(req, timeout=45).read()
            open(dest, "wb").write(data)
            return slug, True
        except Exception:
            time.sleep(1.5 * (a + 1))
    return slug, False


def parse(slug):
    p = os.path.join(PAGES, slug.replace("/", "__") + ".md")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8", errors="replace").read()

    fm = {}
    mfm = re.match(r'^---\s*\n(.*?)\n---\s*\n', t, re.S)
    if mfm:
        for line in mfm.group(1).split("\n"):
            mk = re.match(r'^(\w+):\s*(.*)$', line)
            if mk:
                fm[mk.group(1)] = mk.group(2).strip().strip('"')

    title = re.search(r'^# (.+?)\s*$', t, re.M)

    compat = {}
    mc = re.search(r'##\s*Compatibility\s*\n+((?:\|[^\n]*\n)+)', t)
    if mc:
        for row in mc.group(1).strip().split("\n"):
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0] in PRODUCTS:
                compat[cells[0]] = cells[1]

    orig = re.search(r'##\s*Originated in version\s*\n+(.+?)\s*$', t, re.M)

    opts = None
    mo = re.search(r'##\s*Options\s*\n+(.*?)(?=\n##\s|\Z)', t, re.S)
    if mo:
        opts = mo.group(1).strip()

    return {
        "slug": slug,
        "title": title.group(1).strip() if title else None,
        "topic_type": fm.get("topic_type"),
        "doc_title": fm.get("title"),
        "compatibility": compat,
        "originated_in_version": orig.group(1).strip() if orig else None,
        "has_options": bool(opts),
        "options_raw": opts,
        "url": fm.get("url"),
        "bytes": os.path.getsize(p),
    }


if __name__ == "__main__":
    jobs = urls_from_sitemap(os.path.join(HERE, "llms-full.txt"))
    print(f"enumerated {len(jobs)} en/pro-help pages", file=sys.stderr)
    t0 = time.time()
    ok = fail = 0
    with ThreadPoolExecutor(max_workers=12) as ex:
        for slug, good in ex.map(fetch, jobs):
            ok += good
            fail += (not good)
    print(f"fetched ok={ok} fail={fail} in {time.time()-t0:.1f}s", file=sys.stderr)

    recs = [r for r in (parse(s) for s, _ in jobs) if r]
    json.dump(recs, open(os.path.join(HERE, "harvest.json"), "w"), indent=1)
    print(f"parsed {len(recs)} -> harvest.json", file=sys.stderr)

    from collections import Counter
    print("\ntopic_type census:", file=sys.stderr)
    for k, v in Counter(r["topic_type"] for r in recs).most_common():
        print(f"  {k!s:24} {v}", file=sys.stderr)
    print(f"\npages with Compatibility table: "
          f"{sum(1 for r in recs if r['compatibility'])}", file=sys.stderr)
