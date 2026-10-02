# Logical, JSON & AI Functions — Examples

## Contents
- Logical Functions
  - Case ( test1 ; result1 {; test2 ; result2 ; ... ; defaultResult } )
  - Choose ( test ; result0 {; result1 ; result2...} )
  - Evaluate ( expression {; [field1 ; field2 ;...]} )
  - EvaluationError ( expression )
  - ExecuteSQL ( sqlQuery ; fieldSeparator ; rowSeparator { ; arguments... } )
  - ExecuteSQLe ( sqlQuery ; fieldSeparator ; rowSeparator { ; arguments... } )
  - GetAsBoolean ( data )
  - GetField ( fieldName )
  - GetNthRecord ( field ; recordNumber )
  - GetSummary ( summaryField ; breakField )
  - If ( test ; result1 {; result2 } )
  - IsEmpty ( field )
  - IsValid ( field )
  - IsValidExpression ( expression )
  - Let ( {[} var1 = expression1 {; var2 = expression2...]} ; calculation )
  - Lookup ( sourceField {; failExpression } )
  - LookupNext ( sourceField ; lower/higherFlag )
  - Self
  - SetRecursion ( expression ; maxIterations )
  - While ( [ initialVariable ] ; condition ; [ logic ] ; result )
  - Common patterns
- JSON Functions
  - JSONDeleteElement ( json ; keyOrIndexOrPath )
  - JSONFormatElements ( json )
  - JSONGetElement ( json ; keyOrIndexOrPath )
  - JSONGetElementType ( json ; keyOrIndexOrPath )
  - JSONListKeys ( json ; keyOrIndexOrPath )
  - JSONListValues ( json ; keyOrIndexOrPath )
  - JSONMakeArray ( listOfValues ; separator ; type )
  - JSONParse ( json )
  - JSONParsedState ( json )
  - JSONSetElement ( json ; keyOrIndexOrPath ; value ; type )
  - Common patterns
- AI Functions
  - AddEmbeddings ( v1 ; v2 )
- Use $Combined with Perform Semantic Find to find "premium smartphone" records
  - ComputeModel ( modelName ; parameterName1 ; value1 )
  - CosineSimilarity ( v1 ; v2 )
  - GetEmbedding ( account ; model ; input )
  - GetEmbeddingAsFile ( text {; fileNameWithExtension } )
  - GetEmbeddingAsText ( data )
  - GetFieldsOnLayout ( layoutName )
  - GetModelAttributes ( modelName )
  - GetRAGSpaceInfo ( ragAccountName {; spaceID } )
  - GetTableDDL ( tableOccurrenceNames ; ignoreError )
  - GetTokenCount ( text )
  - NormalizeEmbedding ( data { ; dimension } )
  - PredictFromModel ( modelName ; v1 )
  - SubtractEmbeddings ( v1 ; v2 )
  - Common patterns
- 1. Configure the account first — every AI call needs it
- 2. Store embeddings (batch: Insert Embedding in Found Set)
- 3. At search time — the step embeds the query itself
- Perform SQL Query by Natural Language builds this DDL itself; use Data Tables: By DDL
- when you want to send a hand-edited schema instead.

---

# FileMaker Logical Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/logical-functions.html  
All 20 logical functions with verified syntax, parameters, return types, and usage patterns.  

**Overview:** Logical functions control flow, evaluate expressions, access field contents dynamically, and bridge scripting with calculations. `Let` and `While` are the two most powerful — master these first.

---

