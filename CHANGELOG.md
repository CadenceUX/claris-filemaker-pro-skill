## [1.9.1] — 2026-06-26

### Fixed — catalog parameter-list errors found during a live FileMaker session

A live agentic session generating a reference script that exercises all 368 functions and
165 script steps against a real `Functions.fmp12` file surfaced four genuine catalog/example
defects (verified against live Claris docs and live FileMaker calculation evaluation). No new
functions or script steps — total counts remain **368 functions** and **165 script steps**.

- **`FieldAnnotation`** — `function-catalog.json` listed a bogus 3-parameter signature
  `( fileName ; layoutName ; fieldName )`. The live Claris doc and its own "Originated in
  version 26.0" note confirm the real signature is **`( fileName ; fieldName )`** — `layoutName`
  doesn't exist as a parameter. Corrected `format` and `parameters` in the catalog; corrected
  the matching section and both calculation examples in `design-container-functions-examples.md`.
- **`FieldDisplayNames`** — same defect, same fix: catalog and examples corrected from the
  bogus `( fileName ; layoutName ; fieldName )` to the real **`( fileName ; fieldName )`**.
- **`TextColor`** — `function-catalog.json`'s `parameters` array was `["text", "RGB ( red",
  "green", "blue )"]` — the nested `RGB(...)` call had been split across three bogus fragments
  by whatever process generated the array, even though `format` was already correct. Corrected
  to `["text", "color"]` (two logical parameters, second one a nested RGB() call).
- **`TextColorRemove`** — identical `parameters`-array mis-split, identical fix.

### Verified accurate — no catalog changes, usage notes added instead

The same session also flagged five functions as "broken" that turned out to be **correct in the
catalog** — the live FileMaker errors were caused by treating placeholder-style usage (bare
literals, wrong data shape) as if it were valid input. Documented here so this doesn't get
mis-diagnosed as a catalog bug again:

| Function | What looked wrong | Why the catalog is actually right |
|---|---|---|
| `Evaluate` | `Evaluate ( "text" ; field )` returns nothing useful | First argument must itself be a *valid calculation string* (e.g. `"1+1"`), not arbitrary text — `"text"` alone isn't parseable as a calc |
| `GetSummary` | `GetSummary ( field1 ; field2 )` silently fails | `summaryField` must be a real **Summary-type** field in the same table as the break field, sorted by it — a plain Text/Number field never works |
| `Let` | Positional args like `Let ( 1 ; 1 ; "text" )` are invalid | `Let` uses `var = expression` **assignment** syntax inside the first clause (`Let ( x = 5 ; x*x )`), not positional parameters — the catalog's `parameters: ["var1","var2","calculation"]` names the *roles*, not literal positions |
| `While` | Same positional-args mistake | Same root cause — `While ( [ init ] ; condition ; [ logic ] ; result )` needs real assignment/condition expressions, not bare literals |
| `NPV` | `NPV ( 1 ; .05 )` fails with error 1214 | `payment` requires a **repeating field** containing the unequal payment series — FileMaker validates the type, so a plain number is rejected at the field-type level, not a calc syntax level |

Also clarified for **all `Get()` functions**: the catalog's `parameters` array entry (e.g.
`["AccountExtendedPrivileges"]`) is the literal constant name that's already embedded in `format`
(`"Get ( AccountExtendedPrivileges )"`) — it is not a runtime argument to substitute a value into.
Treating it as a positional parameter to fill in (the mistake made in this session) produces
malformed calls like `Get(AccountExtendedPrivileges) ( 1 )`.

### Fixed — full live audit of every function and script step against help.claris.com

Following the `FieldAnnotation`/`FieldDisplayNames` parameter-count bugs found above, every one
of the 368 functions and 165 script steps was re-checked against its live `doc_url` page (533
pages fetched directly from help.claris.com and diffed programmatically against the catalog —
not a sample). This is a data-accuracy pass only: no functions or script steps were added or
removed, counts remain **368 functions** and **165 script steps**.

**`function-catalog.json`:**
- **176 `originated_in_version` values were wrong** — not just formatting (e.g. `"16"` vs
  `"16.0"`, which are the same version and were left alone), but genuinely different version
  numbers. Examples: `Get(AccountExtendedPrivileges)` was `"7"`, live docs say `"11.0"`;
  `Base64Decode`/`Base64Encode` were `"12"`, live docs say `"13.0"`; `ConvertFromFileMakerPath`/
  `ConvertToFileMakerPath` were `"12"`, live docs say `"19.0"`. Roughly half the catalog had this
  defect — likely a systematic error from however `originated_in_version` was originally
  populated, not isolated typos. All 176 corrected to match the live "Originated in version"
  text, normalised to the catalog's existing convention (e.g. `"6.0 or earlier"` → `"legacy"`,
  `"13.0"` → `"13"`, real patch versions like `"19.6.1"` kept as-is).
- **`GetRecordIDsFromFoundSet`** — `format`/`parameters` had stale FM 26 parameter naming
  (`tableOccurrenceName`) that didn't match the live doc's actual parameter name
  (`tableOccurrenceOrPortal`). Corrected.

**`script-steps-catalog.json`:**
- **11 dead `doc_url` links** found and fixed. Three resolved to a real but differently-named
  page (`If` → `if-script-step.md`, not `if.md`, since Claris uses separate `-function`/
  `-script-step` suffixes to disambiguate the `If()` function from the `If` step; `Send DDE
  Execute` → `send-dde-execute-windows.md`; `Speak` → `speak-os-x.md`). Eight steps (`Check
  Spelling`, `Log Out`, `Manage Add-ons`, `Navigate to Object`, `Show/Hide Status Toolbar`, `Set
  Window Animation`, `Show Alert`, `Show/Hide Script Editor`) have **no individual doc page** on
  Claris's site as of this audit — their `doc_url` now points at the general script steps
  reference instead of a 404, with a `doc_url_note` field flagging this so it's not mistaken for
  an oversight later.
- **17 steps had wrong or missing clauses** in `syntax`, found by checking each step's real
  `Options` section on its live page:
  - `Move/Resize Window`, `Close Window`, `Set Window Title` were all missing the **`Current file
    only`** clause that's a real, documented option on each (this is the same clause this skill's
    catalog should have always had — see the now-removed "not in scope" note in this changelog's
    previous edit, which incorrectly attributed this to a third-party plugin bug rather than a
    genuine gap in this catalog).
  - `Set Window Title` also had the wrong clause name — `New Name` doesn't exist; the real option
    is `New Title`.
  - `Insert Picture`, `Insert PDF`, `Insert Audio/Video` all listed a `Storage:
    Embedded/By Reference/Externally` enum that doesn't exist for any of these three steps — the
    real (and only) option is a simple `Store only as a reference` toggle.
  - The AI category had the most drift, likely because these are the newest steps (FM 22–26) and
    were never checked against docs after initial authoring: `Insert Embedding`'s real option
    names are `Input`/`Target` (catalog had `Source Field`/`Target Field`, and was missing
    `Parameters`); `Insert Image Caption`/`Insert Image Captions in Found Set` use `Account Name`/
    `Model`/`Input` (catalog had `AI Account Name`/`Image`); `Fine-Tune Model`'s real target
    option is `Response Target`, not `Output Model`, and it was missing `Fine-Tune Parameters`;
    `Generate Response from Model`'s real option is `Response`, not `Response Target`.
  - `Trigger Claris Connect Flow` was the most wrong — catalog had `Flow Name`/`Parameters`/
    `Response Target`, but the real options are `URL`/`JSON Data`/`AppID:APIKey for Webhooks`/
    `Target`/`Flow`. Rewritten to match.
  - `Perform Semantic Find` was rewritten in full — catalog had `Table::EmbeddingField ; Query
    Embedding: value ; Top K: n`, none of which are real option names; the actual options are
    `Query by`, `Record set`, `Target field`, `Return count`, `Cosine similarity condition`/
    `value`, `Parameters`, `Save result`.
  - `Open File` and `Import Records` were rewritten to use real option names (`Add FileMaker Data
    Source`/`Add ODBC Data Source`; `Specify data source`/`Specify import order`) instead of
    fabricated ones.
  - `Go to Record/Request/Page` and `Go to Portal Row` were missing the documented `Exit after
    last` option; added.
- **Known gap at the time of writing the section above, fixed later in this same release** — see
  "Script step `originated_in_version` added" below.

**Example accuracy** (`date-time-`, `design-container-`, `logical-json-ai-`, `numeric-`,
`specialty-`, and `text-functions-examples.md`):
- Spot-checking earlier in this session's history found that most illustrative examples in these
  files were synthetic — written when the skill was authored, not copied from Claris docs. All
  six example files were systematically re-checked: of 256 function sections with worked
  examples, **143 had their primary example replaced** with Claris's actual documented example
  (verbatim where the live page uses a fenced code block; reconstructed into this skill's
  established `expression` / `// → result` comment style where the live page instead uses inline
  prose like `` `Round(123.456;2)` returns `123.46` ``). Secondary examples in each section —
  "pair with X" combination patterns, alternate usage notes — were left untouched, since those
  are this skill's own added value rather than claims about what Claris's docs say.
  - 9 functions' live examples use complex prose or multi-table walkthroughs (`Lookup`,
    `LookupNext`, `StDev`, `StDevP`, `Furigana`, `ConvertFromFileMakerPath`, `GetTokenCount`,
    `JSONParsedState`, `FieldStyle`) that don't reduce cleanly to a single expression/result pair
    — left as-is rather than risk a mangled auto-edit; flagged here for manual review if accuracy
    on these specific functions matters for a future task.
  - `Get()` functions are documented in this skill as summary tables, not per-function example
    sections, so they were out of scope for this example pass (not because they're assumed
    accurate — they simply have no example block to compare).

