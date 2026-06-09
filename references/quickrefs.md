# Quick References — Error Codes, SQL, Data API & Sitemap

---

# FileMaker Error Codes — Quick Reference

Source: https://help.claris.com/en/pro-help/content/error-codes.html  
Last verified: 2026-06 against live Claris Help Centre.  
Last audited: 2026-06 — full replacement against official Claris docs (282 discrete codes + 2 ranges).

Codes marked with `*` are returned by the web publishing engine or a FileMaker REST API.

**Usage:** Call `Get ( LastError )` immediately after a script step to capture the error code. Use `Set Error Capture [ On ]` to suppress FileMaker dialogs and handle errors programmatically.

```
Set Error Capture [ On ]
Perform Find [ Restore ]
Set Variable [ $err ; Value: Get ( LastError ) ]
If [ $err ≠ 0 ]
  // handle error
End If
```

For calculation functions: `ExecuteSQL` returns `"?"` on error — use `ExecuteSQLe` for a message. `Evaluate` errors are captured via `EvaluationError()`.

---

## -1 — Unknown error
Returned when FileMaker cannot determine the specific error.

---

## 0 — Success
No error.

---

## System errors (1–21)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1 | User canceled action | User pressed Escape/Cancel in a dialog |
| 2 | Memory error | Insufficient RAM |
| 3 | Command is unavailable (for example, wrong operating system or mode) | Step used in wrong mode (e.g. New Record in Find mode) |
| 4 | Command is unknown | Step not supported on this platform |
| 5 | Command is invalid (for example, a Set Field script step does not have a calculation specified) | No record selected, or invalid context |
| 6 | File is read-only | File opened as read-only or on read-only media |
| 7 | Running out of memory | Low memory condition |
| 9 | Insufficient privileges | Privilege set does not allow this action |
| 10 | Requested data is missing | Data or file not found |
| 11 | Name is not valid | Invalid field/table/object name |
| 12 | Name already exists | Duplicate name in schema |
| 13 | File or object is in use | File locked by another user/process |
| 14 | Out of range | Value or index out of valid range |
| 15 | Can't divide by zero | Division by zero |
| 16 | Operation failed; request retry (for example, a user query) | Transient failure — retry the operation |
| 17 | Attempt to convert foreign character set to UTF-16 failed | Character encoding conversion issue |
| 18 | Client must provide account information to proceed | Authentication required before continuing |
| 19 | String contains characters other than A-Z, a-z, 0-9 (ASCII) | Non-ASCII characters in a field requiring ASCII only |
| 20 | Command/operation canceled by triggered script | A triggered script cancelled the calling operation |
| 21 | Request not supported (for example, when creating a hard link on a file system that does not support hard links) | Platform or filesystem limitation |

> **Note:** Code 8 does not appear in the official Claris error-codes table. If you encounter it, treat as unknown and log for investigation.

---

## Object missing errors (100–131)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 100 | File is missing | File not found at specified path |
| 101 | Record is missing | Record ID no longer exists |
| 102 | Field is missing | Field not found in table |
| 103 | Relationship is missing | Relationship definition deleted |
| 104 | Script is missing | Script not found |
| 105 | Layout is missing | Layout not found |
| 106 | Table is missing | Table not found |
| 107 | Index is missing | Field index missing — rebuild index |
| 108 | Value list is missing | Value list not found |
| 109 | Privilege set is missing | Privilege set deleted |
| 110 | Related tables are missing | Tables in relationship not found |
| 111 | Field repetition is invalid | Repetition index out of range |
| 112 | Window is missing | Named window not found |
| 113 | Function is missing | Custom function not found |
| 114 | File reference is missing | External file reference invalid |
| 115 | Menu set is missing | Custom menu set not found |
| 116 | Layout object is missing | Named object not on layout |
| 117 | Data source is missing | External data source not found |
| 118 | Theme is missing | Theme not found |
| 119 | No supported email client found | No compatible email app installed |
| 130 | Files are damaged or missing and must be reinstalled | Corrupt or missing FileMaker installation files |
| 131 | Language pack files are missing | Localisation files not installed |

---

## Account / access errors (200–219)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 200 | Record access is denied | Privilege set restricts read |
| 201 | Field cannot be modified | Field is calculated or protected |
| 202 | Field access is denied | Privilege set restricts field access |
| 203 | No records in file to print, or password doesn't allow print access | Table is empty, or privilege set blocks printing |
| 204 | No access to field(s) in sort order | Privilege set restricts a field used in the sort |
| 205 | User does not have access privileges to create new records; import will overwrite existing data | Privilege set blocks record creation |
| 206 | User does not have password change privileges, or file is not modifiable | Cannot change own password |
| 207 | User does not have privileges to change database schema, or file is not modifiable | Full Access required |
| 208 | Password does not contain enough characters | Password too short (see security settings) |
| 209 | New password must be different from existing one | Password reuse not allowed |
| 210 | User account is inactive | Account has been disabled |
| 211 | Password has expired | Account password must be changed |
| 212 | Invalid user account or password | Wrong credentials |
| 214 | Too many login attempts | Account locked after repeated failures |
| 215 | Administrator privileges cannot be duplicated | Cannot copy Full Access account |
| 216 | Guest account cannot be duplicated | Guest account is a singleton |
| 217 | User does not have sufficient privileges to modify administrator account | Full Access required to edit admin account |
| 218 | Password and verify password do not match | Confirm-password field differs |
| 219 | Cannot open file; must be licensed user; contact team manager | Licensing limit reached |

---

## Concurrency / locking errors (300–310)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 300 | File is locked or in use | Another process holds the file lock |
| 301 | Record is in use by another user | Record locked by another session |
| 302 | Table is in use by another user | Schema change blocked by active user |
| 303 | Database schema is in use by another user | DDL change blocked |
| 304 | Layout is in use by another user | Layout edit blocked |
| 305 | Layout was not created | Layout creation failed |
| 306 | Record modification ID does not match | Optimistic locking conflict — record modified elsewhere |
| 307 | Transaction could not be locked because of a communication error with the host | Network issue during commit |
| 308 | Theme is locked and in use by another user | Theme edit blocked |
| 310 | Cannot modify items because another user is modifying them | Concurrent modification conflict |

---