## Case ( test1 ; result1 {; test2 ; result2 ; ... ; defaultResult } )
Evaluates tests in order and returns the result paired with the first true test. Returns `defaultResult` (or empty) if no test is true.  
Parameters: alternating test/result pairs; optional trailing `defaultResult` with no paired test.  
Returns: any type (matches the result expressions)
```
Case ( Score >= 90 ; "Excellent" ; Score > 50 ; "Satisfactory" ; "Needs Improvement" )
// → `Excellent` when the score is 90 or above, `Satisfactory` when the score is between 50 and 90, and `Needs Improvement` for any other score
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

## Choose ( test ; result0 {; result1 ; result2...} )
Use Choose (not Case) to map a 0-based number to a result — `Case ( Get ( Device ) ; … )` treats the number as a true/false test.
Returns the result at position `test` (0-based). Returns empty if `test` is out of range or negative.  
Parameters: `test` — integer index; `result0…resultN` — return values.  
Returns: any type
```
Choose ( Rating ; "Not Applicable" ; "Good" ; "Fair" ; "Poor" )
```
Map a status code to a label:
```
Choose ( StatusCode ; "New" ; "Active" ; "On Hold" ; "Closed" )
// StatusCode 0→New, 1→Active, 2→On Hold, 3→Closed
```
---

## Evaluate ( expression {; [field1 ; field2 ;...]} )
Evaluates `expression` (a text string) as a FileMaker calculation at runtime. The optional field list tells FileMaker to recalculate when those fields change.  
Parameters: `expression` — text containing a valid FileMaker calculation; optional field dependency list.  
Returns: any type (result of the evaluated expression)
```
Evaluate(TextField)
// → `4 `when TextField contains 2 + 2

Evaluate("textfield")
// → `2 + 2` when textfield contains 2 + 2

Evaluate(GetField("textfield"))
// → `4` when textfield contains 2 + 2

Evaluate(TextField;[Amount])
// → `.80` when TextField contains .08 * Amount and the Amount field contains 10.00
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
⚠️ Server-side scripts: use English function names inside the Evaluate text — localised names aren't recognised there.

---

## EvaluationError ( expression )
Returns the error code from evaluating `expression`, or 0 if there's no error. To catch **syntax** errors in formula text, `EvaluationError` must enclose `Evaluate` — given a plain text string it just sees text and returns 0.  
Parameters: `expression` — any calculation expression.  
Returns: number (error code)
```
EvaluationError( GetField ( "total" ) + 1 )
// → `102` (Field Missing) when the field total has been deleted or renamed
```
Guard before using Evaluate (wrap `Evaluate`, not the text):
```
Let ( expr = "Table::" & $fieldName ;
  If ( EvaluationError ( Evaluate ( expr ) ) = 0 ;
    Evaluate ( expr ) ;
    "Field not found"
  )
)
```
```
EvaluationError ( Evaluate ( "1 +" ) )
// → 1204
```
---

## ExecuteSQL ( sqlQuery ; fieldSeparator ; rowSeparator { ; arguments... } )
Runs a SQL SELECT statement against a table occurrence and returns results as text. Field and row separators define the output format.  
Parameters: `sqlQuery` — SQL text; `fieldSeparator` — separator between fields (e.g. `","` or `¶`); `rowSeparator` — separator between rows; `arguments` — optional `?` parameter substitution values.  
Returns: text (or `"?"` on error)
```
ExecuteSQL ( "SELECT Department FROM Employees WHERE EmpID = 1"; ""; "" )
// → `Development` regardless of the current record, found set, or layout
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
- `FROM` and `JOIN` name **table occurrences** (as in the relationships graph), not base tables
- Ignores relationships defined in FileMaker — join explicitly in the query
- SELECT only: no INSERT, UPDATE, DELETE or schema changes
- Returns `"?"` on any error; wrap with `If ( result = "?" ; … )` or use `ExecuteSQLe`
- Date/time literals use ODBC format: `DATE 'YYYY-MM-DD'`, `TIME 'HH:MM:SS'`
- Use `?` parameters instead of concatenating values — handles quoting automatically

---

## ExecuteSQLe ( sqlQuery ; fieldSeparator ; rowSeparator { ; arguments... } )
Identical to `ExecuteSQL`, except that on failure it returns `?` followed by an error in the form `? ERROR: FQLnnnn/(line:offset): message`.  
Returns: text (results or error message)
```
ExecuteSQLe ( "SELECT Title FROM Employees WHERE EmpID = 1"; ""; "" )
// → ? ERROR: FQL0007/(1:7): The column named "Title" does not exist in any table in the column reference's scope.
```
Check with `Left ( $result ; 1 ) = "?"`.
---

## GetAsBoolean ( data )
Returns 1 if `data` converts to a **non-zero number**, or if a container holds data; otherwise 0. Text with no digits is 0 — it's not an "is not empty" test.  
Returns: number (0 or 1)
```
GetAsBoolean ( "" )
// → 0

