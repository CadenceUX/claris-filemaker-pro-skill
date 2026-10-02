# FileMaker Get() Functions — Quick Reference

## Contents
  - Date & Time
  - Account & Privileges
  - File & Database
  - Paths & File System
  - Record & Found Set
  - Layout & Window
  - Script & Trigger
  - Field & Object State
  - Sorting & Printing
  - Network & Connectivity
  - Device & Screen (FileMaker Go / iOS)
  - Calculation & Custom Function Context
  - Common Get() patterns

Source: https://help.claris.com/en/pro-help/content/get-functions.html  
All 138 Get() functions grouped by category (FM 26 added Get(AccountPasswordDaysRemaining), Get(GuidedAccessState) and Get(WindowUUID)).

**Overview:** Get() functions report the current user, file, record, window, device, time and system state. Most enumerations are **numbers whose meaning isn't obvious** — check the table rather than guessing; several look similar but differ (`Get(Device)` 3 = iPad, `Get(SystemPlatform)` 3 = iOS).

> Only the parameters listed here exist. A made-up one such as `Get ( RecordCount )` is a calculation error (1215), not an empty result.

---

## Date & Time

| Function | Returns | Notes |
|---|---|---|
| `Get(CurrentDate)` | date | Today's date per system clock |
| `Get(CurrentTime)` | time | Current time per system clock |
| `Get(CurrentTimestamp)` | timestamp | Current date+time |
| `Get(CurrentTimeUTCMilliseconds)` | number | Milliseconds since **1/1/0001** UTC (not the Unix epoch). Unix ms = this − 62135596800000 |
| `Get(CurrentTimeUTCMicroseconds)` | number | Microseconds since **1/1/0001** UTC (not the Unix epoch) |
| `Get(CurrentHostTimestamp)` | timestamp | Server-side timestamp (consistent across all clients) |

```
Get ( CurrentDate )               // → 6/4/2026
Get ( CurrentTimestamp )          // → 6/4/2026 9:15:00 AM
Get ( CurrentTimeUTCMilliseconds ) // → 63926499600000  (2 Oct 2026 01:00 UTC — counted from 1/1/0001)
Get ( CurrentHostTimestamp )      // use on server or PSOS for consistent timestamps
```

Days overdue:
```
If ( Due::DueDate < Get ( CurrentDate ) ;
  Get ( CurrentDate ) - Due::DueDate ;
  0
)
```

ISO 8601 date string for APIs:
```
Year ( Get ( CurrentDate ) ) & "-" &
Right ( "0" & Month ( Get ( CurrentDate ) ) ; 2 ) & "-" &
Right ( "0" & Day ( Get ( CurrentDate ) ) ; 2 )
// → "2026-06-04"
```

---

## Account & Privileges