## Find / sort / data errors (400–418)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 400 | Find criteria are empty | Find performed with no criteria entered |
| 401 | No records match the request | **Most common** — find returned zero records |
| 402 | Selected field is not a match field for a lookup | Field not configured as a lookup match field |
| 404 | Sort order is invalid | Sort references a missing or invalid field |
| 405 | Number of records specified exceeds number of records that can be omitted | Omit count too large |
| 406 | Replace/reserialize criteria are invalid | Replace Field Contents or Serialize criteria broken |
| 407 | One or both match fields are missing (invalid relationship) | Relationship match field deleted |
| 408 | Specified field has inappropriate data type for this operation | Wrong field type for the operation |
| 409 | Import order is invalid | Import field mapping broken |
| 410 | Export order is invalid | Export field mapping broken |
| 412 | Wrong version of FileMaker Pro used to recover file | Version mismatch during recovery |
| 413 | Specified field has inappropriate field type | Wrong field type (e.g. container where text expected) |
| 414 | Layout cannot display the result | Result type incompatible with layout |
| 415 | One or more required related records are not available | Related data missing |
| 416 | A primary key is required from the data source table | External data source missing primary key |
| 417 | File is not a supported data source | Unsupported external data source type |
| 418 | Internal failure in INSERT operation into a field | Internal error placing data into a field |

---

## Validation errors (500–513)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 500 | Date value does not meet validation entry options | Field validation failed (date) |
| 501 | Time value does not meet validation entry options | Field validation failed (time) |
| 502 | Number value does not meet validation entry options | Field validation failed (number) |
| 503 | Value in field is not within the range specified in validation entry options | Range validation failed |
| 504 | Value in field is not unique, as required in validation entry options | Unique validation failed |
| 505 | Value in field is not an existing value in the file, as required in validation entry options | Existing value validation failed |
| 506 | Value in field is not listed in the value list specified in validation entry option | Value list validation failed |
| 507 | Value in field failed calculation test of validation entry option | Calculation validation failed |
| 508 | Invalid value entered in Find mode | Find criteria invalid for field type |
| 509 | Field requires a valid value | Required field is empty |
| 510 | Related value is empty or unavailable | Related field has no value |
| 511 | Value in field exceeds maximum field size | Text too long for field |
| 512 | Record was already modified by another user | Conflict on commit |
| 513 | No validation was specified but data cannot fit into the field | Data too large for unvalidated field |

---

## Print errors (600–603)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 600 | Print error has occurred | General print failure |
| 601 | Combined header and footer exceed one page | Header + footer height exceeds page size |
| 602 | Body doesn't fit on a page for current column setup | Column layout too wide for page |
| 603 | Print connection lost | Printer disconnected during print job |

---

## File type / import / export errors (700–738)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 700 | File is of the wrong file type for import | Unsupported file format for import |
| 706 | EPS file has no preview image | EPS lacks embedded preview |
| 707 | Graphic translator cannot be found | Missing image translation library |
| 708 | Can't import the file, or need color monitor support to import file | Platform or display restriction |
| 711 | Import translator cannot be found | Missing import translation library |
| 714 | Password privileges do not allow the operation | Privilege set blocks import/export |
| 715 | Specified Excel worksheet or named range is missing | Excel target sheet or range not found |
| 716 | A SQL query using DELETE, INSERT, or UPDATE is not allowed for ODBC import | Only SELECT is permitted for ODBC import |
| 717 | There is not enough XML/XSL information to proceed with the import or export | Missing XML grammar or XSL stylesheet |
| 718 | Error in parsing XML file | Malformed XML |
| 719 | Error in transforming XML using XSL | XSL transformation failed |
| 720 | Error when exporting; intended format does not support repeating fields | Repeating field export format limitation |
| 721 | Unknown error occurred in the parser or the transformer | XML/XSL parser internal error |
| 722 | Cannot import data into a file that has no fields | Target file has no fields defined |
| 723 | You do not have permission to add records to or modify records in the target table | Privilege restriction on import target |
| 724 | You do not have permission to add records to the target table | Cannot create records in target |
| 725 | You do not have permission to modify records in the target table | Cannot edit records in target |
| 726 | Source file has more records than the target table; not all records were imported | Import truncated — record count exceeded |
| 727 | Target table has more records than the source file; not all records were updated | Update import left extra target records untouched |
| 729 | Errors occurred during import; records could not be imported | Import partial failure |
| 730 | Unsupported Excel version; convert file to the current Excel format and try again | Old .xls format — convert to .xlsx |
| 731 | File you are importing from contains no data | Source file is empty |
| 732 | This file cannot be inserted because it contains other files | Cannot insert a container file |
| 733 | A table cannot be imported into itself | Self-import not permitted |
| 734 | This file type cannot be displayed as a picture | File cannot render as inline image |
| 735 | This file type cannot be displayed as a picture; it will be inserted and displayed as a file | File stored as file reference, not picture |
| 736 | Too much data to export to this format; data will be truncated | Export format has a data size limit |
| 738 | The theme you are importing already exists | Duplicate theme name on import |

---

## File I/O errors (800–853)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 800 | Unable to create file on disk | Permissions or disk issue |
| 801 | Unable to create temporary file on System disk | Temp folder full or restricted |
| 802 | Unable to open file | File locked, missing, or corrupt |
| 803 | File is single-user, or host cannot be found | Single-user file accessed remotely, or host offline |
| 804 | File cannot be opened as read-only in its current state | File state prevents read-only open |
| 805 | File is damaged; use Recover command | Corruption detected — run File > Recover |
| 806 | File cannot be opened with this version of a FileMaker client | Client version too old or too new |
| 807 | File is not a FileMaker Pro file or is severely damaged | Not a valid FileMaker file |
| 808 | Cannot open file because access privileges are damaged | Privilege data corrupt |
| 809 | Disk/volume is full | No free space on disk |
| 810 | Disk/volume is locked | Volume is write-protected |
| 811 | Temporary file cannot be opened as FileMaker Pro file | Temp file corrupt or wrong type |
| 812 | Exceeded host's capacity | Host connection limit reached |
| 813 | Record synchronization error on network | Network sync failure on commit |
| 814 | File(s) cannot be opened because maximum number is open | Too many files open simultaneously |
| 815 | Couldn't open lookup file | Lookup source file unavailable |
| 816 | Unable to convert file | File conversion (older format) failed |
| 817 | Unable to open file because it does not belong to this solution | File not in the same solution bundle |
| 819 | Cannot save a local copy of a remote file | Save a Copy restricted for hosted files |
| 820 | File is being closed | File is in the process of closing |
| 821 | Host forced a disconnect | Server kicked the client |
| 822 | FileMaker Pro files not found; reinstall missing files | Core FileMaker files missing |
| 823 | Cannot set file to single-user; guests are connected | Active guests prevent single-user mode |
| 824 | File is damaged or not a FileMaker Pro file | Corruption or wrong file type |
| 825 | File is not authorized to reference the protected file | External file reference not authorised |
| 826 | File path specified is not a valid file path | Path syntax invalid for the OS |
| 827 | File was not created because the source contained no data or is a reference | Empty or reference-only source |
| 850 | Path is not valid for the operating system | OS-specific path format error |
| 851 | Cannot delete an external file from disk | Permission denied deleting container external file |
| 852 | Cannot write a file to the external storage | Cannot write to container external storage location |
| 853 | One or more containers failed to transfer | Container data transfer error |

