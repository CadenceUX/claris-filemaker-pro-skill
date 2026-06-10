# FileMaker Get() Functions — Quick Reference

Source: https://help.claris.com/en/pro-help/content/get-functions.html  
All 138 Get() functions grouped by category with return type, typical use, and examples (135 through FM 22 + 3 new in FM 26: Get(AccountPasswordDaysRemaining), Get(GuidedAccessState), Get(WindowUUID)).  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** Get() functions return environmental and contextual information — the current user, file, record, window, device, date/time, and system state. They take no arguments and are recalculated dynamically. All return text or number unless noted.

> **Removed/renamed functions:** `Get(ExtendedPrivileges)` → use `Get(AccountExtendedPrivileges)`;  `Get(PrivilegeSetName)` → use `Get(AccountPrivilegeSetName)`; `Get(RecordCount)` → use `Get(TotalRecordCount)` or `Get(FoundCount)`; `Get(LastExternalErrorDetail)` → use `Get(LastErrorDetail)`; `Get(LastODBCError)` → use `Get(LastErrorDetail)`. `Get(LocationValues)` and `Get(LocationAccuracy)` are FileMaker Go–only and may not be available on all platforms.

---

## Date & Time

| Function | Returns | Notes |
|---|---|---|
| `Get(CurrentDate)` | date | Today's date per system clock |
| `Get(CurrentTime)` | time | Current time per system clock |
| `Get(CurrentTimestamp)` | timestamp | Current date+time |
| `Get(CurrentTimeUTCMilliseconds)` | number | Milliseconds since Unix epoch (UTC) |
| `Get(CurrentTimeUTCMicroseconds)` | number | Microseconds since Unix epoch (UTC) |
| `Get(CurrentHostTimestamp)` | timestamp | Server-side timestamp (consistent across all clients) |

```
Get ( CurrentDate )               // → 6/4/2026
Get ( CurrentTimestamp )          // → 6/4/2026 9:15:00 AM
Get ( CurrentTimeUTCMilliseconds ) // → 1748996100000
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
| `Get(AccountType)` | number | 0=FileMaker, 1=External server, 2=Claris ID |
| `Get(AccountGroupName)` | text | External server group name (LDAP/Active Directory) |
| `Get(AccountPrivilegeSetName)` | text | Name of the current privilege set |
| `Get(AccountExtendedPrivileges)` | text | Return-delimited list of extended privilege keywords |
| `Get(AccountPasswordDaysRemaining)` | number | **FM 26+** — Days before current password must change; empty if no expiry set |
| `Get(CurrentPrivilegeSetName)` | text | Synonym for `AccountPrivilegeSetName` |
| `Get(CurrentExtendedPrivileges)` | text | Synonym for `AccountExtendedPrivileges` |
| `Get(UserName)` | text | OS-level username (not account name) |
| `Get(UserCount)` | number | Number of users connected to the hosted file |

```
Get ( AccountName )               // → "bjones"
Get ( AccountPrivilegeSetName )   // → "[Full Access]"
Get ( AccountExtendedPrivileges ) // → "fmwebdirect¶fmmobileapp"
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
| `Get(EncryptionState)` | number | 1 if file is encrypted at rest |
| `Get(FileLocaleElements)` | text | JSON of file locale settings |
| `Get(HostName)` | text | Server hostname or "localhost" |
| `Get(HostIPAddress)` | text | IP address of the host |
| `Get(HostApplicationVersion)` | text | FileMaker Server version string |
| `Get(ApplicationVersion)` | text | FileMaker Pro/Go/WebDirect version |
| `Get(ApplicationLanguage)` | text | UI language of the application |
| `Get(ApplicationArchitecture)` | text | `"x86"` or `"arm64"` |
| `Get(FileMakerPath)` | text | Path to the FileMaker application executable |
| `Get(CacheFileName)` | text | Name of the local cache file (hosted files) |
| `Get(CacheFilePath)` | text | Path to the local cache file |
| `Get(OpenDataFileInfo)` | text | Info about any open data files |
| `Get(SessionIdentifier)` | text | Unique ID for the current session |
| `Get(SystemVersion)` | text | OS version string |
| `Get(SystemDrive)` | text | Boot drive path |
| `Get(SystemIPAddress)` | text | Client's IP address (newline-delimited if multiple) |
| `Get(SystemNICAddress)` | text | Network interface card MAC address |
| `Get(SystemLanguage)` | text | OS language setting |
| `Get(SystemPlatform)` | number | 1=macOS, 2=Windows, 3=unused, 4=iOS/iPadOS |
| `Get(SystemAppearance)` | text | `"Light"` or `"Dark"` (OS appearance mode) |
| `Get(SystemLocaleElements)` | text | JSON of OS locale settings |
| `Get(SystemStorageAvailable)` | number | Available storage in bytes |
| `Get(MultiUserState)` | number | 0=local only, 1=hosted/no share, 2=network sharing |
| `Get(InstalledFMPlugins)` | text | Return-delimited list of installed plug-ins |
| `Get(InstalledFMPluginsAsJSON)` | text | JSON array of installed plug-in details |

