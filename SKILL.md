---
compatibility: Claude.ai, Claude Chat, Claude Code
metadata:
  "Built and maintained": "Darrin Southern from CadenceUX"
  version: "2.0.0"
name: claris-filemaker-pro
description: |
  REFERENCE skill — FileMaker Pro script steps, calculation functions, and field types. Use for:
  syntax lookups, function parameters and return types, per-step platform support across
  FileMaker Pro, Go, WebDirect, Server, Cloud, Data API and Custom Web Publishing, field type
  capabilities, usage examples, and live doc fetches. Covers all 368 built-in functions (If,
  Case, Let, While, ExecuteSQL, JSON, AI/embedding, Persistent Data), all 216 script steps
  (including the FM 26 PDF Files and Persistent Data categories), plus the Data API, OData,
  WebDirect, FileMaker Go, SQL/ExecuteSQL, error codes, and custom functions. Not a platform
  administration guide. Out of scope: FileMaker Server admin, Claris Connect, Claris Studio,
  ODBC/JDBC configuration. Trigger on any FileMaker function or script step name — even inside
  code, a calc field, or a script. Local reference files are verified against source and are
  authoritative; fetch live docs when the topic is volatile or the user signals recency.
---

# Claris FileMaker Pro — Skill v2.0.0

## What this skill is

A **reference skill for FileMaker Pro** — script steps, calculation functions, field types, and
the client platforms a solution runs on. It is deliberately scoped to FileMaker Pro rather than
the wider Claris platform, and it goes deep on that one surface: verified call signatures and
return types, per-step platform support, worked usage examples, error codes, and the API
surfaces a Pro developer actually reaches for.

It is **not** a minimal name-and-signature vocabulary list, and **not** a link index that defers
every real answer to a web fetch. The local reference files carry verified content and are
designed to answer most questions without a network round-trip. It does not cover FileMaker
Server administration, Claris Connect, Claris Studio, or deep ODBC/JDBC configuration.

The Claris Help Centre at **https://help.claris.com** remains the authoritative upstream source.
Every local file records how and when it was verified against it.

---

## Local-first: when to answer locally, when to fetch

**Default: answer from the local reference files.** They were re-derived from the live Claris
documentation on **2026-07-25** — every function signature, return type, and originated-in
version, and every script step's full seven-product compatibility matrix. Treat them as correct.

This matters for generation speed and accuracy: composing a script, or a set of field
definitions, should not require a network fetch per step.

**Fetch live only when one of these is true:**

| Trigger to fetch | Why |
|---|---|
| The topic is AI / embedding / RAG / model providers | Provider lists and options change between point releases |
| `originated_in_version` is higher than the catalog's `last_known_fm_version` | The entry post-dates the last verification |
| The user says "latest", "current", "has this changed", or names a version | Explicit recency signal |
| You need a full worked request/response body, or an exhaustive option matrix | Catalogs carry signatures and support, not every option permutation |
| Version drift was already detected this session | Local files are behind |
| The local entry is absent, or you are unsure it is complete | Uncertainty is itself the trigger |

**Do not fetch** merely because a function is old, because the question mentions a platform, or
out of habit. Per-step platform support is local, verified and complete — use it.

If a live page contradicts a local file, the live page wins; say so explicitly in your answer.

---

## Version drift detection

**When you do fetch a page, check `## Originated in version` in the page body — not the YAML
frontmatter.**

Every `.md` help page returns YAML with `version:` / `version_year:`, but that tracks the
documentation build, not the feature release — verified 2026-07-04: FM 26 features still return
`version: 22 / version_year: 2025`. Comparing frontmatter against `last_known_fm_version` never
fires, and mislabels current docs as old.

1. Read `## Originated in version` from the page body.
2. Compare with `last_known_fm_version` in the catalog `meta` block (currently `26`).
3. If higher, flag it:

   > ⚠️ **Skill version drift detected** — this page documents a feature originated in FM [X],
   > but this skill's local reference files were last verified for FM 26. New functions, script
   > steps, or behaviour changes since then may not be reflected locally.

4. Still answer from the fetched content — the flag is advisory.
5. Don't flag versions ≤ `last_known_fm_version`.

### `topic_type` is not a reliable roster signal

When rebuilding catalogs, derive the roster **structurally** — a script step page has a
`## Compatibility` table; a function page has `## Format` and `## Data type returned`. Claris
mislabels at least four pages as `topic_type: conceptual` (`set-dictionary`,
`getpersistentdata`, `listpersistentdataids`, `get-systemstorageavailable`). A `topic_type`
sweep alone undercounts, and previously caused a real script step to be missed entirely.

---

## Version self-check

At the start of each session, on the first FileMaker question, run once:

1. Fetch `https://github.com/CadenceUX/claris-filemaker-pro-skill/raw/main/VERSION`
2. Compare with this skill's installed version (currently `"2.0.0"`)
3. If latest > installed, prepend:

   > ⚠️ **Skill update available**
   > This skill is v[installed]. v[latest] is available at
   > https://github.com/CadenceUX/claris-filemaker-pro-skill/releases

