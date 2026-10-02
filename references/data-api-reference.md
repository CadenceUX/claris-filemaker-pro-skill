# FileMaker Data API — Quick Reference

## Contents
  - Base URL
  - Authentication
  - Records
  - Find
  - Metadata
  - Scripts
  - Global fields
  - Upload container data
  - HTTP Headers summary
  - Key notes

Source: https://help.claris.com/en/data-api-guide/content/index.html  
Full detail: always fetch the live page for complete request/response examples.

---

## Base URL
```
https://{host}/fmi/data/v1/databases/{database-name}
```
Versions: `v1`, `v2` or `vLatest` (always the current version).

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
Pass the parameter as `?script.param=…` (one text string — pack several values as JSON).
Response: `{ "response": { "scriptError": "0", "scriptResult": "…" }, "messages": [ … ] }` — `scriptResult` is the Exit Script text result (absent if none); `scriptError` is the FileMaker error code.
With other requests the results come back as `scriptResult`, `scriptResult.prerequest`, `scriptResult.presort` (and matching `scriptError…`). Order: prerequest script → action → presort script → sort → `script`. On record and find requests you can also run scripts with `script` / `script.param`, `script.prerequest` / `script.prerequest.param`, and `script.presort` / `script.presort.param`.  
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
