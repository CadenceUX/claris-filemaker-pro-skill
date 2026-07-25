#!/usr/bin/env python3
"""Extract authoritative step/function facts from harvested pages.

Roster is determined STRUCTURALLY, not from `topic_type` — Claris mislabels
4 pages as `conceptual` (set-dictionary, getpersistentdata,
listpersistentdataids, get-systemstorageavailable). Verified 2026-07-25.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
PRODUCTS = ["FileMaker Pro", "FileMaker Go", "FileMaker WebDirect",
            "FileMaker Server", "FileMaker Cloud", "FileMaker Data API",
            "Custom Web Publishing"]
SHORT = {"FileMaker Pro": "Pro", "FileMaker Go": "Go",
         "FileMaker WebDirect": "WebDirect", "FileMaker Server": "Server",
         "FileMaker Cloud": "Cloud", "FileMaker Data API": "DataAPI",
         "Custom Web Publishing": "CWP"}

# Claris topic_type errors — reclassified by page structure. Verified 2026-07-25.
MISLABELLED = {
    "set-dictionary": "script-step-reference",
    "getpersistentdata": "function-reference",
    "listpersistentdataids": "function-reference",
    "get-systemstorageavailable": "function-reference",
}


def sec(text, name):
    m = re.search(rf'^##\s+{re.escape(name)}\s*\n+(.*?)(?=\n##\s|\Z)', text, re.S | re.M)
    return m.group(1).strip() if m else None


def load(slug):
    p = os.path.join(PAGES, slug + ".md")
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None


def main():
    h = json.load(open(os.path.join(HERE, "harvest.json")))
    by_slug = {r["slug"]: r for r in h}
    for s, tt in MISLABELLED.items():
        if s in by_slug:
            by_slug[s]["topic_type"] = tt
            by_slug[s]["_reclassified"] = True

    steps, funcs = [], []
    for r in by_slug.values():
        t = load(r["slug"])
        if not t:
            continue
        if r["topic_type"] == "script-step-reference":
            compat = {SHORT[k]: v for k, v in r["compatibility"].items()}
            # delta encoding: only record non-"Yes" products
            exc = {k: v for k, v in compat.items() if v != "Yes"}
            steps.append({
                "name": r["title"],
                "slug": r["slug"],
                "originated_in_version": r["originated_in_version"],
                "platform_full": compat,
                "platform_exceptions": exc,
                "options": sec(t, "Options"),
                "reclassified": r.get("_reclassified", False),
            })
        elif r["topic_type"] == "function-reference":
            funcs.append({
                "name": r["title"],
                "slug": r["slug"],
                "format": (sec(t, "Format") or "").strip(),
                "return_type": (sec(t, "Data type returned") or "").strip(),
                "originated_in_version": r["originated_in_version"],
                "reclassified": r.get("_reclassified", False),
            })

    steps.sort(key=lambda x: x["name"] or "")
    funcs.sort(key=lambda x: x["name"] or "")
    out = {"steps": steps, "functions": funcs}
    json.dump(out, open(os.path.join(HERE, "facts.json"), "w"), indent=1)

    print(f"steps={len(steps)} functions={len(funcs)}")
    print(f"steps with full 7-product compat: "
          f"{sum(1 for s in steps if len(s['platform_full']) == 7)}")
    print(f"steps supported everywhere (no exceptions): "
          f"{sum(1 for s in steps if not s['platform_exceptions'])}")
    print(f"functions with return_type: {sum(1 for f in funcs if f['return_type'])}")
    from collections import Counter
    print("\nreturn_type distribution:")
    for k, v in Counter(f["return_type"] for f in funcs).most_common(12):
        print(f"  {k!s:28} {v}")


if __name__ == "__main__":
    main()
