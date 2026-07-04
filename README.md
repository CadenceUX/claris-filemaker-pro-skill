# claris-filemaker-pro-skill

A [Claude skill](https://docs.claude.ai/skills) for Claris FileMaker Pro development. Gives Claude accurate, version-aware knowledge of every FileMaker calculation function, script step, error code, and help centre URL — without relying on potentially stale training data.

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).

---

## What it does

When this skill is active, Claude will:

- Look up any of the **368 calculation functions** by name, category, or description — with correct syntax, parameters, and a direct link to the Claris Help Centre page
- Look up any of the **215 script steps** across 16 categories, including all FM 2025 v22 AI steps, FM 26 AI additions, and the new FM 26 PDF Files and Persistent Data categories
- Reference **accurate error codes** (0–899, 1630–1631, AI/ML 870–892) with official descriptions
- Fetch **live Claris documentation** using the correct URL pattern for any of the 33 help guides
- Detect **version drift** — if a fetched page's "Originated in version" is newer than the FileMaker version the skill was built against, it flags it so you know the local reference files may be behind
- Route intelligently across **ExecuteSQL**, **Data API**, **Admin API**, **OData**, **WebDirect**, **FileMaker Go**, **FileMaker Server**, and **Claris MCP** topics

---

## Coverage

| Reference file | Contents |
|---|---|
| `function-catalog.json` | All 368 functions through FM 26 — format, parameters, purpose, category, doc_url, originated_in_version. Includes 8 FM 26 additions: BaseTableComment, FieldAnnotation, FieldDisplayNames (Design); Get(AccountPasswordDaysRemaining), Get(GuidedAccessState), Get(WindowUUID) (Get); GetPersistentData, ListPersistentDataIDs (Persistent Data). |
| `script-steps-catalog.json` | All 215 script steps through FM 26 across 16 categories — syntax, purpose, doc_url, and full notes for all FM 22 AI steps and FM 26 additions. New FM 26 categories: PDF Files (7 steps), Persistent Data (1 step). |
| `logical-json-ai-functions-examples.md` | Logical (20), JSON (10), AI/embedding (14) functions with usage examples |
| `get-functions-examples.md` | All 138 Get() functions across 12 categories (includes FM 26 Get additions) |
| `design-container-functions-examples.md` | Design (26, includes FM 26 additions) + Container/Crypt/OCR (24) functions |
| `text-functions-examples.md` | Text (39) + Text Formatting (10) functions |
| `date-time-functions-examples.md` | Date (10) + Time/Timestamp (5) functions |
| `numeric-functions-examples.md` | Number (18) + Financial (4) + Trigonometric (9) + Repeating (3) |
| `specialty-functions-examples.md` | Aggregate (10) + Japanese (12) + Mobile/Go (5) + Miscellaneous (9) + Persistent Data (2 FM 26 functions) |
| `quickrefs.md` | Error codes, ExecuteSQL syntax, Data API endpoints, full help centre sitemap (33 guides) |

**FileMaker version coverage:** Functions tagged from `legacy` (pre-FM7) through `26` (FM Pro 26, June 2026). Script steps current through FM 26 — 215 unique steps in local catalog across 16 categories.

---

## Installation

1. Download the latest release zip from the [Releases](../../releases) page
2. Unzip and place the `claris-filemaker-pro` folder in your Claude skills directory:
   - **macOS:** `~/Library/Application Support/Claude/skills/`
   - **Windows:** `%APPDATA%\Claude\skills\`
3. Restart Claude or reload skills

The skill is then active for any conversation where you're working on FileMaker topics.

---

## How it works

The skill uses a **local-first, live-verify** strategy:

1. **Local reference files** answer common questions instantly — function syntax, script step options, error code meanings
2. **Live doc fetches** (`web_fetch` with `html_extraction_method: markdown`) fill in detail that the local files don't carry — full parameter descriptions, platform restrictions, edge cases
3. **Version drift detection** compares each fetched page's "Originated in version" value against `last_known_fm_version` (stored in the catalogs' `meta` block) and warns you if the local files may be behind — the pages' YAML frontmatter `version:` field tracks the doc build, not the FileMaker release, so it is not used

This means you get fast, accurate answers for everyday questions, and authoritative live-doc answers for anything nuanced — without Claude hallucinating function signatures or inventing error code meanings.

All functions and script steps — including FM 26 additions — are handled identically: check local first, then fetch the live doc_url if full parameter detail is needed. There is no special-case routing for any version.

---

## Keeping it current

The skill's `last_known_fm_version` (recorded in both catalogs' `meta` block) is `26` (FM Pro 26, released June 2026).

When a new FileMaker release ships:
1. The version drift detector will flag it on the first live doc fetch that references the new version
2. A skill rebuild picks up new functions, renamed script steps, and updated error codes
3. A new release is tagged here with updated reference files

Watch this repo or check the [Releases](../../releases) page to stay current.

---

## Contributing

Issues and PRs welcome — particularly:
- Corrections to `originated_in_version` values in `function-catalog.json`
- Missing or renamed script steps
- New error codes
- Stale help centre URLs

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use, adapt, and redistribute with attribution.