---

## AI / Machine Learning errors (870–892)

Source: https://help.claris.com/en/pro-help/content/error-codes.html (verified 2026-06)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 870 | Cannot modify file because another user is modifying it | Concurrent modification conflict |
| 871 | Error occurred loading Core ML model | ML model file issue |
| 872 | Core ML model was not loaded because it contained an unsupported input or output parameter | Incompatible Core ML model |
| 875 | Endpoint is empty | No endpoint URL configured for AI account |
| 876 | Current layout doesn't show records from the specified table | Layout/table mismatch in AI step |
| 877 | Can't find AI account | Account name not found in Configure AI Account |
| 878 | JSON data for Options contains a formatting error and couldn't be parsed | Malformed Options JSON |
| 879 | JSON data for Parameters contains a formatting error and couldn't be parsed | Malformed Parameters JSON |
| 882 | Invalid AI request | Bad request sent to AI provider |
| 883 | Invalid request to custom model provider | Custom/3rd-party provider rejected request |
| 885 | Endpoint is invalid or server is unreachable | Wrong URL or network issue |
| 886 | Invalid Custom/Open Source Provider request | Open-source provider request error |
| 887 | Invalid RAG space action | Bad action specified in Perform RAG Action |
| 892 | Can't find RAG account | RAG account name not found |

---

## Spelling engine errors (900–923)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 900 | General spelling engine error | Spelling engine failure |
| 901 | Main spelling dictionary not installed | Spelling dictionary files missing |
| 903 | Command cannot be used in a shared file | Spelling operation not available in multi-user |
| 905 | Command requires a field to be active | No field is currently active |
| 906 | Current file is not shared; command can be used only if the file is shared | Requires hosted/shared file |
| 920 | Cannot initialize the spelling engine | Spelling engine failed to start |
| 921 | User dictionary cannot be loaded for editing | User dictionary file inaccessible |
| 922 | User dictionary cannot be found | User dictionary file missing |
| 923 | User dictionary is read-only | Cannot write to user dictionary |

---

## Web publishing / Custom Web Publishing errors (951–960) *

| Code | Official Description | Notes |
|------|---------------------|-------|
| 951 | An unexpected error occurred (*) | General web publishing error |
| 952 | Invalid FileMaker Data API token (*) | Session token expired or invalid |
| 953 | Exceeded limit on data the FileMaker Data API and OData can transmit (*) | Response payload too large |
| 954 | Unsupported XML grammar (*) | XML grammar not recognised by web publishing |
| 955 | No database name (*) | Database name missing from request |
| 956 | Maximum number of database or Admin API sessions exceeded (*) | Session pool exhausted |
| 957 | Conflicting commands (*) | Two operations conflict |
| 958 | Parameter missing (*) | Required parameter absent from request |
| 959 | Custom Web Publishing technology is disabled | CWP not enabled in Admin Console |
| 960 | Parameter is invalid | Parameter value not valid |

---

## Calculation errors (1200–1225)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1200 | Generic calculation error | Unspecified calculation failure |
| 1201 | Too few parameters in the function | Not enough arguments passed |
| 1202 | Too many parameters in the function | Too many arguments passed |
| 1203 | Unexpected end of calculation | Calculation text ends prematurely |
| 1204 | Number, text constant, field name, or "(" expected | Syntax error — expected value or open paren |
| 1205 | Comment is not terminated with "*/" | Unclosed `/* */` comment |
| 1206 | Text constant must end with a quotation mark | Unclosed string literal |
| 1207 | Unbalanced parenthesis | Mismatched `(` or `)` |
| 1208 | Operator missing, function not found, or "(" not expected | Unknown function or missing operator |
| 1209 | Name (such as field name or layout name) is missing | Expected identifier not found |
| 1210 | Plug-in function or script step has already been registered | Duplicate plug-in registration |
| 1211 | List usage is not allowed in this function | List/repeating value not valid here |
| 1212 | An operator (for example, +, -, *) is expected here | Missing arithmetic or logical operator |
| 1213 | This variable has already been defined in the Let function | Duplicate variable name in `Let()` |
| 1214 | A function parameter contains an expression where a field is required | Expression used where a field reference is required |
| 1215 | This parameter is an invalid Get function parameter | Invalid argument to `Get()` |
| 1216 | Only summary fields are allowed as first argument in GetSummary | Non-summary field passed to `GetSummary()` |
| 1217 | Break field is invalid | Break field for `GetSummary()` is invalid |
| 1218 | Cannot evaluate the number | Number evaluation failed |
| 1219 | A field cannot be used in its own formula | Circular reference in calculation |
| 1220 | Field type must be normal or calculated | Storage type incompatible with operation |
| 1221 | Data type must be number, date, time, or timestamp | Wrong data type in calculation |
| 1222 | Calculation cannot be stored | Calculation result cannot be stored (unstored required) |
| 1223 | Function referred to is not yet implemented | Function exists but not yet available in this context |
| 1224 | Function referred to does not exist | Unknown function name |
| 1225 | Function referred to is not supported in this context | Function not available in this context (e.g. WebDirect) |

---

## Custom function errors (1300–1301)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1300 | The specified name can't be used | Name conflicts with a reserved word |
| 1301 | A parameter of the imported or pasted function has the same name as a function in the file | Name collision on custom function import |

---