### Added — script step `originated_in_version` field

Functions have always carried `originated_in_version`; script steps never did, despite every
live step page having an "Originated in version" section. Added the field to
`script-steps-catalog.json` using the same live-fetched, same-session data as the audit above —
no new network round trip, just a second pass over the already-cached pages.

- **157 of 165 steps** now have a confirmed `originated_in_version`, sourced and normalised the
  same way as the function fix above (`"6.0 or earlier"` → `"legacy"`, `"22.0"` → `"22"`, real
  patch versions kept as-is, e.g. `"19.6.1"`, `"21.1.1"`).
- **8 steps have no `originated_in_version`** because they have no individual doc page to source
  it from (the same 8 flagged with a `doc_url_note` in the dead-link fix above): `Check Spelling`,
  `Log Out`, `Manage Add-ons`, `Navigate to Object`, `Show/Hide Status Toolbar`, `Set Window
  Animation`, `Show Alert`, `Show/Hide Script Editor`. Left absent rather than guessed.
- Distribution sanity-checked: 103 steps are `legacy` (pre-FM7, as expected for core control/
  navigation/editing steps), clustering at `22` (10 steps) and `26` (10 steps) for the FM 22 and
  FM 26 AI/PDF/Persistent Data additions — consistent with where new step categories actually
  landed in recent FileMaker releases.