GetAsBoolean ( "Some text here." )
// → 0

GetAsBoolean ( "5x" )
// → 1

GetAsBoolean ( Container Field )
// → `1` when the field named Container Field contains data, or returns `0` when Container Field is empty
```
Safe checkbox test:
```
If ( GetAsBoolean ( Contacts::Newsletter ) ; "Subscribed" ; "Not subscribed" )
```
---

## GetField ( fieldName )
Returns the contents of the field whose name `fieldName` evaluates to. An unqualified name resolves in the table the calculation is evaluated in; use `"TableOccurrence::FieldName"` for any other table.  
Returns: any type (field contents)
```
GetField ( "Phone" )
// → Customer::Phone when evaluated in the Customer table

GetField ( ContactMethod )
// → the contents of Phone or Email, whichever name ContactMethod holds
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
GetNthRecord(First Name;2)
// → the contents of the First Name field for record 2 in the current table
```
Compare with the previous record without navigating:
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
Returns the value of a summary field for the current sort group. The result is blank unless the found set is sorted by `breakField`. Pass the summary field as its own break field to get the grand summary.  
Parameters: `summaryField` — a summary field; `breakField` — the sort break field.  
Returns: number, date, time or timestamp. Calculations using it are unstored.
```
GetSummary(Total Sales;Country)
// → a summary of all records pertaining to the value in the Country field
```
Sub-summary percentage:
```
GetSummary ( Sales::Total ; Sales::Region ) / GetSummary ( Sales::Total ; Sales::Total ) * 100
// group total ÷ grand total (summary field used as its own break field)
```
---

## If ( test ; result1 {; result2 } )
Returns `resultIfTrue` if `test` evaluates to a non-zero number, otherwise `resultIfFalse` (or empty). Text with no digits counts as false: `If ( "abc" ; 1 ; 0 )` → `0`.  
Parameters: `test` — boolean expression; `resultIfTrue`; optional `resultIfFalse`.  
Returns: any type
```
If ( Country = "USA" ; "US Tech Support" ; "International Tech Support" )
// → `International Tech Support`, if the Country field contains France or Japan. Returns `US Tech Support` if the Country field contains USA
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
Returns 1 if `field` is empty — and also if the field, related table, relationship or file is missing, or another error occurs. Returns 0 otherwise; zero is not empty: `IsEmpty ( 0 )` → `0`. For a container, returns 0 when it holds a file.  
Returns: number (0 or 1)
```
IsEmpty ( OrderNum )
// → `1` if the OrderNum field is empty
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
IsValid(Datefield)
// → `0` if there is non-date data in Datefield, for example if text was imported into it
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
IsValidExpression(calculationField)
// → 1 (true) if calculationField contains total + 1; 0 if it contains abs(-1
```
Validate user-entered formula before Evaluate:
```
If ( IsValidExpression ( $userFormula ) ;
  Evaluate ( $userFormula ) ;
  "Invalid formula"
)
```
---