```
Get ( FileName )             // → "CRM"
Get ( FilePath )             // → "filemacosx:/Volumes/Data/CRM.fmp12"
Get ( SystemPlatform )       // → 1 (macOS)
Get ( ApplicationVersion )   // → "ProAdvanced 22.0.4.401"
Get ( ApplicationArchitecture ) // → "arm64"
Get ( SystemAppearance )     // → "Dark"
Get ( EncryptionState )      // → 1 (file is encrypted)
```

Platform-conditional logic:
```
Case (
  Get ( SystemPlatform ) = 1 ; "mac" ;
  Get ( SystemPlatform ) = 2 ; "win" ;
  Get ( SystemPlatform ) = 4 ; "ios" ;
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
| `Get(ActiveRecordNumber)` | number | Row number of active record in portal (0 if not in portal) |
| `Get(TotalRecordCount)` | number | All records in the table |
| `Get(FoundCount)` | number | Records in current found set |
| `Get(RecordOpenCount)` | number | Number of records currently open/locked |
| `Get(RecordOpenState)` | number | 0=unmodified, 1=modified, 2=new |
| `Get(RecordModificationCount)` | number | Cumulative modification count for current record |
| `Get(RecordAccess)` | number | Access level for current record (bitmask) |
| `Get(ModifiedFields)` | text | Return-delimited list of modified field names (unsaved) |

```
Get ( RecordID )              // → 1042
Get ( RecordNumber )          // → 3  (3rd record in found set)
Get ( FoundCount )            // → 47
Get ( RecordOpenState )       // → 1 if unsaved changes exist
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
| `Get(LayoutAccess)` | number | Access level for current layout (bitmask) |
| `Get(WindowName)` | text | Current window title |
| `Get(WindowHeight)` | number | Window height in points |
| `Get(WindowWidth)` | number | Window width in points |
| `Get(WindowTop)` | number | Window top position in points |
| `Get(WindowLeft)` | number | Window left position in points |
| `Get(WindowContentHeight)` | number | Usable content area height |
| `Get(WindowContentWidth)` | number | Usable content area width |
| `Get(WindowDesktopHeight)` | number | Total desktop/screen height |
| `Get(WindowDesktopWidth)` | number | Total desktop/screen width |
| `Get(WindowMode)` | number | 0=Browse, 1=Find, 2=Preview, 3=disabled |
| `Get(WindowStyle)` | number | 0=Document, 1=Floating document, 2=Dialog |
| `Get(WindowZoomLevel)` | number | Current zoom percentage |
| `Get(WindowVisible)` | number | 1=visible, 0=hidden |
| `Get(WindowOrientation)` | number | 0=portrait, 1=landscape (FileMaker Go only) |
| `Get(WindowUUID)` | text | **FM 26+** — Unique stable UUID for the active window; useful for managing multiple windows of the same file |
| `Get(ActiveLayoutObjectName)` | text | Name of the currently focused layout object |
| `Get(StatusAreaState)` | number | 0=hidden, 1=visible, 2=locked |
| `Get(MenubarState)` | number | 0=hidden, 1=locked, 2=normal |
| `Get(CustomMenuSetName)` | text | Name of the active custom menu set |
| `Get(AllowFormattingBarState)` | number | 1 if formatting bar is allowed |
| `Get(TextRulerVisible)` | number | 1 if text ruler is visible |
| `Get(TouchKeyboardState)` | number | 1 if touch keyboard is visible (Go) |