## ODBC errors (1400–1415)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1400 | ODBC client driver initialization failed; make sure ODBC client drivers are properly installed | ODBC driver not found or not installed |
| 1401 | Failed to allocate environment (ODBC) | ODBC environment allocation failure |
| 1402 | Failed to free environment (ODBC) | ODBC environment teardown failure |
| 1403 | Failed to disconnect (ODBC) | ODBC disconnect error |
| 1404 | Failed to allocate connection (ODBC) | ODBC connection allocation failure |
| 1405 | Failed to free connection (ODBC) | ODBC connection teardown failure |
| 1406 | Failed check for SQL API (ODBC) | ODBC SQL API not supported by driver |
| 1407 | Failed to allocate statement (ODBC) | ODBC statement allocation failure |
| 1408 | Extended error (ODBC) | ODBC driver extended error — check driver logs |
| 1409 | Error (ODBC) | General ODBC error |
| 1413 | Failed communication link (ODBC) | ODBC network communication failure |
| 1414 | SQL statement is too long | SQL query exceeds maximum length |
| 1415 | Connection is being disconnected (ODBC) | ODBC connection is closing |
| 1450 | Action requires PHP privilege extension (*) | PHP web publishing privilege not granted |
| 1451 | Action requires that current file be remote | Operation only valid on a hosted file |

---

## SMTP / email errors (1501–1507)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1501 | SMTP authentication failed | Wrong SMTP credentials |
| 1502 | Connection refused by SMTP server | SMTP server rejected the connection |
| 1503 | Error with SSL | SSL handshake failed with SMTP server |
| 1504 | SMTP server requires the connection to be encrypted | Server requires TLS/SSL; enable it in Send Mail settings |
| 1505 | Specified authentication is not supported by SMTP server | Auth method not supported by server |
| 1506 | Email message(s) could not be sent successfully | General send failure |
| 1507 | Unable to log in to the SMTP server | SMTP login rejected |

---

## JWT / token errors (1541–1543)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1541 | JSON Web Token (JWT) could not be generated successfully. Please check to make sure you have entered the private key correctly. | Private key invalid or malformed |
| 1542 | Access token could not be generated successfully. | Token generation failure |
| 1543 | Test email could not be sent successfully. | Test email via SMTP settings failed |

---

## Plug-in errors (1550–1559)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1550 | Cannot load the plug-in, or the plug-in is not a valid plug-in | Plug-in file corrupt or incompatible |
| 1551 | Cannot install the plug-in; cannot delete an existing plug-in or write to the folder or disk | Permissions issue installing plug-in |
| 1552–1559 | Returned by plug-ins; see the documentation that came with the plug-in | Custom error range — consult plug-in vendor |

---

## Network / SSL / Insert From URL errors (1626–1638)

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1626 | Protocol is not supported | URL protocol not supported by Insert From URL |
| 1627 | Authentication failed | Credential rejection from remote server |
| 1628 | There was an error with SSL | SSL/TLS error on connection |
| 1629 | Connection timed out; the timeout value is 60 seconds | Server did not respond within 60 s |
| 1630 | URL format is incorrect | Malformed URL — check scheme, host, path |
| 1631 | Connection failed | Server unreachable or connection refused |
| 1632 | The certificate has expired | Server SSL certificate past its expiry date |
| 1633 | The certificate is self-signed | Server uses a self-signed cert; not trusted by default |
| 1634 | A certificate verification error occurred | SSL cert could not be verified |
| 1635 | Connection is unencrypted | Server requires encrypted connection |
| 1638 | The host is not allowing new connections. Try again later. | Server has hit its connection limit |

**Note:** HTTP status codes (404, 500 etc.) are NOT FileMaker error codes — they are returned in the response body/variable. Check the result text for `"HTTP/1.1 4"` or `"HTTP/1.1 5"` patterns.

---

## Data API REST errors (1700–1715) *

| Code | Official Description | Notes |
|------|---------------------|-------|
| 1700 | Resource doesn't exist (*) | Requested database, layout, or record not found |
| 1701 | Host is currently unable to receive requests (*) | Server overloaded or starting up |
| 1702 | Authentication information wasn't provided in the correct format; verify the value of the Authorization header (*) | Malformed Authorization header |
| 1703 | Invalid username or password, or JSON Web Token (*) | Bad credentials or expired JWT |
| 1704 | Resource doesn't support the specified HTTP verb (*) | Wrong HTTP method (GET/POST/PATCH/DELETE) |
| 1705 | Required HTTP header wasn't specified (*) | Missing required header (e.g. Content-Type) |
| 1706 | Parameter isn't supported (*) | Unsupported query parameter |
| 1707 | Required parameter wasn't specified in the request (*) | Missing required parameter |
| 1708 | Parameter value is invalid (*) | Parameter value out of range or wrong type |
| 1709 | Operation is invalid for the resource's current status (*) | State conflict (e.g. editing a record locked by another) |
| 1710 | JSON input isn't syntactically valid (*) | Malformed JSON in request body |
| 1711 | Host's license has expired (*) | FileMaker Server license lapsed |
| 1712 | Private key file already exists; remove it and run the command again (*) | Key file conflict in Admin API |
| 1713 | The API request is not supported for this operating system (*) | OS limitation on this Admin API call |
| 1714 | External group name is invalid (*) | External auth group name not found |
| 1715 | External server account sign-in is not enabled (*) | External auth not configured on server |

---

## Custom errors (5000–5499)

| Range | Description |
|-------|-------------|
| 5000–5499 | Custom errors returned by the Revert Transaction script step. These codes are defined by the developer and have no predefined meaning — document your error code assignments in your solution. |

---

## SQL / ExecuteSQL errors

ExecuteSQL returns `"?"` (not an error code) on failure. Use `ExecuteSQLe` to get a descriptive message, or check:
- Error 401: No records match (used when ExecuteSQL is inside a script context)

SQL-specific error strings from `ExecuteSQLe`:
| Message pattern | Likely cause |
|---|---|
| `"ERROR: column ... does not exist"` | Wrong field name (remember: base table names, not TO names) |
| `"ERROR: table ... does not exist"` | Wrong table occurrence name |
| `"ERROR: syntax error"` | SQL syntax mistake |
| `"ERROR: type mismatch"` | Comparing wrong data types |

---

## Common error handling patterns

**Error after any critical step:**
```
Set Error Capture [ On ]
Commit Records/Requests [ No dialog ]
Set Variable [ $err ; Value: Get ( LastError ) ]
If [ $err ≠ 0 and $err ≠ 1 ]
  Show Custom Dialog [ "Save failed" ; "Error " & $err & ": please try again." ]
End If
```