| Function | Returns | Notes |
|---|---|---|
| `Get(AccountName)` | text | Current user's account name |
| `Get(AccountType)` | text | `FileMaker File`, `Guest`, `External`, `Apple ID`, `Amazon`, `Google`, `Azure`, `Custom OAuth`, or `Claris ID <Team Name>` |
| `Get(AccountGroupName)` | text | External server group name (LDAP/Active Directory) |
| `Get(AccountPrivilegeSetName)` | text | Name of the current privilege set |
| `Get(AccountExtendedPrivileges)` | text | Return-delimited list of extended privilege keywords |
| `Get(AccountPasswordDaysRemaining)` | number | **FM 26+** — days until the password must change; `0` if expired; `-1` if no expiry, no password, or not a FileMaker File account |
| `Get(CurrentPrivilegeSetName)` | text | Privilege set **evaluating this calculation** — `[Full Access]` inside a script set to run with full access, even when the account's set differs |
| `Get(CurrentExtendedPrivileges)` | text | Extended privileges of the privilege set currently in effect (differs from the account's under full-access scripts) |
| `Get(UserName)` | text | User name set in FileMaker Pro / Go Settings (not the OS login, not the account); `[WebDirect-xxxxx]` in WebDirect |
| `Get(UserCount)` | number | Number of users connected to the hosted file |

```
Get ( AccountName )               // → "bjones"
Get ( AccountPrivilegeSetName )   // → "[Full Access]"
Get ( AccountExtendedPrivileges ) // → "fmapp¶fmwebdirect"   (also fmrest, fmodata, fmxml, fmphp, fmurlscript, fmextscriptaccess, fmreauthenticate10)
Get ( UserCount )                 // → 14  (users on server)
```

Check for full access:
```
Get ( AccountPrivilegeSetName ) = "[Full Access]"
```

Check extended privilege:
```
PatternCount ( Get ( AccountExtendedPrivileges ) ; "fmwebdirect" ) > 0
```

---

## File & Database

| Function | Returns | Notes |
|---|---|---|
| `Get(FileName)` | text | File name without extension |
| `Get(FilePath)` | text | Full path to the file on disk |
| `Get(FileSize)` | number | File size in bytes |
| `Get(EncryptionState)` | text | `0` not encrypted; `1¶<shared ID>` if encrypted at rest |
| `Get(FileLocaleElements)` | text | JSON of file locale settings |
| `Get(HostName)` | text | Server hostname or "localhost" |
| `Get(HostIPAddress)` | text | IP address of the host |
| `Get(HostApplicationVersion)` | text | FileMaker Server version string |
| `Get(ApplicationVersion)` | text | FileMaker Pro/Go/WebDirect version |
| `Get(ApplicationLanguage)` | text | UI language of the application |
| `Get(ApplicationArchitecture)` | text | `x86_64` (Intel Mac, Windows, Server, Cloud, WebDirect…) or `arm64` (Apple silicon, Go, ARM Linux Server) |
| `Get(FileMakerPath)` | text | Path to the **folder** of the running FileMaker app (Pro and Server only) |
| `Get(CacheFileName)` | text | Name of the local cache file (hosted files) |
| `Get(CacheFilePath)` | text | Path to the local cache file |
| `Get(OpenDataFileInfo)` | text | Info about any open data files |
| `Get(SessionIdentifier)` | text | Value set by **Set Session Identifier** in this session on a hosted file; otherwise empty |
| `Get(SystemVersion)` | text | OS version string |
| `Get(SystemDrive)` | text | Boot drive path |
| `Get(SystemIPAddress)` | text | Client's IP address (newline-delimited if multiple) |
| `Get(SystemNICAddress)` | text | Network interface card MAC address |
| `Get(SystemLanguage)` | text | OS language setting |
| `Get(SystemPlatform)` | number | `1` macOS · `-2` Windows · `3` iOS/iPadOS · `4` WebDirect · `5` CentOS Linux · `8` Ubuntu Linux |
| `Get(SystemAppearance)` | text | macOS/iOS: the system appearance name (e.g. `Dark`); Windows: the active high-contrast scheme name, else empty |
| `Get(SystemLocaleElements)` | text | JSON of OS locale settings |
| `Get(SystemStorageAvailable)` | number | Available storage in bytes |
| `Get(MultiUserState)` | number | `0` sharing off · `1` sharing on, accessed on the host · `2` sharing on, accessed from a client |
| `Get(InstalledFMPlugins)` | text | Return-delimited list of installed plug-ins |
| `Get(InstalledFMPluginsAsJSON)` | text | JSON array of installed plug-in details |

```
Get ( FileName )             // → "CRM"
Get ( FilePath )             // → "file:/Macintosh HD/Users/bjones/CRM.fmp12"  (fmnet:/host/CRM.fmp12 when hosted)
Get ( SystemPlatform )       // → 1 (macOS)
Get ( ApplicationVersion )   // → "Pro 26.0.1"  (also Go, Go_iPad, Server, Web Publishing Engine, FileMaker Data API Engine…)
Get ( ApplicationArchitecture ) // → "arm64"
Get ( SystemAppearance )     // → "Dark"
Get ( EncryptionState )      // → 0, or 1¶<shared ID> when encrypted at rest
```

Platform-conditional logic:
```
Case (
  Get ( SystemPlatform ) = 1 ; "mac" ;
  Get ( SystemPlatform ) = -2 ; "win" ;
  Get ( SystemPlatform ) = 3 ; "ios" ;
  Get ( SystemPlatform ) = 4 ; "webdirect" ;
  "other"
)
```

Dark mode adaptive UI:
```
If ( Get ( SystemAppearance ) = "Dark" ; darkColour ; lightColour )
```

---

## Paths & File System

| Function | Returns | Notes |
|---|---|---|
| `Get(DesktopPath)` | text | Path to the Desktop folder |
| `Get(DocumentsPath)` | text | Path to the Documents folder |
| `Get(DocumentsPathListing)` | text | Return-delimited file listing of Documents folder |
| `Get(PreferencesPath)` | text | Path to the application preferences folder |
| `Get(TemporaryPath)` | text | Path to the system temporary folder |

```
Get ( DesktopPath )          // → "/Users/bjones/Desktop/"
Get ( DocumentsPath )        // → "/Users/bjones/Documents/"
Get ( TemporaryPath )        // → "/var/folders/…/T/"
Get ( DocumentsPathListing ) // → list of files in Documents
```

Build a path for Export to Folder:
```
Get ( TemporaryPath ) & "export_" &
  Substitute ( Get ( CurrentTimestamp ) ; [" ";"_"] ; [":";""] ) & ".csv"
```

---

## Record & Found Set

| Function | Returns | Notes |
|---|---|---|
| `Get(RecordID)` | number | Internal unique record ID (never reused) |
| `Get(RecordNumber)` | number | Position in current found set (1-based) |
| `Get(ActiveRecordNumber)` | number | Record number shown in the status toolbar (position in the found set) — not a portal row |
| `Get(TotalRecordCount)` | number | All records in the table |
| `Get(FoundCount)` | number | Records in current found set |
| `Get(RecordOpenCount)` | number | Number of records currently open/locked |
| `Get(RecordOpenState)` | number | `0` closed (committed) · `1` **new** uncommitted · `2` **modified** uncommitted · `3` deleted uncommitted |
| `Get(RecordModificationCount)` | number | Cumulative modification count for current record |
| `Get(RecordAccess)` | number | `0` no view/edit · `1` view only · `2` edit (privilege-set record access for the current record) |
| `Get(ModifiedFields)` | text | Return-delimited list of modified field names (unsaved) |

```
Get ( RecordID )              // → 1042
Get ( RecordNumber )          // → 3  (3rd record in found set)
Get ( FoundCount )            // → 47
Get ( RecordOpenState )       // → 2 for an existing record with uncommitted changes (1 = new record)
Get ( RecordModificationCount ) // → 23  (modified 23 times total)
Get ( ModifiedFields )        // → "FirstName¶Email"  (fields changed but not committed)
```

Warn before leaving unsaved record:
```
If ( Get ( RecordOpenState ) > 0 ;
  Show Custom Dialog [ "Unsaved changes" ; "Commit before continuing?" ]
)
```

Progress indicator:
```
"Record " & Get ( RecordNumber ) & " of " & Get ( FoundCount )
```

---

## Layout & Window

| Function | Returns | Notes |
|---|---|---|
| `Get(LayoutName)` | text | Current layout name |
| `Get(LayoutNumber)` | number | Layout's position in layout list |
| `Get(LayoutCount)` | number | Total number of layouts |
| `Get(LayoutTableName)` | text | Table occurrence the layout is based on |
| `Get(LayoutViewState)` | number | 0=form, 1=list, 2=table |
| `Get(LayoutAccess)` | number | `0` no access · `1` view only (also for read-only files) · `2` modifiable — via this layout |
| `Get(WindowName)` | text | Current window title |
| `Get(WindowHeight)` | number | Window height in points |
| `Get(WindowWidth)` | number | Window width in points |
| `Get(WindowTop)` | number | Window top position in points |
| `Get(WindowLeft)` | number | Window left position in points |
| `Get(WindowContentHeight)` | number | Usable content area height |
| `Get(WindowContentWidth)` | number | Usable content area width |
| `Get(WindowDesktopHeight)` | number | Total desktop/screen height |
| `Get(WindowDesktopWidth)` | number | Total desktop/screen width |
| `Get(WindowMode)` | number | `0` Browse · `1` Find · `2` Preview · `3` printing · `4` Layout mode (Data Viewer only; scripts switch to Browse) |
| `Get(WindowStyle)` | number | `0` document · `1` floating document · `2` dialog · `3` card |
| `Get(WindowZoomLevel)` | text | Zoom percentage of the current window; WebDirect returns 100 |
| `Get(WindowVisible)` | number | 1=visible, 0=hidden |
| `Get(WindowOrientation)` | number | Pro & Go: `-2` landscape left · `-1` landscape right · `0` square · `1` portrait · `2` portrait upside down |
| `Get(WindowUUID)` | text | **FM 26+** — Unique stable UUID for the active window; useful for managing multiple windows of the same file |
| `Get(ActiveLayoutObjectName)` | text | Name of the currently focused layout object |
| `Get(StatusAreaState)` | number | `0` hidden · `1` visible · `2` visible & locked · `3` hidden & locked |
| `Get(MenubarState)` | number | `0` hidden & unlocked · `1` visible & unlocked · `2` visible & locked · `3` hidden & locked |
| `Get(CustomMenuSetName)` | text | Name of the active custom menu set |
| `Get(AllowFormattingBarState)` | number | 1 if formatting bar is allowed |
| `Get(TextRulerVisible)` | number | 1 if text ruler is visible |
| `Get(TouchKeyboardState)` | number | FileMaker Go and Windows: `1` touch keyboard enabled · `0` disabled |

```
Get ( LayoutName )         // → "Invoices - Detail"
Get ( LayoutTableName )    // → "Invoices"
Get ( WindowMode )         // → 0 (Browse)
Get ( WindowContentWidth ) // → 1024
Get ( WindowOrientation )  // → 1 (portrait); -1 / -2 landscape
Get ( StatusAreaState )    // → 1 (status toolbar visible)
Get ( CustomMenuSetName )  // → "Customer Portal Menus"
```

Responsive layout sizing:
```
If ( Get ( WindowContentWidth ) < 768 ; "mobile" ; "desktop" )
```

Detect Find mode in a calc:
```
If ( Get ( WindowMode ) = 1 ; "" ; actualCalculation )
```

---

## Script & Trigger

| Function | Returns | Notes |
|---|---|---|
| `Get(ScriptName)` | text | Currently running script name |
| `Get(ScriptParameter)` | text | Parameter passed to current script |
| `Get(ScriptResult)` | text | Result returned by a called sub-script |
| `Get(LastError)` | number | Error code from last script step (0=none) |
| `Get(LastErrorDetail)` | text | Detail message for the last error |
| `Get(LastErrorLocation)` | text | Script name and step where last error occurred |
| `Get(LastMessageChoice)` | number | Button pressed in last dialog (1=first, 2=second, 3=third) |
| `Get(LastStepTokensUsed)` | text | JSON for the last AI script step: `model`, `summary` (records embedded/skipped), `usage` (`prompt_tokens`, `total_tokens`) |
| `Get(ErrorCaptureState)` | number | 1 if Set Error Capture is On |
| `Get(AllowAbortState)` | number | 1 if Allow User Abort is On |
| `Get(ScriptAnimationState)` | number | 1 if script animations are enabled |
| `Get(RequestCount)` | number | Number of find requests defined |
| `Get(RequestOmitState)` | number | 1 if current find request is set to Omit |
| `Get(TransactionOpenState)` | number | 1 if inside an open transaction block |
| `Get(RevertTransactionOnErrorState)` | number | 1 if Revert Transaction on Error is active |
| `Get(TriggerCurrentPanel)` | text | `index¶objectName` of the panel being left (OnPanelSwitch only); `0` if invalid |
| `Get(TriggerTargetPanel)` | text | `index¶objectName` of the panel being switched to (OnPanelSwitch only); `0` if invalid |
| `Get(TriggerGestureInfo)` | text | List (OnGestureTap, Go and Windows): `Tap`, tap count, finger count, x, y, object name |
| `Get(TriggerKeystroke)` | text | Key pressed in an OnObjectKeystroke trigger |
| `Get(TriggerModifierKeys)` | number | Modifier keys held during trigger (bitmask) |
| `Get(TriggerExternalEvent)` | number | FileMaker Go remote-control event: `0` unknown · `1` play · `2` pause · `3` toggle · `4` next · `5` previous · `6` seek · `7` stop |

```
Get ( ScriptParameter )   // → JSON or text passed from calling context
Get ( LastError )         // → 401 (no records match)
Get ( LastErrorDetail )   // → human-readable error description
Get ( LastErrorLocation ) // → script name, step name and line number of the last error
Get ( LastMessageChoice ) // → 2 (user clicked second button)
Get ( ScriptResult )      // → result from last Perform Script
Get ( LastStepTokensUsed ) // → {"model":"…","usage":{"prompt_tokens":…,"total_tokens":342}}
```

Parse JSON script parameter:
```
Set Variable [ $action ; Value: JSONGetElement ( Get ( ScriptParameter ) ; "action" ) ]
Set Variable [ $id     ; Value: JSONGetElement ( Get ( ScriptParameter ) ; "id" ) ]
```

Error handling with detail:
```
If [ Get ( LastError ) ≠ 0 ]
  Set Variable [ $err ; Value:
    "Error " & Get ( LastError ) & ": " & Get ( LastErrorDetail ) &
    " (at " & Get ( LastErrorLocation ) & ")"
  ]
End If
```

---

## Field & Object State

| Function | Returns | Notes |
|---|---|---|
| `Get(ActiveFieldName)` | text | Name of the field currently in focus |
| `Get(ActiveFieldTableName)` | text | Table name of the focused field |
| `Get(ActiveFieldContents)` | text | Contents of the field currently in focus |
| `Get(ActiveRepetitionNumber)` | number | Repetition number of the active field |
| `Get(ActiveSelectionSize)` | number | Length of the current text selection |
| `Get(ActiveSelectionStart)` | number | Start position of the current text selection |
| `Get(ActiveModifierKeys)` | number | Modifier keys currently held (bitmask) |
| `Get(ActivePortalRowNumber)` | number | Currently active portal row (0 if none) |
| `Get(QuickFindText)` | text | Text currently in the Quick Find search box |

```
Get ( ActiveFieldName )         // → "EmailAddress"
Get ( ActiveFieldContents )     // → "alice@example.com"
Get ( ActiveSelectionStart )    // → 6  (cursor at position 6)
Get ( ActivePortalRowNumber )   // → 3  (third portal row is active)
Get ( QuickFindText )           // → "smith"
```

---

## Sorting & Printing

| Function | Returns | Notes |
|---|---|---|
| `Get(SortState)` | number | 0=unsorted, 1=sorted, 2=semi-sorted |
| `Get(PageNumber)` | number | Current page number (Preview mode only) |
| `Get(PageCount)` | number | Total page count (Preview mode only) |
| `Get(PrinterName)` | text | Name of the current printer |
| `Get(UseSystemFormatsState)` | number | 1 if file is using system date/time formats |

```
Get ( SortState )  // → 1 (sorted)
Get ( PageNumber ) // → 3 (on page 3 of Preview)
Get ( PageCount )  // → 12 (total pages in Preview)
```

---

## Network & Connectivity

| Function | Returns | Notes |
|---|---|---|
| `Get(NetworkProtocol)` | text | Network protocol in use (e.g. "TCP/IP") |
| `Get(NetworkType)` | number | FileMaker Go: `0` local file · `1` unknown · `2` cellular · `3` Wi-Fi |
| `Get(ConnectionState)` | number | `0` no network connection · `1` unencrypted · `2` encrypted, certificate **not** verified · `3` encrypted & verified |
| `Get(ConnectionAttributes)` | text | Encrypted connection details JSON |
| `Get(PersistentID)` | text | 32-hex-digit ID of the **device / computer** (or WebDirect session) — not the file. On FileMaker Server 26+, stable across restarts and upgrades |
| `Get(UUID)` | text | New 16-byte UUID each evaluation (unstored) |
| `Get(UUIDNumber)` | number | New 24-byte (192-bit) unique number each evaluation; may index faster than Get(UUID) as a key |

```
Get ( UUID )             // → "A1B2C3D4-E5F6-7890-ABCD-EF1234567890"
Get ( ConnectionState )  // → 3 (encrypted, verified certificate)
```

Generate a unique key:
```
// In a field auto-enter calc:
Get ( UUID )
```

---

## Device & Screen (FileMaker Go / iOS)

| Function | Returns | Notes |
|---|---|---|
| `Get(Device)` | number | `0` unknown · `1` Mac · `2` Windows · `3` **iPad** · `4` **iPhone** · `5` Android · `6` Linux |
| `Get(ScreenDepth)` | number | Colour depth in bits |
| `Get(ScreenHeight)` | number | Screen height in points |
| `Get(ScreenWidth)` | number | Screen width in points |
| `Get(ScreenScaleFactor)` | number | Display scale factor (2.0 for Retina, 3.0 for Super Retina) |
| `Get(HighContrastState)` | number | 1 if OS high contrast / accessibility mode is active |
| `Get(GuidedAccessState)` | number | **FM 26+, FileMaker Go only** — 1 if iOS Guided Access is currently active; use to detect kiosk/locked-screen mode |
| `Get(RegionMonitorEvents)` | text | JSON of pending region monitor events (Go only) |

```
Get ( Device )             // → 3 (iPad)
Get ( ScreenWidth )        // → 1024
Get ( ScreenScaleFactor )  // → 2  (Retina display)
Get ( HighContrastState )  // → 0 (normal mode)
```

Detect iPad vs iPhone:
```
Case (
  Get ( Device ) = 3 ; "iPad layout" ;
  Get ( Device ) = 4 ; "iPhone layout" ;
  "Desktop layout"
)
```

---

## Calculation & Custom Function Context

| Function | Returns | Notes |
|---|---|---|
| `Get(CalculationRepetitionNumber)` | number | Repetition being evaluated in a repeating calc |

```
Get ( CalculationRepetitionNumber )
// Use inside a repeating calculation to vary output per repetition
```

---

## Common Get() patterns

**Audit trail stamp:**
```
Get ( AccountName ) & " @ " & Get ( CurrentTimestamp ) & " on " & Get ( HostName )
```

**Unique record ID for sync:**
```
// Auto-enter, do not replace:
Get ( UUID )
```

**Responsive window size detection:**
```
Let ( w = Get ( WindowContentWidth ) ;
  Case (
    w < 480  ; "small" ;
    w < 1024 ; "medium" ;
    "large"
  )
)
```

**Pass context to a sub-script via JSON:**
```
Perform Script [ "ProcessRecord" ; Parameter:
  JSONSetElement ( "{}" ;
    ["recordID"  ; Get ( RecordID )   ; JSONNumber] ;
    ["layout"    ; Get ( LayoutName ) ; JSONString] ;
    ["user"      ; Get ( AccountName ); JSONString]
  )
]
```

**Check if script is running on server (PSOS):**
```
PatternCount ( Get ( ApplicationVersion ) ; "Server" ) > 0
```

**Error-safe script pattern with detail logging:**
```
Set Error Capture [ On ]
// ... perform operation ...
If [ Get ( LastError ) ≠ 0 ]
  Set Variable [ $log ; Value:
    Get ( LastError ) & " | " & Get ( LastErrorDetail ) &
    " | " & Get ( LastErrorLocation )
  ]
  // Log or show dialog
End If
```

**AI tokens budget check:**
```
// After an AI script step:
If [ JSONGetElement ( Get ( LastStepTokensUsed ) ; "usage.total_tokens" ) > 5000 ]
  // Log or warn — high token usage
End If
```
