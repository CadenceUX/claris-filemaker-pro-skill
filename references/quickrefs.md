# Quick References — Error Codes, SQL, Data API & Sitemap

---

# FileMaker Error Codes — Quick Reference

Source: https://help.claris.com/en/pro-help/content/error-codes.html  
Last verified: 2026-06 against live Claris Help Centre.

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

## 0 — Success
No error.

---

## System errors (1–99)

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 1 | User cancelled action | User pressed Escape/Cancel in a dialog |
| 2 | Memory error | Insufficient RAM |
| 3 | Command unavailable (wrong mode) | Step used in wrong mode (e.g. New Record in Find mode) |
| 4 | Command unknown | Step not supported on this platform |
| 5 | Command invalid (wrong context) | No record selected, or invalid context |
| 6 | File is read-only | File opened as read-only or on read-only media |
| 7 | Running out of memory | Low memory condition |
| 8 | Empty result | Find returned no records, or calculation returned empty |
| 9 | Insufficient privileges | Privilege set does not allow this action |
| 10 | Requested data is missing | Data or file not found |
| 11 | Name is not valid | Invalid field/table/object name |
| 12 | Name already exists | Duplicate name in schema |
| 13 | File or object is in use | File locked by another user/process |
| 14 | Out of range | Value or index out of valid range |
| 15 | Can't divide by zero | Division by zero |
| 16 | Operation failed; will retry | Transient failure |
| 17 | Foreign key violation | Referential integrity constraint (FM 17+) |
| 18 | Failed to import records | Import failed |
| 19 | Unexpected error | Unspecified error |
| 20 | Record already open | Record locked by current user |
| 21 | Data type mismatch | Wrong type passed to step/function |
| 26 | Record modified by another user | Optimistic locking conflict |

---

## File errors (100–199)

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 100 | File is missing | File not found at specified path |
| 101 | Record is missing | Record ID no longer exists |
| 102 | Field is missing | Field not found in table |
| 103 | Relationship is missing | Relationship definition deleted |
| 104 | Script is missing | Script not found |
| 105 | Layout is missing | Layout not found |
| 106 | Table is missing | Table not found |
| 107 | Index is missing | Field index missing (rebuild index) |
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

---

## Account/security errors (200–299)

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 200 | Record access denied | Privilege set restricts read |
| 201 | Field cannot be modified | Field is calculated or protected |
| 202 | Field access denied | Privilege set restricts field access |
| 203 | No records in file | Table is empty |
| 204 | No related records | No matching related records |
| 205 | Record already present | Unique constraint violation |
| 206 | Record modification in progress | Record committed by another |
| 207 | Transaction timed out | Server-side transaction expired |
| 208 | TOO_MANY_RECORDS | Found set exceeds limit |
| 212 | Password not valid | Wrong password |
| 213 | User account not valid | Account does not exist |
| 214 | Password does not meet requirements | Password too short/weak |
| 215 | Password has expired | Account password expired |
| 216 | Account is disabled | Account disabled by admin |
| 217 | Account already exists | Duplicate account name |
| 218 | Too many login attempts | Account locked after failed attempts |

---

## Import/export errors (400–499)

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 400 | Find criteria are empty | Find performed with no criteria |
| 401 | No records match find criteria | **Most common** — find returned zero records |
| 402 | Selected field is not a match field | Field used in find is not indexed/findable |
| 403 | Exceeds maximum record limit | Too many records for operation |
| 404 | Sort order is invalid | Sort references missing field |
| 405 | Number of records exceeds spelling checker limit | Too many records for spell check |
| 406 | Record import failed | Import failed for one record |
| 407 | Matching fields not found | Import field mapping failed |
| 408 | Field type does not match | Import type mismatch |
| 409 | Import order is invalid | Import mapping broken |
| 410 | Export order is invalid | Export mapping broken |
| 412 | Wrong file type for import | Unsupported file format |
| 413 | File encrypted | Cannot import encrypted file |
| 414 | Password mismatch | File password required for import |

---

## Printing/spelling errors (500–599)

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 500 | Date value does not meet validation criteria | Field validation failed (date) |
| 501 | Time value does not meet validation criteria | Field validation failed (time) |
| 502 | Number value does not meet validation criteria | Field validation failed (number) |
| 503 | Value in field is not within the range specified | Range validation failed |
| 504 | Value in field is not unique | Unique validation failed |
| 505 | Value in field is not an existing value | Existing value validation failed |
| 506 | Value in field is not a member of the value list specified | Value list validation failed |
| 507 | Value in field failed calculated value test | Calculation validation failed |
| 508 | Invalid value entered in Find mode | Find criteria invalid for field type |
| 509 | Field requires a valid value | Required field is empty |
| 510 | Related value is empty or unavailable | Related field has no value |
| 511 | Value in field exceeds maximum field size | Text too long for field |
| 512 | Record was already modified by another user | Conflict on commit |
| 513 | No validation was specified | No validation defined for field |

---

## Network errors (700–799)

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 700 | No network access | Network unavailable |
| 701 | Network connection failed | Timeout or dropped connection |
| 702 | No such host | DNS resolution failed |
| 703 | Unexpected data received | Server returned unexpected response |
| 704 | No permission to open file | Server refused connection |
| 706 | JPEG or PDF export failed | Cannot write output file |
| 707 | Graphics translator not found | Missing image library |
| 708 | Can't import that file type on this platform | Platform import restriction |
| 709 | Cannot save a runtime solution into itself | Dev tool restriction |
| 710 | File is already open | Can't open second copy |
| 711 | Cannot set file to single-user (users connected) | Guests still connected |
| 712 | User is not allowed to modify the password | Privilege restriction |
| 713 | Password does not match file's password | Wrong password |
| 714 | Password is too short | Minimum length not met |
| 715 | Passwords do not match | Confirm password differs |
| 716 | Must supply at least one uppercase letter | Password policy |
| 717 | Must supply at least one lowercase letter | Password policy |
| 718 | Must supply at least one numeric character | Password policy |
| 719 | Must supply at least one special character | Password policy |

---

## Insert From URL / HTTP errors (1630–1631)

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 1630 | Connection failed | Server unreachable, timeout |
| 1631 | Connection was refused | Server rejected connection (wrong port/IP) |

**Note:** HTTP status codes (404, 500 etc.) are NOT FileMaker error codes — they are returned in the response body/variable. Check the result text for `"HTTP/1.1 4"` or `"HTTP/1.1 5"` patterns.

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

**Note:** Codes 873, 874, 876 (old meanings), 878–881 from earlier FileMaker versions have been
reassigned or removed. Always reference the live error-codes page for the authoritative list.

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