**Find with no-records handling:**
```
Set Error Capture [ On ]
Perform Find [ Restore ]
Set Variable [ $err ; Value: Get ( LastError ) ]
If [ $err = 401 ]
  Show All Records
  Show Custom Dialog [ "No records found" ; "Your search returned no results." ]
Else If [ $err ≠ 0 ]
  Show Custom Dialog [ "Find error" ; "Error code: " & $err ]
End If
```

**Insert From URL with HTTP error detection:**
```
Set Error Capture [ On ]
Insert From URL [ Select ; No dialog ; $response ; $url ; $curlOptions ]
Set Variable [ $fmErr ; Value: Get ( LastError ) ]
If [ $fmErr = 1630 or $fmErr = 1631 ]
  Show Custom Dialog [ "Connection failed" ; "Cannot reach the server." ]
Else If [ PatternCount ( $response ; "\"error\"" ) > 0 ]
  Show Custom Dialog [ "API error" ; JSONGetElement ( $response ; "error.message" ) ]
End If
```

**Retry loop pattern:**
```
Set Variable [ $attempts ; Value: 0 ]
Set Variable [ $maxAttempts ; Value: 3 ]
Set Variable [ $err ; Value: 99 ]
Loop
  Exit Loop If [ $err = 0 or $attempts ≥ $maxAttempts ]
  Set Variable [ $attempts ; Value: $attempts + 1 ]
  Set Error Capture [ On ]
  // ... perform operation ...
  Set Variable [ $err ; Value: Get ( LastError ) ]
End Loop
```

---

# FileMaker SQL / ExecuteSQL — Quick Reference

Source: https://help.claris.com/en/sql-reference/content/index.html  
Always fetch the live page for complete syntax details.

---

## Two modes of use

1. **ExecuteSQL function** (inside FileMaker): SELECT only, reads any table occurrence in the current file.
2. **ODBC/JDBC** (external apps): Full SELECT, INSERT, UPDATE, DELETE, CREATE/DROP TABLE/INDEX.

---

## ExecuteSQL syntax

```
ExecuteSQL ( sqlQuery ; fieldSeparator ; rowSeparator { ; arguments... } )
```

- `fieldSeparator` — character between fields in each row (e.g. `","`)
- `rowSeparator` — character between rows (e.g. `¶`)
- Arguments are passed as `?` placeholders in the query

### Simple example
```
ExecuteSQL (
  "SELECT Name, Email FROM Contacts WHERE Status = ?"
  ; ","
  ; ¶
  ; "Active"
)
```

---

## Supported SQL: SELECT statement
```sql
SELECT [DISTINCT] column1, column2, ...
FROM TableName [AS alias]
[JOIN TableName2 ON ...]
[WHERE expression]
[GROUP BY column]
[HAVING expression]
[ORDER BY column [ASC|DESC]]
[OFFSET n ROWS]
[FETCH FIRST n ROWS ONLY]
```

---

## Data types in FileMaker SQL
| FileMaker type | SQL type |
|---------------|----------|
| Text | VARCHAR, CHAR |
| Number | NUMERIC, DECIMAL, INT, FLOAT |
| Date | DATE — format `date 'yyyy-mm-dd'` |
| Time | TIME — format `time 'hh:mm:ss'` |
| Timestamp | TIMESTAMP — format `timestamp 'yyyy-mm-dd hh:mm:ss'` |
| Container | Not queryable via SQL |
| Calculation | Queryable as its result type |

---

## Date / Time literals
```sql
WHERE BirthDate = date '1990-05-15'
WHERE StartTime = time '09:00:00'
WHERE CreatedAt = timestamp '2024-01-01 00:00:00'
```

---

## Key SQL functions (FileMaker subset)
| Function | Description |
|----------|-------------|
| `COUNT(*)` | Count rows |
| `SUM(col)` | Sum of column |
| `AVG(col)` | Average |
| `MIN(col)` | Minimum |
| `MAX(col)` | Maximum |
| `TRIM(str)` | Remove leading/trailing spaces |
| `UPPER(str)` / `LOWER(str)` | Case conversion |
| `SUBSTR(str, start, len)` | Substring |
| `LENGTH(str)` | String length |
| `CAST(val AS type)` | Type conversion |
| `COALESCE(a, b, ...)` | First non-null value |
| `CASE WHEN ... THEN ... ELSE ... END` | Conditional |

---

## JOINs
```sql
SELECT C.Name, O.OrderDate
FROM Customers AS C
INNER JOIN Orders AS O ON C.CustomerID = O.CustomerID
```
Supported: INNER JOIN, LEFT OUTER JOIN  
Note: Use **table occurrence names** exactly as they appear in the Relationships Graph.

---

## Special FileMaker SQL objects
| Object | SQL name |
|--------|----------|
| Record ID | `RECORDID` pseudo-column |
| Modification count | `MODID` pseudo-column |

```sql
SELECT RECORDID, Name FROM Contacts
```

---

## Common gotchas
- Field names with spaces must be quoted: `"First Name"`
- Table names must match the **table occurrence** name (not the underlying table name)
- ExecuteSQL returns text; use `GetAsNumber()` etc. to convert
- NULL handling: use `IS NULL` / `IS NOT NULL`
- No subqueries support in ExecuteSQL
- No INSERT/UPDATE/DELETE in ExecuteSQL (ODBC/JDBC only)

---

## Reserved keywords
Full list: https://help.claris.com/en/sql-reference/content/reserved-sql-keywords.html  
If a field/table name is a reserved word, quote it with double quotes.

---

## Full reference
- SQL statements: https://help.claris.com/en/sql-reference/content/sql-statements.html
- SQL clauses: https://help.claris.com/en/sql-reference/content/sql-clauses.html
- SQL expressions: https://help.claris.com/en/sql-reference/content/sql-expressions.html
- SQL functions: https://help.claris.com/en/sql-reference/content/sql-functions.html
- System objects: https://help.claris.com/en/sql-reference/content/filemaker-system-objects.html
- Error codes: https://help.claris.com/en/sql-reference/content/filemaker-sql-error-codes.html

---

# FileMaker Data API — Quick Reference

Source: https://help.claris.com/en/data-api-guide/content/index.html  
Full detail: always fetch the live page for complete request/response examples.

---

## Base URL
```
https://{host}/fmi/data/v1/databases/{database-name}
```
Or use `vLatest` instead of `v1` to always get the current version.

