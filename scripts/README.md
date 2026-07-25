# Rebuild scripts — maintainer tools

These scripts regenerate this skill's reference catalogs from live Claris documentation. They
are **maintainer tools for the developer to run**, not something the skill executes during a
conversation. They need a local Python 3 environment and network access, so they run from
Claude Code, a code-execution-enabled session, or a plain terminal — not from a standard
Claude.ai chat.

## Why they exist

The catalogs are only as trustworthy as their last verification. Re-deriving from source each
release is what keeps the coverage claims ("all 368 functions", "all 216 script steps") honest,
rather than inheriting the previous version's counts.

## Running a rebuild

```bash
# 1. Fetch the authoritative page enumeration
curl -s --compressed https://help.claris.com/llms-full.txt -o llms-full.txt

# 2. Harvest every en/pro-help page (~1,100 pages, ~30s at 12-way parallelism)
python3 rebuild_harvest.py

# 3. Extract structured facts -> facts.json
python3 rebuild_extract.py
```

`rebuild_harvest.py` writes `pages/` and `harvest.json`. `rebuild_extract.py` writes
`facts.json` with one record per script step and per function.

## The two traps these scripts encode

**1. `topic_type` is unreliable.** Claris mislabels at least four reference pages as
`topic_type: conceptual` — `set-dictionary`, `getpersistentdata`, `listpersistentdataids` and
`get-systemstorageavailable`. A `topic_type` sweep alone undercounts the roster and previously
caused a real script step to be omitted from this skill entirely. `rebuild_extract.py` carries
an explicit reclassification map and determines the roster **structurally** (a step page has a
`## Compatibility` table; a function page has `## Format` and `## Data type returned`).

Re-check that map on each rebuild — if Claris fixes the labelling, entries in `MISLABELLED`
become redundant, and if they mislabel new pages the structural sweep in the harvest output
will reveal them.

**2. Frontmatter `version:` is not a feature-release signal.** It tracks the documentation
build. Use the `## Originated in version` section in the page body instead.

## After a rebuild

Diff the new `facts.json` against the shipped catalogs before committing. Expect the diff to be
small; investigate anything that isn't. Then update:

- `meta.verified_on` in each catalog
- `meta.step_count` / `meta.function_count`
- `VERSION`, `metadata.version` in SKILL.md, and CHANGELOG.md — all three must match