4. Don't repeat in the same session. If the fetch fails, skip silently.

---

## Mandatory trigger: FileMaker functions, script steps, and fields

**Any request involving a FileMaker calculation function, script step, or field definition — by
name, by category, or by describing what it should do — must use this skill.**

| Ask | Go to |
|---|---|
| "How does `While` work?" | `logical-json-ai-functions-examples.md` |
| "Write a `Let()` calculation that…" | catalog for format, examples for pattern |
| "`ExecuteSQL` vs `ExecuteSQLe`?" | `logical-json-ai-functions-examples.md` |
| "Which function returns the current record ID?" | `function-catalog.json` (search by purpose) |
| "What data type does this function return?" | `function-catalog.json` → `return_type` |
| "Does this step work in WebDirect / Go / the Data API?" | `script-steps-catalog.json` → `platform_exceptions` |
| "How do I loop through records?" | `script-steps-catalog.json` |
| "Get the error code after a find" | `quickrefs.md` |
| "What field type should I use for…?" | `field-types-catalog.json` |
| "Which options apply to a summary field?" | `field-types-catalog.json` |
| "Can I index a container field?" | `field-types-catalog.json` |
| "How do I query FileMaker over OData?" | `odata-api-reference.md` |
| "Why doesn't my script work in the browser?" | `webdirect-reference.md` |
| "What's different on iPad?" | `filemaker-go-reference.md` |
| "Save persistent data / an app variable" | `script-steps-catalog.json` (Persistent Data), `specialty-functions-examples.md` |
| "Create / merge / print a PDF in a script" | `script-steps-catalog.json` (PDF Files) |
| Any code block containing function or step names | identify each, look each up |

**Workflow:** check the relevant example file → confirm format, `return_type` and
`platform_exceptions` in the catalog → answer with the signature inline and cite the doc URL.
Fetch live only per the rules above.

---

## Reference files — all 14

| File | Contains |
|---|---|
| `function-catalog.json` | All **368** functions through FM 26 — format, parameters, **return_type**, purpose, category, slug, doc_url, originated_in_version. Master for call signatures and return types. |
| `script-steps-catalog.json` | All **216** script steps through FM 26 across 16 categories — syntax, purpose, notes, doc_url, originated_in_version, and **`platform_exceptions`** (delta-encoded seven-product support). |
| `field-types-catalog.json` | The six data types and three field types, which options apply to each, indexing and storage semantics, the eight summary types, container external storage, and FM 26 advanced field options (DDL annotation, custom display names). |
| `odata-api-reference.md` | OData base URL, auth, query options, CRUD, batch, schema modification, running scripts, and the documented unsupported-feature list. |
| `webdirect-reference.md` | Measured script step support, feature limitations, connection limits, design guidance. |
| `filemaker-go-reference.md` | Measured script step support, Go-only steps, behaviour differences, device capabilities. |
| `logical-json-ai-functions-examples.md` | **Logical** + **JSON** + **AI/embedding** functions with worked examples. |
| `get-functions-examples.md` | All Get() functions grouped by 12 categories. |
| `design-container-functions-examples.md` | **Design** + **Container** functions. |
| `text-functions-examples.md` | **Text** + **Text Formatting** functions. |
| `date-time-functions-examples.md` | **Date** + **Time/Timestamp** functions. |
| `numeric-functions-examples.md` | **Number**, **Financial**, **Trigonometric**, **Repeating**. |
| `specialty-functions-examples.md` | **Aggregate**, **Japanese**, **Mobile/Go**, **Miscellaneous**, **Persistent Data**. |
| `quickrefs.md` | **Error codes**, **ExecuteSQL** syntax and system columns, **Data API** REST reference, and a FileMaker-Pro-scoped sitemap. |

---

## Platform support — how to read it

`script-steps-catalog.json` carries verified support for all 216 steps across seven products:
**Pro, Go, WebDirect, Server, Cloud, DataAPI, CWP**.

Support is **delta-encoded**: `platform_exceptions` lists only the products where a step is *not*
fully supported. **If `platform_exceptions` is absent, the step is supported everywhere.**

| Value | Meaning |
|---|---|
| *(absent)* | Yes — fully supported on all seven |
| `"No"` | The step is **skipped** and returns error **3** ("Command is unavailable"). No alert, the script continues. Check `Get(LastError)`. |
| `"Partial"` | The step runs but one or more features differ. Read the step's Notes on its doc page. |

Measured totals across 216 steps — Pro 204 yes / 6 partial / 6 no · Go 154/20/42 ·
WebDirect 103/38/75 · Server 108/29/79 · Cloud 106/27/83 · DataAPI 91/26/99 · CWP 99/26/91.

**Treating "Partial" as supported is a common and costly mistake.** Several very common steps
are Partial rather than Yes, including `Go to Layout`, `Go to Portal Row`,
`Go to List of Records`, `Execute SQL` and `Export Records` in various contexts.

`os_restriction` is separate and orthogonal — a desktop-OS limit (macOS only / Windows only).