---

## Authentication

### Log in (get session token)
```
POST /fmi/data/v1/databases/{db}/sessions
Content-Type: application/json
Authorization: Basic {base64(user:password)}
Body: {}
```
Returns: `{ "response": { "token": "..." } }`  
Token is valid for 15 minutes of inactivity; each call resets the counter.  
Doc: https://help.claris.com/en/data-api-guide/content/log-in-database-session.html

### Log out
```
DELETE /fmi/data/v1/databases/{db}/sessions/{token}
```
Doc: https://help.claris.com/en/data-api-guide/content/log-out-database-session.html

### Validate session
```
GET /fmi/data/v1/validateSession
Authorization: Bearer {token}
```
Doc: https://help.claris.com/en/data-api-guide/content/validate-database-session.html

### FileMaker Cloud (Claris ID)
```
Authorization: FMID {claris-id-token}
```
Doc: https://help.claris.com/en/data-api-guide/content/log-in-database-session-claris-id.html

---

## Records

### Create record
```
POST /fmi/data/v1/databases/{db}/layouts/{layout}/records
Authorization: Bearer {token}
Content-Type: application/json
Body: { "fieldData": { "field1": "value1", ... } }
```
Doc: https://help.claris.com/en/data-api-guide/content/create-record.html

### Get single record
```
GET /fmi/data/v1/databases/{db}/layouts/{layout}/records/{recordId}
Authorization: Bearer {token}
```
Doc: https://help.claris.com/en/data-api-guide/content/get-single-record.html

### Get range of records
```
GET /fmi/data/v1/databases/{db}/layouts/{layout}/records?_offset=1&_limit=100
Authorization: Bearer {token}
```
Doc: https://help.claris.com/en/data-api-guide/content/get-range-of-records.html

### Edit record
```
PATCH /fmi/data/v1/databases/{db}/layouts/{layout}/records/{recordId}
Authorization: Bearer {token}
Content-Type: application/json
Body: { "fieldData": { "field1": "newValue" } }
```
Doc: https://help.claris.com/en/data-api-guide/content/edit-record.html

### Duplicate record
```
POST /fmi/data/v1/databases/{db}/layouts/{layout}/records/{recordId}
Authorization: Bearer {token}
```
Doc: https://help.claris.com/en/data-api-guide/content/duplicate-record.html

### Delete record
```
DELETE /fmi/data/v1/databases/{db}/layouts/{layout}/records/{recordId}
Authorization: Bearer {token}
```
Doc: https://help.claris.com/en/data-api-guide/content/delete-record.html

---

## Find

### Perform find request
```
POST /fmi/data/v1/databases/{db}/layouts/{layout}/_find
Authorization: Bearer {token}
Content-Type: application/json
Body: {
  "query": [
    { "field1": "=value", "field2": ">100" }
  ],
  "sort": [{ "fieldName": "field1", "sortOrder": "ascend" }],
  "limit": "50",
  "offset": "1"
}
```
Doc: https://help.claris.com/en/data-api-guide/content/perform-find-request.html

---

## Metadata
```
GET /fmi/data/v1/databases/{db}/layouts
GET /fmi/data/v1/databases/{db}/layouts/{layout}
GET /fmi/data/v1/databases/{db}/scripts
Authorization: Bearer {token}
```
Doc: https://help.claris.com/en/data-api-guide/content/get-metadata.html

---

## Scripts
```
GET /fmi/data/v1/databases/{db}/layouts/{layout}/script/{scriptName}
Authorization: Bearer {token}
```
Also: pass `script` and `scriptParam` query params on find/get requests.  
Doc: https://help.claris.com/en/data-api-guide/content/run-filemaker-scripts.html

---

## Global fields
```
PATCH /fmi/data/v1/databases/{db}/globals
Authorization: Bearer {token}
Content-Type: application/json
Body: { "globalFields": { "TableName::FieldName": "value" } }
```
Doc: https://help.claris.com/en/data-api-guide/content/set-global-field-values.html

---

## Upload container data
```
POST /fmi/data/v1/databases/{db}/layouts/{layout}/records/{recordId}/containers/{fieldName}/1
Authorization: Bearer {token}
Content-Type: multipart/form-data
Body: file upload
```
Doc: https://help.claris.com/en/data-api-guide/content/upload-container-data.html

---

## HTTP Headers summary
| Header | When used |
|--------|-----------|
| `Content-Type: application/json` | POST/PATCH with JSON body |
| `Content-Type: multipart/form-data` | Container upload |
| `Authorization: Bearer {token}` | All authenticated calls |
| `Authorization: Basic {b64}` | Login only |
| `Authorization: FMID {token}` | FileMaker Cloud login |

---

## Key notes
- CORS is **not** supported — Data API must be called server-side
- Sessions expire after 15 minutes of inactivity
- Maximum concurrent sessions: configurable in Admin Console
- JSON responses always include `{ "response": {...}, "messages": [{"code":"0","message":"OK"}] }`
- Error code `0` = success; any non-zero = error

For full error codes: https://help.claris.com/en/data-api-guide/content/error-responses.html

---

# Claris Help Centre — Complete Sitemap Reference

Source: https://help.claris.com/en/claris-help-center/content/index.html  
Last verified: 2026-06

---

## Hub Page
```
https://help.claris.com/en/claris-help-center/content/index.html
```

---

## FileMaker Pro Help
**Guide slug:** `pro-help`  
**Index:** https://help.claris.com/en/pro-help/content/index.html

### Top-level chapters
| Topic | URL |
|-------|-----|
| New features | `.../new-features.html` |
| FileMaker Pro basics | `.../basics.html` |
| Using Help | `.../using-help.html` |
| About FileMaker Pro custom apps | `.../solutions.html` |
| About FileMaker Pro modes | `.../modes.html` |
| Using the status toolbar | `.../status-toolbar.html` |
| Opening and managing files | `.../opening-managing-files.html` |
| Adding and viewing data | `.../adding-viewing-data.html` |
| Finding records | `.../finding-records.html` |
| Find requests | `.../find-request.html` |
| Sorting records | `.../sorting-records.html` |
| Previewing and printing | `.../previewing-printing.html` |
| Creating a custom app | `.../creating-a-custom-app.html` |
| Creating a FileMaker Pro file | `.../creating-files.html` |
| Working with related tables | `.../related-tables-files.html` |
| Creating and managing layouts and reports | `.../layouts-and-reports.html` |
| Editing objects, layout parts, background | `.../editing-objects-parts-background.html` |
| Creating charts from data | `.../creating-charts.html` |
| Automating tasks with scripts | `.../scripts.html` |
| Creating and editing scripts | `.../creating-editing-scripts.html` |
| Managing security | `.../protecting-databases.html` |
| Sharing files on a network | `.../sharing-files.html` |
| Saving, importing, and exporting data | `.../saving-importing-exporting-data.html` |
| Importing data into a file | `.../importing-data-into-file.html` |
| Publishing databases on the web | `.../publishing-databases-web.html` |
| Using ODBC and JDBC | `.../odbc-jdbc.html` |
| Accessing external data sources | `.../external-data-sources.html` |
| Using advanced tools | `.../using-advanced.html` |

