# claris-filemaker-pro-skill

A [Claude skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) (and plugin) for Claris FileMaker Pro development. Gives Claude accurate, version-aware knowledge of every FileMaker calculation function, script step, field type, and platform support matrix — verified against Claris documentation rather than relying on training data.

Built and maintained by [Darrin Southern](https://www.linkedin.com/in/darrin-southern/) from [CadenceUX](https://cadenceux.com.au).

**Which skill to start with.** If you have Claris's FileMaker Agentic Development Kit (ADK),
start with [cadenceux-dx](https://github.com/CadenceUX/cadenceux-dx-skill): it
routes each task, ADK included, and checks that your skills, ADK and FileMaker Pro are current.
This skill is the reference it calls on. Without ADK (FileMaker 26.0.3 or earlier, or a plain
chat), this skill works on its own as your FileMaker Pro reference.

---

## What it does

When this skill is active, Claude will:

- Look up any of the **370 calculation functions** by name, category or description — with correct syntax, parameters, **return type**, and a direct link to the Claris Help Centre page — including FileMaker 26.1's `Get(SortOrder)` and `CreateToolDefinitions`
- Look up any of the **218 script steps** across 16 categories, including FileMaker 26.1's `Set Variable by Name` and `Replace Field Contents by Name`, the FM 26 AI additions and the PDF Files and Persistent Data categories
- Answer **"does this step work in WebDirect / FileMaker Go / the Data API?"** from a verified matrix covering all 216 steps across seven products — Pro, Go, WebDirect, Server, Cloud, Data API, Custom Web Publishing
- Advise on **field types** — which options apply to which type, indexing and storage behaviour, the eight summary types, container external storage, and FM 26 advanced field options
- Reference **accurate error codes** with official descriptions
- Cover the **OData API**, **FileMaker Data API**, **WebDirect** and **FileMaker Go** surfaces directly
- Detect **version drift** — if a fetched page's "Originated in version" is newer than the version the reference files were verified against, it flags it
- **Know FileMaker 26.1 ahead of the docs.** Most 26.1 additions aren't in Claris's Help yet, and ADK's bundled Help predates them all. The catalogs carry them, marked "announced" until Claris publishes the page
- **Work with Claris's FileMaker Agentic Development Kit (ADK).** When ADK is installed (Claude Code, or any harness running its `adk-mcp` server), the skill defers to the real FileMaker engine and Claris's own Help pages for exact signatures, validates every calculation it writes, and adds the platform, version and API detail ADK doesn't carry. Without ADK it works on its own

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
| `function-catalog.json` | All 370 functions through FM 26.1 (369 documented by Claris, one announced) — format, parameters, **return_type**, purpose, category, doc_url, originated_in_version |
| `script-steps-catalog.json` | All 218 script steps through FM 26.1 (216 documented, two announced) across 16 categories — syntax, purpose, notes, doc_url, originated_in_version, and delta-encoded **seven-product platform support** |
| `field-types-catalog.json` | Six data types × three field types, applicable options, indexing and storage semantics, eight summary types, FM 26 advanced field options |
| `odata-api-reference.md` | Base URL, auth, query options, CRUD, `$batch`, schema modification, running scripts, unsupported features |
| `webdirect-reference.md` | Measured step support (106 yes / 35 partial / 75 no, as of 26.0.3), feature limits, connection limits, design guidance |
| `filemaker-go-reference.md` | Measured step support (154 / 20 / 42), Go-only steps, behaviour differences, device capabilities |
| `logical-json-ai-functions-examples.md` | Logical + JSON + AI/embedding functions with usage examples |
| `get-functions-examples.md` | All Get() functions across 12 categories |
| `design-container-functions-examples.md` | Design + Container/Crypt/OCR functions |
| `text-functions-examples.md` | Text + Text Formatting functions |
| `date-time-functions-examples.md` | Date + Time/Timestamp functions |
| `numeric-functions-examples.md` | Number + Financial + Trigonometric + Repeating |
| `specialty-functions-examples.md` | Aggregate + Japanese + Mobile/Go + Miscellaneous + Persistent Data |
| `error-codes.md` | Every FileMaker error code with Claris's description |
| `sql-reference.md` | ExecuteSQL / FileMaker SQL syntax, joins, subqueries, ROWID / ROWMODID |
| `data-api-reference.md` | FileMaker Data API endpoints, auth, scripts, containers |
| `help-sitemap.md` | FileMaker-Pro-scoped map of the Claris Help Centre |
| `adk-mode.md` | How the skill works alongside ADK: detection in any harness, the 26.1 gap in ADK's Help, engine validation, page lookup, hand-offs |
| `version-26-1.md` | FileMaker 26.1 for developers: new and changed steps, calculated value lists, self-documenting solutions, WebDirect and Go parity, Server |

**Version coverage:** FileMaker 26.1 — catalogs re-derived from the live Claris pages on
2026-11-18 against FileMaker Pro 26.1.1 (build 26.1.1.54, the latest public release), and every
function checked against the 26.1.1 engine. Every example that can run without a record was
evaluated on the FileMaker engine (via ADK) — 255 passed, 0 failed.

---

## Installation

**Claude Code** (from the `cadenceux` plugin marketplace):

```bash
claude plugin marketplace add https://github.com/CadenceUX/cadenceux-skills.git
claude plugin install claris-filemaker-pro@cadenceux
```

**claude.ai and Cowork:** Customize → Plugins → Add marketplace from GitHub →
`CadenceUX/cadenceux-skills`, then install **claris-filemaker-pro**.

**Claude desktop app (macOS):** download [`claris-filemaker-pro.skill`](https://github.com/CadenceUX/claris-filemaker-pro-skill/releases/latest/download/claris-filemaker-pro.skill) and
double-click it.

**Claude.ai in a browser, as a single skill:** Customize → Skills → upload
[`claris-filemaker-pro.zip`](https://github.com/CadenceUX/claris-filemaker-pro-skill/releases/latest/download/claris-filemaker-pro.zip).

> Both files are attached to the latest [release](https://github.com/CadenceUX/claris-filemaker-pro-skill/releases).
> Don't use GitHub's green **Code → Download ZIP** button or a release's **Source code (zip)**:
> those are snapshots of the repository, not a packaged skill, and Claude won't install them
> as one.

This repository is itself a valid plugin (`.claude-plugin/plugin.json`), so
`claude --plugin-dir <this folder>` loads it for local testing.

---

## How it works

**Without ADK** the skill is local-first: Claude answers from the bundled reference files and
fetches the live Claris page only when a topic is volatile (AI providers), an entry is newer
than the last verification, you ask for "latest", or it's unsure the local data is complete.
If a live page contradicts a local file, the live page wins and Claude says so.

**With ADK** (Claris's FileMaker Agentic Development Kit, FileMaker Pro 26.1 or later) the order
changes: the FileMaker engine first (Claude validates and evaluates the calculations it
writes), then Claris's own Help pages, then this skill. The skill still supplies the
seven-product platform matrix, version notes, the FileMaker 26.1 additions ADK's Help doesn't
carry yet, the Data API / OData / WebDirect / Go / SQL references, and a warning for steps the
engine knows that no documentation covers.

---

## Keeping it current

`last_known_fm_version` is `26.1`. Two mechanisms keep the skill honest:

1. **Version drift detection** flags any fetched page whose "Originated in version" exceeds it.
2. **Maintainer tools** (`maintainer/`, not part of the installed skill):
   - `rebuild_harvest.py` / `rebuild_extract.py` re-derive the catalogs from Claris's pages.
   - `verify_examples.py` runs every runnable example through the FileMaker engine (needs ADK)
     and fails on any mismatch — the release gate since 2.1.0.

The rebuild scripts encode a trap found the hard way: Claris's page `topic_type` metadata is
unreliable for determining the roster — derive it from page structure instead.

---

## Related skills

Part of the CadenceUX skill set, installed together from the
[`cadenceux` marketplace](https://github.com/CadenceUX/cadenceux-skills):

| Skill | Covers |
|---|---|
| [fmp-dev-design-patterns](https://github.com/CadenceUX/fmp-dev-design-patterns) | Scripting conventions and patterns |
| [goya-be-plugin](https://github.com/CadenceUX/goya-be-plugin-skill) | BaseElements plug-in |
| [monkeybread-mbs-plugin](https://github.com/CadenceUX/monkeybread-mbs-plugin-skill) | MBS plug-in |
| [beezwax-bbox-plugin](https://github.com/CadenceUX/beezwax-bbox-plugin-skill) | bBox plug-in |
| [cadenceux-dx](https://github.com/CadenceUX/cadenceux-dx-skill) | Routing across the set |

With Claris's FileMaker Agentic Development Kit (ADK) installed, schema, scripts and layouts are
written to the file directly, so clipboard XML skills aren't needed.

---

## Contributing

Issues and PRs welcome — particularly corrections to `originated_in_version` values, missing or
renamed script steps, platform-support changes, new error codes, and stale help centre URLs.

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use, adapt, and redistribute with attribution.
