## [1.8] — 2026-06

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

## [1.7] — 2026-06

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

## [1.6] — 2026-06

### Changed

- `SKILL.md` — `last_known_fm_version` updated from `22` → `26` in preparation for FM 26 release
  (which released June 2026, after v1.5 shipped).
- `SKILL.md` — Added "Coverage gap — FM 26 (2026)" section documenting known FM 26 additions
  that require live fetch until a full v1.7 catalog rebuild.
- `SKILL.md` — Version drift detection examples updated to reference `last_known_fm_version: 26`.
- `SKILL.md` — heading and frontmatter version bumped to 1.6.

---

## [1.5] — 2026-06

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

## [1.3] — 2026-05

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

## [1.2] — 2026-05

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

## [1.1] — 2026-05

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
