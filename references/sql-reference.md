# FileMaker SQL / ExecuteSQL — Quick Reference

## Contents
  - Two modes of use
  - ExecuteSQL syntax
  - Supported SQL: SELECT statement
  - Data types in FileMaker SQL
  - Date / Time literals
  - Key SQL functions (FileMaker subset)
  - JOINs
  - Special FileMaker SQL objects
  - CREATE TABLE / ALTER TABLE (ODBC/JDBC and OData — not ExecuteSQL)
  - Common gotchas
  - Reserved keywords
  - Full reference

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
Supported: INNER JOIN, LEFT OUTER JOIN. **Not** supported: RIGHT OUTER JOIN, FULL OUTER JOIN.  
Note: Use **table occurrence names** exactly as they appear in the Relationships Graph.

---

## Special FileMaker SQL objects

FileMaker adds **system columns** to every row of every table. They are usable in `ExecuteSQL`
as well as from ODBC/JDBC.

| Object | SQL name | Equivalent function |
|--------|----------|---------------------|
| Record ID | `ROWID` | `Get(RecordID)` |
| Modification count | `ROWMODID` | `Get(RecordModificationCount)` |

```sql
SELECT ROWID, ROWMODID FROM MyTable WHERE ROWMODID > 3
```

**Corrected 2026-07-25:** earlier versions of this file listed these as `RECORDID` and `MODID`.
Those names appear nowhere in the Claris SQL reference and do not work — use `ROWID` and
`ROWMODID`. Verified against
`https://help.claris.com/markdown/en/sql-reference/filemaker-system-columns.md`.

**FM 26 changes:** `ROWID` and `ROWMODID` may now be written double-quoted (`"ROWID"`), and both
are available as named constants.

See also FileMaker **system tables** —
`https://help.claris.com/markdown/en/sql-reference/filemaker-system-tables.md`

---

## CREATE TABLE / ALTER TABLE (ODBC/JDBC and OData — not ExecuteSQL)

`table_element_list` format:

```
field_name field_type [[repetitions]]
[DEFAULT expr] [UNIQUE | NOT NULL | PRIMARY KEY | GLOBAL]
[FOREIGN KEY REFERENCES table_name(column_name)]
[EXTERNAL relative_path_string [SECURE | OPEN calc_path_string] [FEWER_FOLDERS]]
```

**FM 26 addition:** `FOREIGN KEY` syntax is supported in both `CREATE TABLE` and `ALTER TABLE`.

Table and field names have a 100-character limit and must begin with an alphabetic character;
otherwise enclose them in double quotes (quoted identifier).

```sql
CREATE TABLE "_EMPLOYEE" (ID INT PRIMARY KEY, "_FIRSTNAME" VARCHAR(20), "_LASTNAME" VARCHAR(20))
```

---

## Common gotchas
- Field names with spaces must be quoted: `"First Name"`
- Table names must match the **table occurrence** name (not the underlying table name)
- ExecuteSQL returns text; use `GetAsNumber()` etc. to convert
- NULL handling: use `IS NULL` / `IS NOT NULL`
- Subqueries are supported (`IN ( SELECT … )`, `EXISTS`, `= ANY`, `> ALL`)
- No INSERT / UPDATE / DELETE in ExecuteSQL (ODBC/JDBC and OData only)
- `RIGHT OUTER JOIN` and `FULL OUTER JOIN` are not supported

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
