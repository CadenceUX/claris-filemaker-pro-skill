# ADT mode

Read this file when the Claris Agentic Development Toolkit is present (see SKILL.md → Mode).
In ADT mode this skill is **not** the authority on function or script step facts. Claris's own
page and the FileMaker engine are. This skill adds what they don't carry: platform support
as data, version awareness, the Data API / OData / WebDirect / Go / SQL references, and
engine-tested patterns.

*Written for Claris ADT in its preview program (October 2026). Nothing below depends on a
particular ADT version. For which ADT and FileMaker Pro you have, and whether they're current,
use `fmp-dev-orchestrator`'s stack check or `adt doctor`.*

---

## Contents
1. Look up the Claris page by slug
2. Validate every calculation; evaluate where you can
3. Check a script step exists against the engine
4. Hand-offs
5. What stays with this skill

## 1. Look up the Claris page by slug

Every entry in `function-catalog.json` and `script-steps-catalog.json` carries Claris's `slug`.
The `filemaker-help` skill stores each page as `<slug>.md` somewhere under its `pages/` folder.
Use the **installed** copy — the plugin cache can hold several older ADT versions. The active
one is the `installPath` for `filemaker-agentic-development@claris` in
`~/.claude/plugins/installed_plugins.json`. Then locate the page by filename:

```bash
H=$(jq -r '.plugins["filemaker-agentic-development@claris"][0].installPath' ~/.claude/plugins/installed_plugins.json)/skills/filemaker-help/pages
find "$H" -name '<slug>.md'
```

Read **Format**, **Parameters**, **Data type returned**, **Originated in version**, **Options** and
**Compatibility** from that page. Where it disagrees with a catalog here, the page wins. Say so.

## 2. Validate every calculation you write; evaluate where you can

`filemaker` (the `fm-cli` skill covers it) runs formulas through the real FileMaker engine. Use a
throwaway file in the session's scratch or temp directory, never the user's solution file:

```bash
cat > calc.ndjson <<'EOF'
{"op":"validate:calculation","calculation":"<formula>"}
{"op":"evaluate:calculation","calculation":"<formula>"}
EOF
filemaker --file="<scratch>/calc.fmp12" --create calc.ndjson
```

Outside Claude Code, `filemaker` may not be on PATH. Run
`"$HOME/Library/Application Support/ADT/MCP/fm-cli/fm-cli"` with the same arguments.

- **validate**: parses without running. It catches unknown functions (1208), bad `Get()`
  parameters (1215), wrong argument counts and unbalanced parentheses. Do this for every formula,
  including ones with field references. Pass `context` (a table occurrence) to check field
  references against real schema in a real file.
- **evaluate**: returns the value as text plus its `dataType`. Use it for any formula without
  field references, and for any "→ result" you're about to state.

What evaluate can't do. Say so rather than presenting a guess:

- No record context: field references validate but don't evaluate (1224).
- `Self` never evaluates (1225); `ValueListItems` and `WindowNames` are refused here.
- `Get()` functions describe the CLI process, not FileMaker Pro (`Get(ApplicationVersion)` →
  `1.0`). Don't quote them as what a user's client returns.
- Design functions answer about the `--file` file only.

When you've evaluated a result, say so ("evaluated on the FileMaker engine"). When you
couldn't, label the result as from documentation.

## 3. Check that a script step exists against the engine

```bash
filemaker help script steps                      # the engine's step palette, by category
filemaker help script steps "Set Variable"       # one step's keys and options
```

The engine roster can be **ahead of Claris's documentation**: it may list steps no Claris page
documents yet. List the engine's palette with `filemaker help script steps` and compare it with
the names in `script-steps-catalog.json`
(`jq -r '.categories[].steps[].name' references/script-steps-catalog.json`). When a user asks
about a step:

- in the engine **and** the docs: answer normally;
- in the engine, **not** in the docs: you MUST say it exists in this engine build but is
  undocumented and probably pre-release (not safe to ship in a solution yet); give only what
  `help` shows; don't invent behaviour;
- in **neither**: it doesn't exist; say so.

## 4. Hand-offs: don't duplicate these

| Need | Use |
|---|---|
| Naming tables, fields, scripts, layouts; script headers | `filemaker-standards` |
| Reading or changing schema, scripts, layouts in a file | `fm-cli` |
| Running a script (`adt script run`), SQL against a live file, the `adt-mcp` tools (e.g. `adt-mcp:execute_filemaker_sql`, `adt-mcp:troubleshoot_setup`) | `fm-mcp-guide` |
| ADT projects and web viewer apps | `adt-project-setup`, `adt-webviewer-app` |

## 5. What stays with this skill

- **Platform support across products**: `script-steps-catalog.json` → `platform_exceptions`.
  One file answers cross-step questions that would otherwise mean reading 216 pages.
- **Version notes**: `originated_in_version`, plus the gap between the latest public release
  (`meta.latest_public_release`) and the engine (first line of `filemaker --help` → `engine …`).
- **Data API, OData, WebDirect, FileMaker Go, SQL**: the `filemaker-help` corpus is Pro Help only
  and has none of these.
- **Patterns and gotchas** in the example files: every example that runs without a record is
  engine-tested before release; field-based examples are checked against Claris's pages.