## Let ( {[} var1 = expression1 {; var2 = expression2...]} ; calculation )
Declares variables, then evaluates `result` using them. Plain names last for the calculation only; `$var` / `$$var` names set real local / global variables (a `$var` set outside a script is file-scoped until a script runs).  
Parameters: variable assignment list (use `[]`); `result` expression.  
Returns: any type (result of the final expression)
```
Let ( x = 5; x*x )
// → 25

Let ( [ x = 5; squared = x*x; cubed = squared*x ]; cubed )
// → 125
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
Last word of a name:
```
Let ( [
  parts    = Substitute ( FullName ; " " ; ¶ ) ;
  lastName = RightValues ( parts ; 1 )
] ;
  Trim ( lastName )
)
```
---

## Lookup ( sourceField {; failExpression } )
Returns the value of `sourceField` from a related record via a relationship. If no related record is found, returns `failExpression` (or empty).  
Parameters: `sourceField` — a field in a related table occurrence; `failExpression` — optional fallback value.  
Returns: any type
```
Lookup ( Products::Price ; 0 )
// → Price from the related Products record, or 0 if none found
```
---

## LookupNext ( sourceField ; lower/higherFlag )
Returns the next lower or higher value from `sourceField` in the related table when no exact match exists.  
Parameters: `sourceField` — related field; `lower` or `higher` keyword.  
Returns: any type
```
LookupNext ( PriceBreaks::Price ; lower )
// → the price for the next lower quantity break when exact match not found
```
---

## Self
Returns the content of the object the calculation is defined in. Usable only in conditional formatting, tooltips, placeholder text, **Hide object when**, the Accessibility **Title** and **Help** options, and field definition calculations (including auto-enter and validation). Not in scripts.  
Returns: text, number, date, time or timestamp
```
self > 10
// → `1` (True) when applied to a layout field object whose value is greater than 10
```
```
// In a conditional format calc (highlight negative numbers):
Self < 0
```
---

## SetRecursion ( expression ; maxIterations )
Sets the iteration limit for `While` loops and recursive custom functions inside `expression`. The default limit is **50,000**; past the limit the calculation returns `?`. Non-tail-recursive custom functions can also fail earlier when stack space runs out.  
Parameters: `expression` — any calculation; `maxIterations` — the new limit.  
Returns: any type (result of expression)
```
SetRecursion ( 
    While (  
        [ i = 0 ; out = "" ] ;
        i ≤ 10 ;  
        [ 
            i = i + 1 ; 
            out = out & $variable[ i ] & ¶ 
        ] ;
        out 
    ) ; 
5 )
// → ? (11 iterations exceeds the limit of 5)
```
Raise the limit above the default:
```
SetRecursion ( While ( i = 0 ; i < 100000 ; i = i + 1 ; i ) ; 200000 )
// → 100000   (without SetRecursion this returns ? — over 50,000 iterations)
```
---

## While ( [ initialVariable ] ; condition ; [ logic ] ; result )
Repeats `logicVars` while `condition` is true, then returns `result`. Replaces recursive custom functions for most iteration patterns. Limited to 50,000 iterations unless wrapped in `SetRecursion`.  
Parameters: `[initialVars]` — initial variable assignments; `condition` — loop test; `[logicVars]` — variables updated each iteration; `result` — expression to return after loop ends.  
Returns: any type

5 to the power of 3:
```
Let (
    [
        value = 5 ;
        power = 3
    ] ;
    While (
        [ result = value ; i = 1 ] ;
        i < power ;
        [ i = i + 1 ; result = result * value ] ;
        result
    )
)
// → 125
```
Build a list of squares:
```
While (
  [i = 1 ; output = ""] ;
  i ≤ 5 ;
  [output = output & i^2 & ¶ ; i = i + 1] ;
  Left ( output ; Length ( output ) - 1 )
)
// → 1¶4¶9¶16¶25
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
All 10 native JSON functions.

**Overview:** `JSONGetElement` and `JSONSetElement` do the heavy lifting; `JSONListKeys` / `JSONListValues` drive iteration; `JSONParse` / `JSONParsedState` (FM 22) avoid re-parsing large JSON.

**Paths** (`keyOrIndexOrPath`): key `"a"`, index `"[0]"`, dot path `"items[0].name"`, bracket path `"['a.b'][0]"` for keys containing dots, `"[:]"` for the last array element, and `"[+]"` (in JSONSetElement) for the position after the last element.

**Key order:** FileMaker sorts object keys alphabetically in the JSON it returns — don't rely on insertion order.

**JSON type constants** (the `type` parameter of JSONSetElement and JSONMakeArray; JSONGetElementType returns 1–6, never JSONRaw):
| Constant | Value | Meaning |
|---|---|---|
| `JSONString` | 1 | String (quoted) |
| `JSONNumber` | 2 | Number |
| `JSONObject` | 3 | Object `{}` |
| `JSONArray` | 4 | Array `[]` |
| `JSONBoolean` | 5 | `true` or `false` |
| `JSONNull` | 6 | `null` |
| `JSONRaw` | 0 | JSON element (or JSON string, if `value` is not valid JSON) — valid JSON is inserted as-is |

---

