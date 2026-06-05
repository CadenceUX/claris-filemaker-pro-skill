# Logical, JSON & AI Functions — Examples

---

# FileMaker Logical Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/logical-functions.html  
All 20 logical functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** Logical functions control flow, evaluate expressions, access field contents dynamically, and bridge scripting with calculations. `Let` and `While` are the two most powerful — master these first.

---

## Case ( test1 ; result1 {; test2 ; result2 ; … ; defaultResult} )
Evaluates tests in order and returns the result paired with the first true test. Returns `defaultResult` (or empty) if no test is true.  
Parameters: alternating test/result pairs; optional trailing `defaultResult` with no paired test.  
Returns: any type (matches the result expressions)

```
Case (
  Score ≥ 90 ; "A" ;
  Score ≥ 80 ; "B" ;
  Score ≥ 70 ; "C" ;
  "F"
)
```

Multiple conditions in one test:
```
Case (
  Status = "Active" and Balance > 0 ; "Overdue" ;
  Status = "Active"                  ; "Current" ;
  Status = "Closed"                  ; "Archived" ;
  "Unknown"
)
```

Nested Case for complex routing (keep flat where possible):
```
Case (
  Type = "Invoice" ; Case ( Paid = 1 ; "Paid" ; "Unpaid" ) ;
  Type = "Quote"   ; "Pending" ;
  "Other"
)
```

---

## Choose ( test ; result0 {; result1 ; result2…} )
Returns the result at position `test` (0-based). Returns empty if `test` is out of range or negative.  
Parameters: `test` — integer index; `result0…resultN` — return values.  
Returns: any type

```
Choose ( DayOfWeek ( Get(CurrentDate) ) - 1 ;
  "Sunday" ; "Monday" ; "Tuesday" ; "Wednesday" ;
  "Thursday" ; "Friday" ; "Saturday"
)
```

Map a status code to a label:
```
Choose ( StatusCode ; "New" ; "Active" ; "On Hold" ; "Closed" )
// StatusCode 0→New, 1→Active, 2→On Hold, 3→Closed
```

---

## Evaluate ( expression {; [field1 ; field2 ;…]} )
Evaluates `expression` (a text string) as a FileMaker calculation at runtime. The optional field list tells FileMaker to recalculate when those fields change.  
Parameters: `expression` — text containing a valid FileMaker calculation; optional field dependency list.  
Returns: any type (result of the evaluated expression)

```
Evaluate ( "Get ( CurrentDate )" )
// → today's date, evaluated at runtime
```

Dynamic field reference:
```
Evaluate ( "Table::" & $fieldName )
// accesses a field whose name is in $fieldName at runtime
```

Combine with Let for safe dynamic evaluation:
```
Let ( expr = "Round ( " & Table::Rate & " * " & Table::Units & " ; 2 )" ;
  Evaluate ( expr )
)
```

⚠️ Performance: avoid in auto-enter or unstored calcs on large tables — Evaluate recalculates every time any referenced field changes.

---

## EvaluationError ( expression )
Returns the FileMaker error code that would result from evaluating `expression`, or 0 if no error.  
Parameters: `expression` — text (same as Evaluate).  
Returns: number (error code)

```
EvaluationError ( "Table::" & $fieldName )
// → 0 if field exists, non-zero if it doesn't
```

Guard before using Evaluate:
```
Let ( expr = "Table::" & $fieldName ;
  If ( EvaluationError ( expr ) = 0 ;
    Evaluate ( expr ) ;
    "Field not found"
  )
)
```

---

## ExecuteSQL ( sqlQuery ; fieldSeparator ; rowSeparator {; arguments…} )
Runs a SQL SELECT statement against a table occurrence and returns results as text. Field and row separators define the output format.  
Parameters: `sqlQuery` — SQL text; `fieldSeparator` — separator between fields (e.g. `","` or `¶`); `rowSeparator` — separator between rows; `arguments` — optional `?` parameter substitution values.  
Returns: text (or `"?"` on error)

```
ExecuteSQL ( "SELECT FirstName, LastName FROM Contacts WHERE Active = 1" ; "," ; "¶" )
```

Parameterised query (prevents injection, handles data types correctly):
```
ExecuteSQL (
  "SELECT InvoiceNum, Total FROM Invoices WHERE CustomerID = ? AND Status = ?" ;
  "," ; "¶" ;
  Customers::CustomerID ; "Open"
)
```

Aggregate:
```
ExecuteSQL ( "SELECT SUM(Total) FROM Invoices WHERE CustomerID = ?" ; "" ; "" ; Customers::ID )
```

⚠️ Important notes:
- Field names in SQL must match **base table** field names (not table occurrence names)
- No relationship-driven finds — all data must be in the query
- Returns `"?"` on any error; wrap with `If ( result = "?" ; … )` or use `ExecuteSQLe`
- Date/time literals use ODBC format: `DATE 'YYYY-MM-DD'`, `TIME 'HH:MM:SS'`
- Use `?` parameters instead of concatenating values — handles quoting automatically

---

## ExecuteSQLe ( sqlQuery ; fieldSeparator ; rowSeparator {; arguments…} )
Identical to `ExecuteSQL` but returns a descriptive error message string instead of `"?"` on failure.  
Returns: text (results or error message)

```
Let ( result = ExecuteSQLe ( "SELECT Name FROM Contacts WHERE ID = ?" ; "" ; "" ; $id ) ;
  If ( Left ( result ; 5 ) = "ERROR" ;
    "Query failed: " & result ;
    result
  )
)
```