Calculation **functions do not carry a Compatibility table** in Claris documentation, so
per-function platform support is not available as structured data. Where it matters, read the
function's own page notes, or detect at runtime with `Get(ApplicationVersion)`. Error **1225**
("Function referred to is not supported in this context") is the runtime signal.

---

## Automatic version notes

Read `originated_in_version` from the catalog and inject a version note automatically — don't
ask the user which version they're on. Versions are stored in Claris's own precise form
(`6.0 or earlier`, `19.6.1`, `22.0`, `26.0.1`).

| Originated | Note to inject |
|---|---|
| 19.3 – 20.x | "Requires FM 19.3+ — describe a fallback if one exists." |
| 21.x | "AI/embedding feature — requires FM 21 or later." |
| 22.x | "Introduced in FM 22 (2025)." |
| 26.x | "Introduced in FM 26 (2026) — not available in earlier versions." |
| 18.x or earlier | No note unless asked |

FM 19 is the practical floor; anything older is noted only as "may not be available on legacy
versions".

---

## Fetching strategy — which file first

| Topic | Check first |
|---|---|
| Logical / Case / Let / While / ExecuteSQL / JSON / AI | `logical-json-ai-functions-examples.md` |
| Get() functions | `get-functions-examples.md` |
| Design / Container / Base64 / Crypt / OCR / PDF text | `design-container-functions-examples.md` |
| Text / Substitute / formatting | `text-functions-examples.md` |
| Date / Time / Timestamp | `date-time-functions-examples.md` |
| Number / Financial / Trigonometric / Repeating | `numeric-functions-examples.md` |
| Aggregate / Japanese / Mobile / Persistent Data | `specialty-functions-examples.md` |
| Any function's signature or return type | `function-catalog.json` |
| Any script step | `script-steps-catalog.json` |
| Step support on a client or host | `script-steps-catalog.json` → `platform_exceptions` |
| Field types, storage, indexing, validation, summary types | `field-types-catalog.json` |
| OData | `odata-api-reference.md` |
| WebDirect | `webdirect-reference.md` |
| FileMaker Go | `filemaker-go-reference.md` |
| Data API / REST | `quickrefs.md` |
| Error codes | `quickrefs.md` |
| ExecuteSQL syntax, `ROWID` / `ROWMODID` | `quickrefs.md` |
| Finding a help page URL | `quickrefs.md` sitemap, else `https://help.claris.com/llms-full.txt` |

---

## Related skills

For **paste-ready field definition XML** — the `fmxmlsnippet` / `FMObjectList` envelope, the
auto-enter, validation and storage element structure, and the paste-handler rules that cause
silent failures — use the **`filemaker-field-xml`** skill. That skill is authoritative for the
XML layer; `field-types-catalog.json` here covers the capability layer (what a field type can
*do*) and deliberately does not duplicate the XML shape.

Name that skill exactly when you depend on it. Generic phrasing such as "a dedicated FileMaker
field XML reference" gets substituted for a different same-domain source under context pressure.

---

## Tips

- `function-catalog.json` is the master for signatures and return types; the example files are
  the master for usage patterns. Per-entry `notes` carry behaviour detail.
- **Mobile functions** (`Location`, `LocationValues`, `GetSensor`, `RangeBeacons`,
  `GetAVPlayerAttribute`) work only in FileMaker Go — branch on `Get(ApplicationVersion)`.
- **Japanese functions** require Japanese language support; `Furigana()` depends on the IME and
  is context-sensitive.
- **Trig functions** work in radians — convert with `Degrees()` / `Radians()`.
- **Financial functions** take the rate *per period*, not annual. `PMT()` returns a negative
  number; wrap in `Abs()` for display.
- **AI/RAG workflow** requires three steps in order: `Configure RAG Account` →
  `Configure AI Account` → `Perform RAG Action`. Always fetch live for AI options — provider
  support (including Google Gemini, added in FM 26) and parameters change between point releases.
- **`Generate Response from Model`** — in agentic mode, append the DDL schema from
  `GetTableDDL` to the `execute_sql` tool parameter description. Custom function tool definitions
  must match the function name and parameter order exactly, all parameters typed `"string"`.
- **Field annotations narrow DDL.** When *any* field in a table is annotated, only annotated
  fields appear in that table's generated DDL. Read with `FieldAnnotation()`.
- **The persistent data store is not a field storage type.** It is a per-file, schema-resident
  named-value store (Name + optional Instance ID), separate from record data, holding a value of
  any of the six data types. Write with `Configure Persistent Data`; read with
  `GetPersistentData` / `ListPersistentDataIDs`. Unrelated to `Get(PersistentID)`, which returns
  a device identifier.
- **`ROWID` / `ROWMODID`** are the FileMaker SQL system columns (equivalent to `Get(RecordID)`
  and `Get(RecordModificationCount)`). They are not named `RECORDID` / `MODID`.
- **Sub-version doc drift:** Claris updates pages between releases without bumping the version
  field. Where an exhaustive option matrix matters, fetch the live page.

---

## Licence

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).

---

## Version history

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