```
Get ( LayoutName )         // → "Invoices - Detail"
Get ( LayoutTableName )    // → "Invoices"
Get ( WindowMode )         // → 0 (Browse)
Get ( WindowContentWidth ) // → 1024
Get ( WindowOrientation )  // → 1 (landscape, on iPad)
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
| `Get(LastStepTokensUsed)` | number | AI tokens consumed by the last AI script step |
| `Get(ErrorCaptureState)` | number | 1 if Set Error Capture is On |
| `Get(AllowAbortState)` | number | 1 if Allow User Abort is On |
| `Get(ScriptAnimationState)` | number | 1 if script animations are enabled |
| `Get(RequestCount)` | number | Number of find requests defined |
| `Get(RequestOmitState)` | number | 1 if current find request is set to Omit |
| `Get(TransactionOpenState)` | number | 1 if inside an open transaction block |
| `Get(RevertTransactionOnErrorState)` | number | 1 if Revert Transaction on Error is active |
| `Get(TriggerCurrentPanel)` | number | Panel index being navigated to (panel triggers) |
| `Get(TriggerTargetPanel)` | number | Target panel in a panel navigation trigger |
| `Get(TriggerGestureInfo)` | text | JSON describing touch/swipe gesture |
| `Get(TriggerKeystroke)` | text | Key pressed in an OnObjectKeystroke trigger |
| `Get(TriggerModifierKeys)` | number | Modifier keys held during trigger (bitmask) |
| `Get(TriggerExternalEvent)` | text | External event name that fired the trigger |

```
Get ( ScriptParameter )   // → JSON or text passed from calling context
Get ( LastError )         // → 401 (no records match)
Get ( LastErrorDetail )   // → human-readable error description
Get ( LastErrorLocation ) // → "InvoicesSave : Set Field [Invoice::Status]"
Get ( LastMessageChoice ) // → 2 (user clicked second button)
Get ( ScriptResult )      // → result from last Perform Script
Get ( LastStepTokensUsed ) // → 342 (tokens used by last AI step)
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
| `Get(NetworkType)` | text | Connection type |
| `Get(ConnectionState)` | number | 1=connected to host, 0=not connected |
| `Get(ConnectionAttributes)` | text | Encrypted connection details JSON |
| `Get(PersistentID)` | text | Unique persistent ID for the current file instance |
| `Get(UUID)` | text | Generates a new UUID (v4) each time evaluated |
| `Get(UUIDNumber)` | text | UUID formatted as a large number |

```
Get ( UUID )             // → "A1B2C3D4-E5F6-7890-ABCD-EF1234567890"
Get ( ConnectionState )  // → 1 (connected to server)
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
| `Get(Device)` | number | 0=unknown, 1=Mac, 2=Windows, 3=unused, 4=iPad, 5=iPhone |
| `Get(ScreenDepth)` | number | Colour depth in bits |
| `Get(ScreenHeight)` | number | Screen height in points |
| `Get(ScreenWidth)` | number | Screen width in points |
| `Get(ScreenScaleFactor)` | number | Display scale factor (2.0 for Retina, 3.0 for Super Retina) |
| `Get(HighContrastState)` | number | 1 if OS high contrast / accessibility mode is active |
| `Get(GuidedAccessState)` | number | **FM 26+, FileMaker Go only** — 1 if iOS Guided Access is currently active; use to detect kiosk/locked-screen mode |
| `Get(RegionMonitorEvents)` | text | JSON of pending region monitor events (Go only) |

```
Get ( Device )             // → 4 (iPad)
Get ( ScreenWidth )        // → 1024
Get ( ScreenScaleFactor )  // → 2  (Retina display)
Get ( HighContrastState )  // → 0 (normal mode)
```

Detect iPad vs iPhone:
```
Case (
  Get ( Device ) = 4 ; "iPad layout" ;
  Get ( Device ) = 5 ; "iPhone layout" ;
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
If [ Get ( LastStepTokensUsed ) > 5000 ]
  // Log or warn — high token usage
End If
```