### Reference sections
| Topic | URL |
|-------|-----|
| Functions reference (all functions) | `.../functions-reference.html` |
| Script steps reference | `.../script-steps-reference.html` |
| FileMaker error codes | `.../error-codes.html` |

**Base URL for all:** `https://help.claris.com/en/pro-help/content/`

---

## FileMaker Server Help
**Guide slug:** `server-help`  
**Index:** https://help.claris.com/en/server-help/content/index.html

### Top-level pages (note: uses short relative slugs)
| Topic | URL |
|-------|-----|
| About FileMaker Server | `.../about-server.html` |
| New features | `.../about-whats-new.html` |
| Testing FileMaker Server | `.../deploy-fm-server-test.html` |
| Checking the status (dashboard) | `.../dashboard.html` |
| Uninstall FileMaker Server | `.../deploy-uninstall.html` |
| Starting Admin Console | `.../start-admin-console.html` |
| Hosting databases | `.../hostdb.html` |
| Hosting websites | `.../hostsite.html` |
| Starting or stopping FMS components | `.../start-stop-fms.html` |
| Administering databases | `.../admin-databases.html` |
| Administering clients | `.../admin-clients.html` |
| Understanding backup options | `.../config-backup-about.html` |
| Scheduling database backups | `.../schedule-db-backup.html` |
| Server information settings | `.../config-general-settings.html` |
| Startup settings | `.../config-general-autostart.html` |
| FileMaker client session timeouts | `.../config-client-timeouts.html` |
| FileMaker HTTPS tunneling | `.../config-https-tunneling.html` |
| Scripting maximum threads limit | `.../config-max-sase.html` |
| Filter databases setting | `.../config-client-filter-databases.html` |
| Database and backup folders | `.../config-dbserver-folders.html` |
| Scheduling administrative tasks | `.../schedule-admin-tasks.html` |
| Saving and loading schedules | `.../settings-save-load.html` |
| Notifications settings | `.../config-notifications.html` |
| Securing your data | `.../security.html` |
| Monitoring FileMaker Server | `.../monitor-server.html` |
| Web publishing settings | `.../config-web-publishing.html` |
| PHP and XML web publishing settings | `.../config-webpub-php.html` |
| FileMaker WebDirect settings | `.../config-webpub-webdirect.html` |
| FileMaker Data API settings | `.../config-webpub-fmdapi.html` |
| OData API settings | `.../config-webpub-fm-odata-api.html` |
| Managing plug-ins | `.../plugins-manage.html` |
| Using ODBC and JDBC with Server | `.../xdbc-about.html` |
| Configuring AI services | `.../config-ai-services.html` |
| License settings | `.../license-settings.html` |
| Administrator settings | `.../administrator-settings.html` |
| Restrict access | `.../restrict-access.html` |
| Administrator roles | `.../administrator-roles.html` |
| External authentication settings | `.../config-auth-settings.html` |
| Troubleshooting | `.../trouble.html` |

**Base URL for all:** `https://help.claris.com/en/server-help/content/`

---

## FileMaker Data API Guide
**Guide slug:** `data-api-guide`  
**Index:** https://help.claris.com/en/data-api-guide/content/index.html

| Topic | URL |
|-------|-----|
| Introduction | `.../index.html` |
| How a Data API call is processed | `.../how-data-api-call-is-processed.html` |
| Web integration alternatives | `.../web-integration-alternatives.html` |
| Prepare databases for Data API access | `.../prepare-databases-for-access.html` |
| Design the Data API solution | `.../design-app.html` |
| Write FileMaker Data API calls | `.../write-data-api-calls.html` |
| Connect to or disconnect from a database | `.../connect-disconnect-database.html` |
| Log in to a database session | `.../log-in-database-session.html` |
| Log in to an external data source | `.../log-in-external-data-source.html` |
| Log in using OAuth | `.../log-in-database-session-oauth.html` |
| Log in using Claris ID (Cloud) | `.../log-in-database-session-claris-id.html` |
| Log out of a database session | `.../log-out-database-session.html` |
| Validate a database session | `.../validate-database-session.html` |
| Get metadata | `.../get-metadata.html` |
| Work with records | `.../work-with-records.html` |
| Create a record | `.../create-record.html` |
| Edit a record | `.../edit-record.html` |
| Duplicate a record | `.../duplicate-record.html` |
| Delete a record | `.../delete-record.html` |
| Get a single record | `.../get-single-record.html` |
| Get a range of records | `.../get-range-of-records.html` |
| Upload container data | `.../upload-container-data.html` |
| Perform a find request | `.../perform-find-request.html` |
| Set global field values | `.../set-global-field-values.html` |
| Run FileMaker scripts | `.../run-filemaker-scripts.html` |
| Run a script | `.../run-a-script.html` |
| Error responses | `.../error-responses.html` |
| Host a Data API solution | `.../host-data-api-app.html` |
| Test the Data API solution | `.../test-data-api-app.html` |
| Monitor Data API solutions | `.../monitor-data-api-app.html` |

**Base URL for all:** `https://help.claris.com/en/data-api-guide/content/`

---

## FileMaker Admin API Guide
**Guide slug:** `admin-api-guide`  
**Index:** https://help.claris.com/en/admin-api-guide/content/index.html

**Base URL:** `https://help.claris.com/en/admin-api-guide/content/`

---

## FileMaker OData API Guide
**Guide slug:** `odata-guide`  
**Index:** https://help.claris.com/en/odata-guide/content/index.html

**Base URL:** `https://help.claris.com/en/odata-guide/content/`

---

