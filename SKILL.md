---
name: claris-filemaker-pro
metadata:
  version: "1.8"
  last_known_fm_version: "26"
description: >
  REFERENCE skill — FileMaker Pro script steps, calculation functions, and custom functions ONLY.
  Use for: syntax lookups, function parameters, usage examples, and live doc fetches across all
  376 built-in functions (If, Case, Let, While, ExecuteSQL, JSON, AI/embedding, Persistent Data),
  all 165 script steps (including FM 26 PDF Files and Persistent Data categories), Data API (REST),
  SQL/ExecuteSQL, WebDirect, FileMaker Go, error codes, and custom function patterns. Not a platform
  administration guide. Out of scope: FileMaker Server admin, Claris Connect, Claris Studio,
  ODBC/JDBC deep configuration. Trigger on any FileMaker function name — even inside code, a calc
  field, or a script. Always check local reference files first for format, doc_url, and
  originated_in_version before fetching live docs. Prefer live doc fetches over training data —
  Claris docs are versioned and frequently updated.
---

# Claris FileMaker Pro — Skill v1.8

## Overview

This is a **reference-only** skill covering FileMaker Pro **script steps**, **calculation functions**,
and **custom functions**. It is not a general FileMaker Pro assistant and does not cover platform
administration, server configuration, or Claris Connect workflows.

The Claris Help Centre at **https://help.claris.com** is the authoritative documentation source.
This skill instructs Claude to use local reference files first, then fetch live documentation
when deeper detail is needed, rather than relying on potentially stale training data.

