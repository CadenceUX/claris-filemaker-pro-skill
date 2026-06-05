# Changelog

All notable changes to this skill are documented here.

---

## [1.2] — 2026-06

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

## [1.1] — 2025

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

## [1.0] — 2025

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

## [0.9] — 2025

### Added
- `originated_in_version` field added to all 360 functions in `function-catalog.json`, ranging from `legacy` (pre-FM7) through `22.0.1`

---

## [0.8] — 2025

### Fixed
- SKILL.md accuracy pass — corrected container key functions list, script step counts, design functions list, Get() category breakdown, AI functions list

---

## [0.7] — 2025

### Changed
- Reference file quality pass — `design-container-functions-examples.md` complete rewrite; `get-functions-examples.md` expanded with 47 missing functions; deprecated function synonyms documented

---

## [0.6] — 2025

### Added
- Complete function coverage — time/timestamp, financial, trigonometric, repeating, miscellaneous, mobile, and Japanese example files; all 360 functions now covered by a local example file

---

## [0.5] — 2025

### Added
- `aggregate-functions-examples.md`, `date-functions-examples.md`, `design-functions-examples.md`, `container-functions-examples.md`

---

## [0.4] — 2025

### Added
- `script-steps-catalog.json`
- `logical-functions-examples.md`, `json-functions-examples.md`, `error-codes-quickref.md`

---

## [0.3] — 2025

### Changed
- Replaced `functions-index.md` with enriched `function-catalog.json`
- Hardened function trigger language in SKILL.md

---

## [0.2] — 2025

### Added
- `get-functions-examples.md`

---

## [0.1] — 2025

### Added
- `functions-index.md` — initial function index
