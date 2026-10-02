# FileMaker WebDirect — Reference

Verified against the live `webdirect-guide` (40 pages) on 2026-07-25 and the per-step
Compatibility tables on **2026-10-02** (FileMaker 26.0.3).

WebDirect runs a hosted custom app in a browser. It resembles FileMaker Pro but is **not**
feature-equivalent — the differences below are the ones that break layouts and scripts.

---

## Script step support — measured

Of the **216** script steps, under `WebDirect`:

| | Count |
|---|---|
| Fully supported (Yes) | 106 |
| **Partial** | 35 |
| **Not supported (No)** | 75 |

Per-step truth is in `script-steps-catalog.json` → `platform_exceptions.WebDirect`. Absent means
supported.

**Semantics that matter:**

- **No** — the step is *skipped* and returns error **3** ("Command is unavailable"). It does not
  halt the script and shows no alert. Check `Get(LastError)`.
- **Partial** — the step runs, but one or more features behave differently. Read the step's
  Notes section on its help page.

A frequent authoring mistake is treating *Partial* as *supported*. Several very common steps are
Partial in WebDirect, including `Go to Layout`, `Go to Portal Row`, `Go to List of Records`,
`Execute SQL`, `Export Records`, `Export Field Contents`, `Copy`, `Cut`, `Clear`,
and `Delete Portal Row`.

**FileMaker 26.0.3** made `Open PDF`, `Append PDF` and `Close PDF` fully supported: with
**From: File**, the user picks a PDF to upload in a browser dialog, and `Close PDF` with
**Save to: File** offers the result as a browser download. Older 26.0.x hosts treat them as
Partial.

---

## Steps that don't run in WebDirect (generated from script-steps-catalog.json)

**Not supported — skipped, error 3:**

- **Control:** Configure Local Notification, Configure NFC Reading, Configure Region Monitor Script
- **Navigation:** Enter Preview Mode, Scroll Window
- **Editing:** Insert from Index, Perform Find/Replace
- **Fields:** Set Use System Formats, Insert from Device
- **Records:** Copy Record/Request, Copy All Records/Requests, Save Records as Excel
- **Windows:** Arrange All Windows, Set Zoom Level, Show/Hide Text Ruler
- **Files:** Close File, Convert File, New File, Open File, Recover File, Save Records as JSONL, Save a Copy as, Set Multi-User, Close Data File, Create Data File, Delete File, Get Data File Position, Get File Exists, Get File Size, Open Data File, Read from Data File, Rename File, Save a Copy as XML, Set Data File Position, Write to Data File
- **Spelling:** Check Found Set, Check Record, Check Selection, Correct Word, Edit User Dictionary, Select Dictionaries, Set Dictionary, Spelling Options
- **Open Menu Item:** Open Manage Database, Open Manage Value Lists, Open Manage Data Sources, Open Settings, Open File Options, Open Help, Open Edit Saved Finds, Open Favorites, Open Find/Replace, Open Hosts, Open Manage Containers, Open Manage Layouts, Open Manage Themes, Open Script Workspace, Open Upload To Host
- **Miscellaneous:** Beep, Speak (macOS), Flush Cache to Disk, Install Menu Set, Send DDE Execute (Windows), Send Event, Flush Web Viewer Cookies, Allow Formatting Bar, Enable Touch Keyboard, Perform AppleScript (macOS), Save a Copy as Add-on Package, AVPlayer Play, AVPlayer Set Options, AVPlayer Set Playback State, Dial Phone, Get Folder Path
- **AI:** Configure Machine Learning Model

**Partial — runs, but some options differ (read the step's Claris page):**

- **Navigation:** Go to Layout, Go to Related Record, Go to Portal Row, Select Window
- **Editing:** Insert File, Insert Picture, Insert Audio/Video, Insert PDF, Replace Field Contents, Export Field Contents, Cut, Copy, Paste, Clear
- **Fields:** Set Selection
- **Records:** Delete Portal Row, Import Records, Export Records, Save Records as Snapshot Link
- **Found Sets:** Go to List of Records
- **Windows:** New Window, Move/Resize Window, Show/Hide Menubar, Adjust Window, View As
- **Accounts:** Re-Login
- **Open Menu Item:** Open Sharing, Open URL
- **Miscellaneous:** Exit Application, Send Mail, Set Web Viewer, Execute SQL
- **PDF Files:** Save Records as PDF, Print PDF
- **Printing:** Print Setup

---

## Feature limitations

**Schema and structure** — web users can choose layouts and views but cannot add, delete or
modify fields, layouts, scripts, relationships, value lists or any other schema.

**Table View is not supported.** Script steps or step options that switch to Table View don't
work. A layout whose default view is Table View displays in another enabled view; if none are
enabled, it displays in List View.

**Object stacking** — WebDirect can't select objects behind other objects, even when the front
object is transparent or the click lands on empty space in a group. Instead of stacking:

- use calculated values for tab labels
- add icons to buttons rather than stacking images in front of them
- group objects and apply button settings to the group

**Text styling is limited.** No highlighting, paragraph styles or tab stops. Only rich text the
browser supports. Rich text applies only to buttons and layout text; for fields, only the object
style is shown. Web users cannot enter rich text, and **editing a field removes existing rich
text formatting**.

**Custom menus are not supported.**

---

## Connections and sessions

- Generally **up to 100 connections per server machine**. Check FileMaker Technical
  Specifications for the exact maximum for a deployment.
- Exceeding the maximum shows an error in the browser when further users try to open the app.
- Each browser window **or tab** consumes its own connection — advise users not to open the same
  app in several tabs.
- A user who doesn't sign out properly holds a connection until the session times out; close the
  file or disconnect the user from Admin Console to reclaim it.

---

## Design guidance

- Design layouts explicitly for mobile browsers where mobile users are expected.
- Hide the menu bar and status toolbar where you want a controlled UI.
- Give users an explicit way to close the file (there's no application quit).
- Review functions, scripts and script triggers against WebDirect support before deploying.
- Set up external data sources deliberately — multi-file solutions need each file hosted and
  reachable.

---

## Related surfaces

- `Get(ApplicationVersion)` identifies the client at runtime — branch on it rather than assuming.
- Function-level restrictions exist too: error **1225** ("Function referred to is not supported
  in this context") is the signal that a calculation function isn't available in WebDirect.
- Functions do **not** carry a Compatibility table in Claris docs, so per-function platform
  support must come from the function's own page notes or from testing.

---

## When to fetch live

Fetch for browser-version support matrices, Admin Console configuration, custom homepage setup,
or HTTP POST sign-in detail. Index:
`https://help.claris.com/markdown/en/webdirect-guide/index.md`