## [1.9] — 2026-06-11

### Fixed — accuracy corrections from skill review; FM 26 changed-function drift captured

A review of v1.8 against the local catalogs and live Claris docs found five factual errors and
two count inconsistencies. All are corrected in this release. No new functions or script steps —
total counts remain **368 functions** and **165 script steps**.

#### SKILL.md corrections:

- **Frontmatter description:** function count corrected 376 → **368** (the 376 figure matched
  nothing — README, CHANGELOG, and the catalog all said 368).
- **JSONParsedState type mapping (Tips):** corrected to match Claris docs — positive return values
  use the JSONSetElement type constants: 1 = string, 2 = number, 3 = object, 4 = array,
  5 = boolean, 6 = null. (Previously listed as 1 = object, 2 = array, 3 = string, 4 = number,
  contradicting the skill's own JSON examples file, which was already correct.)
- **GetRecordIDsFromFoundSet (Tips):** result formats corrected to the five named constants
  (ValueNumber, JSONString, JSONNumber, ValueNumberRanges, JSONStringRanges) and the FM 26
  optional second parameter documented (see below).
- **GetTextFromPDF (Tips):** FM 26 macOS scanned-PDF OCR support noted.
- **Reference table counts:** JSON functions 12 → **10**; Container functions 25 → **24**
  (both now match the catalog and example file headers).

#### FM 26 changed-function drift (existing entries updated):

The v1.8 rebuild added new FM 26 functions and steps but missed FM 26 changes to *existing*
functions, per the FileMaker Pro Release Notes:

| Function | FM 26 change |
|---|---|
| `GetRecordIDsFromFoundSet` | New optional second parameter — `GetRecordIDsFromFoundSet ( type {; tableOccurrenceName} )` — accepts a table occurrence or portal object name and returns IDs from the related/filtered set instead of the current found set |
| `GetTextFromPDF` | macOS now supports scanned PDFs (no text layer) via built-in OCR; other platforms unchanged |

Updated in `function-catalog.json` (format, parameters, purpose) and the relevant example files.

#### Reference file corrections:

- **`specialty-functions-examples.md`** — GetRecordIDsFromFoundSet entry was incomplete (documented
  only types 0 and 1). Replaced with the full 0–4 type table including both Ranges variants,
  empty-found-set return values, and the FM 26 optional parameter.
- **`design-container-functions-examples.md`** — GetTextFromPDF entry updated with the FM 26
  macOS scanned-PDF note.
- **`script-steps-catalog.json`** — stale meta `last_updated` string corrected (claimed
  "step count 157 → 167"; actual unique count is 165, as already stated in the v1.8 revised
  changelog and SKILL.md).
- **`function-catalog.json`** — meta `last_updated` refreshed for v1.9.

#### Housekeeping:

- `VERSION` bumped to 1.9; SKILL.md frontmatter `version` and self-check reference updated.
- Product version references (e.g. "FM 22 (2025)", "FM 26 (2026)") deliberately unchanged —
  only build-date headings reflect the current date, per established convention.

---

## [1.8] — 2026-06-10 (revised)

### Changed — FM 26 functions and script steps added to local reference files; FM 26 special-case routing removed

All 18 FM 26 additions (8 functions, 10 script steps) are now present in the local reference
catalogs. The previous v1.8 documented FM 26 additions but kept them fetch-live-only. This
revision adds them to local files so they are handled identically to all other functions and
steps: check local first, then fetch the live doc_url for full parameter detail.

Two pre-existing duplicate entries were also removed from `script-steps-catalog.json` (Insert
Embedding was present in both Editing and AI categories; Perform Semantic Find was present in
both Found Sets and AI categories). Corrected unique step count: 157 → 165 after removing 2
duplicates and adding 10 FM 26 steps.

#### functions added to function-catalog.json (8):

| Category | Function | Signature |
|---|---|---|
| Design | `BaseTableComment` | `BaseTableComment ( fileName ; baseTableName )` |
| Design | `FieldAnnotation` | `FieldAnnotation ( fileName ; layoutName ; fieldName )` |
| Design | `FieldDisplayNames` | `FieldDisplayNames ( fileName ; layoutName ; fieldName )` |
| Get | `Get(AccountPasswordDaysRemaining)` | `Get ( AccountPasswordDaysRemaining )` |
| Get | `Get(GuidedAccessState)` | `Get ( GuidedAccessState )` |
| Get | `Get(WindowUUID)` | `Get ( WindowUUID )` |
| Persistent Data | `GetPersistentData` | `GetPersistentData ( name ; instanceID )` |
| Persistent Data | `ListPersistentDataIDs` | `ListPersistentDataIDs ( name )` |

**Total functions: 368** (360 through FM 22 + 8 FM 26).

#### Script steps added to script-steps-catalog.json (10 new + 1 moved + 2 duplicates removed):

| Category | Step | Change |
|---|---|---|
| AI | `Insert Image Caption` | New FM 26 |
| AI | `Insert Image Captions in Found Set` | New FM 26 |
| Miscellaneous | `Flush Web Viewer Cookies` | New FM 26 |
| Persistent Data *(new category)* | `Configure Persistent Data` | New FM 26 |
| PDF Files *(new category)* | `Create PDF` | New FM 26 |
| PDF Files | `Open PDF` | New FM 26 |
| PDF Files | `Append PDF` | New FM 26 |
| PDF Files | `Close PDF` | New FM 26 |
| PDF Files | `Cancel PDF` | New FM 26 |
| PDF Files | `Print PDF` | New FM 26 |
| PDF Files | `Save Records as PDF` | Moved from Records; updated with FM 26 Save to option |
| Editing | `Insert Embedding` | Duplicate removed (kept AI category version) |
| Found Sets | `Perform Semantic Find` | Duplicate removed (kept AI category version) |

**Total script steps: 165** (two new categories: PDF Files with 7 steps, Persistent Data with 1 step).

#### Reference example files updated:

- **`design-container-functions-examples.md`** — Added BaseTableComment, FieldAnnotation, FieldDisplayNames with examples. Updated header: 23 → 26 design functions.
- **`get-functions-examples.md`** — Added Get(AccountPasswordDaysRemaining) (Account section), Get(GuidedAccessState) (Device section), Get(WindowUUID) (Layout/Window section) to tables. Updated header: 135 → 138 Get() functions.
- **`specialty-functions-examples.md`** — Added new **Persistent Data Functions** section with GetPersistentData and ListPersistentDataIDs examples.

#### SKILL.md changes:

- Removed **"FM 26 (2026) coverage status"** section (previously flagged FM 26 as fetch-live-only with a special routing table — no longer needed).
- Removed **"FM 26 — live fetch strategy"** section and its special routing table.
- Updated mandatory trigger examples: FM 26 triggers now point to local files instead of "FM 26 live docs".
- Removed FM 26 row from "Always fetch live" table (FM 26 is no longer a coverage gap).
- Updated reference table entries: function-catalog.json now lists 368 functions including FM 26 additions; script-steps-catalog.json now lists 165 steps including FM 26 additions and new categories.
- Updated fetching strategy table: added explicit local-file routing rows for all FM 26 additions.
- Updated version notes table: FM 26 row no longer says "Fetch live docs for full detail" as a special instruction — it gets the same note as other recent versions.
- Updated frontmatter description: function count 368, step count 165.

### Fixed

- Removed duplicate `Insert Embedding` entry from Editing category in `script-steps-catalog.json`.
- Removed duplicate `Perform Semantic Find` entry from Found Sets category in `script-steps-catalog.json`.
- `meta.last_updated` and `meta.version` updated in both JSON catalogs.

### Updated

- `VERSION` — remains `1.8` (this is a content revision of the same version)
- `README.md` — updated function and step counts, added FM 26 coverage note

---

## [1.8] — 2026-06-10

### Changed — FM 26 coverage section rewritten with confirmed additions

Full audit of FM 26 (released June 9, 2026) new script steps and functions, sourced directly
from the Claris release notes. The speculative "may include" FM 26 section in SKILL.md has been
replaced with two precise reference tables.

**No local reference file changes** — `function-catalog.json` and `script-steps-catalog.json`
remain at FM 22.0.x. All FM 26 additions are fetch-live-only until a future catalog rebuild.

#### New script steps documented (10, all fetch-live):

| Category | Step |
|---|---|
| AI | `Insert Image Caption` |
| AI | `Insert Image Captions in Found Set` |
| Miscellaneous / Web Viewer | `Flush Web Viewer Cookies` |
| Persistent Data | `Configure Persistent Data` |
| PDF Files *(new category)* | `Create PDF` |
| PDF Files | `Open PDF` |
| PDF Files | `Append PDF` |
| PDF Files | `Close PDF` |
| PDF Files | `Cancel PDF` |
| PDF Files | `Print PDF` |

Note: `Save Records as PDF` moved to the new PDF Files category and gained a **Save to** option
(file path, container, variable, or append to an open PDF).

#### New functions documented (8, all fetch-live):

| Category | Function |
|---|---|
| Design | `FieldAnnotation ( fileName ; layoutName ; fieldName )` |
| Design | `FieldDisplayNames ( fileName ; layoutName ; fieldName )` |
| Design | `BaseTableComment ( fileName ; baseTableName )` |
| Get() | `Get(GuidedAccessState)` |
| Get() | `Get(AccountPasswordDaysRemaining)` |
| Get() | `Get(WindowUUID)` |
| Persistent Data | `GetPersistentData ( name ; instanceID )` |
| Persistent Data | `ListPersistentDataIDs ( name )` |

**Total known functions:** 368 (+8 FM 26, fetch-live).
**Total known script steps:** 167 (+10 FM 26, fetch-live). PDF Files is a new script step category.

### Added to SKILL.md

- **FM 26 coverage section** — complete rewrite; two tables (script steps, functions) with category,
  name/signature, and one-line description for each FM 26 addition. `Save Records as PDF` move and
  new Save to option documented.
- **FM 26 — live fetch strategy section** — new dedicated routing table giving the exact
  `llms-full.txt` search or direct fetch action for every FM 26 item.
- **14 new trigger examples** — one per FM 26 addition, covering AI captioning, PDF Files workflow,
  persistent data, all three Design functions, all three Get() functions.
- **9 new tips** — Insert Image Caption/batch, PDF Files workflow (full Create→Close chain),
  Configure Persistent Data/GetPersistentData/ListPersistentDataIDs (instance ID model, delete
  pattern), FieldAnnotation, FieldDisplayNames, BaseTableComment, Get(GuidedAccessState),
  Get(AccountPasswordDaysRemaining), Get(WindowUUID).

### Updated in SKILL.md

- Frontmatter `version`: `"1.7"` → `"1.8"`
- Frontmatter description: function count 360 → 368; step count 157 → 167
- Overview heading: v1.7 → v1.8
- Version self-check installed version: `"1.7"` → `"1.8"`
- AI script step count in tips: 14 → 16 (Insert Image Caption and Insert Image Captions in Found Set)
- `function-catalog.json` reference table entry: notes FM 26 adds 8 functions (fetch-live)
- `script-steps-catalog.json` reference table entry: notes FM 26 adds 10 steps (fetch-live);
  PDF Files is a new category
- `design-container-functions-examples.md` reference entry: flags FM 26 Design additions by name
- `get-functions-examples.md` reference entry: flags FM 26 Get() additions by name
- "Always fetch live" table: FM 26 row clarified to reference the confirmed additions list

### Updated

- `VERSION` — bumped to `1.8`
- `README.md` — function count 360 → 368; step count 157 → 167; version coverage note updated

---

# Changelog

All notable changes to this skill are documented here.

---

## [1.7] — 2026-06-10

### Added — 2 missing script steps added to script-steps-catalog.json

Full audit of `script-steps-catalog.json` against FileMaker Pro 22.0.1 and 21.1.1 release notes
identified two steps that were missing from the local catalog.

**Added — `Go to List of Records`** (Found Sets category, FM 22.0.1):

- Goes to a layout and returns a found set specified by a list of record IDs.
- Accepts: carriage-return-separated value list, JSON array of string/number IDs, or JSON array
  of objects with `recordId` keys.
- Companion to `GetRecordIDsFromFoundSet` — together they enable saving and restoring found sets
  across script jumps or file switches.
- Not supported in FileMaker WebDirect.
- `doc_url`: `https://help.claris.com/markdown/en/pro-help/go-to-list-of-records.md`

**Added — `Set Revert Transaction on Error`** (Control category, FM 21.1.1):

- Controls whether an error inside an Open Transaction block auto-reverts the transaction.
- When set to Off, the script continues after an error and can decide to commit or revert manually.
- Use `Get(RevertTransactionOnErrorState)` to query the current state.
- Always reset to On before exiting a script that set it to Off.
- `doc_url`: `https://help.claris.com/markdown/en/pro-help/set-revert-transaction-on-error.md`

**Step count:** corrected from 155 → **157**.

### Changed

- `SKILL.md` — version bumped to 1.7; step count references updated 155 → 157 in frontmatter
  description and reference table.
- `SKILL.md` — "Coverage gap — FM 26 (2026)" section renamed to "FM 26 (2026) coverage status"
  and updated to reflect that FM 26 was released June 9, 2026; docs are new and still settling.
- `SKILL.md` — version self-check installed version updated from `"1.6"` → `"1.7"`.
- `SKILL.md` — Automatic version notes table: added FM 21.1.1 row for Set Revert Transaction on Error.
- `SKILL.md` — Mandatory triggers: added Go to List of Records, Set Revert Transaction on Error,
  GetTextFromPDF, JSONParse/JSONParsedState examples.
- `SKILL.md` — Fetching strategy table: added Go to List of Records, Set Revert Transaction on Error,
  JSONParse/JSONParsedState, GetTextFromPDF rows.
- `SKILL.md` — Tips section: added Go to List of Records, JSONParse/JSONParsedState,
  GetTextFromPDF, Set Revert Transaction on Error guidance.
- `SKILL.md` — Reference table: updated Container count (24 → 25 including GetTextFromPDF),
  JSON count (10 → 12 including JSONParse/JSONParsedState), script steps catalog description.
- `script-steps-catalog.json` — `meta.last_updated` updated to reflect v1.7 additions.
- `VERSION` — bumped to `1.7`.

---

## [1.6] — 2026-06-10

### Changed

- `SKILL.md` — `last_known_fm_version` updated from `22` → `26` in preparation for FM 26 release
  (which released June 2026, after v1.5 shipped).
- `SKILL.md` — Added "Coverage gap — FM 26 (2026)" section documenting known FM 26 additions
  that require live fetch until a full v1.7 catalog rebuild.
- `SKILL.md` — Version drift detection examples updated to reference `last_known_fm_version: 26`.
- `SKILL.md` — heading and frontmatter version bumped to 1.6.

---

## [1.5] — 2026-06-08

### Fixed — script-steps-catalog.json catalogue integrity pass

Full audit of `script-steps-catalog.json` against the `skill-update-recommendations.md` comparison
report (2026-06-08) and the source FileMaker 22 documentation.

**Removed — 2 stale/duplicate entries:**

- `Execute SQL Query by Natural Language` (Miscellaneous category) — **stale entry**. This name did
  not exist in FileMaker 22. The step was always named `Perform SQL Query by Natural Language` and
  this entry appears to be an artefact from an earlier draft. Its slug
  (`execute-sql-query-by-natural-language`) does not resolve to a valid Claris Help page. Removed.
- `Perform SQL Query by Natural Language` (Miscellaneous category) — **duplicate with wrong purpose**.
  Purpose field incorrectly read `"Alias for Execute SQL Query by Natural Language in some contexts"`.
  The authoritative entry with full notes (action options, Data Tables modes, server-side compatibility
  caveat) is correctly located in the AI category. Cross-listing a partial copy with an inaccurate
  purpose in Miscellaneous created confusion and inflated the step count. Removed.

**Fixed — 2 cross-category entries:**

- `Insert Embedding` (Editing category) — added `originated_in_version: "21.0.1"`. This step
  legitimately appears in FileMaker's Editing category in the Script Workspace; the Editing entry
  is retained as a discovery path alongside the primary AI category entry.
- `Perform Semantic Find` (Found Sets category) — synced `purpose` text with the AI category entry
  (`"Finds the top K records most semantically similar to a query embedding vector"`) and added
  `originated_in_version: "21.0.1"`. Step legitimately appears in Found Sets in the Script
  Workspace; entry retained for discoverability.

**Step count:** corrected from 157 → **155** (2 stale/duplicate Miscellaneous entries removed).
Note: `Insert Embedding` and `Perform Semantic Find` each appear in two categories by design
(FileMaker natively cross-lists them); these are not counted as duplicates.

### Changed

- `SKILL.md` — version bumped to 1.5; step count references updated 157 → 155 in frontmatter
  description and reference table.
- `script-steps-catalog.json` — `meta.last_updated` updated to reflect v1.5 audit.

---


### Fixed — Error codes complete rewrite (`quickrefs.md`)
Full audit of `quickrefs.md` error codes section against the live Claris Help Centre
(`https://help.claris.com/en/pro-help/content/error-codes.html`), verified June 2026.

**Coverage:** 121 codes → 282 discrete codes + 2 ranges (1552–1559 plug-in, 5000–5499 custom).

**Removed — 12 phantom codes not in official docs:**
- `8`, `26`, `213`, `403` (system/account range)
- `701`, `702`, `703`, `704`, `709`, `710`, `712`, `713` (labelled "Network errors" — not in Claris table)

**Fixed — 18 description mismatches (code number existed but meaning was wrong):**
- `17–21`: Replaced fabricated descriptions (foreign key, failed import, unexpected, record open, data type mismatch) with official Claris descriptions (UTF-16 conversion, account info required, ASCII-only string, triggered-script cancel, unsupported request)
- `205–208`: Replaced Data-API-sourced descriptions (record already present, modification in progress, transaction timeout, TOO_MANY_RECORDS) with correct `Get(LastError)` desktop descriptions (access privileges, password change privileges, schema privileges, password length)
- `212`: "Password not valid" → "Invalid user account or password"
- `406–408, 413–414`: Replaced import-centric descriptions with correct find/sort/field descriptions matching official docs
- `715–719`: **Critical fix** — replaced password-policy descriptions (passwords don't match, uppercase/lowercase/numeric/special char requirements) with correct official descriptions (Excel worksheet missing, ODBC SQL restriction, XML/XSL import errors)

**Added — 173 missing codes across 11 blocks:**
- `-1`: Unknown error
- `119`, `130–131`: Email client, installation/language pack errors
- `209–212`, `219`: Account/password errors (new password, inactive, expired, too many attempts, licensing)
- `300–310`: Full concurrency/locking block (file, record, table, schema, layout, theme locking)
- `415–418`: Remaining find/data errors (related records, primary key, data source, INSERT failure)
- `600–603`: Full print error block
- `720–738`: Upper import/export block (XML, theme, format, permission errors)
- `800–853`: Full file I/O block (disk, network file ops, container storage)
- `900–923`: Full spelling engine block
- `951–960`: Full web publishing / Custom Web Publishing block
- `1200–1225`: Full calculation error block
- `1300–1301`: Custom function name errors
- `1400–1415`, `1450–1451`: Full ODBC block + PHP/remote errors
- `1501–1507`: Full SMTP/email block
- `1541–1543`: JWT / token errors
- `1550–1551`: Plug-in load/install errors; `1552–1559` range documented
- `1626–1629`, `1632–1635`, `1638`: Remaining network/SSL errors (protocol, auth, SSL, timeout, cert expiry, self-signed, unencrypted, connection limit)
- `1700–1715`: Full Data API REST block (resource, auth, verb, header, parameter, JSON, license, OS, external auth)
- `5000–5499`: Custom Revert Transaction range documented

**Restructured sections:**
- "Network errors (700–799)" renamed to "File type / import / export errors (700–738)" — these are not network errors
- "Account/security errors" corrected to official descriptions throughout
- "Import/export errors (400–499)" renamed to "Find / sort / data errors (400–418)"
- "Printing/spelling errors (500–599)" renamed to "Validation errors (500–513)"
- New sections added: Concurrency/locking (300s), Print (600s), File I/O (800s), Spelling engine (900s), Web publishing (951–960), Calculation (1200s), Custom functions (1300s), ODBC (1400s), SMTP (1500s), JWT (1541–1543), Plug-in (1550s), Data API REST (1700s), Custom (5000–5499)

---

## [1.3] — 2026-06-08

### Added
- **7 new Tips** in SKILL.md: Generate Response from Model (agentic tool use, DDL schema requirement),
  Fine-Tune Model (Apple silicon restriction), GetFieldsOnLayout [LLM] prefix filtering, GetEmbedding
  binary container performance note, GetTableDDL ignoreError parameter, GetModelAttributes/ComputeModel
  macOS/iOS platform restriction, NormalizeEmbedding usage guidance, PredictFromModel + Configure
  Regression Model paired workflow, GetRecordIDsFromFoundSet + Go to List of Records pairing,
  RAG three-step workflow sequence
- **5 new mandatory trigger examples** in SKILL.md: PredictFromModel, GetRecordIDsFromFoundSet,
  Fine-Tune Model, AddEmbeddings, Configure RAG Account
- **2 new rows** in fetching strategy table: AI regression / PredictFromModel and
  Miscellaneous / GetRecordIDsFromFoundSet
- **Trigger Claris Connect Flow** (v20.1) added to script-steps-catalog.json Miscellaneous category
- **Set Session Identifier** (v19.4.1) added to script-steps-catalog.json Miscellaneous category

### Changed
- `script-steps-catalog.json` — 9 FM 22 AI steps enriched with full `notes` field documentation:
  - **Generate Response from Model**: agentic mode detail, built-in tool definitions (execute_sql,
    retrieve_image), custom function tool requirements, streaming, conversation history, error messages
  - **Perform RAG Action**: Add Data sub-actions, Async notes, Send Prompt parameters, Remove Data warning
  - **Configure RAG Account**: endpoint URL trailing-slash requirement, session scope, Admin Console key
  - **Configure Prompt Template**: template types (SQL Query, Find Request, RAG Prompt), all 6 constants,
    case-sensitivity, session scope
  - **Configure Regression Model**: Train/Save/Load/Unload actions, Random Forest parameters, memory scope
  - **Fine-Tune Model**: LoRA technique, OpenAI/Apple silicon restriction, fm-mlx- prefix, async response
  - **Perform SQL Query by Natural Language**: 5 action options, 3 Data Tables modes, field comment context,
    server-side compatibility caveat
  - **Perform Find by Natural Language**: 3 Get options, GetFieldsOnLayout integration, error 401 detail
  - **Save Records as JSONL**: fine-tuning On/Off format differences, container field handling, Go/WebDirect restriction
- `script-steps-catalog.json` — 3 existing steps enriched:
  - **Insert Embedding in Found Set**: Parameters JSON keys documented (MaxRecPerCall, MaxRetryPerWorker,
    MaxWaitPerRetry, TruncateTokenLimit, TruncateEnabled, RetryOnError)
  - **Perform Semantic Find**: image query mode and Save result JSON array documented
  - **Set AI Call Logging**: Verbose mode detail, Truncate Messages option documented
- SKILL.md reference table: script steps count updated 155 → 157
- SKILL.md specialty-functions-examples.md description: GetRecordIDsFromFoundSet added to Miscellaneous list
- SKILL.md AI functions list in logical-json-ai description: new v22 functions explicitly listed
- SKILL.md heading and frontmatter version bumped to 1.3

---

## [1.2] — 2026-06-07

### Changed (description update)
- Clarified skill scope in frontmatter description: this is a **reference skill** (syntax, parameters, examples, live doc fetches) — not a platform administration guide
- Explicitly scoped out FileMaker Server admin, Claris Connect, Claris Studio, and ODBC/JDBC deep configuration (reserved for future skills)
- Replaced broad "ANY FileMaker Pro topic" language with explicit in-scope / out-of-scope boundaries

### Added
- 8 new FM 2025 v22 AI script steps: Configure Prompt Template, Fine-Tune Model, Generate Response from Model, Insert Embedding in Found Set, Perform Find by Natural Language, Perform RAG Action, Perform SQL Query by Natural Language, Set AI Call Logging
- Save Records as JSONL to Files script step category
- 3 missing help centre guides to sitemap: `cloud-getting-started-guide`, `go-release-notes`, `connect-release-notes` (sitemap now covers all 33 current Claris help guides)

### Changed
- AI/ML error codes (870–892) completely rewritten against live Claris Help Centre docs — previous descriptions were inaccurate; now includes new codes 883, 885, 886, 887, 892
- Script steps total updated from 151 to 155
- Sitemap `Last verified` updated to 2026-06
- SKILL.md heading version corrected from v1.0 to v1.2
- Version drift detection examples corrected to use realistic FM version strings
- All `prototype` field references corrected to `format` (actual field name in function-catalog.json)
- `quickrefs.md` error codes description updated to reflect verified AI/ML range (870–892)
- Added error code accuracy caveat to Tips section directing to live docs for unfamiliar codes
- Catalog meta version bumped to FM 2025 v22 / Claris 2026

### Removed
- 5 deprecated/renamed AI script steps: Set AI Call Parameters, Perform AI Completion, Send to AI Chat, Manage RAG Space, Perform RAG Find (all removed or renamed in FM 2025 v22)

---

## [1.1] — 2026-06-05

### Changed
- `originated_in_version` audit and corrections across `function-catalog.json` — 28 functions corrected across 8 version buckets, verified against official Claris/FileMaker archived new-features pages (FM13–FM18) and community release roundups
- Key corrections: entire FM16 Crypt/JSON-adjacent wave (Base64EncodeRFC, CryptAuthCode, CryptDecrypt, CryptDecryptBase64, CryptDigest, CryptEncrypt, CryptEncryptBase64, HexDecode, HexEncode, TextDecode, TextEncode, SortValues, UniqueValues, Get(AccountGroupName), Get(RegionMonitorEvents)) shifted from incorrect FM17/FM18/FM15/FM14/FM19 assignments to FM16
- FM13 Go functions corrected: Get(ScriptAnimationState), Get(WindowOrientation), GetContainerAttribute shifted from FM17 to FM13
- Pre-tracking functions corrected from FM15/FM17 to legacy
- Container functions corrected: GetThumbnail FM12, GetLayoutObjectAttribute FM8
- Get(TouchKeyboardState) corrected from FM17 to FM14; While corrected from FM14 to FM18
- Get(ActiveRecordNumber) and Get(UUIDNumber) corrected to FM17

Updated version distribution: 103 legacy, 90 FM7, 25 FM8, 15 FM9, 6 FM10, 8 FM11, 14 FM12, 7 FM13, 2 FM14, 14 FM15, 27 FM16, 2 FM17, 7 FM18, 9 FM19, 4 FM19.3, 5 FM20.1.1, 9 FM21.0.1, 3 FM21.1.1, 10 FM22.0.1

---

## [1.0] — 2026-05

Initial public release.

### Added
- `function-catalog.json` — all 360 calculation functions with format, parameters, purpose, category, doc_url, originated_in_version
- `script-steps-catalog.json` — 151 script steps across 14 categories
- `logical-json-ai-functions-examples.md` — Logical, JSON, and AI function usage examples
- `get-functions-examples.md` — all 135 Get() functions across 12 categories
- `design-container-functions-examples.md` — Design and Container/Crypt/OCR functions
- `text-functions-examples.md` — Text and Text Formatting functions
- `date-time-functions-examples.md` — Date, Time, and Timestamp functions
- `numeric-functions-examples.md` — Number, Financial, Trigonometric, and Repeating functions
- `specialty-functions-examples.md` — Aggregate, Japanese, Mobile/Go, and Miscellaneous functions
- `quickrefs.md` — error codes, ExecuteSQL syntax, Data API endpoints, help centre sitemap
- Version drift detection — flags live doc pages that reference a newer FM version than the skill was built against

---

## [0.9] — 2026-05

### Added
- `originated_in_version` field added to all 360 functions in `function-catalog.json`, ranging from `legacy` (pre-FM7) through `22.0.1`

---

## [0.8] — 2026-05

### Fixed
- SKILL.md accuracy pass — corrected container key functions list, script step counts, design functions list, Get() category breakdown, AI functions list

---

## [0.7] — 2026-05

### Changed
- Reference file quality pass — `design-container-functions-examples.md` complete rewrite; `get-functions-examples.md` expanded with 47 missing functions; deprecated function synonyms documented

---

## [0.6] — 2026-05

### Added
- Complete function coverage — time/timestamp, financial, trigonometric, repeating, miscellaneous, mobile, and Japanese example files; all 360 functions now covered by a local example file

---

## [0.5] — 2026-05

### Added
- `aggregate-functions-examples.md`, `date-functions-examples.md`, `design-functions-examples.md`, `container-functions-examples.md`

---

## [0.4] — 2026-05

### Added
- `script-steps-catalog.json`
- `logical-functions-examples.md`, `json-functions-examples.md`, `error-codes-quickref.md`

---

## [0.3] — 2026-05

### Changed
- Replaced `functions-index.md` with enriched `function-catalog.json`
- Hardened function trigger language in SKILL.md

---

## [0.2] — 2026-05

### Added
- `get-functions-examples.md`

---

## [0.1] — 2026-05

### Added
- `functions-index.md` — initial function index
