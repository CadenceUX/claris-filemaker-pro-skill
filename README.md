# claris-filemaker-pro-skill

A [Claude skill](https://docs.claude.ai/skills) for Claris FileMaker Pro development. Gives Claude accurate, version-aware knowledge of every FileMaker calculation function, script step, error code, and help centre URL — without relying on potentially stale training data.

Built and maintained by [Cadence UX](https://cadenceux.com.au).

---

## What it does

When this skill is active, Claude will:

- Look up any of the **360 calculation functions** by name, category, or description — with correct syntax, parameters, and a direct link to the Claris Help Centre page
- Look up any of the **155 script steps** across 14 categories, including all FM 2025 v22 AI steps
- Reference **accurate error codes** (0–899, 1630–1631, AI/ML 870–892) with official descriptions
- Fetch **live Claris documentation** using the correct URL pattern for any of the 33 help guides
- Detect **version drift** — if a fetched page references a newer FileMaker version than the skill was built against, it flags it so you know the local reference files may be behind
- Route intelligently across **ExecuteSQL**, **Data API**, **Admin API**, **OData**, **WebDirect**, **FileMaker Go**, **FileMaker Server**, and **Claris MCP** topics

---

## Coverage

| Reference file | Contents |
|---|---|
| `function-catalog.json` | All 360 functions — format, parameters, purpose, category, doc_url, originated_in_version |
| `script-steps-catalog.json` | All 157 script steps across 14 categories — syntax, purpose, doc_url, and full notes for all FM 22 AI steps, Go to List of Records (FM 22.0.1), and Set Revert Transaction on Error (FM 21.1.1) |
| `logical-json-ai-functions-examples.md` | Logical (20), JSON (10), AI/embedding (14) functions with usage examples |
| `get-functions-examples.md` | All 135 Get() functions across 12 categories |
| `design-container-functions-examples.md` | Design (23) + Container/Crypt/OCR (24) functions |
| `text-functions-examples.md` | Text (39) + Text Formatting (10) functions |
| `date-time-functions-examples.md` | Date (10) + Time/Timestamp (5) functions |
| `numeric-functions-examples.md` | Number (18) + Financial (4) + Trigonometric (9) + Repeating (3) |
| `specialty-functions-examples.md` | Aggregate (10) + Japanese (12) + Mobile/Go (5) + Miscellaneous (9) |
| `quickrefs.md` | Error codes, ExecuteSQL syntax, Data API endpoints, full help centre sitemap (33 guides) |

**FileMaker version coverage:** Functions tagged from `legacy` (pre-FM7) through `22.0.1` (FM 2025 v22). Script steps current as of FM 2025 v22.0.1 (157 steps). FM 26 additions require live doc fetch — see SKILL.md for details.

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
3. **Version drift detection** watches for FileMaker version strings in fetched pages that exceed `last_known_fm_version` and warns you if the local files may be behind

This means you get fast, accurate answers for everyday questions, and authoritative live-doc answers for anything nuanced — without Claude hallucinating function signatures or inventing error code meanings.

---

## Keeping it current

The skill's `last_known_fm_version` is `26` (FM Pro 26, released June 2026).

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