## JSONDeleteElement ( json ; keyOrIndexOrPath )
Deletes an element from a JSON object or array by key name, index, or dot-notation path.  
Parameters: `json` — JSON text; `keyOrIndexOrPath` — key, 0-based array index, or path.  
Returns: text (modified JSON)
```
JSONDeleteElement ( "{ \"a\" : 11 , \"b\" : 12 , \"c\" : 13 }" ; "b" )
// → {"a":11,"c":13}
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
Adds tabs and line breaks for readability **and sorts object keys alphabetically**. Returns `?` plus an error message if the JSON is invalid.  
Parameters: `json` — any JSON text.  
Returns: text (formatted JSON)
```
JSONFormatElements ( "{ \"a\" : { \"lnk\" : false, \"id\" : 12 } }" )
```
→
```
{
	"a" : 
	{
		"id" : 12,
		"lnk" : false
	}
}
```
Use in a Show Custom Dialog for debugging:
```
Show Custom Dialog [ JSONFormatElements ( $apiResponse ) ]
```
---

## JSONGetElement ( json ; keyOrIndexOrPath )
Extracts a value, object or array by key, index or path. Returns empty for a key that doesn't exist.  
Parameters: `json` — JSON text; `keyOrIndexOrPath` — key, 0-based index, or path.  
Returns: **number** for JSON numbers and Booleans (true → 1, false → 0); otherwise text (strings unquoted, objects and arrays as JSON).
```
JSONGetElement ( "{ \"a\" : 11, \"b\" : 22, \"c\" : 33 }" ; "b" )
// → `22` as a number
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

## JSONGetElementType ( json ; keyOrIndexOrPath )
Validates JSON and returns the type of an element. *Originated: 19.5*  
Parameters: same as JSONGetElement.  
Returns: number 1–6 (String, Number, Object, Array, Boolean, Null) when valid. A missing key or index, or invalid JSON, returns **text** starting with `?` — e.g. `? Incorrect key, index, or path` — never 0. JSONRaw is never returned.
```
(JSONGetElementType( "{ \"a\" : 11 }"; "" ) = JSONObject)
// → `1` (true) as a number

(JSONGetElementType( "{ a : 11 }"; "" ) = JSONObject)
// → `0` (false) as a number
```
```
JSONGetElementType ( "{ \"a\" : 11 , \"b\" : false }" ; "b" )
// → 5

JSONGetElementType ( "[100, 200]" ; "3" )
// → ? Incorrect key, index, or path
```
Type-safe extraction pattern (test for the error text, not 0):
```
Let ( [
  t   = JSONGetElementType ( $json ; "startDate" ) ;
  val = JSONGetElement ( $json ; "startDate" )
] ;
  Case (
    Left ( t ; 1 ) = "?" ; ""   ;  // missing key or invalid JSON
    t = JSONNull         ; ""   ;
    GetAsDate ( val )
  )
)
```
---

## JSONListKeys ( json ; keyOrIndexOrPath )
Returns a return-delimited list of keys (object) or indexes (array) at the specified path.  
Parameters: `json` — JSON text; `keyOrIndexOrPath` — path to the object or array (`""` for the top level).  
Object keys come back in alphabetical order.  
Returns: text (return-delimited list)

Top-level keys of an object:
```
JSONListKeys( "{ \"a\" : 11, \"b\" : 22, \"c\" : 33 }" ; "" )
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

## JSONListValues ( json ; keyOrIndexOrPath )
Returns a return-delimited list of values at the specified path (object or array).  
Parameters: same as JSONListKeys.  
Returns: text (return-delimited list of values)

Object values:
```
JSONListValues( "{ \"a\" : 11, \"b\" : 22, \"c\" : 33 }" ; "" )
// → 11¶22¶33
```
Array values:
```
JSONListValues ( "[\"Alice\",\"Bob\",\"Carol\"]" ; "" )
// → Alice¶Bob¶Carol
```
---

## JSONMakeArray ( listOfValues ; separator ; type )
Converts a list of separated values into a JSON array of one type. *Originated: 21.0*  
Parameters: `listOfValues` — the values; `separator` — text between values (`""` = any line separator); `type` — JSON type constant (JSONRaw inserts each valid JSON value as-is).  
Returns: text (JSON array)

```
JSONMakeArray ( "34,600,18,600,18.0" ; "," ; JSONNumber )
// → [34,600,18,600,18]
```
From a return-delimited field:
```
JSONMakeArray ( Product::Colors ; "" ; JSONString )
// → ["green","red","yellow"] when Colors holds green¶red¶yellow
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

