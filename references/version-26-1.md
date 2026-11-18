# FileMaker 26.1: what changed for developers

FileMaker 26.1 is the current public release (FileMaker Pro 26.1.1, build 26.1.1.54, checked
2026-11-18). This page covers the developer-facing changes. New functions and script steps are
in the two catalogs; this page adds the features that aren't a function or a step, and where
each one works. Claris's Help doesn't document most of these yet: where an answer depends on
exact option names or JSON keys, say so and fetch the live page if one has appeared.

## Contents
- New functions and script steps
- Changed script steps
- Value lists, buttons and fields
- Self-documenting solutions
- Where the changes work (WebDirect and FileMaker Go)
- FileMaker Server
- What 26.1 means for agentic development

## New functions and script steps

| Item | Kind | Catalog |
|---|---|---|
| `Get(SortOrder)` | function | `function-catalog.json` (Claris page published) |
| `CreateToolDefinitions` | AI function | `function-catalog.json` (announced; no Claris page yet) |
| `Set Variable by Name` | script step | `script-steps-catalog.json` (announced) |
| `Replace Field Contents by Name` | script step | `script-steps-catalog.json` (announced) |

The by-name steps and Go to Related Record by calculation are the release's main theme: a
script decides at runtime which variable to set, which field to change and which related table
to go to, instead of branching or duplicating steps.

## Changed script steps

- **Go to Related Record:** "Table by Calculation" picks the source table occurrence from a
  calculation.
- **Show Custom Dialog:** a dialog can have no buttons and close itself after a set number of
  seconds; `Get ( LastMessageChoice )` then returns 0. Useful for brief status messages,
  including on FileMaker Go.
- **Configure Persistent Data:** a Value calculation that returns only `Char ( 9249 )` deletes
  the entry, so one step can set or delete.
- **Perform Find by Natural Language:** documented Get modes (Found Set, Found Set as JSON, Find
  Request as JSON), a prompt template, and a Parameters JSON that accepts `CURLOPT_TIMEOUT` and
  `context_prompt`.

## Value lists, buttons and fields

- **Calculated value lists:** a value list can come from a calculation returning
  return-delimited values, or JSON describing several columns for display and data entry.
  Claris changed the JSON key names during testing, so confirm them against the live Help page
  before writing them into a solution.
- **Calculated button icons:** a button can take its SVG icon from a calculation.
- **Single checkbox without a value:** a checkbox set tied to a value list can show one
  unlabelled checkbox, for clean yes/no fields. One-value and two-value lists behave
  differently.
- **Clipped-content indicator:** an edit box can show an ellipsis when its content doesn't fit.
- **Portal new-record row at the top:** Portal Setup can place the blank row for a new record
  above the existing rows, keeping the sort.
- **Export field names:** "Use field names as column names in first row" moved to Specify Field
  Order for Export and now covers CSV and Excel.
- **AVIF images** can be inserted into container fields.

## Self-documenting solutions

- **Custom function descriptions:** a custom function and each of its parameters can carry a
  description, shown in the Specify Calculation dialog. Write them: `CreateToolDefinitions`
  turns them into the tool descriptions an AI model sees.
- **Field display names and annotations** (phase 2): fields carry a readable display name and an
  annotation beside the real field name, and Sort, Export and Table View show the real name
  again where display names used to hide it. Remember the existing gotcha: once any field in a
  table is annotated, only annotated fields appear in that table's generated DDL.
- **Copy and paste** reports what actually came across.

## Where the changes work (WebDirect and FileMaker Go)

- `Set Variable by Name`, `Replace Field Contents by Name` and Go to Related Record by
  calculation work in WebDirect in the same release as the desktop.
- The single unlabelled checkbox works in WebDirect.
- The clipped-content indicator works on the desktop, WebDirect and FileMaker Go.
- Self-closing custom dialogs work on FileMaker Go.
- Claris certified WebDirect against WCAG 2.2 Level AA, for WebDirect in FileMaker Server
  26.0.2 and later. Use that exact wording; it isn't "fully compliant".

Full per-product support for the new steps is unconfirmed until Claris publishes their Help
pages; the catalog marks them `platform_verified: false`.

## FileMaker Server

- Standby Server can switch over automatically when the primary's Database Server quits or the
  primary becomes unreachable, and keeps its own host name.
- SSL certificates can be imported without a restart, except for the first move from the
  self-signed certificate to a custom one.
- SMTP settings can be exported and imported; backups can be scheduled monthly; remote backup
  settings are in the Admin API; restored files can be renamed in Admin Console; backups can
  leave out externally stored container data.
- Add-on packages can be created by a server-side script (they still install from FileMaker Pro).

For Server administration beyond this, use Claris's Server documentation; it's outside this
skill.

## What 26.1 means for agentic development

ADK works with FileMaker Pro 26.1 or later, and files hosted on FileMaker Server need 26.1.1 or
later. Self-documenting schema (display names, annotations, custom function descriptions) is
also the context an agent reads, so it pays twice. How this skill works alongside ADK is in
SKILL.md, under Mode.
