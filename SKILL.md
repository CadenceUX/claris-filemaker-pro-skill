---
name: claris-filemaker-pro
description: >-
  FileMaker Pro reference for calculation functions, script steps, field types and error codes:
  exact syntax, parameters, return types, the release that introduced each, and which script
  steps work in FileMaker Go, WebDirect, Server, Cloud, the Data API and Custom Web Publishing.
  Also covers the FileMaker Data API, OData, ExecuteSQL and FileMaker SQL, and WebDirect and
  FileMaker Go limits. Use whenever a FileMaker function or script step is named, written,
  reviewed or debugged, including inside a calculation, a script or other code, or when asked
  whether something works on a given FileMaker client or version. When the Claris Agentic
  Development Toolkit (ADT) is installed, it defers to ADT's filemaker-help pages and the
  FileMaker engine for exact signatures, and adds platform, version and API detail ADT does not
  carry. Not for FileMaker Server administration, Claris Connect, Claris Studio or ODBC/JDBC
  driver setup.
license: CC-BY-4.0
compatibility: >-
  Claude.ai, Claude Desktop, Cowork and Claude Code. ADT mode needs the Claris Agentic
  Development Toolkit plugin (macOS); everything else works without it.
metadata:
  author: Darrin Southern, CadenceUX
  version: "2.2.0"
---

# Claris FileMaker Pro

Reference for FileMaker Pro's calculation functions, script steps and field types, the clients
they run on, and the APIs around them. The source of truth is Claris's FileMaker Pro Help; this
skill adds structured platform support, version notes and tested patterns.

## Mode: check for ADT first

At the start of the first FileMaker question in a session, decide the mode:

**ADT mode** if any of these is true:
1. The session lists a `filemaker-agentic-development:` skill (for example `filemaker-help`).
2. Tools named `mcp__plugin_filemaker-agentic-development_adt-mcp__*` are available.
3. A shell is available and `"$HOME/Library/Application Support/ADT/MCP/fm-cli/fm-cli"` exists.

In ADT mode, read [references/adt-mode.md](references/adt-mode.md) before answering. Claris's
page and the FileMaker engine become the authority for signatures and behaviour; this skill
supplies platform support, versions and the API references. Never install ADT from this skill.

ADT reaches the file through FileMaker Pro's Agent Access, which needs the FileMaker Pro version
ADT states. If an ADT tool can't reach the file, run `adt doctor` (or `fmp-dev-orchestrator`'s
stack check) and relay its fix. ADT is in Claris's preview programs: report ADT and preview
FileMaker Pro version numbers to the user only; never write them into files or anything published.

**Standalone mode** otherwise (Claude.ai chat, Windows, any host without ADT). Answer from the
files below; fetch the live Claris page when the rules in "When to fetch live" apply.

### Which source wins

| ADT mode | Standalone mode |
|---|---|
| 1. FileMaker engine (`validate` / `evaluate`, `help script steps`) | 1. Live help.claris.com page |
| 2. Claris page (`filemaker-help`, or live when newer) | 2. This skill's reference files |
| 3. This skill's reference files | 3. Memory — never alone for a signature |
| 4. Memory — never alone for a signature | |

When two sources disagree, say so and name both.

## Answering a FileMaker question

Copy this checklist into your working and tick it off:

```
- [ ] 1. List every function and script step named or implied
- [ ] 2. Signature: ADT mode → Claris page; standalone → catalog (live page if volatile)
- [ ] 2b. A step missing from script-steps-catalog.json but known to the engine
        (`filemaker help script steps "<name>"`) → say "undocumented, probably pre-release,
        not safe to ship" before anything else
- [ ] 3. Platform: check platform_exceptions for the user's client(s) — Partial is not Yes
- [ ] 4. Version: add the note for originated_in_version (table below)
- [ ] 5. ADT mode: validate every calculation, evaluate where possible; fix and repeat until valid
- [ ] 6. Answer with the signature inline, cite the Claris page as
        https://help.claris.com/en/pro-help/content/<slug>.html, say what was engine-verified
```

## Where to look