## JSONParse ( json )
Parses `json` once and keeps the parsed (binary) form attached to the value. Store the result in a variable or pass it as a script parameter, and later JSON functions on that value skip re-parsing. *Originated: 22.0*  
Parameters: `json` — JSON text.  
Returns: text — the original JSON unchanged if valid; `?` followed by the parse error if not.
```
JSONParse ( "[3]" )
// → [3]
```
Parse once, read many times — the parsed form travels with the variable, not a name:
```
Set Variable [ $inventory ; Value: JSONParse ( Data::JSONField ) ]
Set Variable [ $count ; Value: ValueCount ( JSONListKeys ( $inventory ; "items" ) ) ]
Set Variable [ $first ; Value: JSONGetElement ( $inventory ; "items[0].name" ) ]
```
For a single lookup, calling JSONGetElement on the text directly performs about as well.  
**Insert from URL** (FM 26.0.1+) already parses an `application/json` response stored in a variable — no JSONParse needed after it.

---

## JSONParsedState ( json )
Reports whether `json` already carries a parsed representation, and whether it's valid. *Originated: 22.0*  
Parameters: `json` — a JSON value (usually a variable).  
Returns: number — `0` not parsed · `-1` parsed but invalid · `1`–`6` parsed and valid, the value's JSON type (same numbers as the JSONSetElement type constants).
```
JSONParsedState ( JSONParse ( "[3]" ) )
// → 4

JSONParsedState ( JSONParse ( "[3" ) )
// → -1

JSONParsedState ( "[3]" )
// → 0

JSONParsedState ( JSONSetElement ( "{}" ; "a" ; 1 ; JSONNumber ) )
// → 3
```
JSONSetElement's output is already parsed — no JSONParse needed after building JSON.

---

## JSONSetElement ( json ; keyOrIndexOrPath ; value ; type )
Adds or modifies an element. Creates nested objects and arrays as needed. Pass several `[ key ; value ; type ]` groups to set many elements at once. With `json` = `""` it starts a new object — or an array if the path starts with `[`.  
Parameters: `json` — JSON text; `keyOrIndexOrPath` — key or path (`"[+]"` appends to an array); `value` — the value; `type` — JSON type constant (table above). For JSONBoolean, `true` / non-zero is true and `false` / zero is false.  
Returns: text (modified JSON)

Set a key on a new object:
```
JSONSetElement ( "{ \"a\" : 11 }" ; "b" ; 22.23 ; JSONNumber )
// → {"a":11,"b":22.23}
```
Set multiple keys at once:
```
JSONSetElement ( "{}" ;
  ["name" ; "Alice" ; JSONString] ;
  ["age"  ; 30      ; JSONNumber] ;
  ["active" ; True  ; JSONBoolean]
)
// → {"active":true,"age":30,"name":"Alice"}   (keys come back sorted)
```
Nested key (creates intermediate objects):
```
JSONSetElement ( "{}" ; "address.city" ; "Melbourne" ; JSONString )
// → {"address":{"city":"Melbourne"}}
```
Append to an array with `[+]`:
```
JSONSetElement ( "[1,2,3]" ; "[+]" ; 4 ; JSONNumber )
// → [1,2,3,4]
```
Insert existing JSON without quoting it (JSONRaw = 0):
```
JSONSetElement ( "{}" ; "a" ; "[1,2]" ; JSONRaw )
// → {"a":[1,2]}
```
Build a JSON payload for Insert From URL:
```
Let ( [
  payload = JSONSetElement ( "{}" ;
    ["model"       ; $model       ; JSONString] ;
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
  hasErr = Left ( JSONGetElementType ( raw ; "error" ) ; 1 ) ≠ "?" ;   // "?…" = no such key
  data   = JSONGetElement ( raw ; "data" )
] ;
  If ( hasErr ;
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
All 14 native AI functions.

**Prerequisites:** functions that take an `account` parameter need an AI account set up earlier in the current file with the `Configure AI Account` script step. Supported model providers change between releases (FM 26 added Google Gemini) — fetch the live Configure AI Account page for the current list rather than relying on one here.

**Model-loading functions:**
- `ComputeModel`, `GetModelAttributes` — **Core ML** models loaded with `Configure Machine Learning Model`; iOS, iPadOS and macOS only.
- `PredictFromModel` — **regression** models trained or loaded with `Configure Regression Model` (Random Forest). Not Core ML.

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
// → `[0.40160966445124940405, 0.56225353023174917677, 0.722897396012249005]`. The addition is [1+4, 2+5, 3+6] = [5, 7, 9]. Then the function normalizes this vector and returns it as a JSON array because both inputs were text
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
[
    {
        "classification" : "grand piano, grand",
        "confidence" : 0.998073041439056
    },
    {
        "classification" : "upright, upright piano",
        "confidence" : 0.00192673446144909
    },
    {
        "classification" : "pool table, billiard table, snooker table",
        "confidence" : 8.34678601790984e-08
    },
    {
        "classification" : "dining table, board",
        "confidence" : 2.60599577472931e-08
    },
    {
        "classification" : "puffer, pufferfish, blowfish, globefish",
        "confidence" : 5.19516656696278e-18
    }
]
```
→ JSON array of classifications with confidence scores, e.g.:
```json
[{"classification": "grand piano, grand", "confidence": 0.998}, ...]
```
Vision models also accept `confidenceLowerLimit` (0.0–1.0, drops lower-confidence results) and `returnAtLeastOne` (non-zero returns the best result even when all are below the limit). Claris's Format line for these is ambiguous — fetch the ComputeModel page before relying on their exact positions.
---