---

## GetAsBoolean ( data )
Returns 1 if `data` is non-zero/non-empty, 0 otherwise. Converts any data type to a boolean.  
Returns: number (0 or 1)

```
GetAsBoolean ( 0 )        // → 0
GetAsBoolean ( 42 )       // → 1
GetAsBoolean ( "" )       // → 0
GetAsBoolean ( "false" )  // → 1  (any non-empty text is truthy)
GetAsBoolean ( 0.00 )     // → 0
```

Safe checkbox test:
```
If ( GetAsBoolean ( Contacts::Newsletter ) ; "Subscribed" ; "Not subscribed" )
```

---

## GetField ( fieldName )
Returns the contents of the field named by the text expression `fieldName`. Field name must be fully qualified: `"TableOccurrence::FieldName"`.  
Returns: any type (field contents)

```
GetField ( "Contacts::Email" )
// Same as Contacts::Email, but the name is a string
```

Dynamic field access (combine with a variable):
```
GetField ( "Contacts::" & $columnName )
```

⚠️ Unlike `Evaluate`, `GetField` accepts only a field reference — not a full expression.

---

## GetNthRecord ( field ; recordNumber )
Returns the value of `field` in record number `recordNumber` of the current found set.  
Parameters: `field` — a field reference; `recordNumber` — integer position (1-based).  
Returns: any type

```
GetNthRecord ( Contacts::FullName ; 1 )
// → name from the first record in the found set
```

Loop through found set without navigating:
```
Let ( [
  total = Get ( FoundCount ) ;
  i     = Get ( RecordNumber )
] ;
  List (
    GetNthRecord ( Invoices::Total ; i - 1 ) ;  // previous record's total
    Invoices::Total                              // current
  )
)
```

---

## GetSummary ( summaryField ; breakField )
Returns the value of a summary field for the current sort group. `breakField` must be the field the records are currently sorted by.  
Parameters: `summaryField` — a summary field; `breakField` — the sort break field.  
Returns: number/text (summary result for the current group)

```
GetSummary ( Invoices::TotalSummary ; Invoices::CustomerID )
// → sum of TotalSummary for the current CustomerID group (when sorted by CustomerID)
```

Sub-summary percentage:
```
GetSummary ( Sales::GroupTotal ; Sales::Region ) / GetSummary ( Sales::GrandTotal ; Sales::Region ) * 100
```

---

## If ( test ; resultIfTrue {; resultIfFalse} )
Returns `resultIfTrue` if `test` is non-zero/non-empty, otherwise `resultIfFalse` (or empty).  
Parameters: `test` — boolean expression; `resultIfTrue`; optional `resultIfFalse`.  
Returns: any type

```
If ( Balance > 0 ; "Overdue" ; "Paid" )
```

Nested If (prefer `Case` for more than 2 branches):
```
If ( Score ≥ 90 ; "Excellent" ; If ( Score ≥ 70 ; "Pass" ; "Fail" ) )
```

Guard against division by zero:
```
If ( Denominator ≠ 0 ; Numerator / Denominator ; 0 )
```

---

## IsEmpty ( field )
Returns 1 if `field` is empty (null, zero-length text, or 0 for numbers depending on field type); 0 otherwise.  
Returns: number (0 or 1)

```
IsEmpty ( Contacts::Email )   // → 1 if no email entered
```

Require field before saving:
```
If ( IsEmpty ( Orders::CustomerID ) ; "Customer required" ; "OK" )
```

---

## IsValid ( field )
Returns 0 if `field` contains an invalid value for its data type (e.g. text in a date field); 1 if valid or empty.  
Returns: number (0 or 1)

```
IsValid ( Contacts::BirthDate )  // → 0 if "not a date" was entered
```

Validate before calculation:
```
If ( IsValid ( Events::StartDate ) and IsValid ( Events::EndDate ) ;
  Events::EndDate - Events::StartDate ;
  "Invalid dates"
)
```

---

## IsValidExpression ( expression )
Returns 1 if `expression` is a syntactically valid FileMaker calculation; 0 if not.  
Parameters: `expression` — text.  
Returns: number (0 or 1)

```
IsValidExpression ( "1 + 1" )        // → 1
IsValidExpression ( "1 + " )         // → 0 (incomplete expression)
IsValidExpression ( "GetField ( " )  // → 0
```

Validate user-entered formula before Evaluate:
```
If ( IsValidExpression ( $userFormula ) ;
  Evaluate ( $userFormula ) ;
  "Invalid formula"
)
```

---

## Let ( [var1 = expr1 ; var2 = expr2 ; …] ; result )
Declares local variables within the calculation, then evaluates `result` using those variables. Variables only exist for the duration of the Let expression.  
Parameters: variable assignment list (use `[]`); `result` expression.  
Returns: any type (result of the final expression)

```
Let ( tax = Price * TaxRate ;
  Price + tax
)
```

Multiple variables (use square brackets for readability):
```
Let ( [
  subtotal = Quantity * UnitPrice ;
  discount = If ( Quantity > 10 ; subtotal * 0.1 ; 0 ) ;
  tax      = ( subtotal - discount ) * TaxRate
] ;
  subtotal - discount + tax
)
```

Recursive Let (self-referencing via custom function — Let itself is not recursive):
```
Let ( [
  parts    = Substitute ( FullName ; " " ; ¶ ) ;
  lastName = RightValues ( parts ; 1 )
] ;
  Trim ( lastName )
)
```

---

