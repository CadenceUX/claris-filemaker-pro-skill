---
name: claris-filemaker-pro
metadata:
  version: "1.2"
  last_known_fm_version: "22"
description: >
  USE THIS SKILL for ANY FileMaker Pro topic. Mandatory triggers include: any FileMaker calculation
  function (e.g. "how do I use If()", "what does ExecuteSQL return", "write a Let() calc", "fix
  this calculation"), script steps, Data API, SQL/ExecuteSQL, WebDirect, FileMaker Go, FileMaker
  security, layouts, relationships, portals, container fields, ODBC/JDBC, AI/embedding functions,
  error codes, or any other FileMaker Pro topic. When a FileMaker function name appears anywhere
  in the request — even inside code, a calc field, or a script — treat that as a mandatory trigger
  for this skill. Always consult references/function-catalog.json first for format, doc_url,
  and originated_in_version before fetching live docs. Prefer live doc fetches over training data for
  all other topics, since Claris docs are versioned and frequently updated.
---

# Claris FileMaker Pro — Skill v1.2

## Overview

The Claris Help Centre at **https://help.claris.com** is the authoritative documentation source for
all Claris/FileMaker products. This skill instructs Claude to use local reference files first, then
fetch live documentation when deeper detail is needed, rather than relying on potentially stale
training data.

For the latest FileMaker Pro release notes, see the [FileMaker Pro Release Notes](https://help.claris.com/en/pro-release-notes/content/index.html).

The frontmatter field `last_known_fm_version` records the highest FileMaker version this skill's
local reference files were built against. It is updated with each skill rebuild — it is **not** a
cap on which version you can answer questions about.

---

## Version drift detection

**Every time a live help page is fetched, check for a newer FileMaker version.**

Claris help pages include version indicators in breadcrumbs, page titles, or release note headings
(e.g. "FileMaker Pro 2026", "v23.0", "22.1", "version 23"). When fetching any page:

1. Parse the returned content for version strings higher than `last_known_fm_version` (currently
   `22`), e.g. `FileMaker Pro 2026`, `version 23`, `v23.0`, `22.1.x`.
2. If a higher version is detected, **immediately flag it** in your response:

   > Warning: **Skill version drift detected** — this page references FileMaker [X], but the local
   > reference files in this skill were last built for FM 22 (2025). New functions, script steps, or
   > behaviour changes introduced since FM 22 may not be reflected in local catalogs.
   > Consider running a skill rebuild to pick up new additions.

3. Still answer the question using the fetched content — the flag is advisory, not a blocker.
4. Do **not** flag version strings that are <= `last_known_fm_version` (e.g. references to FM 19,
   FM 21 history).

---

## Mandatory trigger: FileMaker functions and script steps

**Any request that involves a FileMaker calculation function OR script step — by name, by category,
or by describing what a calculation or script should do — MUST use this skill.**

Examples that are mandatory triggers:
- "How does `While` work?" -> check `logical-json-ai-functions-examples.md`, then `function-catalog.json`
- "Write me a Let() calculation that..." -> look up format in catalog, compose from examples
- "What's the difference between `ExecuteSQL` and `ExecuteSQLe`?" -> logical-json-ai-functions-examples.md
- "Fix this calc: `Case ( Status = \"Open\" ; ...`" -> identify functions, look each up
- "Which function returns the current record ID?" -> search catalog by purpose/category
- "How do I loop through records in a script?" -> script-steps-catalog.json (Loop, Exit Loop If)
- "Get the error code after a find" -> quickrefs.md (error codes section)
- "Sum all related line items" -> specialty-functions-examples.md (aggregate section)
- "Add 30 days to a date" -> date-time-functions-examples.md
- "List all field names on a layout" -> design-container-functions-examples.md (FieldNames)
- "Encode a container to Base64" -> design-container-functions-examples.md (container section)
- "Extract a value from a JSON response" -> logical-json-ai-functions-examples.md (JSON section)
- "What time is it in seconds?" -> date-time-functions-examples.md (time section)
- "Calculate a loan payment" -> numeric-functions-examples.md (financial section)
- "Get the sine of 45 degrees" -> numeric-functions-examples.md (trig section)
- "Convert katakana to hiragana" -> specialty-functions-examples.md (Japanese section)
- "Get GPS coordinates on FileMaker Go" -> specialty-functions-examples.md (mobile section)
- "Access the 3rd repetition of a field" -> numeric-functions-examples.md (repeating section)
- "Get a named layout object's width" -> specialty-functions-examples.md (miscellaneous section)
- Any code block containing function names or script step names

**Workflow for function questions:**
1. Check the relevant reference file (see table below) for syntax, parameters, and usage patterns
2. Open `references/function-catalog.json` for the exact format and `doc_url`
3. Use `doc_url` to `web_fetch` the live help page for authoritative parameter detail if needed
4. Answer with the format inline and cite the doc URL

**Workflow for script step questions:**
1. Check `references/script-steps-catalog.json` for syntax and `doc_url`
2. Fetch the live `doc_url` page if detailed option behaviour is needed
3. Answer with the syntax inline

---

## Step-by-step workflow (general)

1. **Identify the guide** — from `quickrefs.md` (sitemap section), find the best-matching guide
   slug and the most relevant page URL(s).
2. **For function questions** — check the relevant example file first, then `function-catalog.json`
   for format + doc_url, then fetch the live page for examples and edge cases.
3. **For script step questions** — check `script-steps-catalog.json` first, then fetch live page.
4. **Fetch the index** (if unsure which page) — `web_fetch` the guide's `index.html` to read
   the full table of contents from the sidebar, then identify the specific page(s).
5. **Fetch the specific page(s)** — `web_fetch` each relevant page. For technical topics, fetch
   2-4 pages if they are clearly related.
6. **Answer from the fetched content** — synthesise an accurate, direct answer. Include the
   doc URL(s) as a reference.

---

## URL patterns

All Claris Help pages follow this pattern:

```
https://help.claris.com/en/{guide-slug}/content/{page-slug}.html
```

Guide index pages are always:
```
https://help.claris.com/en/{guide-slug}/content/index.html
```

---

## Reference files — all 10

| File | Contains |
|---|---|
| `function-catalog.json` | All 360 functions — format, parameters, purpose, category, category_url, slug, doc_url, originated_in_version. Master for call signatures. |
| `script-steps-catalog.json` | All 155 script steps across 14 categories — syntax, purpose, doc_url. Includes AI steps (FM 2025 v22 names). |
| `logical-json-ai-functions-examples.md` | **Logical** (20 functions: If, Case, Let, While, ExecuteSQL, ExecuteSQLe, Evaluate, GetField, GetNthRecord…) + **JSON** (10 functions: JSONGetElement, JSONSetElement, JSONListKeys, JSONMakeArray…) + **AI** (14 functions: GetEmbedding, CosineSimilarity, GetTokenCount, GetTableDDL, GetRAGSpaceInfo…) |
| `get-functions-examples.md` | All 135 Get() functions grouped by 12 categories: Date/Time, Account, File, Paths, Record, Layout/Window, Script/Trigger, Field, Sorting, Network, Device, Calculation |
| `design-container-functions-examples.md` | **Design** (23 functions: FieldNames, FieldType, LayoutNames, TableNames, ValueListItems, ScriptNames, BaseTableIDs…) + **Container** (24 functions: Base64Encode/Decode, CryptEncrypt/Decrypt, CryptDigest, GetContainerAttribute, GetLiveText, ReadQRCode…) |
| `text-functions-examples.md` | **Text** (39 functions: Left, Right, Middle, Position, Substitute, PatternCount, Trim, Filter…) + **Text Formatting** (10 functions: TextColor, TextSize, TextFont, TextStyleAdd…) |
| `date-time-functions-examples.md` | **Date** (10 functions: Date, Day, Month, Year, DayOfWeek, DayName, MonthName, WeekOfYear…) + **Time & Timestamp** (5 functions: Hour, Minute, Seconds, Time, Timestamp) |
| `numeric-functions-examples.md` | **Number** (18 functions: Round, Int, Mod, Abs, Ceiling, Floor, Random…) + **Financial** (4: FV, NPV, PMT, PV) + **Trigonometric** (9: Sin, Cos, Tan, Asin, Acos, Atan, Degrees, Radians, Pi) + **Repeating** (3: Extend, GetRepetition, Last) |
| `specialty-functions-examples.md` | **Aggregate** (10: Sum, Count, Average, List, Max, Min, StDev…) + **Japanese** (12: Hiragana, Katakana, NumToJText, Furigana, YearName…) + **Mobile/Go** (5: Location, LocationValues, GetSensor, GetAVPlayerAttribute, RangeBeacons) + **Miscellaneous** (9: GetLayoutObjectAttribute, GetFieldName, ConvertFromFileMakerPath, LayoutObjectUUID…) |
| `quickrefs.md` | **Error codes** (0-899 + 1630-1631, AI/ML errors 870-892 verified against live docs 2026-06) + **ExecuteSQL** syntax, clauses, data types, date literals + **Data API** REST endpoints, auth, CRUD, find, portal data + **Sitemap** of all Claris Help guides and URL patterns |

---

## Fetching strategy — which file to check first

| Topic | Check first | Then |
|---|---|---|
| Logical / Case / Let / While / ExecuteSQL | `logical-json-ai-functions-examples.md` | `function-catalog.json` → live doc |
| JSON functions | `logical-json-ai-functions-examples.md` | `function-catalog.json` → live doc |
| AI / embedding functions | `logical-json-ai-functions-examples.md` | `function-catalog.json` → live doc |
| Get() functions | `get-functions-examples.md` | `function-catalog.json` → live doc |
| Design / FieldNames / LayoutNames | `design-container-functions-examples.md` | `function-catalog.json` → live doc |
| Container / Base64 / Crypt / OCR | `design-container-functions-examples.md` | `function-catalog.json` → live doc |
| Text / Substitute / PatternCount | `text-functions-examples.md` | `function-catalog.json` → live doc |
| Text formatting / TextColor | `text-functions-examples.md` | `function-catalog.json` → live doc |
| Date functions | `date-time-functions-examples.md` | `function-catalog.json` → live doc |
| Time / Timestamp | `date-time-functions-examples.md` | `function-catalog.json` → live doc |
| Number / Round / Mod / Random | `numeric-functions-examples.md` | `function-catalog.json` → live doc |
| Financial / PMT / NPV | `numeric-functions-examples.md` | `function-catalog.json` → live doc |
| Trigonometric / Sin / Cos / GPS | `numeric-functions-examples.md` | `function-catalog.json` → live doc |
| Repeating fields | `numeric-functions-examples.md` | `function-catalog.json` → live doc |
| Aggregate / Sum / Count / List | `specialty-functions-examples.md` | `function-catalog.json` → live doc |
| Japanese text functions | `specialty-functions-examples.md` | `function-catalog.json` → live doc |
| FileMaker Go / mobile | `specialty-functions-examples.md` | `function-catalog.json` → live doc |
| Miscellaneous / GetLayoutObjectAttribute | `specialty-functions-examples.md` | `function-catalog.json` → live doc |
| Script steps | `script-steps-catalog.json` | live doc_url |
| Error codes | `quickrefs.md` | live error-codes.html for obscure codes |
| ExecuteSQL syntax | `quickrefs.md` | live sql-reference guide |
| Data API / REST | `quickrefs.md` | live data-api-guide |
| Finding a help page URL | `quickrefs.md` (sitemap section) | fetch guide index.html |

Use `html_extraction_method: markdown` in web_fetch for clean output.

---

## Tips

- The sidebar on any help page lists the **complete navigation tree** for that guide — very useful
  for discovering related pages.
- `function-catalog.json` is the master for function formats; example files are the master for usage patterns.
- For script step option details (platform support on Go, WebDirect, Server) always fetch the live
  doc_url — platform restrictions are not fully captured in the catalog.
- AI/embedding functions are in `logical-json-ai-functions-examples.md`; AI script steps are in
  `script-steps-catalog.json` (AI category: 14 steps including Generate Response from Model, Configure AI Account, Perform SQL Query by Natural Language, Perform Find by Natural Language, Insert Embedding, etc.).
- **Error codes:** The AI/ML error range (870–892) in `quickrefs.md` is verified against live docs (2026-06). The general error tables (0–899, 1630–1631) are a good quick reference but descriptions may drift — always fetch `https://help.claris.com/en/pro-help/content/error-codes.html` for authoritative descriptions of any unfamiliar code.
- **Mobile functions** (Location, GetSensor, RangeBeacons, GetAVPlayerAttribute, LocationValues) only
  work in FileMaker Go. Always advise checking platform with `Get(ApplicationVersion)` before use.
- **Japanese functions** require Japanese language support in FileMaker. `Furigana()` relies on the
  Japanese IME and may produce different results based on context.
- **Trig functions** all work in radians — use `Degrees()` and `Radians()` to convert. The Haversine
  GPS distance formula in `numeric-functions-examples.md` is a ready-to-use real-world example.
- **Financial functions** require `interestRate` per period, not annual — divide annual rate by
  payment frequency (12 for monthly). `PMT()` returns a negative number; use `Abs()` for display.

---

## Licence

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Version history

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
