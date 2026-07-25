# claris-filemaker-pro-skill

A [Claude skill](https://docs.claude.ai/skills) for Claris FileMaker Pro development. Gives Claude accurate, version-aware knowledge of every FileMaker calculation function, script step, field type, and platform support matrix — verified against Claris documentation rather than relying on training data.

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).

---

## What it does

When this skill is active, Claude will:

- Look up any of the **368 calculation functions** by name, category or description — with correct syntax, parameters, **return type**, and a direct link to the Claris Help Centre page
- Look up any of the **216 script steps** across 16 categories, including the FM 26 AI additions and the new PDF Files and Persistent Data categories
- Answer **"does this step work in WebDirect / FileMaker Go / the Data API?"** from a verified matrix covering all 216 steps across seven products — Pro, Go, WebDirect, Server, Cloud, Data API, Custom Web Publishing
- Advise on **field types** — which options apply to which type, indexing and storage behaviour, the eight summary types, container external storage, and FM 26 advanced field options
- Reference **accurate error codes** with official descriptions
- Cover the **OData API**, **FileMaker Data API**, **WebDirect** and **FileMaker Go** surfaces directly
- Detect **version drift** — if a fetched page's "Originated in version" is newer than the version the reference files were verified against, it flags it

### Scope

Deliberately **FileMaker Pro only**, and deep on that surface. It is not a minimal
name-and-signature vocabulary list, and not a link index that defers every real answer to a web
fetch — the local files carry verified content and answer most questions without a network
round-trip.

Out of scope: FileMaker Server administration, Claris Connect, Claris Studio, and deep
ODBC/JDBC configuration.

---

## Coverage

| Reference file | Contents |
|---|---|
| `function-catalog.json` | All 368 functions through FM 26 — format, parameters, **return_type**, purpose, category, doc_url, originated_in_version |
| `script-steps-catalog.json` | All 216 script steps through FM 26 across 16 categories — syntax, purpose, notes, doc_url, originated_in_version, and delta-encoded **seven-product platform support** |
| `field-types-catalog.json` | Six data types × three field types, applicable options, indexing and storage semantics, eight summary types, FM 26 advanced field options |
| `odata-api-reference.md` | Base URL, auth, query options, CRUD, `$batch`, schema modification, running scripts, unsupported features |
| `webdirect-reference.md` | Measured step support (103 yes / 38 partial / 75 no), feature limits, connection limits, design guidance |
| `filemaker-go-reference.md` | Measured step support (154 / 20 / 42), Go-only steps, behaviour differences, device capabilities |
| `logical-json-ai-functions-examples.md` | Logical + JSON + AI/embedding functions with usage examples |
| `get-functions-examples.md` | All Get() functions across 12 categories |
| `design-container-functions-examples.md` | Design + Container/Crypt/OCR functions |
| `text-functions-examples.md` | Text + Text Formatting functions |
| `date-time-functions-examples.md` | Date + Time/Timestamp functions |
| `numeric-functions-examples.md` | Number + Financial + Trigonometric + Repeating |
| `specialty-functions-examples.md` | Aggregate + Japanese + Mobile/Go + Miscellaneous + Persistent Data |
| `quickrefs.md` | Error codes, ExecuteSQL syntax and system columns, Data API reference, FileMaker-Pro-scoped sitemap |

**Version coverage:** verified against FileMaker 26 (26.0.1) documentation on 2026-07-25.

---

## Installation

**Easiest — double-click (macOS):** download the `.skill` file from the
[Releases](../../releases) page and double-click it. Claude Desktop registers the `.skill`
extension and opens its install flow directly. (The `.skill` file is the release zip with a
different extension. Not yet confirmed on Windows.)

**Fallback — upload the zip:** in Claude.ai, go to **Customize → Skills** and upload the release
`.zip`. This is the path for the web app and any platform where the double-click association
isn't available.

---

## How it works

The skill is **local-first**: the bundled reference files are treated as authoritative, because
every entry was re-derived from its own live Claris page at build time. Claude fetches live
documentation only when the topic is genuinely volatile (AI/model providers), when an entry
post-dates the last verification, when you signal recency, or when it is uncertain the local
data is complete.

That matters for generation speed — composing a script or a set of field definitions shouldn't
need a network fetch per step. When a live page does contradict a local file, the live page wins
and Claude says so.

---

## Keeping it current

`last_known_fm_version` is `26`. Two mechanisms keep the skill honest:

1. **Version drift detection** flags any fetched page whose "Originated in version" exceeds it.
2. **Bundled rebuild scripts** (`scripts/`) re-derive the catalogs from source, so coverage
   claims are re-verified each release rather than inherited. See `scripts/README.md` — these
   are maintainer tools you run locally, not something Claude executes in a conversation.

The rebuild scripts encode two traps found the hard way: Claris's page `topic_type` metadata is
unreliable for determining the roster, and the frontmatter `version:` field tracks the
documentation build rather than the feature release.

---

## Contributing

Issues and PRs welcome — particularly corrections to `originated_in_version` values, missing or
renamed script steps, platform-support changes, new error codes, and stale help centre URLs.

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use, adapt, and redistribute with attribution.