## Lookup ( sourceField {; failExpression} )
Returns the value of `sourceField` from a related record via a relationship. If no related record is found, returns `failExpression` (or empty).  
Parameters: `sourceField` — a field in a related table occurrence; `failExpression` — optional fallback value.  
Returns: any type

```
Lookup ( Products::Price ; 0 )
// → Price from the related Products record, or 0 if none found
```

---

## LookupNext ( sourceField ; lower/higher )
Returns the next lower or higher value from `sourceField` in the related table when no exact match exists.  
Parameters: `sourceField` — related field; `lower` or `higher` keyword.  
Returns: any type

```
LookupNext ( PriceBreaks::Price ; lower )
// → the price for the next lower quantity break when exact match not found
```

---

## Self
Returns the current contents of the object that contains the calculation. Used in field validation, button scripts, and conditional formatting to refer to the field or object being evaluated without naming it explicitly.  
Returns: any type (current object's value)

```
// In a field validation calc for an Email field:
If ( IsEmpty ( Self ) or PatternCount ( Self ; "@" ) > 0 ; 1 ; 0 )
// → validates that the field is empty OR contains "@"
```

```
// In a conditional format calc (highlight negative numbers):
Self < 0
```

---

## SetRecursion ( expression ; maxIterations )
Sets the maximum number of recursion iterations for a custom function or `While` expression. Default is 10,000; maximum is 10,000,000.  
Parameters: `expression` — a recursive expression; `maxIterations` — integer.  
Returns: any type (result of expression)

```
SetRecursion ( MyRecursiveCustomFunction ( data ) ; 500000 )
```

---

## While ( [initialVars] ; condition ; [logicVars] ; result )
Repeats `logicVars` while `condition` is true, then returns `result`. Replaces recursive custom functions for most iteration patterns.  
Parameters: `[initialVars]` — initial variable assignments; `condition` — loop test; `[logicVars]` — variables updated each iteration; `result` — expression to return after loop ends.  
Returns: any type

Sum values in a return-delimited list:
```
While (
  [list = "10¶20¶30¶40" ; i = 1 ; total = 0] ;
  i ≤ ValueCount ( list ) ;
  [total = total + GetValue ( list ; i ) ; i = i + 1] ;
  total
)
// → 100
```

Build a list of squares:
```
While (
  [i = 1 ; output = ""] ;
  i ≤ 5 ;
  [output = output & i^2 & ¶ ; i = i + 1] ;
  Left ( output ; Length ( output ) - 1 )
)
// → "1¶4¶9¶16¶25"
```

Find first value in list matching a condition:
```
While (
  [list = valueList ; i = 1 ; found = ""] ;
  i ≤ ValueCount ( list ) and IsEmpty ( found ) ;
  [v = GetValue ( list ; i ) ; found = If ( Left ( v ; 1 ) = "A" ; v ; "" ) ; i = i + 1] ;
  found
)
```

---

## Common patterns

**Null-safe division:**
```
Let ( d = Denominator ; If ( d = 0 ; 0 ; Numerator / d ) )
```

**Safe JSON extraction with fallback:**
```
Let ( val = JSONGetElement ( data ; "status" ) ;
  If ( IsEmpty ( val ) ; "unknown" ; val )
)
```

**Multi-step calculation with Let:**
```
Let ( [
  days     = Get(CurrentDate) - StartDate ;
  rate     = Lookup ( Rates::DailyRate ; 0 ) ;
  subtotal = days * rate ;
  gst      = subtotal * 0.1
] ;
  subtotal + gst
)
```

**While for CSV parsing:**
```
While (
  [csv = rawCSV ; i = 1 ; result = ""] ;
  i ≤ ValueCount ( Substitute ( csv ; "," ; ¶ ) ) ;
  [
    val    = Trim ( GetValue ( Substitute ( csv ; "," ; ¶ ) ; i ) ) ;
    result = List ( result ; val ) ;
    i      = i + 1
  ] ;
  result
)
```

---

# FileMaker JSON Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/json-functions-category.html  
All 10 native JSON functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** FileMaker's JSON functions provide full read/write access to JSON structures. `JSONGetElement` and `JSONSetElement` do the heavy lifting; `JSONListKeys`/`JSONListValues` are essential for iteration; `JSONParse`/`JSONParsedState` (added later) cache parsed JSON in memory for performance.

**JSON type constants** (used as the `type` parameter in JSONSetElement and returned by JSONGetElementType):
| Constant | Value | Meaning |
|---|---|---|
| `JSONString` | 1 | String (quoted) |
| `JSONNumber` | 2 | Number |
| `JSONObject` | 3 | Object `{}` |
| `JSONArray` | 4 | Array `[]` |
| `JSONBoolean` | 5 | `true` or `false` |
| `JSONNull` | 6 | `null` |
| `JSONRaw` | 7 | Raw (unquoted) — inserts value as-is |

---

## JSONDeleteElement ( json ; keyOrIndex )
Deletes an element from a JSON object or array by key name, index, or dot-notation path.  
Parameters: `json` — JSON text; `keyOrIndex` — key name string, 0-based array index, or dot-notation path.  
Returns: text (modified JSON)

```
JSONDeleteElement ( "{\"a\":1,\"b\":2,\"c\":3}" ; "b" )
// → {"a":1,"c":3}
```

Delete by array index:
```
JSONDeleteElement ( "[10,20,30,40]" ; 2 )
// → [10,20,40]  (removes 30 at index 2)
```

Delete nested key:
```
JSONDeleteElement ( myJSON ; "address.city" )
```

---

## JSONFormatElements ( json )
Formats JSON text with indentation and line breaks for human readability. Does not change the data — only whitespace.  
Parameters: `json` — any valid JSON text.  
Returns: text (pretty-printed JSON)

```
JSONFormatElements ( "{\"name\":\"Alice\",\"age\":30}" )
```
→
```json
{
	"name" : "Alice",
	"age" : 30
}
```

Use in a Show Custom Dialog for debugging:
```
Show Custom Dialog [ JSONFormatElements ( $apiResponse ) ]
```

---

## JSONGetElement ( json ; keyOrIndex )
Extracts a single value, object, or array from JSON by key, index, or dot-notation path. Returns empty if the key doesn't exist.  
Parameters: `json` — JSON text; `keyOrIndex` — key name, 0-based index number, or dot-notation path.  
Returns: text (the element value, unquoted if string)

```
JSONGetElement ( "{\"name\":\"Alice\",\"age\":30}" ; "name" )
// → Alice

JSONGetElement ( "[10,20,30]" ; 1 )
// → 20  (index 1)
```

Dot-notation path (nested):
```
JSONGetElement ( data ; "address.city" )
// → "Melbourne" from {"address":{"city":"Melbourne"}}
```

Bracket notation for arrays inside objects:
```
JSONGetElement ( data ; "items[0].name" )
// → first item's name
```

Extract a sub-object (returns as JSON string):
```
JSONGetElement ( data ; "address" )
// → {"city":"Melbourne","postcode":"3000"}
```

---

## JSONGetElementType ( json ; keyOrIndex )
Returns the JSON data type of an element as a number constant.  
Parameters: same as JSONGetElement.  
Returns: number (1=String, 2=Number, 3=Object, 4=Array, 5=Boolean, 6=Null, 0=does not exist)

```
JSONGetElementType ( "{\"active\":true}" ; "active" )
// → 5  (JSONBoolean)

JSONGetElementType ( "{\"score\":42}" ; "score" )
// → 2  (JSONNumber)

JSONGetElementType ( "{\"name\":\"Alice\"}" ; "missing" )
// → 0  (does not exist)
```

Type-safe extraction pattern:
```
Let ( [
  t   = JSONGetElementType ( $json ; "startDate" ) ;
  val = JSONGetElement ( $json ; "startDate" )
] ;
  Case (
    t = 0 ; ""         ;  // missing
    t = 6 ; ""         ;  // null
    GetAsDate ( val )
  )
)
```

---

## JSONListKeys ( json ; keyOrIndex )
Returns a return-delimited list of keys (object) or indexes (array) at the specified path.  
Parameters: `json` — JSON text; `keyOrIndex` — path to the object/array (use `""` for top level).  
Returns: text (return-delimited list)

Top-level keys of an object:
```
JSONListKeys ( "{\"a\":1,\"b\":2,\"c\":3}" ; "" )
// → a¶b¶c
```

Array indexes (returns 0, 1, 2…):
```
JSONListKeys ( "[\"x\",\"y\",\"z\"]" ; "" )
// → 0¶1¶2
```

Keys of a nested object:
```
JSONListKeys ( data ; "address" )
// → city¶postcode¶state
```

Count fields in a JSON object:
```
ValueCount ( JSONListKeys ( $json ; "" ) )
```

Iterate all keys with While:
```
While (
  [keys = JSONListKeys ( $json ; "" ) ; i = 1 ; output = ""] ;
  i ≤ ValueCount ( keys ) ;
  [
    k      = GetValue ( keys ; i ) ;
    v      = JSONGetElement ( $json ; k ) ;
    output = output & k & ": " & v & ¶ ;
    i      = i + 1
  ] ;
  Trim ( output )
)
```

---

## JSONListValues ( json ; keyOrIndex )
Returns a return-delimited list of values at the specified path (object or array).  
Parameters: same as JSONListKeys.  
Returns: text (return-delimited list of values)

Object values:
```
JSONListValues ( "{\"a\":1,\"b\":2,\"c\":3}" ; "" )
// → 1¶2¶3
```

Array values:
```
JSONListValues ( "[\"Alice\",\"Bob\",\"Carol\"]" ; "" )
// → Alice¶Bob¶Carol
```

---

## JSONMakeArray ( valueList ; separator ; type )
Converts a delimited list into a JSON array. Handles quoting and encoding.  
Parameters: `valueList` — delimited text; `separator` — delimiter character (e.g. `","` or `¶`); `type` — JSON type constant for elements.  
Returns: text (JSON array)

From a return-delimited list:
```
JSONMakeArray ( "Alice¶Bob¶Carol" ; ¶ ; JSONString )
// → ["Alice","Bob","Carol"]
```

Number array from comma-delimited:
```
JSONMakeArray ( "10,20,30" ; "," ; JSONNumber )
// → [10,20,30]
```

Build array from a field:
```
JSONMakeArray ( Contacts::Tags ; "," ; JSONString )
```

Used with GetTableDDL:
```
GetTableDDL ( JSONMakeArray ( "Orders,Customers,Products" ; "," ; JSONString ) ; True )
```

---

## JSONParse ( json ; parseName )
Parses and caches a JSON structure in memory under `parseName`. Subsequent calls using the same name avoid re-parsing — significant performance improvement for large JSON accessed many times.  
Parameters: `json` — JSON text; `parseName` — text name for the cached parse.  
Returns: number (0 = success, non-zero = error)

```
Let ( parseResult = JSONParse ( $largeJSON ; "myData" ) ;
  If ( parseResult = 0 ;
    JSONGetElement ( "myData" ; "records[0].name" ) ;
    "Parse failed: " & parseResult
  )
)
```

Parse once, read many times in a loop:
```
// Parse once
Set Variable [ $err ; Value: JSONParse ( Data::JSONField ; "inventory" ) ]
// Then use "inventory" as the json parameter in JSONGetElement calls
While (
  [keys = JSONListKeys ( "inventory" ; "items" ) ; i = 0 ; out = ""] ;
  i < ValueCount ( keys ) ;
  [
    name = JSONGetElement ( "inventory" ; "items[" & i & "].name" ) ;
    qty  = JSONGetElement ( "inventory" ; "items[" & i & "].qty" ) ;
    out  = out & name & " × " & qty & ¶ ;
    i    = i + 1
  ] ;
  Trim ( out )
)
```

---

## JSONParsedState ( parseName )
Returns the current parse state of a named cached JSON structure.  
Parameters: `parseName` — name used in a prior JSONParse call.  
Returns: number (0 = not parsed, 1 = parsed and available, -1 = parse error)

```
JSONParsedState ( "myData" )
// → 1 if JSONParse("myData") succeeded and is still in cache
// → 0 if not yet parsed or cache was cleared
// → -1 if parse failed
```

Guard pattern:
```
If ( JSONParsedState ( "inventory" ) ≠ 1 ;
  Set Variable [ $$parseErr ; Value: JSONParse ( Data::JSONField ; "inventory" ) ]
)
// Now safe to use "inventory" in JSONGetElement
```

---

## JSONSetElement ( json ; keyOrIndex ; value ; type )
Adds or modifies an element in a JSON structure. Creates nested objects/arrays if they don't exist. Pass multiple key/value/type triples to set several elements at once.  
Parameters: `json` — JSON text (or `""` to start new); `keyOrIndex` — key/path; `value` — new value; `type` — JSON type constant.  
Returns: text (modified JSON)

Set a key on a new object:
```
JSONSetElement ( "{}" ; "name" ; "Alice" ; JSONString )
// → {"name":"Alice"}
```

Set multiple keys at once:
```
JSONSetElement ( "{}" ;
  ["name" ; "Alice" ; JSONString] ;
  ["age"  ; 30      ; JSONNumber] ;
  ["active" ; True  ; JSONBoolean]
)
// → {"name":"Alice","age":30,"active":true}
```

Nested key (creates intermediate objects):
```
JSONSetElement ( "{}" ; "address.city" ; "Melbourne" ; JSONString )
// → {"address":{"city":"Melbourne"}}
```

Append to an array by using array length as index:
```
Let ( [
  arr = "[1,2,3]" ;
  len = ValueCount ( JSONListKeys ( arr ; "" ) )
] ;
  JSONSetElement ( arr ; len ; 4 ; JSONNumber )
)
// → [1,2,3,4]
```

Build a JSON payload for Insert From URL:
```
Let ( [
  payload = JSONSetElement ( "{}" ;
    ["model"       ; "gpt-4o"     ; JSONString] ;
    ["temperature" ; 0.7          ; JSONNumber] ;
    ["max_tokens"  ; 1000         ; JSONNumber]
  )
] ;
  payload
)
```

---

## Common patterns

**Safe get with default:**
```
Let ( val = JSONGetElement ( $json ; "status" ) ;
  If ( IsEmpty ( val ) ; "unknown" ; val )
)
```

**Build request body for Insert From URL:**
```
Set Variable [ $body ; Value:
  JSONSetElement ( "{}" ;
    ["query" ; $searchText ; JSONString] ;
    ["limit" ; 10          ; JSONNumber] ;
    ["filters.active" ; True ; JSONBoolean]
  )
]
Insert From URL [
  Select ; No dialog ; $result ;
  "https://api.example.com/search" ;
  "-X POST -H \"Content-Type: application/json\" -d " & Quote ( $body )
]
```

**Iterate a JSON array with While:**
```
While (
  [
    arr   = JSONGetElement ( $response ; "results" ) ;
    count = ValueCount ( JSONListKeys ( arr ; "" ) ) ;
    i     = 0 ;
    names = ""
  ] ;
  i < count ;
  [
    names = List ( names ; JSONGetElement ( arr ; "[" & i & "].name" ) ) ;
    i     = i + 1
  ] ;
  names
)
```

**Parse API response defensively:**
```
Let ( [
  raw    = $apiResponse ;
  errTyp = JSONGetElementType ( raw ; "error" ) ;
  data   = JSONGetElement ( raw ; "data" )
] ;
  If ( errTyp ≠ 0 ;
    "Error: " & JSONGetElement ( raw ; "error.message" ) ;
    data
  )
)
```

**Convert FileMaker value list to JSON array for an API:**
```
JSONMakeArray ( ValueListItems ( Get(FileName) ; "Status Values" ) ; ¶ ; JSONString )
// → ["New","Active","On Hold","Closed"]
```

---

# FileMaker AI Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/artificial-intelligence-functions.html  
All 14 native AI functions with verified format, parameters, version introduced, and usage patterns.
Last verified: 2026-06 against live Claris Help Centre.

**Prerequisites:** All LLM functions require an AI account configured in the current file via the `Configure AI Account` script step. Functions that take `account` and `model` parameters call out to the external provider (OpenAI, Anthropic, or a custom OpenAI-compatible endpoint such as the FileMaker Server AI Model Server).

**Core ML functions** (`ComputeModel`, `GetModelAttributes`, `PredictFromModel`) require a model loaded first via `Configure Machine Learning Model` or `Configure Regression Model`. Core ML functions are supported only on iOS, iPadOS, and macOS.

**Error codes relevant to AI functions:**
- `877` — Can't find AI account (no account configured for the given name)
- `882` — Invalid AI request (e.g. unsupported image type or file too large for image embedding)

---

## AddEmbeddings ( v1 ; v2 )
Adds two embedding vectors and returns the result as a normalised vector.  
Parameters: `v1`, `v2` — text (JSON arrays) or container data containing embedding vectors with the same dimensions.  
Returns: text or container (matches input format)  
*Originated: 22.0*

Returns `"?"` if vectors have different dimensions or the result is a zero vector (can't normalise zero).  
Both vectors must come from the same model.

```
AddEmbeddings ( "[1, 2, 3]" ; "[4, 5, 6]" )
```
→ `[0.40160966..., 0.56225353..., 0.72289739...]` (normalised sum [5,7,9])

Combine concepts for broader semantic search:
```
Set Variable [ $Combined ; Value: AddEmbeddings ( Concepts::Smartphone_Embedding ; Concepts::Premium_Embedding ) ]
# Use $Combined with Perform Semantic Find to find "premium smartphone" records
```

King − Man + Woman ≈ Queen analogy:
```
Set Variable [ $KingMinusMan ; Value: SubtractEmbeddings ( Concepts::King_Embedding ; Concepts::Man_Embedding ) ]
Set Variable [ $QueenAnalogy ; Value: AddEmbeddings ( $KingMinusMan ; Concepts::Woman_Embedding ) ]
CosineSimilarity ( $QueenAnalogy ; Concepts::Queen_Embedding )  // close to 1 if analogy holds
```

---

## ComputeModel ( modelName ; parameterName1 ; value1 )
Evaluates a Core ML model and returns a JSON object containing the prediction result.  
For general models: `ComputeModel ( modelName ; parameterName1 ; value1 )`  
For vision models: `ComputeModel ( modelName ; "image" ; value1 { ; "confidenceLowerLimit" ; returnAtLeastOne } )`  
Parameters: `modelName` — name of a previously loaded model; `parameterName1` / `value1` — input parameter name/value pairs as defined by the model; `confidenceLowerLimit` (vision, optional) — 0.0–1.0 to exclude low-confidence results; `returnAtLeastOne` (vision) — 1 to return the top result even if all are below the limit.  
Returns: text (JSON)  
*Originated: 19.0*  
*Supported: iOS, iPadOS, macOS only*

Must first load model with `Configure Machine Learning Model` script step.

```
ComputeModel ( "MobileNet" ; "image" ; myImageField )
```
→ JSON array of classifications with confidence scores, e.g.:
```json
[{"classification": "grand piano, grand", "confidence": 0.998}, ...]
```

With confidence filter (returns top result even if nothing beats 1.0):
```
ComputeModel ( "MobileNet" ; "image" ; myImageField ; "confidenceLowerLimit" ; 1.0 ; "returnAtLeastOne" ; 1 )
```

---

## CosineSimilarity ( v1 ; v2 )
Returns the semantic similarity between two embedding vectors as a number from -1 (opposite) to 1 (identical/similar), with 0 meaning no relationship.  
Parameters: `v1`, `v2` — text (JSON arrays) or container fields containing normalised embedding vectors from the **same** model with the same dimensions.  
Returns: number  
*Originated: 21.0*

```
CosineSimilarity ( InputEmbedding ; StoredEmbedding )
```
→ e.g. `0.90848158767415143622` for highly similar texts

Check similarity between user input and a stored note:
```
Configure AI Account [ Account Name: "my-account" ; Model Provider: OpenAI ; API key: "sk-..." ]
Show Custom Dialog [ "Enter search text:" ; $Input ]
Set Variable [ $InputEmb ; Value: GetEmbedding ( "my-account" ; "text-embedding-3-small" ; $Input ) ]
Set Variable [ $NoteEmb  ; Value: GetEmbedding ( "my-account" ; "text-embedding-3-small" ; Meetings::Note ) ]
Show Custom Dialog [ "Similarity:" ; CosineSimilarity ( $InputEmb ; $NoteEmb ) ]
```

---

## GetEmbedding ( account ; model ; input )
Sends `input` to an embedding model and returns the vector representation as **binary container data**.  
Parameters: `account` — AI account name (text); `model` — embedding model name (text); `input` — text or container (supports image embedding via FileMaker Server AI Model Server).  
Returns: container  
*Originated: 21.0*

Binary container format is more compact than text and improves downstream performance.

```
Set Field [ Meetings::Note_Embedding ;
  GetEmbedding ( "my-account" ; "text-embedding-3-small" ; Meetings::Note ) ]
```

Image embedding (FileMaker Server AI Model Server):
```
Set Field [ Products::Image_Embedding ;
  GetEmbedding ( "my-account" ; "clip-vit-base-patch32" ; Products::ProductImage ) ]
```

---

## GetEmbeddingAsFile ( text { ; fileNameWithExtension } )
Converts an embedding vector from **text (JSON array) format to binary container data**.  
Parameters: `text` — JSON array of embedding values; `fileNameWithExtension` (optional) — filename for the container, e.g. `"embedding.fve"`.  
Returns: container  
*Originated: 21.0*

```
Set Field [ Meetings::Note_Embedding ;
  GetEmbeddingAsFile ( Meetings::Note_Embedding_JSON ; "embedding_from_FileMaker.fve" ) ]
```

---

## GetEmbeddingAsText ( data )
Converts an embedding vector from **binary container data to text (JSON array) format**.  
Parameters: `data` — container field or variable holding binary embedding data.  
Returns: text (JSON array)  
*Originated: 21.0*

```
GetEmbeddingAsText ( Meetings::Note_Embedding )
```
→ `[-0.06650865, 0.0034368848, 0.051363964, ...]`

---

## GetFieldsOnLayout ( layoutName )
Returns a JSON object describing fields on the specified layout that are accessible to a find. Pass `""` for the current layout.  
Parameters: `layoutName` — text (use `""` for current layout).  
Returns: text (JSON)  
*Originated: 22.0*

Excludes: fields outside the layout area, hidden fields with "Apply in Find mode", fields with Find Mode entry disabled, fields excluded from Quick Find, fields with no read access, and summary/global/container fields.

If any field comment starts with `[LLM]`, only fields tagged `[LLM]` include a description (prefix stripped from output).

```
GetFieldsOnLayout ( "Products" )
```
→ JSON object:
```json
{
  "layout_name": "Products",
  "fields": {
    "Products::ProductName": {"type": "string", "description": "Descriptive name of the product"},
    "Products::Price":       {"type": "number", "description": "Price of the product in USD"},
    "Products::Status":      {"type": "string"}
  }
}
```

Current layout:
```
GetFieldsOnLayout ( "" )
```

Compare all layout fields vs find-accessible fields:
```
Let ( [
  all   = SortValues ( FieldNames ( Get(FileName) ; Get(LayoutName) ) ; 1 ) ;
  find  = SortValues ( JSONListKeys ( GetFieldsOnLayout ( Get(LayoutName) ) ; "fields" ) ; 1 )
] ;
  "All fields:¶" & all & "¶Find-accessible:¶" & find
)
```

---

## GetModelAttributes ( modelName )
Returns metadata in JSON format about a named Core ML model that is currently loaded.  
Parameters: `modelName` — text name of a model loaded via `Configure Machine Learning Model`.  
Returns: text (JSON)  
*Originated: 19.3.1*  
*Supported: iOS, iPadOS, macOS only*

```
Configure Machine Learning Model [ Operation: Vision ; Name: "TestModel" ; From: Table::ModelContainerField ]
Set Variable [ $attrs ; Value: JSONFormatElements ( GetModelAttributes ( "TestModel" ) ) ]
Show Custom Dialog [ $attrs ]
```

Returned JSON includes: `APIVers`, `configuration` (computeUnits), `modelDescription` (classLabels, inputDescriptions, metadata, outputDescriptions), `modelName`.

Check if a model's first input has a sizeRange key:
```
Let ( [
  attrs     = GetModelAttributes ( "TestModel" ) ;
  firstInput = "modelDescription.inputDescriptions.[0]" ;
  keys      = JSONListKeys ( attrs ; firstInput )
] ;
  If ( PatternCount ( keys ; "sizeRange" ) > 0 ; 1 ; 0 )
)
```

---

## GetRAGSpaceInfo ( ragAccountName { ; spaceID } )
Returns information about a specific RAG space or all RAG spaces for the given RAG account.  
Parameters: `ragAccountName` — name of a RAG account configured via `Configure RAG Account` script step; `spaceID` (optional) — ID of a specific RAG space.  
Returns: text (JSON)  
*Originated: 22.0*

Returns error message `[RAG Space] error. Reason: RAG space {space_id} not found` if the space doesn't exist. Returns `"?"` if the RAG account is invalid.

All spaces for an account:
```
GetRAGSpaceInfo ( "customer-support-rag-account" )
```
→ `{"rag_space_list": [{"space_id": "knowledge-base", "model": "multi-qa-MiniLM-L6-cos-v1"}, ...]}`

Specific space:
```
GetRAGSpaceInfo ( "customer-support-rag-account" ; "knowledge-base" )
```
→ JSON with `rag_space_id`, `model`, `entries`, and `values` array (PDF filenames and text chunks).

Verify space exists before use:
```
Set Variable [ $info ; Value: GetRAGSpaceInfo ( "my-rag-account" ; "knowledge-base" ) ]
If [ PatternCount ( $info ; "[RAG Space] error" ) > 0 or $info = "?" ]
  Show Custom Dialog [ "RAG space not found." ]
Else
  // proceed
End If
```

---

## GetTableDDL ( tableOccurrenceNames ; ignoreError )
Returns table schema in DDL (SQL CREATE TABLE) format for the specified table occurrences. Used to supply schema context to an LLM for natural-language SQL generation.  
Parameters: `tableOccurrenceNames` — JSON array of table occurrence name strings; `ignoreError` — `True` to return DDL for tables that succeed (skip errors), `False` to return `"?"` if any table causes an error (and log to AI call log).  
Returns: text (DDL SQL)  
*Originated: 21.0*

```
GetTableDDL ( "[\"Invoices\", \"LineItems\", \"Customers\"]" ; True )
```
→ SQL CREATE TABLE statements for each occurrence with field names, types, comments, and foreign key relationships.

Using `JSONMakeArray` to build the input cleanly:
```
Set Variable [ $DDL ; Value:
  GetTableDDL ( JSONMakeArray ( "Orders,Customers,Products" ; "," ; JSONString ) ; False ) ]
If [ $DDL = "?" ]
  Show Custom Dialog [ "Schema error — check AI call log." ]
End If
```

---

## GetTokenCount ( text )
Returns the approximate token count for `text`. Use for guidance only; actual counts charged by models may vary.  
Parameters: `text` — any text expression or field.  
Returns: number  
*Originated: 21.0*

```
GetTokenCount ( "Claris FileMaker" )  // → 4
```

Pre-flight check before embedding:
```
If [ GetTokenCount ( Meetings::Note ) > 1024 ]
  Show Custom Dialog [ "Note is too long to embed. Please shorten it." ]
Else
  Insert Embedding [ Account Name: "my-account" ; Embedding Model: "text-embedding-3-small" ;
    Source Field: Meetings::Note ; Target Field: Meetings::Note_Embedding ]
End If
```

---

## NormalizeEmbedding ( data { ; dimension } )
Normalises an embedding vector. If `dimension` is specified, truncates to that many dimensions first, then normalises — returning a shorter vector.  
Parameters: `data` — text (JSON array) or container field; `dimension` (optional) — number of dimensions to use (truncates result to this size).  
Returns: text or container (matches input format)  
*Originated: 22.0*

**Note:** Most embedding models return already-normalised vectors — calling this on them is a no-op. Use when working with models that don't normalise, or when you want Matryoshka/MRL dimension reduction.

Full normalisation:
```
NormalizeEmbedding ( "[3, 4]" )
```
→ `[0.6, 0.8]` (magnitude scaled to 1: √(3²+4²)=5, so [3/5, 4/5])

Truncate to 256 dimensions and normalise (Matryoshka reduction):
```
NormalizeEmbedding ( Table::EmbeddingData ; 256 )
```
→ new vector with only the first 256 dimensions, normalised.

---

## PredictFromModel ( modelName ; v1 )
Returns the predicted value from a trained **regression** model for the given input features.  
Parameters: `modelName` — name of a model loaded via `Configure Regression Model`; `v1` — JSON array of features or binary container embedding vector.  
Returns: number  
*Originated: 22.0*

Must first train and load a model with `Configure Regression Model`. Input features must match the same structure and dimensionality as training data. Returns `"?"` if the model isn't loaded or dimensions don't match.

Simple prediction with numeric features (house price):
```
PredictFromModel ( "HousePriceModel" ; "[1600, 3, 20]" )
```
→ e.g. `256.96` (1600 sq ft, 3 bedrooms, 20 years old)

Predict from text embedding (review rating):
```
Show Custom Dialog [ "Enter Your Review:" ; $reviewInput ]
Configure AI Account [ Account Name: "AI_Model_Server" ; Model Provider: Custom ;
  Endpoint: "https://myserver.example.com:8080/" ; API key: Global::API_Key ]
Insert Embedding [ Account Name: "AI_Model_Server" ; Embedding Model: "all-MiniLM-L12-v2" ;
  Input: $reviewInput ; Target: $reviewEmbedding ]
Configure Regression Model [ Action: Load Model ; Model Name: "ReviewModel" ;
  Load Model From: Reviews::ReviewModel ]
Show Custom Dialog [ "Predicted Rating:" ; PredictFromModel ( "ReviewModel" ; $reviewEmbedding ) ]
Configure Regression Model [ Action: Unload Model ; Model Name: "ReviewModel" ]
```

---

## SubtractEmbeddings ( v1 ; v2 )
Subtracts embedding vector `v2` from `v1` and returns the result as a normalised vector.  
Parameters: `v1`, `v2` — text (JSON arrays) or container data containing embedding vectors with the same dimensions from the same model.  
Returns: text or container (matches input format)  
*Originated: 22.0*

Returns `"?"` if vectors have different dimensions or the result is a zero vector (v1 and v2 are identical).

```
SubtractEmbeddings ( "[1, 2, 3]" ; "[4, 5, 6]" )
```
→ `[-0.577..., -0.577..., -0.577...]` (normalised [-3,-3,-3])

Remove a concept from a search vector:
```
SubtractEmbeddings ( Concepts::Winter_Embedding ; Concepts::Cold_Embedding )
// → vector for "winter" with "cold" removed; useful for finding non-weather winter content
```

---

## Common patterns

**Semantic search pipeline (full):**
```
# 1. Store embeddings when records are created/updated
Set Field [ Table::Embedding ; GetEmbedding ( "acct" ; "text-embedding-3-small" ; Table::Content ) ]

# 2. At search time
Configure AI Account [ Account Name: "acct" ; Model Provider: OpenAI ; API key: "sk-..." ]
Show Custom Dialog [ "Search:" ; $Query ]
Set Variable [ $QueryEmb ; Value: GetEmbedding ( "acct" ; "text-embedding-3-small" ; $Query ) ]

# 3. Perform Semantic Find (script step, not a function)
Perform Semantic Find [ Table::Embedding ; Query Embedding: $QueryEmb ; Top K: 10 ]
```

**Passing schema to a model for natural-language SQL:**
```
Set Variable [ $Schema ; Value: GetTableDDL ( "[\"Orders\",\"Customers\"]" ; True ) ]
# Include $Schema in your Perform SQL Query by Natural Language prompt
```

**LLM-tagged field comments for GetFieldsOnLayout:**  
In Manage Database, prefix field comments with `[LLM]` to control exactly which fields and descriptions are exposed to the model. Only tagged fields get descriptions; untagged fields appear with type only; the `[LLM]` prefix is stripped in output.
