# FileMaker OData API — Reference

Verified against the live `odata-guide` (57 pages) on **2026-07-25**, FileMaker 26.

FileMaker supports OData at the **intermediate conformance level**, with documented exceptions
(see *Not supported* below). OData needs **no layouts** — it addresses tables directly, unlike
the FileMaker Data API.

---

## Choosing between OData and the Data API

| | OData | FileMaker Data API |
|---|---|---|
| Access model | Tables directly — **no layout required** | Through **layouts**; portals available |
| Best when | Interoperating with other OData sources; transactions needed; replacing ODBC/JDBC | You want FileMaker concepts — layouts, portals |
| Batch / transactions | **Yes** — `$batch`, atomic operation sets | No |
| Schema create/modify/delete | **Yes** | No |
| Client software | None needed | None needed |

Both require a hosted file on FileMaker Server or FileMaker Cloud.

---

## Terminology mapping

| OData term | FileMaker term |
|---|---|
| entity | record |
| entity set | table |
| property | field |
| entity container | a group of fields that isn't necessarily a record (e.g. database name and URL) |
| raw value | a binary value — a string of bytes rather than structured JSON/Atom |

---

## Base URL and authentication

```
https://<host>/fmi/odata/v4/<database-name>/<table-name>
```

`v4` is the OData version and is always `v4`. `<table-name>` accepts either the table name or
the FileMaker Table ID (FMTID).

| Host | Credentials |
|---|---|
| FileMaker Server | A FileMaker file account and password defined in the hosted database |
| FileMaker Cloud | Claris ID account and password |

Header (Server): `Authorization: Basic <base64 of account:password>` — standard HTTP Basic.
FileMaker Cloud additionally supports an OAuth sign-in flow for a database session.

Access must be enabled per file, and the file hosted for OData access.

---

## Query options

| Option | Purpose | Notes |
|---|---|---|
| `$filter` | Filter records by expression; only rows evaluating true are returned | ISO 8601 date/time/timestamp; offsets relative to the **server's** time zone. Quote field names containing spaces or underscores in double quotes. |
| `$select` | Return only named fields | |
| `$expand` | Include related records | `?$expand=Orders` |
| `$orderby` | Sort the result set | |
| `$top` / `$skip` | Page through results — take / omit N | Usable alone or together |
| `$count` | Return the number of records | |
| `$apply` | Aggregation and grouping transformations | |

Example: `/fmi/odata/v4/ContactMgmt/Contacts?$filter=Title eq 'Manager' or startswith(Title,'Admin')`

---

## Operations

| Task | Method | Path |
|---|---|---|
| Service document / database names | GET | `/fmi/odata/v4/` |
| Metadata (schema) | GET | `/fmi/odata/v4/<db>/$metadata` |
| List tables | GET | `/fmi/odata/v4/<db>/` |
| Read records | GET | `/fmi/odata/v4/<db>/<table>` |
| Read one record | GET | `/fmi/odata/v4/<db>/<table>(<id>)` |
| Create record | POST | `/fmi/odata/v4/<db>/<table>` |
| Update record | PATCH | `/fmi/odata/v4/<db>/<table>(<id>)` |
| Delete record | DELETE | `/fmi/odata/v4/<db>/<table>(<id>)` |
| Batch | POST | `/fmi/odata/v4/<db>/$batch` |
| Run a script | POST | `/fmi/odata/v4/<db>/Script.<scriptName>` |
| Create / alter / delete table, field, index | POST / PATCH / DELETE | schema endpoints |

**Schema modification** is an OData-only capability: create tables, add fields, create and
delete indexes, delete tables.

---

## Running scripts

POST to the `Script` system table followed by the script name.

- Body must be **completely empty** when the script takes no parameter.
- Otherwise the body contains a single field `scriptParameterValue` — accepts string, number,
  or JSON object.
- `Exit Script`'s text result is returned as `resultParameter`.

```json
{ "scriptResult": { "code": 0, "resultParameter": "Hello World" } }
```

Script names **cannot** contain special characters (`@`, `&`, `/`) or begin with a number.
Only scripts that run without user interaction are supported.

---

## Not supported

**OData intermediate-conformance features absent in FileMaker:**

- `$search` query option
- `lambda` operators `any` and `all`
- canonical functions `fractionalseconds()`, `isof()`, `geo.distance()`, `geo.length()`,
  `geo.intersects()`

**FileMaker features not available to standard OData calls:**

- Data in external ODBC data sources
- Calculation fields that depend on plug-ins, host file-system information
  (e.g. `Get(TemporaryPath)`), plug-in information, or script-trigger information
- Script trigger activation

**Workaround:** these *are* available inside scripts invoked by OData, because those run
server-side with the same semantics as `Perform Script on Server`. Put the logic in a script
and call it.

---

## Script step support

Per-step OData support is not tracked separately — the `Custom Web Publishing` (CWP) column in
`script-steps-catalog.json` covers the web-publishing context, and `DataAPI` covers the Data
API. Of the 216 script steps, **99 are unsupported and 26 partial** under `DataAPI`; **91
unsupported and 26 partial** under `CWP`. Read `platform_exceptions` on the individual step.

**FM 26 change:** `Export Field Contents` is now supported in FileMaker Server, Data API and
OData contexts.

---

## Error codes

OData and Data API share the REST error range **1700–1715** — see `quickrefs.md`. Error **953**
(*Exceeded limit on data the FileMaker Data API and OData can transmit*) indicates the response
payload is too large.

---

## When to fetch live

Fetch the guide when you need a full worked request/response body, webhook option detail,
container upload specifics, or exact `$apply` transformation syntax. Index:
`https://help.claris.com/markdown/en/odata-guide/index.md`