For the latest FileMaker Pro release notes, see the [FileMaker Pro Release Notes](https://help.claris.com/markdown/en/pro-release-notes/index.md).

The frontmatter field `last_known_fm_version` records the highest FileMaker version this skill's
local reference files were built against. It is updated with each skill rebuild — it is **not** a
cap on which version you can answer questions about.

---

## Version drift detection

**Every time a live help page is fetched, check for version drift using frontmatter.**

Every `.md` help page returns structured YAML at the top:

```yaml
version: 26
version_year: 2026
```

When fetching any page:

1. Parse `version:` from the frontmatter of the returned `.md` page.
2. Compare with `last_known_fm_version` (currently `26`).
3. If the page frontmatter `version` is higher than `last_known_fm_version`, **immediately flag it**:

   > ⚠️ **Skill version drift detected** — this page references FM [X], but the local reference
   > files in this skill were last built for FM 26 (2026). New functions, script steps, or behaviour
   > changes introduced since FM 26 may not be reflected in local catalogs.
   > Consider running a skill rebuild to pick up new additions.

4. Still answer the question using the fetched content — the flag is advisory, not a blocker.
5. Do **not** flag versions that are ≤ `last_known_fm_version`.

---

## Version self-check

At the start of each session — on the first FileMaker question in the conversation — run this
check once:

1. Fetch `https://github.com/CadenceUX/claris-filemaker-pro-skill/raw/main/VERSION`
2. Parse the returned string as the latest available version
3. Compare with this skill's installed version (currently `"1.8"`)
4. If latest > installed, prepend this notice to your first response:

   > ⚠️ **Skill update available**
   > This skill is v[installed]. v[latest] is available at
   > https://github.com/CadenceUX/claris-filemaker-pro-skill/releases
   > Update your local skill files to get the latest FM coverage.

5. Do not repeat the notice again in the same session.
6. If the fetch fails or returns an unexpected value, skip silently — do not surface the error.

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
- "Parse and reuse JSON multiple times" -> logical-json-ai-functions-examples.md (JSONParse section)
- "What time is it in seconds?" -> date-time-functions-examples.md (time section)
- "Calculate a loan payment" -> numeric-functions-examples.md (financial section)
- "Get the sine of 45 degrees" -> numeric-functions-examples.md (trig section)
- "Convert katakana to hiragana" -> specialty-functions-examples.md (Japanese section)
- "Get GPS coordinates on FileMaker Go" -> specialty-functions-examples.md (mobile section)
- "Access the 3rd repetition of a field" -> numeric-functions-examples.md (repeating section)
- "Get a named layout object's width" -> specialty-functions-examples.md (miscellaneous section)
- Any code block containing function names or script step names
- "Predict a value from a trained model" → `logical-json-ai-functions-examples.md` (PredictFromModel)
- "Get IDs from found set" → `specialty-functions-examples.md` (GetRecordIDsFromFoundSet)
- "Restore a found set I saved earlier" → `script-steps-catalog.json` (Go to List of Records)
- "Fine-tune a model from my data" → `script-steps-catalog.json` (Fine-Tune Model)
- "Combine two embedding vectors" → `logical-json-ai-functions-examples.md` (AddEmbeddings)
- "Set up a RAG account" → `script-steps-catalog.json` (Configure RAG Account)
- "Control transaction revert on error" → `script-steps-catalog.json` (Set Revert Transaction on Error)
- "Get text out of a PDF in a container" → `design-container-functions-examples.md` (GetTextFromPDF)
- "Caption this image with AI" → `script-steps-catalog.json` (AI category — Insert Image Caption)
- "Caption all images in found set" → `script-steps-catalog.json` (AI category — Insert Image Captions in Found Set)
- "Clear web viewer cookies" → `script-steps-catalog.json` (Miscellaneous — Flush Web Viewer Cookies)
- "Save persistent data / app variable" → `script-steps-catalog.json` (Persistent Data — Configure Persistent Data); `specialty-functions-examples.md` (GetPersistentData, ListPersistentDataIDs)
- "Create / build / merge a PDF in script" → `script-steps-catalog.json` (PDF Files category)
- "Print a PDF from a container" → `script-steps-catalog.json` (PDF Files — Print PDF)
- "Get the annotation on a field" → `design-container-functions-examples.md` (FieldAnnotation)
- "Get display names for a field" → `design-container-functions-examples.md` (FieldDisplayNames)
- "Get base table comment" → `design-container-functions-examples.md` (BaseTableComment)
- "Is Guided Access on?" → `get-functions-examples.md` (Get(GuidedAccessState), Device section)
- "Password expiry / days remaining" → `get-functions-examples.md` (Get(AccountPasswordDaysRemaining), Account section)
- "Get the window UUID" → `get-functions-examples.md` (Get(WindowUUID), Layout & Window section)

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

1. **Identify the guide** — from `quickrefs.md` (sitemap section) as a fast-path shortcut, or from
   `https://help.claris.com/llms-full.txt` for any URL that is unknown or needs confirming.
2. **For function questions** — check the relevant example file first, then `function-catalog.json`
   for format + doc_url, then fetch the live page for examples and edge cases.
3. **For script step questions** — check `script-steps-catalog.json` first, then fetch live page.
4. **Fetch the index** (if unsure which page) — `web_fetch` the guide's `index.md` to read
   the full table of contents from the sidebar, then identify the specific page(s).
5. **Fetch the specific page(s)** — `web_fetch` each relevant page. For technical topics, fetch
   2–4 pages if they are clearly related.
6. **Answer from the fetched content** — synthesise an accurate, direct answer. Include the
   doc URL(s) as a reference.

---

## URL patterns

All Claris Help pages are available as clean Markdown at this pattern:

```
https://help.claris.com/markdown/en/{guide-slug}/{page-slug}.md
```

Guide index pages:
```
https://help.claris.com/markdown/en/{guide-slug}/index.md
```

The `.md` endpoints return native Markdown — no `html_extraction_method` needed in `web_fetch`.

---

## Live sitemap

When a page URL is unknown, a guide slug needs confirming, a page is not found at its expected
path, or version drift is suspected:

- **`https://help.claris.com/llms-full.txt`** — canonical live sitemap; complete per-page
  enumeration across all 12 locales (~18,988 pages). Fetch this to scan for new guides or
  confirm any URL.
- **`https://help.claris.com/llms.txt`** — curated product landing page index; faster for
  finding a guide's root URL when you don't need the full page list.

The sitemap section in `quickrefs.md` is a fast-path shortcut for known common pages — useful
for quick lookups but not authoritative. When in doubt, fetch `llms-full.txt`.

---

## Local vs live — decision rules

### Use local data

| Situation | Source |
|---|---|
| Function syntax and call format | `function-catalog.json` is authoritative |
| `originated_in_version` lookups | Local catalog only |
| Common error codes (quick lookup) | `quickrefs.md` sufficient |
| Script step name and basic syntax | `script-steps-catalog.json` |

### Always fetch live

| Situation | Reason |
|---|---|
| `originated_in_version` is FM 19.3 or later | Docs may have been updated post-release |
| Any AI/ML function or script step, any version | Rapidly evolving — local files lag |
| Platform compatibility (Go, WebDirect, Server, Data API) | Restrictions change between point releases |
| User mentions "latest", "current", a specific version, or "has this changed" | Explicit recency signal |
| Version drift detected in this session | Local files are behind |
| Exact parameter behaviour, option names, or restrictions | Claris updates docs within a version without bumping the version number — local files capture a point in time only |

---

## Automatic version notes

When answering a function or script step question, read `originated_in_version` from the catalog
and inject the appropriate version note automatically — do not ask the user which version they are on.

| `originated_in_version` | Note to inject |
|---|---|
| FM 19.3 – FM 20 | "Requires FM 19.3+. If you're on an earlier version, [describe fallback if one exists]." |
| FM 21.0.1 | "AI/embedding feature — requires FM 21 or later." |
| FM 21.1.1 | "Requires FM 21.1.1 or later (FileMaker Pro 2024 update, November 2024)." |
| FM 22.0.1 | "Introduced in FM 22 (2025) — not available in earlier versions." |
| FM 26 | "Introduced in FM 26 (2026) — not available in earlier versions." |
| FM 18 or earlier | No version note unless the user asks |

FM 19 is the practical floor for version-awareness — anything older noted as "may not be available
on legacy versions" without detail.

---

## Reference files — all 10

| File | Contains |
|---|---|
| `function-catalog.json` | All 368 functions through FM 26 — format, parameters, purpose, category, category_url, slug, doc_url, originated_in_version. Master for call signatures. Includes FM 26 additions: BaseTableComment, FieldAnnotation, FieldDisplayNames (Design); Get(AccountPasswordDaysRemaining), Get(GuidedAccessState), Get(WindowUUID) (Get); GetPersistentData, ListPersistentDataIDs (Persistent Data). |
| `script-steps-catalog.json` | All 165 script steps through FM 26, across 16 categories — syntax, purpose, notes, doc_url. Includes FM 26 additions: Insert Image Caption, Insert Image Captions in Found Set (AI category); Flush Web Viewer Cookies (Miscellaneous); Configure Persistent Data (new Persistent Data category); Create PDF, Open PDF, Append PDF, Close PDF, Cancel PDF, Print PDF + updated Save Records as PDF (new PDF Files category). Note: 2 pre-existing duplicates (Insert Embedding, Perform Semantic Find) were removed; net unique steps corrected from 157 to 165. |
| `logical-json-ai-functions-examples.md` | **Logical** (20 functions: If, Case, Let, While, ExecuteSQL, ExecuteSQLe, Evaluate, GetField, GetNthRecord…) + **JSON** (12 functions: JSONGetElement, JSONSetElement, JSONListKeys, JSONMakeArray, JSONParse, JSONParsedState…) + **AI** (14 functions: GetEmbedding, CosineSimilarity, GetTokenCount, GetTableDDL, GetRAGSpaceInfo, PredictFromModel, AddEmbeddings, SubtractEmbeddings, NormalizeEmbedding, GetFieldsOnLayout…) |
| `get-functions-examples.md` | All 138 Get() functions through FM 26, grouped by 12 categories: Date/Time, Account, File, Paths, Record, Layout/Window, Script/Trigger, Field, Sorting, Network, Device, Calculation. FM 26 additions: Get(AccountPasswordDaysRemaining) (Account); Get(GuidedAccessState) (Device); Get(WindowUUID) (Layout/Window). |
| `design-container-functions-examples.md` | **Design** (26 functions through FM 26: FieldNames, FieldType, LayoutNames, TableNames, ValueListItems, ScriptNames, BaseTableIDs, BaseTableComment, FieldAnnotation, FieldDisplayNames…) + **Container** (25 functions: Base64Encode/Decode, CryptEncrypt/Decrypt, CryptDigest, GetContainerAttribute, GetLiveText, ReadQRCode, GetTextFromPDF…) |
| `text-functions-examples.md` | **Text** (39 functions: Left, Right, Middle, Position, Substitute, PatternCount, Trim, Filter…) + **Text Formatting** (10 functions: TextColor, TextSize, TextFont, TextStyleAdd…) |
| `date-time-functions-examples.md` | **Date** (10 functions: Date, Day, Month, Year, DayOfWeek, DayName, MonthName, WeekOfYear…) + **Time & Timestamp** (5 functions: Hour, Minute, Seconds, Time, Timestamp) |
| `numeric-functions-examples.md` | **Number** (18 functions: Round, Int, Mod, Abs, Ceiling, Floor, Random…) + **Financial** (4: FV, NPV, PMT, PV) + **Trigonometric** (9: Sin, Cos, Tan, Asin, Acos, Atan, Degrees, Radians, Pi) + **Repeating** (3: Extend, GetRepetition, Last) |
| `specialty-functions-examples.md` | **Aggregate** (10: Sum, Count, Average, List, Max, Min, StDev…) + **Japanese** (12: Hiragana, Katakana, NumToJText, Furigana, YearName…) + **Mobile/Go** (5: Location, LocationValues, GetSensor, GetAVPlayerAttribute, RangeBeacons) + **Miscellaneous** (9: GetLayoutObjectAttribute, GetFieldName, ConvertFromFileMakerPath, LayoutObjectUUID, GetRecordIDsFromFoundSet…) + **Persistent Data** (2 FM 26 functions: GetPersistentData, ListPersistentDataIDs) |
| `quickrefs.md` | **Error codes** (0-899 + 1630-1631, AI/ML errors 870-892 verified against live docs 2026-06) + **ExecuteSQL** syntax, clauses, data types, date literals + **Data API** REST endpoints, auth, CRUD, find, portal data + **Sitemap** of common Claris Help guides (fast-path shortcut — use llms-full.txt for authoritative lookups) |

---

## Fetching strategy — which file to check first

| Topic | Check first | Then |
|---|---|---|
| Logical / Case / Let / While / ExecuteSQL | `logical-json-ai-functions-examples.md` | `function-catalog.json` → live doc |
| JSON functions | `logical-json-ai-functions-examples.md` | `function-catalog.json` → live doc |
| JSONParse / JSONParsedState (performance caching) | `logical-json-ai-functions-examples.md` | `function-catalog.json` → live doc |
| AI / embedding functions | `logical-json-ai-functions-examples.md` | `function-catalog.json` → live doc |
| Get() functions | `get-functions-examples.md` | `function-catalog.json` → live doc |
| Get(AccountPasswordDaysRemaining) | `get-functions-examples.md` (Account section) | `function-catalog.json` → live doc |
| Get(GuidedAccessState) | `get-functions-examples.md` (Device section) | `function-catalog.json` → live doc |
| Get(WindowUUID) | `get-functions-examples.md` (Layout/Window section) | `function-catalog.json` → live doc |
| Design / FieldNames / LayoutNames | `design-container-functions-examples.md` | `function-catalog.json` → live doc |
| FieldAnnotation / FieldDisplayNames / BaseTableComment | `design-container-functions-examples.md` | `function-catalog.json` → live doc |
| Container / Base64 / Crypt / OCR | `design-container-functions-examples.md` | `function-catalog.json` → live doc |
| GetTextFromPDF | `design-container-functions-examples.md` | `function-catalog.json` → live doc |
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
| GetPersistentData / ListPersistentDataIDs | `specialty-functions-examples.md` (Persistent Data section) | `function-catalog.json` → live doc |
| AI regression / PredictFromModel | `logical-json-ai-functions-examples.md` | `function-catalog.json` → live doc |
| Miscellaneous / GetRecordIDsFromFoundSet | `specialty-functions-examples.md` | `function-catalog.json` → live doc |
| Script steps | `script-steps-catalog.json` | live doc_url |
| Go to List of Records | `script-steps-catalog.json` (Found Sets) | live doc_url |
| Set Revert Transaction on Error | `script-steps-catalog.json` (Control) | live doc_url |
| Insert Image Caption / in Found Set | `script-steps-catalog.json` (AI category) | live doc_url |
| Flush Web Viewer Cookies | `script-steps-catalog.json` (Miscellaneous) | live doc_url |
| Configure Persistent Data | `script-steps-catalog.json` (Persistent Data) | live doc_url |
| PDF Files steps (Create/Open/Append/Close/Cancel/Print PDF) | `script-steps-catalog.json` (PDF Files category) | live doc_url |
| Save Records as PDF (FM 26 Save to option) | `script-steps-catalog.json` (PDF Files category) | live doc_url |
| Error codes | `quickrefs.md` | fetch `https://help.claris.com/markdown/en/pro-help/error-codes.md` for obscure codes |
| ExecuteSQL syntax | `quickrefs.md` | live sql-reference guide |
| Data API / REST | `quickrefs.md` | live data-api-guide |
| Finding a help page URL | `quickrefs.md` (fast-path) | `https://help.claris.com/llms-full.txt` for authoritative lookup |

---

## Tips

- The sidebar on any help page lists the **complete navigation tree** for that guide — very useful
  for discovering related pages.
- `function-catalog.json` is the master for function formats; example files are the master for usage patterns.
- For script step option details (platform support on Go, WebDirect, Server) always fetch the live
  doc_url — platform restrictions are not fully captured in the catalog.
- AI/embedding functions are in `logical-json-ai-functions-examples.md`; AI script steps are in
  `script-steps-catalog.json` (AI category through FM 26: 16 steps including Generate Response from
  Model, Configure AI Account, Perform SQL Query by Natural Language, Perform Find by Natural Language,
  Insert Embedding, Insert Image Caption, Insert Image Captions in Found Set, etc. — fetch live for
  all AI steps as they evolve rapidly).
- **Error codes:** The AI/ML error range (870–892) in `quickrefs.md` is verified against live docs (2026-06). The general error tables (0–899, 1630–1631) are a good quick reference but descriptions may drift — always fetch `https://help.claris.com/markdown/en/pro-help/error-codes.md` for authoritative descriptions of any unfamiliar code.
- **Sub-version doc drift:** Claris updates documentation pages between FM version releases — adding
  notes, correcting parameters, documenting edge cases — without changing the `version` field in
  frontmatter. For any question where exact parameter behaviour or option names matter, always fetch
  the live `.md` page even if local data appears sufficient. The live page is always authoritative
  over local reference files.
- **Mobile functions** (Location, GetSensor, RangeBeacons, GetAVPlayerAttribute, LocationValues) only
  work in FileMaker Go. Always advise checking platform with `Get(ApplicationVersion)` before use.
- **Japanese functions** require Japanese language support in FileMaker. `Furigana()` relies on the
  Japanese IME and may produce different results based on context.
- **Trig functions** all work in radians — use `Degrees()` and `Radians()` to convert. The Haversine
  GPS distance formula in `numeric-functions-examples.md` is a ready-to-use real-world example.
- **Financial functions** require `interestRate` per period, not annual — divide annual rate by
  payment frequency (12 for monthly). `PMT()` returns a negative number; use `Abs()` for display.
- **Generate Response from Model** is the most powerful AI step in FM 22+. In agentic mode, always
  append the DDL schema (from `GetTableDDL`) to the `execute_sql` tool parameter description so the
  model knows the schema. Custom function tool definitions must match the function name and parameter
  order exactly, with all parameters typed as `"string"`.
- **Fine-Tune Model** is restricted to OpenAI or AI Model Server on Apple silicon Mac — not
  available for other providers, Linux hosts, or Windows hosts. Response Target receives a job JSON
  with `status: "queued"` — training is asynchronous; monitor via Admin Console.
- **GetFieldsOnLayout** uses `[LLM]` prefix filtering: if any field comment starts with `[LLM]`,
  only those fields are sent to the AI model in `Perform Find by Natural Language`. Use this to
  control which fields the model can query on a per-layout basis.
- **GetEmbedding** returns binary **container** data, not text. Binary is smaller and faster than
  the text form returned by `Insert Embedding` into a text field. Use `GetEmbeddingAsText` only
  when a human-readable JSON array is required.
- **GetTableDDL** has an `ignoreError` boolean parameter — when true, partial DDL is returned even
  if some table occurrences fail to resolve, rather than aborting with an error.
- **GetModelAttributes** and **ComputeModel** are macOS/iOS only (Core ML). Always check platform
  before using these. ComputeModel vision variant exposes `confidenceLowerLimit` and `returnAtLeastOne`
  parameters not shown in the catalog stub — fetch the live doc for full option detail.
- **NormalizeEmbedding** is usually unnecessary — most embedding models already output unit-length
  vectors. Use it when working with non-standard models or when doing dimension reduction via the
  optional `dimension` parameter (trims dimensions before normalising).
- **PredictFromModel** and `Configure Regression Model` form a paired on-device ML workflow using
  Random Forest regression. Train on embedding vectors, then call `PredictFromModel` to get a
  predicted numeric value. Models persist in memory until Unload or session end.
- **GetRecordIDsFromFoundSet** pairs with `Go to List of Records` to recreate a found set later —
  useful for preserving found sets across script jumps or file switches. Returns IDs in 5 formats
  (type 0 = ValueNumber list, 1 = JSONString, 2 = JSONNumber, 3/4 = range variants).
- **Go to List of Records** (FM 22.0.1) accepts a carriage-return value list, a JSON array of IDs
  as strings or numbers, or a JSON array of objects with `recordId` keys. Records not found are
  silently skipped; if none match, the found set is empty. Not supported in FileMaker WebDirect.
- **JSONParse / JSONParsedState** (FM 22.0.1) — use `JSONParse` to cache a parsed JSON structure
  in memory by name, then pass the result to any JSON function in place of a raw JSON string.
  Dramatically improves performance when the same JSON is accessed many times in a script.
  `JSONParsedState` returns: 0 = not parsed, -1 = parsed but invalid, positive number = parsed
  type (1 = object, 2 = array, 3 = string, 4 = number, 5 = boolean, 6 = null).
- **GetTextFromPDF** (FM 22.0.1) — returns the text content of a PDF stored in a container field.
  Useful for feeding PDF content into RAG spaces (`Perform RAG Action`) or into AI prompts.
  Returns empty string if the container is not a PDF or has no extractable text layer.
- **Set Revert Transaction on Error** (FM 21.1.1) — when set to Off, errors inside a transaction
  block do not auto-revert; the script can inspect `Get(LastError)` and decide to commit or revert
  manually. Use `Get(RevertTransactionOnErrorState)` to query the current setting. Always reset to
  On before exiting a script that set it to Off.
- **RAG workflow** requires three steps in sequence: `Configure RAG Account` → `Configure AI Account`
  → `Perform RAG Action (Send Prompt)`. The RAG account handles the knowledge store; the AI account
  handles response generation.
- **Insert Image Caption** (FM 26) — sends an image (container field or variable) to a captioning
  model; inserts the returned caption into a target field or variable. `Insert Image Captions in
  Found Set` is the batch version — runs the step on every record in the current found set in sequence.
  Both steps require a configured AI account. Always fetch live docs for model and parameter detail.
- **PDF Files category** (FM 26 — new category) — the scripted PDF workflow: `Create PDF` (blank in
  memory) or `Open PDF` (existing file) → `Append PDF` pages or `Save Records as PDF` (with Save to:
  open PDF option) → `Close PDF` (saves to path/variable/container) or `Cancel PDF` (discards). `Print
  PDF` prints a PDF from a container field, file path, or variable without opening it for editing.
  `Save Records as PDF` has been moved into this category and now accepts a **Save to** option: file
  path, container, variable, or append to the currently open PDF. Always fetch live docs for the full
  option matrix — the category is entirely new in FM 26.
- **Configure Persistent Data / GetPersistentData / ListPersistentDataIDs** (FM 26) — the persistent
  data store survives session end and file close. Entries are keyed by a **name** and an **instance ID**
  (allowing multiple values under the same name). Delete an entry by passing empty or null to
  `Configure Persistent Data`. Use `ListPersistentDataIDs` to enumerate all instance IDs for a named
  key before iterating. Fetch live docs for scope and platform restrictions.
- **FieldAnnotation** (FM 26) — returns the DDL annotation string set in Advanced Options for Field.
  Pair with `GetTableDDL` to build enriched AI prompts or schema documentation workflows.
- **FieldDisplayNames** (FM 26) — returns a field's custom display names as a JSON object (set in
  Advanced Options for Field). Useful for UI layers that need alternate or localised field labels.
- **BaseTableComment** (FM 26) — returns the comment set on a base table in Manage Database. Pair
  with `GetTableDDL` and `FieldAnnotation` to build richer schema context for AI steps.
- **Get(GuidedAccessState)** (FM 26, FileMaker Go only) — returns 1 if iOS Guided Access is currently
  active. Use to detect kiosk/locked-screen mode and adapt UI behaviour accordingly.
- **Get(AccountPasswordDaysRemaining)** (FM 26) — returns the number of days before the current
  account's password must be changed. Returns empty if no expiry is set. Use to show proactive warning
  dialogs in startup scripts.
- **Get(WindowUUID)** (FM 26) — returns a unique, stable UUID for the currently active window.
  Useful for scripted window management when multiple windows of the same file are open.

---

## Licence

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Version history

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