## CosineSimilarity ( v1 ; v2 )
Returns the semantic similarity between two embedding vectors as a number from -1 (opposite) to 1 (identical/similar), with 0 meaning no relationship.  
Parameters: `v1`, `v2` — text (JSON arrays) or container fields containing normalised embedding vectors from the **same** model with the same dimensions.  
Returns: number  
*Originated: 21.0*
```
CosineSimilarity ( "[-0.043686170000000003333, 0.042094484000000001456, ... ]" ; "[-0.049242082999999998993, 0.040926795000000001923, ... ]" )
// → `.90848158767415143622` for a particular model
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
Configure AI Account [ Account Name: "my-account" ; Model Provider: OpenAI ; API key: "sk-RZCtpWT..." ]
Go to Layout [ "Meeting Details" (Meetings) ; Animation: None ]

Set Field [ Meetings::Note_Embedding ; GetEmbedding ( "my-account" ; "text-embedding-3-small" ; "Claris" ) ]
```
Image embedding uses an image model on Claris AI Model Server (see the server's model list). Errors: `?` with EvaluationError 877 (no AI account) or 882 (unsupported image type or file too large).
---

## GetEmbeddingAsFile ( text {; fileNameWithExtension } )
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
// → [-0.06650865,0.0034368848,0.051363964,...]
```
(Claris's own example on this page calls GetEmbeddingAsFile by mistake.)

---

## GetFieldsOnLayout ( layoutName )
Returns a JSON object describing fields on the specified layout that are accessible to a find. Pass `""` for the current layout.  
Parameters: `layoutName` — text (use `""` for current layout).  
Returns: text (JSON)  
*Originated: 22.0*

Excludes: fields outside the layout area, hidden fields with "Apply in Find mode", fields with Find Mode entry disabled, fields excluded from Quick Find, fields with no read access, and summary/global/container fields.

A field's `description` key comes from its **annotation** (Advanced Options, FM 26.0.1+) if it has one, otherwise from its **comment**. A leading `[LLM]` tag is stripped, for compatibility with the pre-26.0.1 tagging convention.
```
JSONFormatElements ( GetFieldsOnLayout ( "Products" ) )
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
*Originated: 19.3*  
*Supported: iOS, iPadOS, macOS only*
```
Configure Machine Learning Model [ Operation: Vision ; Name: "TestModel" ; From: Table::ModelContainerField ]
Set Variable [ $modelAttributes ; Value: 
    JSONFormatElements ( GetModelAttributes ( "TestModel" ) ) ]
Show Custom Dialog [ $modelAttributes ]
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

## GetRAGSpaceInfo ( ragAccountName {; spaceID } )
Returns information about a specific RAG space or all RAG spaces for the given RAG account.  
Parameters: `ragAccountName` — name of a RAG account configured via `Configure RAG Account` script step; `spaceID` (optional) — ID of a specific RAG space.  
Returns: text (JSON)  
*Originated: 22.0*

Returns error message `[RAG Space] error. Reason: RAG space {space_id} not found` if the space doesn't exist. Returns `"?"` if the RAG account is invalid.

All spaces for an account:
```
{
  "rag_space_list": [
    {
      "space_id": "knowledge-base",
      "model": "multi-qa-MiniLM-L6-cos-v1"
    },
    {
      "space_id": "meeting-notes",
      "model": "multi-qa-MiniLM-L6-cos-v1"
    }
  ]
}
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
CREATE TABLE "Meetings" (
"Title" varchar(255),
"Location" varchar(255),
"Date" datetime,
"Start Time" datetime,
"End Time" datetime,
"Duration" varchar(255),
"Note" varchar(255),
"PrimaryKey" varchar(255), /*Unique identifier of each record in this table*/
"CreatedBy" varchar(255), /*Account name of the user who created each record*/
"ModifiedBy" varchar(255), /*Account name of the user who last modified each record*/
"CreationTimestamp" datetime, /*Date and time each record was created*/
"ModificationTimestamp" datetime, /*Date and time each record was last modified*/
"Note_Embedding" varbinary(4096),
PRIMARY KEY (PrimaryKey)
);

CREATE TABLE "Topics" (
"ForeignKey" varchar(255), /*Unique identifier of each record in the related table*/
"PrimaryKey" varchar(255), /*Unique identifier of each record in this table*/
"ModifiedBy" varchar(255), /*Account name of the user who last modified each record*/
"ModificationTimestamp" datetime, /*Date and time each record was last modified*/
PRIMARY KEY (PrimaryKey),
FOREIGN KEY (ForeignKey) REFERENCES Meetings(PrimaryKey)
);
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
// → `[0.5999999999999999778, 0.80000000000000004441]`, which for the purpose of illustration, is approximately `[0.6, 0.8]`. The original vector `[3, 4]` has a length of Sqrt(3^2 + 4^2) = 5. The normalized vector `[0.6, 0.8]` has a length of Sqrt(0.6^2 + 0.8^2) = 1
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
// → `[-0.57735026918962573106, -0.57735026918962573106, -0.57735026918962573106]`. The subtraction is [1-4, 2-5, 3-6] = [-3, -3, -3]. Then the function normalizes this vector and returns it as a JSON array because both inputs were text
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
# 1. Configure the account first — every AI call needs it
Configure AI Account [ Account Name: "acct" ; Model Provider: OpenAI ; API key: Global::API_Key ]

# 2. Store embeddings (batch: Insert Embedding in Found Set)
Insert Embedding in Found Set [ Account Name: "acct" ; Embedding Model: "text-embedding-3-small" ;
  Source Field: Notes::Content ; Target Field: Notes::Embedding ; Replace target contents ]

# 3. At search time — the step embeds the query itself
Perform Semantic Find [ Query by: Natural language ; Account Name: "acct" ;
  Embedding Model: "text-embedding-3-small" ; Text: $Query ; Record set: All records ;
  Target field: Notes::Embedding ; Return count: 10 ;
  Cosine similarity condition: greater than ; Cosine similarity value: .4 ]
```
Query and stored vectors must come from the same model. Use `Query by: Vector data` to reuse a stored query embedding.
**Passing schema to a model for natural-language SQL:**
```
Set Variable [ $Schema ; Value: GetTableDDL ( "[\"Orders\",\"Customers\"]" ; True ) ]
# Perform SQL Query by Natural Language builds this DDL itself; use Data Tables: By DDL
# when you want to send a hand-edited schema instead.
```
**Controlling schema descriptions sent to models (FM 26.0.1+):**  
Field **annotations** (Advanced Options for Field) are the preferred source: when any field in a table is annotated, only annotated fields appear in that table's generated DDL. GetFieldsOnLayout uses the annotation, falling back to the field comment. The older `[LLM]` comment prefix is still stripped for compatibility.
