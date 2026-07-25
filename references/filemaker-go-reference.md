# FileMaker Go — Reference

Verified against the live `go-help` (29 pages) and `go-development-guide` (9 pages), plus the
per-step Compatibility tables, on **2026-07-25**, FileMaker 26.

FileMaker Go runs hosted or local custom apps on iOS and iPadOS. It is a **runtime, not an
authoring tool**.

---

## Script step support — measured

Of the **216** script steps, under `Go`:

| | Count |
|---|---|
| Fully supported (Yes) | 154 |
| **Partial** | 20 |
| **Not supported (No)** | 42 |

Per-step truth is in `script-steps-catalog.json` → `platform_exceptions.Go`.

**Critical behaviour:** FileMaker Go shows **no alert** for an unsupported step. The step is
silently skipped and returns error **3** ("Command is unavailable"). Running unsupported steps
can lead to unintended behaviour, so branch defensively:

```
If [ PatternCount ( Get ( ApplicationVersion ) ; "Go" ) ]
    # Go-safe path
Else
    # desktop path
End If
```

Common **Partial** steps on Go include `Print`, `Print Setup`, `Print PDF`, `Save Records as
PDF`, `Export Records`, `Export Field Contents`, `Import Records`, `Insert File`, `New Window`,
`Move/Resize Window`, `Adjust Window`, `Replace Field Contents`, and
`Save Records as Snapshot Link`.

Conversely, a small set of steps are **Go-only** and unsupported in FileMaker Pro — the
`AVPlayer` family (`AVPlayer Play`, `AVPlayer Set Options`, `AVPlayer Set Playback State`),
`Configure NFC Reading`, `Configure Region Monitor Script`, `Enable Touch Keyboard`, and
`Insert from Device`.

---

## Not supported at all

FileMaker Pro features absent from Go:

- creating or modifying schema — tables, fields, relationships, data sources, privileges
- creating or modifying structure — layouts, scripts, value lists, custom menus
- importing records from Microsoft Excel or XML
- exporting records to FMP12 or XML
- text baselines
- plug-ins
- hosting files

---

## Behaviour differences

**Modes** — Layout and Preview modes don't exist. To preview, save records as PDF and view the
PDF inside Go.

**Layout design** — in Go you can't remove views or layouts, add or remove fields, switch to
layouts not in the Layouts menu (unless you provide a navigation button), define or assign value
lists (except drop-downs and pop-up menus that allow editing), display tooltips, display leader
characters such as "..." in tab control names, or display shadows on layout objects.

**Date and time** — users can't select seconds or fractions of seconds in the picker; they must
switch to the keyboard. Scripted or calculated times **do** display seconds.

**Custom menus** — can't remove the Close File item, can't add items that don't map to existing
Go menu items, and can't override Quick Find via custom menus (use the Edit Custom Menu dialog
instead). Removed items appear but are unavailable. iOS/iPadOS system shortcuts and Go's own
shortcuts override custom-menu shortcuts.

**Printing** — print options set in FileMaker Pro have no effect on Go, and vice versa. For
layouts where exact spacing matters (labels, preprinted forms) set page margins explicitly.

---

## Device capabilities

Available through Go, mostly via functions covered in
`specialty-functions-examples.md` (Mobile/Go section):

| Capability | Surface |
|---|---|
| GPS / location | `Location()`, `LocationValues()` |
| Device sensors | `GetSensor()` |
| iBeacons | `RangeBeacons()` |
| Barcode scanning | Insert from Device; Go's scan-barcode feature |
| Camera, photo, video, audio, signature | `Insert from Device` (FM 26 adds Flash control On/Off/Auto for the back camera) |
| Media playback | `AVPlayer` steps, `GetAVPlayerAttribute()` |
| NFC | `Configure NFC Reading` |
| Region monitoring | `Configure Region Monitor Script` |
| Guided Access detection | `Get(GuidedAccessState)` — FM 26, returns 1 when iOS Guided Access is active |
| Siri Shortcuts | Go development guide |
| Keychain / permitted hosts | Go help |

---

## Files, security and transfer

- Files can be opened from a host or stored locally on the device.
- HTTPS tunnelling to hosts can be enabled.
- Keychain management stores host credentials; permitted hosts can be managed explicitly.
- File transfer in and out of the device is covered in the Go development guide.
- `Get(GuidedAccessState)` is the FM 26 way to detect kiosk/locked-screen mode and adapt UI.

---

## When to fetch live

Fetch for iOS version requirements, Siri Shortcuts detail, keychain and permitted-host
procedures, or file-transfer specifics. Indexes:
`https://help.claris.com/markdown/en/go-help/index.md` and
`https://help.claris.com/markdown/en/go-development-guide/index.md`
