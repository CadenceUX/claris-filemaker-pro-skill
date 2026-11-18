# ADK mode

Read this file when Claris's FileMaker Agentic Development Kit (ADK) is present (see SKILL.md →
Mode). In ADK mode this skill is **not** the authority on function or script step facts. The
FileMaker engine and Claris's own page are. This skill adds what they don't carry: platform
support as data, version awareness, the FileMaker 26.1 additions ADK's bundled Help doesn't
document yet, the Data API / OData / WebDirect / Go / SQL references, and engine-tested patterns.

*Checked against ADK 0.16.0 (November 2026), whose engine reports FileMaker 26.1.1. ADK works
with FileMaker Pro 26.1 or later; files hosted on FileMaker Server need 26.1.1 or later. For
which ADK you have and whether it's current, run `adk doctor`.*

---

## Contents
1. Which ADK pieces you have
2. The 26.1 gap in ADK's bundled Help
3. Look up the Claris page by slug
4. Validate every calculation; evaluate where you can
5. Check a script step exists against the engine
6. Hand-offs
7. What stays with this skill

## 1. Which ADK pieces you have

ADK is two surfaces, and a harness may have either or both:

| Surface | How it shows up | What it gives this skill |
|---|---|---|
| **Claude Code plugin** (`filemaker-agentic-development@claris`) | Skills named `filemaker-help`, `fm-cli`, `fm-mcp-guide`, `filemaker-standards`, `adk-project-setup`, `adk-webviewer-app` | Claris's Pro Help pages, the standards, the guides |
| **The `adk` and `filemaker` command-line tools, and the `adk-mcp` server** | `adk` / `filemaker` on PATH, or MCP tools whose names contain `adk-mcp` (in Claude Code: `mcp__plugin_filemaker-agentic-development_adk-mcp__*`). Cursor, Codex, Gemini CLI and other harnesses get the MCP server only, added with `adk mcp` | The FileMaker engine (validate, evaluate, script step roster) and the live file |

Without the plugin there are no bundled Help pages: fetch Claris's live page instead (step 3).
Without the command-line tools there's no engine: say results are from documentation.

On macOS the tools live in `~/Library/Application Support/ADK/`: `bin/adk` and
`fm-cli/fm-cli` (what `filemaker` runs). If `filemaker` isn't on PATH, call
`"$HOME/Library/Application Support/ADK/fm-cli/fm-cli"` with the same arguments.

**Older preview installs** used the name ADT (`adt`, `adt-mcp`, `~/Library/Application
Support/ADT/MCP/fm-cli/fm-cli`, skills `adt-project-setup` and `adt-webviewer-app`). Treat
those as ADK mode too, and suggest updating to the current ADK from Claris.

## 2. The 26.1 gap in ADK's bundled Help

ADK 0.16.0's engine knows every FileMaker 26.1 addition, but its bundled Help pages predate
them. Claris's live Help has caught up on `Get(SortOrder)` only. Until both are current, answer
these from this skill's catalogs, which mark them `doc_status: "announced"` where no Claris page
exists yet:

| 26.1 addition | Where it is |
|---|---|
| `Get(SortOrder)` | `function-catalog.json` (live Claris page exists) |
| `CreateToolDefinitions` (the dialog also accepts `GetToolDefinitions`) | `function-catalog.json` |
| `Set Variable by Name`, `Replace Field Contents by Name` | `script-steps-catalog.json` |
| Go to Related Record by calculation, self-closing Show Custom Dialog, Configure Persistent Data delete by `Char ( 9249 )`, Perform Find by Natural Language options | the steps' `notes` |

For an `announced` entry, confirm the step's options with `filemaker help script steps "<name>"`
and say there's no Claris Help page yet.

## 3. Look up the Claris page by slug

Every entry in `function-catalog.json` and `script-steps-catalog.json` carries Claris's `slug`.
The `filemaker-help` skill stores each page as `<slug>.md` under its `pages/` folder. Use the
**installed** copy: the plugin cache can hold older ADK versions. The active one is the
`installPath` for `filemaker-agentic-development@claris` in
`~/.claude/plugins/installed_plugins.json`:

```bash
H=$(jq -r '.plugins["filemaker-agentic-development@claris"][0].installPath' ~/.claude/plugins/installed_plugins.json)/skills/filemaker-help/pages
find "$H" -name '<slug>.md'
```

No bundled copy (another harness, or a page missing from it): fetch
`https://help.claris.com/markdown/en/pro-help/<slug>.md`.

Read **Format**, **Parameters**, **Data type returned**, **Originated in version**, **Options** and
**Compatibility** from that page. Where it disagrees with a catalog here, the page wins. Say so.

## 4. Validate every calculation you write; evaluate where you can

`filemaker` (the `fm-cli` skill covers it) runs formulas through the real FileMaker engine. Use a
throwaway file in the session's scratch or temp directory, never the user's solution file:

```bash
cat > calc.ndjson <<'EOF'
{"op":"validate:calculation","calculation":"<formula>"}
{"op":"evaluate:calculation","calculation":"<formula>"}
EOF
filemaker --file="<scratch>/calc.fmp12" --create calc.ndjson
```

- **validate**: parses without running. It catches unknown functions (1208), bad `Get()`
  parameters (1215), wrong argument counts and unbalanced parentheses. Do this for every formula,
  including ones with field references. Pass `context` (a table occurrence) to check field
  references against real schema in a real file.
- **evaluate**: returns the value as text plus its `dataType`. Use it for any formula without
  field references, and for any "→ result" you're about to state.

What evaluate can't do. Say so rather than presenting a guess:

- No record context: field references validate but don't evaluate (1224). Aggregates such as
  `Sum`, `Count` and `List` need a field reference, so they only validate.
- `Self` never evaluates (1225); `ValueListItems` and `WindowNames` are refused here.
- `Get()` functions describe the command-line process, not FileMaker Pro. Don't quote them as
  what a user's client returns.
- Design functions answer about the `--file` file only.

When you've evaluated a result, say so ("evaluated on the FileMaker engine"). When you
couldn't, label the result as from documentation.

## 5. Check that a script step exists against the engine

```bash
filemaker --help | head -1                       # engine version: "... engine 26.1.1"
filemaker help script steps                      # the engine's step roster, by category
filemaker help script steps "Set Variable"       # one step's keys and options
```

The engine roster can be **ahead of Claris's documentation and release material**. The 26.1.1
engine also knows `Execute URL` and `Validate Scripts`, which no Claris document mentions. When a
user asks about a step:

- in the engine **and** the docs or this catalog: answer normally (for `announced` entries, add
  that Claris's Help page isn't published yet);
- in the engine, **not** in either: you MUST say it exists in this engine build but is
  undocumented and probably pre-release (not safe to ship in a solution yet); give only what
  `help` shows; don't invent behaviour;
- in **neither**: it doesn't exist; say so.

The engine's internal names differ from the palette for a few steps: `pageSetup` is Print
Setup, and `findRequests`, `forms` and `printOptions` are option pages, not steps.

## 6. Hand-offs: don't duplicate these

| Need | Use |
|---|---|
| Naming tables, fields, scripts, layouts; script headers; a project's standards pack | `filemaker-standards` (`adk standards`) |
| Reading or changing schema, scripts, layouts in a file | `fm-cli` |
| Running a script (`adk script run`), SQL against a live file, the `adk-mcp` tools | `fm-mcp-guide` |
| ADK projects and web viewer apps | `adk-project-setup`, `adk-webviewer-app` |
| ADK can't reach the file, or isn't healthy | `adk doctor`, and relay its fix |

## 7. What stays with this skill

- **Platform support across products**: `script-steps-catalog.json` → `platform_exceptions`.
  One file answers cross-step questions that would otherwise mean reading 216 pages.
- **Version notes**: `originated_in_version`, plus the gap between the latest public release
  (`meta.latest_public_release`) and the engine (`filemaker --help` → `engine …`).
- **FileMaker 26.1 additions** ADK's bundled Help doesn't carry yet (section 2).
- **Data API, OData, WebDirect, FileMaker Go, SQL**: the `filemaker-help` corpus is Pro Help only
  and has none of these.
- **Patterns and gotchas** in the example files: every example that runs without a record is
  engine-tested before release; field-based examples are checked against Claris's pages.