| Question | File |
|---|---|
| A function's signature, parameters, return type, version | [function-catalog.json](references/function-catalog.json) — search, don't read |
| A script step's syntax, notes, version, platform support | [script-steps-catalog.json](references/script-steps-catalog.json) — search, don't read |
| Logical, JSON, AI / embedding functions | [logical-json-ai-functions-examples.md](references/logical-json-ai-functions-examples.md) |
| Get() functions and their enumerations | [get-functions-examples.md](references/get-functions-examples.md) |
| Text and text formatting | [text-functions-examples.md](references/text-functions-examples.md) |
| Date, time, timestamp | [date-time-functions-examples.md](references/date-time-functions-examples.md) |
| Number, financial, trigonometric, repeating | [numeric-functions-examples.md](references/numeric-functions-examples.md) |
| Design (schema) and container / crypto functions | [design-container-functions-examples.md](references/design-container-functions-examples.md) |
| Aggregate, Japanese, mobile, miscellaneous, persistent data | [specialty-functions-examples.md](references/specialty-functions-examples.md) |
| Field types, options, indexing, storage, summary types | [field-types-catalog.json](references/field-types-catalog.json) |
| An error number | [error-codes.md](references/error-codes.md) |
| ExecuteSQL / FileMaker SQL syntax, ROWID / ROWMODID | [sql-reference.md](references/sql-reference.md) |
| Data API (REST) | [data-api-reference.md](references/data-api-reference.md) |
| OData | [odata-api-reference.md](references/odata-api-reference.md) |
| WebDirect limits | [webdirect-reference.md](references/webdirect-reference.md) |
| FileMaker Go limits and device features | [filemaker-go-reference.md](references/filemaker-go-reference.md) |
| A Claris help page URL | [help-sitemap.md](references/help-sitemap.md), else `https://help.claris.com/llms-full.txt` |
| ADT is installed | [adt-mode.md](references/adt-mode.md) |

### Searching the catalogs

The two JSON catalogs are thousands of lines long. Search them; don't read them whole:

```bash
grep -n -A12 '"name": "JSONSetElement' references/function-catalog.json
jq '.categories[].steps[] | select(.name == "Go to Layout")' references/script-steps-catalog.json
jq -r '.categories[].steps[] | select(.platform_exceptions.WebDirect == "No") | .name' references/script-steps-catalog.json
```

Without a shell, open the matching example file first — each starts with a contents list.

## Platform support

`script-steps-catalog.json` records support for every step on seven products: **Pro, Go,
WebDirect, Server, Cloud, DataAPI, CWP**. It's delta-encoded: `platform_exceptions` lists only
the products where a step isn't fully supported. **No `platform_exceptions` means supported
everywhere.**

| Value | Meaning |
|---|---|
| *(absent)* | Fully supported on all seven |
| `"No"` | Skipped. Returns error **3** ("Command is unavailable"), shows no alert, and the script continues |
| `"Partial"` | Runs, but some options or behaviour differ. Read the step's notes or Claris page |

Treating Partial as supported is a common, costly mistake: `Go to Layout`, `Go to Portal Row`,
`Go to List of Records`, `Execute SQL` and `Export Records` are all Partial somewhere.
`os_restriction` is separate: a macOS-only or Windows-only step.