## FileMaker SQL Reference
**Guide slug:** `sql-reference`  
**Index:** https://help.claris.com/en/sql-reference/content/index.html

| Topic | URL |
|-------|-----|
| Introduction | `.../index.html` |
| Using a FileMaker Pro database as a data source | `.../using-filemaker-pro-database-as-data-source.html` |
| Using the ExecuteSQL function | `.../using-executesql-function.html` |
| SQL statements | `.../sql-statements.html` |
| SQL clauses | `.../sql-clauses.html` |
| SQL expressions | `.../sql-expressions.html` |
| SQL functions | `.../sql-functions.html` |
| FileMaker system objects | `.../filemaker-system-objects.html` |
| FileMaker SQL error codes | `.../filemaker-sql-error-codes.html` |
| Reserved SQL keywords | `.../reserved-sql-keywords.html` |

**Base URL for all:** `https://help.claris.com/en/sql-reference/content/`

---

## FileMaker Security Guide
**Guide slug:** `security-guide`  
**Index:** https://help.claris.com/en/security-guide/content/index.html

**Base URL:** `https://help.claris.com/en/security-guide/content/`

---

## FileMaker WebDirect Guide
**Guide slug:** `webdirect-guide`  
**Index:** https://help.claris.com/en/webdirect-guide/content/index.html

**Base URL:** `https://help.claris.com/en/webdirect-guide/content/`

---

## FileMaker Server Installation and Configuration Guide
**Guide slug:** `server-installation-configuration-guide`  
**Index:** https://help.claris.com/en/server-installation-configuration-guide/content/index.html

**Base URL:** `https://help.claris.com/en/server-installation-configuration-guide/content/`

---

## FileMaker Pro Installation Guide
**Guide slug:** `pro-installation-guide`  
**Index:** https://help.claris.com/en/pro-installation-guide/content/index.html

---

## FileMaker Cloud Help
**Guide slug:** `cloud-help`  
**Index:** https://help.claris.com/en/cloud-help/content/index.html

---

## FileMaker Cloud Getting Started Guide
**Guide slug:** `cloud-getting-started-guide`  
**Index:** https://help.claris.com/en/cloud-getting-started-guide/content/index.html

---

## Claris Customer Console Help
**Guide slug:** `customer-console-help`  
**Index:** https://help.claris.com/en/customer-console-help/content/index.html

---

## FileMaker Go Release Notes
**Guide slug:** `go-release-notes`  
**Index:** https://help.claris.com/en/go-release-notes/content/index.html

---

## FileMaker Go Help
**Guide slug:** `go-help`  
**Index:** https://help.claris.com/en/go-help/content/index.html

---

## FileMaker Go Development Guide
**Guide slug:** `go-development-guide`  
**Index:** https://help.claris.com/en/go-development-guide/content/index.html

---

## iOS App SDK Guide
**Guide slug:** `ios-app-sdk-guide`  
**Index:** https://help.claris.com/en/ios-app-sdk-guide/content/index.html

---

## Claris Connect Release Notes
**Guide slug:** `connect-release-notes`  
**Index:** https://help.claris.com/en/connect-release-notes/content/index.html

---

## Claris Connect Help
**Guide slug:** `connect-help`  
**Index:** https://help.claris.com/en/connect-help/content/index.html

---

## Claris Connect Reference
**Guide slug:** `connect-reference`  
**Index:** https://help.claris.com/en/connect-reference/content/index.html

---

## Claris Studio Help
**Guide slug:** `studio-help`  
**Index:** https://help.claris.com/en/studio-help/content/index.html

| Topic | URL |
|-------|-----|
| What's new | `.../whats-new.html` |
| Index | `.../index.html` |

---

## Claris MCP Help (AI Workspace)
**Guide slug:** `claris-mcp-help`  
**Index:** https://help.claris.com/en/claris-mcp-help/content/index.html

---

## FileMaker Data Migration Tool Guide
**Guide slug:** `data-migration-tool-guide`  
**Index:** https://help.claris.com/en/data-migration-tool-guide/content/index.html

---

## FileMaker Developer Tool Guide
**Guide slug:** `developer-tool-guide`  
**Index:** https://help.claris.com/en/developer-tool-guide/content/index.html

---

## FileMaker Upgrade Tool Guide
**Guide slug:** `app-upgrade-tool-guide`  
**Index:** https://help.claris.com/en/app-upgrade-tool-guide/content/index.html

---

## FileMaker Pro Release Notes
**Guide slug:** `pro-release-notes`  
**Index:** https://help.claris.com/en/pro-release-notes/content/index.html

---

## FileMaker Server Release Notes
**Guide slug:** `server-release-notes`  
**Index:** https://help.claris.com/en/server-release-notes/content/index.html

---

## FileMaker Cloud Release Notes
**Guide slug:** `cloud-release-notes`  
**Index:** https://help.claris.com/en/cloud-release-notes/content/index.html

---

## FileMaker Pro SVG Grammar for Button Icons
**Guide slug:** `pro-svg-grammar-for-button-icons`  
**Index:** https://help.claris.com/en/pro-svg-grammar-for-button-icons/content/index.html

---

## FileMaker Pro Network Install Setup Guide
**Guide slug:** `pro-network-install-setup-guide`  
**Index:** https://help.claris.com/en/pro-network-install-setup-guide/content/index.html

---

## FileMaker Server Network Install Setup Guide
**Guide slug:** `server-network-install-setup-guide`  
**Index:** https://help.claris.com/en/server-network-install-setup-guide/content/index.html

---

## Claris Connect for Apple School Manager User Guide
**Guide slug:** `connect-apple-school-manager-guide`  
**Index:** https://help.claris.com/en/connect-apple-school-manager-guide/content/index.html

---

## Documentation Archive
```
https://help.claris.com/en/claris-help-center/content/archive.html
```
Append `?fmp` (Pro), `?fms` (Server), `?fmc` (Cloud), `?fmg` (Go), `?cc` (Connect), `?cs` (Studio) for filtered views.

---

## PDF/Binary Docs (not HTML guides)
- FileMaker ODBC and JDBC Guide: https://help.claris.com/en/odbc-jdbc-guide.pdf
- FileMaker Server Custom Web Publishing Guide: https://help.claris.com/en/server-custom-web-publishing-guide.pdf
- Apple Remote Desktop Deployment Script: https://www.claris.com/resources/documentation/docs/fmp_osx_deployment.zip