Functions have no compatibility table in Claris's docs. Where it matters, read the function's
page notes, branch on `Get ( ApplicationVersion )`, and watch for error **1225** ("Function
referred to is not supported in this context").

## Version notes

Read `originated_in_version` and add the note without asking which version the user has:

| Originated | Note |
|---|---|
| 26.x | "FileMaker 2026 (26) — not in earlier versions." |
| 22.x | "Introduced in FileMaker 2025 (22)." |
| 21.x | "Requires FileMaker 2024 (21) or later." |
| 19.3 – 20.x | "Requires FileMaker 19.3 or later." Describe a fallback if one exists |
| 18.x or earlier | No note unless asked |

Claris dates some FileMaker 2026 features as 26.0 and others as 26.0.1 (the first public
build). Treat both as FileMaker 2026. The latest public release the catalogs were checked
against is in `meta.latest_public_release` (26.0.3). Point releases can change behaviour
without a new `originated_in_version` — e.g. 26.0.3 made Open / Append / Close PDF fully
supported in WebDirect — so check the step's notes.

**Engine ahead of the docs:** in ADT mode, the first line of `filemaker --help` shows the engine
version (`--version` shows only the ADT version). The engine can be newer than the latest public
release and know script steps no Claris page documents. **When asked about a step that isn't in
`script-steps-catalog.json` but the engine knows, you MUST say it exists in that engine build but
is undocumented and probably pre-release — not safe to ship yet** — and describe only what
`filemaker help script steps "<name>"` shows.

## When to fetch live

Answer from the files by default. Fetch the Claris page when:

- the topic is AI or embedding — providers and options change between point releases
- `originated_in_version` is newer than the catalog's `last_known_fm_version`
- the user says "latest", "current", "has this changed", or names a newer version
- you need a full request/response body or an exhaustive option matrix
- an entry is missing, or you're unsure it's complete

Check **Originated in version** in the page body, not the YAML frontmatter. If a fetched page
documents something newer than `last_known_fm_version`, say the skill's files may lag on it,
and answer from the page. If a live page contradicts a file here, the page wins; say so.

## Version self-check

Once per session, on the first FileMaker question: fetch
`https://github.com/CadenceUX/claris-filemaker-pro-skill/raw/main/VERSION` and compare it with
this skill's version (2.2.0). If newer, start the answer with:

> ⚠️ **Skill update available:** this skill is v[installed]; v[latest] is at
> https://github.com/CadenceUX/claris-filemaker-pro-skill/releases

Skip silently if the fetch fails. If the skill was installed as a plugin, suggest
`claude plugin update` (or the Plugins page on claude.ai) instead of the releases link. If
`fmp-dev-orchestrator` is installed, skip this check: its stack check covers every CadenceUX
skill, plus ADT, FileMaker Pro and the ADT project.

## Gotchas worth knowing up front

- **JSON:** `JSONRaw` = **0**; `JSONGetElementType` returns `?…` text for a missing key, never
  0; FileMaker sorts object keys alphabetically; `"[+]"` appends to an array.
- **Get() enumerations are easy to confuse:** `Get ( Device )` 3 = iPad, 4 = iPhone;
  `Get ( SystemPlatform )` -2 = Windows, 3 = iOS; `Get ( RecordOpenState )` 1 = new, 2 = modified.
- **Time since 1/1/0001:** `Get ( CurrentTimeUTCMilliseconds )` counts from year 1 — subtract
  62135596800000 for Unix milliseconds.
- **Financial functions return positive values:** `PMT`, `PV` and `FV` — no `Abs()` needed.
- **Base64:** `Base64Encode` wraps lines and ends with CR+LF; use `Base64EncodeRFC ( 4648 ; … )`
  for tokens, HMACs and headers.
- **`=` ignores case for text:** `"abcD" = "ABCd"` is true. Compare signatures, tokens and
  hashes with `Exact()`.
- **`Choose` vs `Case`:** map a 0-based number with `Choose ( n ; r0 ; r1 ; … )`;
  `Case` takes test/result pairs.
- **`Substitute ( text ; [ search ; replace ] ; … )`:** each bracket is one pair.
- **Field annotations narrow DDL:** when any field in a table is annotated, only annotated
  fields appear in that table's generated DDL.
- **The persistent data store isn't a field type.** It's schema-resident, needs Full Access to
  write, and isn't copied by the Data Migration Tool. `GetPersistentData` returns `?` when
  nothing matches.
- **AI / RAG order:** `Configure AI Account` (and `Configure RAG Account`) before any AI step
  or function. Always fetch live for provider options.

## Related skills

The CadenceUX skill set (github.com/CadenceUX/cadenceux-skills). Name the skill exactly when
you rely on it:

| Need | Skill |
|---|---|
| Scripting conventions, error handling, JSON parameters, anti-patterns | `fmp-dev-design-patterns` |
| BaseElements, MBS or bBox plug-in functions | `goya-be-plugin`, `monkeybread-mbs-plugin`, `beezwax-bbox-plugin` |
| Which skill owns a topic; is the stack current (skills, ADT, FileMaker Pro, ADT project) | `fmp-dev-orchestrator` |

- With ADT installed: **`filemaker-standards`** for naming, **`fm-cli`** for schema work,
  **`fm-mcp-guide`** for running scripts and SQL against a live file. ADT writes schema,
  scripts and layouts to the file directly, so never generate clipboard or fmxmlsnippet XML.

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Built and maintained by
[Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from
[CadenceUX](https://cadenceux.com.au). Version history:
https://github.com/CadenceUX/claris-filemaker-pro-skill/blob/main/CHANGELOG.md
