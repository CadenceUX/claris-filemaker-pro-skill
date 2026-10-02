# Design & Container Functions — Examples

## Contents
- Design Functions
  - BaseTableIDs ( fileName )
  - BaseTableNames ( fileName )
  - BaseTableComment ( fileName ; baseTableName )
  - DatabaseNames
  - FieldBounds ( fileName ; layoutName ; fieldName )
  - FieldComment ( fileName ; fieldName )
  - FieldAnnotation ( fileName ; fieldName )
  - FieldDisplayNames ( fileName ; fieldName )
  - FieldIDs ( fileName ; layoutName )
  - FieldNames ( fileName ; layoutName )
  - FieldRepetitions ( fileName ; layoutName ; fieldName )
  - FieldStyle ( fileName ; layoutName ; fieldName )
  - FieldType ( fileName ; fieldName )
  - GetNextSerialValue ( fileName ; fieldName )
  - LayoutIDs ( fileName )
  - LayoutNames ( fileName )
  - LayoutObjectNames ( fileName ; layoutName )
  - LayoutTableNames ( fileName ) ⚠️ Does not exist
  - RelationInfo ( fileName ; tableName )
  - ScriptIDs ( fileName )
  - ScriptNames ( fileName )
  - TableIDs ( fileName )
  - TableNames ( fileName )
  - ValueListIDs ( fileName )
  - ValueListItems ( fileName ; valueList )
  - ValueListNames ( fileName )
  - WindowNames {( fileName )}
  - Common patterns
- Container Functions
  - Base64Decode ( text {; fileNameWithExtension } )
  - Base64Encode ( data )
  - Base64EncodeRFC ( RFCNumber ; data )
  - CryptAuthCode ( data ; algorithm ; key )
  - CryptDecrypt ( container ; key )
  - CryptDecryptBase64 ( text ; key )
  - CryptDigest ( data ; algorithm )
  - CryptEncrypt ( data ; key )
  - CryptEncryptBase64 ( data ; key )
  - CryptGenerateSignature ( data ; algorithm ; privateRSAKey ; keyPassword )
  - CryptVerifySignature ( data ; algorithm ; publicRSAKey ; signature )
  - GetContainerAttribute ( field ; attributeName )
  - GetHeight ( field )
  - GetLiveText ( container ; language )
  - GetLiveTextAsJSON ( container ; language )
  - GetTextFromPDF ( container )
  - GetThumbnail ( field ; width ; height )
  - GetWidth ( field )
  - HexDecode ( data {; fileNameWithExtension } )
  - HexEncode ( data )
  - ReadQRCode ( container )
  - TextDecode ( container ; encoding )
  - TextEncode ( text ; encoding ; lineEndings )
  - VerifyContainer ( field )
  - Common patterns

---

# FileMaker Design Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/design-functions.html  
All 26 design functions (FM 26 added BaseTableComment, FieldAnnotation and FieldDisplayNames).

**`fileName`** must name a file that is **already open** — design functions never open one. `""` means the current file.  
**IDs vs names:** `TableNames` / `TableIDs` describe **table occurrences** (relationships graph); `BaseTableNames` / `BaseTableIDs` describe **base tables**.  
**Testing for a name in a list:** search `¶ & list & ¶` for `¶ & name & ¶` — a bare `PatternCount ( list ; "Archive" )` also matches "Archive Old".

> **Note:** `LayoutTableNames` does not exist in current FileMaker releases. Use `TableNames` (table occurrences) or `BaseTableNames` (base tables) instead.

**Overview:** Design functions return schema metadata about the current FileMaker file — tables, fields, layouts, relationships, scripts, value lists, and custom functions. They are essential for:
- Dynamic field/layout references that survive schema changes
- MCP/AI tooling that needs to introspect the database
- Developer utilities and admin scripts
- Building data dictionaries and documentation

**Performance note:** on large schemas, compute design functions once into a variable rather than in unstored calculation fields.

---

## BaseTableIDs ( fileName )
Returns the IDs of all **base tables** in the file, in the same order as `BaseTableNames`. IDs don't reflect creation order. *Originated: 20.1*  
Returns: text (return-delimited)
```
BaseTableIDs ( "" )
// → 130¶131 in a file with two base tables
```
Look up a base table's ID by name:
```
Let ( [
  names = BaseTableNames ( "" ) ;
  pos   = ValueCount ( Left ( names ; Position ( ¶ & names & ¶ ; ¶ & "Contacts" & ¶ ; 1 ; 1 ) ) )
] ;
  GetValue ( BaseTableIDs ( "" ) ; pos )
)
```
---

## BaseTableNames ( fileName )
Returns the names of all **base tables** in the file (`TableNames` returns table occurrences). *Originated: 20.1*  
Returns: text (return-delimited)
```
BaseTableNames ( "" )
// → Contacts¶Invoices
```
---

## BaseTableComment ( fileName ; baseTableName )
Returns the comment entered for a **base table** in Manage Database > Tables. *Originated: 26.0* (table comments themselves date from 22.0.1).  
Returns: text
```
BaseTableComment ( "" ; "Contacts" )
// → the Contacts table's comment
```
Build schema context for an AI prompt (`GetTableDDL` takes a JSON **array** of table occurrence names):
```
Let ( [
  comment = BaseTableComment ( "" ; "Contacts" ) ;
  ddl     = GetTableDDL ( JSONMakeArray ( "Contacts" ; "" ; JSONString ) ; True )
] ;
  "Table: Contacts — " & comment & ¶ & ddl
)
```
---

## DatabaseNames
Returns the names (without extensions) of all files open on this computer — for a hosted solution, the files open on **this client**.  
Returns: text (return-delimited)
```
FilterValues ( DatabaseNames ; "Customers" )
// → Customers¶ if open, empty if not
```
---

## FieldBounds ( fileName ; layoutName ; fieldName )
Returns the position and size of a field on a layout as a space-delimited string: `left top right bottom rotation`.  
Parameters: `fileName` — file name (use `Get(FileName)` for current); `layoutName` — layout name; `fieldName` — fully qualified field name.  
Returns: text (`"left top right bottom rotation"`)
```
FieldBounds ( "Customers" ; "Layout #1" ; "Field" )
// → `36 48 295 65 0` in the example below. Notice that all parameters are enclosed in quotation marks
```
Extract individual components:
```
Let ( bounds = FieldBounds ( Get(FileName) ; Get(LayoutName) ; "Contacts::Email" ) ;
  GetValue ( Substitute ( bounds ; " " ; ¶ ) ; 1 )   // → left position
)
```
---

## FieldComment ( fileName ; fieldName )
Returns the comment entered for a field in Manage Database > Fields. Use `Table::Field` for a field outside the current table.  
Returns: text
```
FieldComment ( "Customers" ; "Accounts::Current Balance" )
// → Customer's current balance
```
For AI schema descriptions, FM 26.0.1 prefers field **annotations** (`FieldAnnotation`); comments are the fallback.

---

## FieldAnnotation ( fileName ; fieldName )
Returns the field's **DDL annotation**, set in Advanced Options for Field — not its comment. *Originated: 26.0* (the annotation option itself shipped in 26.0.1).  
Returns: text
```
FieldAnnotation ( "" ; "Contacts::Email" )
// → the Email field's annotation
```
When any field in a table is annotated, only annotated fields appear in that table's generated DDL (`GetTableDDL`, Perform SQL Query by Natural Language).

---

## FieldDisplayNames ( fileName ; fieldName )
Returns the field's custom **display names** as a JSON object, set in Advanced Options for Field > Customize field display names. *Originated: 26.0*  
Returns: text (JSON). Built-in keys: `fm_common` (default), `fm_export`, `fm_sort`, `fm_table_view`; you can add your own keys.
```
FieldDisplayNames ( "" ; "Customers::FirstName" )
// → {"fm_common":"First Name","fm_table_view":"Given Name"}

JSONGetElement ( FieldDisplayNames ( "" ; "Customers::FirstName" ) ; "fm_table_view" )
// → Given Name
```
A custom key works as a short label in a layout calculation:
```
JSONGetElement ( FieldDisplayNames ( "" ; "Customers::CustomerID" ) ; "my_short_name" )
```
---

## FieldIDs ( fileName ; layoutName )
Returns a return-delimited list of field IDs for all fields on the specified layout.  
Parameters: `fileName`; `layoutName` — use `""` for current layout.  
Returns: text (return-delimited numbers)
```
FieldIDs ( "Customers" ; "" )
// → IDs of all unique fields in the default table of Customers
```
Field IDs are stable across renames — use with `FieldNames` for change-resilient references.

---

## FieldNames ( fileName ; layoutName )
Returns the names of the fields on a layout — or, if `layoutName` names a **table**, all fields in that table. Local fields are **unqualified**; related fields on a layout come back as `Table::Field`. `""` as layoutName means the default table.  
Returns: text (return-delimited)
```
FieldNames ( "" ; "Contacts" )
// → Email¶Phones¶Today
```
Check whether a field exists (match the unqualified name, whole value):
```
PatternCount ( ¶ & FieldNames ( "" ; "Contacts" ) & ¶ ; ¶ & "Email" & ¶ ) > 0
```
---

## FieldRepetitions ( fileName ; layoutName ; fieldName )
Returns the number of repetitions **shown on the layout** and their orientation, as text. A non-repeating field returns `1 vertical`.  
Returns: text
```
FieldRepetitions ( "Customers" ; "Data Entry" ; "Business Phone" )
// → 3 vertical  (field defined with 5 repetitions, layout shows 3)
```
For the defined maximum, use the last value of `FieldType`.

---

## FieldStyle ( fileName ; layoutName ; fieldName )
Returns the control style of a field on a layout as **text**, followed by the value list name if one is attached.  
Returns: text — `Standard`, `Scrolling` (edit box with scroll bar), `Popuplist` (drop-down list), `Popupmenu`, `Checkbox`, `RadioButton`, `Calendar`
```
FieldStyle ( "Customers" ; "Data Entry" ; "Current Customer" )
// → RadioButton Yes/No List
```
```
LeftWords ( FieldStyle ( "" ; Get ( LayoutName ) ; "Status" ) ; 1 ) = "Popupmenu"
```
---

## FieldType ( fileName ; fieldName )
Returns four space-separated values:
1. storage — `Standard`, `StoredCalc`, `UnstoredCalc`, `Summary`, `Global`, `External(Secure)`, `External(Open)`
2. data type — `Text`, `Number`, `Date`, `Time`, `Timestamp`, `Container`
3. `Indexed` or `Unindexed`
4. maximum repetitions (`1` if not repeating)

Returns: text
```
FieldType ( "" ; "Contacts::Email" )
// → Standard Text Unindexed 1

FieldType ( "" ; "Contacts::Phones" )
// → Standard Text Unindexed 3

FieldType ( "" ; "Contacts::Today" )
// → Global Date Unindexed 1
```
Is a field a calculation (not writable)?
```
PatternCount ( LeftWords ( FieldType ( "" ; "Invoices::Total" ) ; 1 ) ; "Calc" ) > 0
```
---

## GetNextSerialValue ( fileName ; fieldName )
Returns the next serial value that will be assigned to a field when a new record is created.  
Parameters: `fileName`; `fieldName` — fully qualified.  
Returns: text (the serial value as a string, since serials can have prefixes)
```
GetNextSerialValue ( "Customers" ; "CustID" )
// → the next serial number for the CustID field
```
Useful for displaying "next invoice number" before creating the record.

---

## LayoutIDs ( fileName )
Returns a return-delimited list of layout IDs for all layouts in the file.  
Parameters: `fileName`.  
Returns: text
```
LayoutIDs ( "Customers" )
// → a list of all the layout IDs in the Customers database file
```
---

## LayoutNames ( fileName )
Returns the names of all layouts in the file.  
Returns: text (return-delimited)
```
LayoutNames ( "" )
```
Check a layout exists before going to it (script):
```
If [ PatternCount ( ¶ & LayoutNames ( "" ) & ¶ ; ¶ & "Archive" & ¶ ) = 0 ]
  Show Custom Dialog [ "Layout 'Archive' not found" ]
Else
  Go to Layout [ "Archive" ]
End If
```
---

## LayoutObjectNames ( fileName ; layoutName )
Returns the names of all **named** objects on a layout. Objects inside a named tab control, slide control, group or portal follow it, wrapped in `<` `>`.  *Originated: 8.5*  
Returns: text (return-delimited)
```
LayoutObjectNames ( "Customers" ; "Data Entry" )
```
Check before `Go to Object` or `Refresh Object` (script):
```
If [ PatternCount ( ¶ & LayoutObjectNames ( "" ; Get ( LayoutName ) ) & ¶ ; ¶ & "myPanel" & ¶ ) > 0 ]
  Go to Object [ Object Name: "myPanel" ]
End If
```
---

## LayoutTableNames ( fileName ) ⚠️ Does not exist
`LayoutTableNames` is **not a valid FileMaker function** and does not appear in the current Claris help documentation. It was likely confused with `TableNames` (returns table occurrence names) or `BaseTableNames` (returns base table names).

To find which table occurrence a layout uses, see `Get(LayoutTableName)` (a Get function, not a Design function):
```
// On the layout in question:
Get ( LayoutTableName )   // → "Invoices"  (the table occurrence this layout is bound to)
```
To list all table occurrences (what most "LayoutTableNames" callers actually want):
```
TableNames ( Get(FileName) )
// → "Contacts¶Invoices¶LineItems_Invoices¶…"
```
---

## RelationInfo ( fileName ; tableName )
Describes every relationship directly attached to a table occurrence. One block per relationship, blocks separated by a blank line. Each block has four parts:
- `Source:` the data source name
- `Table:` the related table occurrence
- `Options:` any of `Delete`, `Create`, `Sorted` (blank if none)
- one line per predicate, fully qualified (`A::x = B::y`)

Returns: text
```
RelationInfo ( "Human Resources" ; "Employees" )
// → Source: Human Resources
//   Table: Company
//   Options: Create
//   Company::Company ID = Employees::Company ID
//
//   Source: Human Resources
//   Table: Addresses
//   Options: Create Sorted
//   Addresses::Employee ID = Employees::Employee ID
//   Addresses::DateMovedIn >= Employees::DateOfHire
```
---

## ScriptIDs ( fileName )
Returns a return-delimited list of script IDs for all scripts in the file.  
Parameters: `fileName`.  
Returns: text
```
ScriptIDs ( "Customers" )
// → a list of all the script IDs in the Customers database file
```
---

## ScriptNames ( fileName )
Returns the names of all scripts in the file.  
Returns: text (return-delimited)
```
ScriptNames ( "" )
```
Check a script exists before calling it (script):
```
If [ PatternCount ( ¶ & ScriptNames ( "" ) & ¶ ; ¶ & "SyncContacts" & ¶ ) > 0 ]
  Perform Script [ Specified: By name ; "SyncContacts" ]
End If
```
---

## TableIDs ( fileName )
Returns the IDs of all **table occurrences** in the relationships graph (for base tables, use `BaseTableIDs`). IDs don't reflect creation order.  
Returns: text (return-delimited)
```
TableIDs ( "" )
// → 1065090¶1065091   (occurrence IDs — base tables in the same file are 130, 131)
```
---

## TableNames ( fileName )
Returns the names of all **table occurrences** in the relationships graph — not base tables (use `BaseTableNames`). Showing an external file's occurrences needs access to that file.  
Returns: text (return-delimited)
```
TableNames ( "" )
// → Contacts¶Invoices¶Invoices_Contacts…
```
Check whether an occurrence exists:
```
PatternCount ( ¶ & TableNames ( "" ) & ¶ ; ¶ & "Archive" & ¶ ) > 0
```
---

## ValueListIDs ( fileName )
Returns a return-delimited list of value list IDs in the file.  
Parameters: `fileName`.  
Returns: text

---

## ValueListItems ( fileName ; valueList )
Returns the values in a value list. In WebDirect it only works for the current file (another file returns empty).  
Returns: text (return-delimited)
```
ValueListItems ( "Customers" ; "Code" )
```
Convert to a JSON array for an API payload:
```
JSONMakeArray ( ValueListItems ( "" ; "Status Values" ) ; "" ; JSONString )
// → ["New","Active","On Hold","Closed"]
```
Validate a value against a value list (field validation calculation):
```
PatternCount ( ¶ & ValueListItems ( "" ; "Status Values" ) & ¶ ; ¶ & Self & ¶ ) > 0
```
---

## ValueListNames ( fileName )
Returns a return-delimited list of all value list names in the file.  
Parameters: `fileName`.  
Returns: text
```
ValueListNames ( "Customers" )
// → a list of all the value list names in the Customers database file
```
---

## WindowNames {( fileName )}
Returns the names of open windows in stacking order — visible, then minimised, then hidden. With `fileName`, only windows based on that file; without it, **all** open windows.  
Returns: text (return-delimited)
```
WindowNames
// → Customers¶Invoices

PatternCount ( ¶ & WindowNames & ¶ ; ¶ & "Invoice Detail" & ¶ ) > 0
// → 1 if a window named Invoice Detail is open
```
Close every other window of this file (script):
```
Set Variable [ $windows ; Value: WindowNames ( Get ( FileName ) ) ]
Set Variable [ $current ; Value: Get ( WindowName ) ]
Set Variable [ $i ; Value: 1 ]
Loop [ Flush: Always ]
  Set Variable [ $w ; Value: GetValue ( $windows ; $i ) ]
  Exit Loop If [ $w = "" ]
  If [ $w ≠ $current ]
    Close Window [ Name: $w ; Current file ]
  End If
  Set Variable [ $i ; Value: $i + 1 ]
End Loop
```
---

## Common patterns

**Build a data dictionary (field name + type for every field in a table):**
```
While (
  [
    fields = FieldNames ( "" ; "Contacts" ) ;
    i = 1 ; dict = ""
  ] ;
  i ≤ ValueCount ( fields ) ;
  [
    f    = GetValue ( fields ; i ) ;
    type = FieldType ( "" ; "Contacts::" & f ) ;   // FieldNames returns unqualified names
    dict = dict & f & " → " & type & ¶ ;
    i    = i + 1
  ] ;
  Trim ( dict )
)
```
**Confirm file and layout exist before navigating (safe cross-file open):**
```
If [ IsEmpty ( FilterValues ( DatabaseNames ; "SharedData" ) ) ]
  Open File [ "SharedData" ]
End If
If [ PatternCount ( ¶ & LayoutNames ( "SharedData" ) & ¶ ; ¶ & "Reports" & ¶ ) > 0 ]
  Go to Layout [ "Reports" (SharedData) ]
End If
```
**Dynamic field export — all fields on current layout:**
```
While (
  [
    fields = FieldNames ( Get(FileName) ; Get(LayoutName) ) ;
    i = 1 ; payload = "{}"
  ] ;
  i ≤ ValueCount ( fields ) ;
  [
    f       = GetValue ( fields ; i ) ;
    key     = Substitute ( f ; "::" ; "_" ) ;  // sanitise for JSON key
    payload = JSONSetElement ( payload ; key ; GetField ( f ) ; JSONString ) ;
    i       = i + 1
  ] ;
  payload
)
```
**Get next serial without creating a record:**
```
Set Variable [ $nextNum ; Value: GetNextSerialValue ( Get(FileName) ; "Invoices::InvoiceNumber" ) ]
Show Custom Dialog [ "Next invoice will be: " & $nextNum ]
```
---

# FileMaker Container Functions — Quick Reference

Source: https://help.claris.com/en/pro-help/content/container-functions.html  
All 24 container functions with syntax, return type, and examples.  

**Encryption:** the `Crypt*` functions (FM 16+) are FileMaker's encryption, hashing and signing functions. Pair them with `Base64EncodeRFC` / `HexEncode` to turn their binary container results into text.

---

## Base64Decode ( text {; fileNameWithExtension } )

Returns container or text. Decodes a Base64-encoded string back to binary (container) or plain text. Supply `fileNameWithExtension` to store the result as a named container file.
```
Base64Decode(Products::Base64;"question.png")
// → ![Help button]() when Products::Base64 is set to a string that begins with "iVBORw0KGgoAAAANSUhEUgAAAB8". The Base64 string in this example was shortened for readability
```
---

## Base64Encode ( data )

Returns text in Base64, following **RFC 2045**: lines wrap at 76 characters and the output **ends with CR+LF**. For tokens, signatures and HTTP headers use `Base64EncodeRFC ( 4648 ; data )` instead — no line breaks. Text is converted to UTF-8 first; container data is encoded as-is (filename not kept).
```
Base64Encode ( "Black" )
// → QmxhY2s=  (then CR+LF)
```
---

## Base64EncodeRFC ( RFCNumber ; data )

Returns text in the chosen Base64 format. `RFCNumber`: `1421` (64-char lines, CRLF) · `2045` (76-char lines, CRLF) · `3548` / `4648` (no line breaks) · `4880` (76-char lines, CRLF, appended CRC). Unrecognised values fall back to 4648. *Originated: 16.0*
```
Base64EncodeRFC ( 4648 ; "Black" )
// → QmxhY2s=
```
URL-safe Base64 (for JWTs) isn't an option — substitute `+`→`-`, `/`→`_` and strip `=` yourself.

---

## CryptAuthCode ( data ; algorithm ; key )

Returns a binary HMAC as container data. `algorithm`: `MD5`, `SHA1`, `SHA224`, `SHA256`, `SHA384`, `SHA512`; `""` means **SHA512**; anything else returns `?`. Encode the result with `Base64EncodeRFC` or `HexEncode`.
```
Base64EncodeRFC ( 4648 ; CryptAuthCode ( "payload" ; "SHA256" ; "secret" ) )
// → uC/LeRrOxXhZuYm0MKgmSIzi5Hn9+SMmvQoug3WkK6Q=
```
---

## CryptDecrypt ( container ; key )

Returns container. Decrypts container data previously encrypted with `CryptEncrypt`. Key must match.
```
CryptDecrypt ( 
    CryptEncrypt ( "This needs protection" ; "My secret password" ) ; 
    "My secret password" 
)
```
---

## CryptDecryptBase64 ( text ; key )

Returns container. Decrypts Base64-encoded text previously produced by `CryptEncryptBase64`.
```
CryptDecryptBase64 ( 
    CryptEncryptBase64 ( "This needs protection" ; "My secret password" ) ; 
    "My secret password" 
)
```
---

## CryptDigest ( data ; algorithm )

Returns a binary hash as container data. Same algorithm names as CryptAuthCode; `""` means SHA512.
```
HexEncode ( CryptDigest ( "abc" ; "SHA256" ) )
// → BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD
```
---

## CryptEncrypt ( data ; key )

Encrypts text or container data with `key` and returns container data (a file named `encrypted.data`). Decrypt with `CryptDecrypt` and the same key. Keep keys out of the file — see Claris's FileMaker Security Guide.
```
CryptEncrypt ( "This needs protection" ; "My secret password" )
```
---

## CryptEncryptBase64 ( data ; key )

Returns text (Base64). Encrypts data and Base64-encodes the result — convenient for storing encrypted text in a text field.
```
CryptEncryptBase64 ( "This needs protection" ; "My secret password" )
```
---

## CryptGenerateSignature ( data ; algorithm ; privateRSAKey ; keyPassword )

Returns container (binary signature). Signs data using an RSA private key. Algorithm: `"SHA256"`, `"SHA384"`, `"SHA512"`.
```
Base64EncodeRFC ( 4648 ; 
    CryptGenerateSignature ( 
        Table::TextToSign ; "SHA512" ; Table::PrivateRSAKey ; $Password 
    )
)
```
---

## CryptVerifySignature ( data ; algorithm ; publicRSAKey ; signature )

Returns number. Verifies an RSA signature against the public key. Returns `1` if valid, `0` if not.
```
CryptVerifySignature ( 
    Table::SignedText ; "SHA512" ; Table::PublicRSAKey ;     
    Base64Decode (         
        Table::Signature ; "sig.data"     
    ) 
)
```
---

## GetContainerAttribute ( field ; attributeName )

Returns file metadata from container data. Attribute names are case-insensitive. Common ones:
- General: `filename`, `fileSize`, `MD5`, `storageType` (Embedded / External (Secure) / External (Open) / File Reference / Text), `internalSize`, `externalSize`, `externalFiles`
- Images: `width`, `height`, `dpiWidth`, `dpiHeight`, `transparency`
- Photos, audio/video, signatures, barcodes: see the Claris page
- `all`: every attribute as a list

Returns: text, number, date, time, timestamp or container, depending on the attribute.
```
GetContainerAttribute ( TextEncode ( "hello" ; "utf-8" ; 1 ) ; "fileSize" )
// → 5
```
Some attributes (`photo`, `created`, `modified`, `all`) can be invalid when the file is hosted on Windows or Cloud and read through the REST APIs.

---

## GetHeight ( field )

Returns number (pixels). Returns the pixel height of the image stored in a container field. Returns `0` for non-image content.
```
GetHeight(product)
// → 768
```
---

## GetLiveText ( container ; language )

Returns the text recognised in an image (on-device OCR) on supported iOS, iPadOS and macOS — not Windows or Linux. *Originated: 19.5*  
`language` must be one of: `"en-US"`, `"fr-FR"`, `"it-IT"`, `"de-DE"`, `"es-ES"`, `"pt-BR"`, `"zh-Hans"`, `"ja-JP"`, `"ko-KR"`, `"uk-UA"`, `"th-TH"`, `"vi-VN"`, `"ar-SA"` and `"ars-SA"` (the last two need iOS/iPadOS 18 or macOS 15). Bare codes like `"en"` aren't in the list.  
Works with PNG, JPEG, GIF, TIFF, BMP and PDF; PNGs with transparent backgrounds aren't supported.
```
Set Field [ Invoices::InvoiceText ; GetLiveText ( Invoices::InvoiceContainer ; "en-US" ) ]
```
---

## GetLiveTextAsJSON ( container ; language )

Like `GetLiveText`, but returns a JSON array with one object per text line: `x` and `y` (pixels from the image's top-left) and `text`. Same language codes. *Originated: 21.0*
```
GetLiveTextAsJSON ( Invoices::InvoiceContainer ; "en-US" )
// → [ { "x": 113, "y": 230, "text": "Erickson's Water Garden" }, … ]
```
---

## GetTextFromPDF ( container )

Returns the plain text in a PDF stored in a container. *Originated: 22.0*  
Returns `?` if the container is empty or not a PDF, no text is found, the PDF is password-protected or unreadable, or — **on Windows and Linux** — the PDF is a scanned image (macOS handles scanned PDFs).
```
PatternCount ( GetTextFromPDF ( Documents::Contract ) ; "indemnification" ) > 0
```
---

## GetThumbnail ( field ; width ; height )

Returns container. Generates a thumbnail of the container image scaled to fit within `width` × `height` pixels, preserving aspect ratio.
```
Set Field [ Invoices::ExportContainer ; GetThumbnail ( Invoices::Container ; 50 ; 50 ) ]
Export Field Contents [ Invoices::ExportContainer ; Create folders: Off ]
```
---

## GetWidth ( field )

Returns number (pixels). Returns the pixel width of the image stored in a container field. Returns `0` for non-image content.
```
GetWidth(Product)
// → 1024
```
---

## HexDecode ( data {; fileNameWithExtension } )

Returns container or text. Decodes a hexadecimal-encoded string back to binary. Inverse of `HexEncode`.
```
HexDecode ( "46696C654D616B6572" )
// → FileMaker
```
---

## HexEncode ( data )

Returns data as **uppercase** hexadecimal text. Text is converted to UTF-8 first; container data is encoded as-is.
```
HexEncode ( "FileMaker" )
// → 46696C654D616B6572
```
---

## ReadQRCode ( container )

Returns the text value of a **QR code** in an image (other barcode types: use Insert from Device in FileMaker Go). On Linux, needs Ubuntu 22.04 or later. *Originated: 19.5*
```
Set Field [ Product::URL ; ReadQRCode ( Invoices::Container ) ]
If [ Left ( Product::URL ; 4 ) = "http" ]
    Open URL [ With dialog: Off ; Product::URL ]
End If
```
---

## TextDecode ( container ; encoding )

Returns text decoded from a text file in a container. `encoding` is one of TextEncode's names (below).
```
TextDecode ( TextEncode ( "café" ; "iso-8859-1" ; 1 ) ; "iso-8859-1" )
// → café
```
---

## TextEncode ( text ; encoding ; lineEndings )

Returns a text file as container data.  
`encoding`: `utf-8`, `iso-8859-1`, `windows-1251`, `shift_jis`, `windows-1252`, `gb18030`, `euc-kr`, `big5`, `macintosh` — anything else returns `?`.  
`lineEndings` is a **number**: `1` unchanged · `2` CR (legacy Mac) · `3` LF (macOS / Unix / Linux) · `4` CRLF (Windows). Unrecognised values — including text like `"Windows"` — are silently treated as unchanged.
```
Set Field [ table::container ; TextEncode ( table::text ; "iso-8859-1" ; 4 ) ]
Export Field Contents [ table::container ; "output.txt" ; Create folders: Off ]
```
---

## VerifyContainer ( field )

Checks **externally stored** container data: `0` if the external file was changed or deleted outside FileMaker, `1` if not, `?` if `field` isn't a container field.
```
If ( VerifyContainer ( Documents::Attachment ) = 0 ; "⚠️ External file changed or missing" ; "OK" )
```
---

## Common patterns

**Encrypt → store as text field, decrypt on demand:**
```
// Encrypt (auto-enter calc on EncryptedSSN field):
CryptEncryptBase64 ( Contacts::SSN_raw ; $$encryptionKey )

// Decrypt for display (custom function or script):
CryptDecryptBase64 ( Contacts::EncryptedSSN ; $$encryptionKey )
```
**HMAC verification for webhook payloads:**
```
Let ( [
  payload    = WebhookData::Body ;
  secret     = $$webhookSecret ;
  computed   = Base64EncodeRFC ( 4648 ; CryptAuthCode ( payload ; "SHA256" ; secret ) ) ;  // not Base64Encode: it appends CR+LF
  received   = Trim ( WebhookData::HmacHeader )   // strip any "sha256=" prefix too
] ;
  Exact ( computed ; received )   // NOT "=": FileMaker's = ignores case, Base64 doesn't
)
// → 1 if payload is authentic. The body must be byte-for-byte what was signed.
```
**Aspect-ratio-aware thumbnail:**
```
Let ( [
  w = GetWidth ( Products::Photo ) ;
  h = GetHeight ( Products::Photo ) ;
  maxDim = 200 ;
  scale = Min ( maxDim / w ; maxDim / h )
] ;
  GetThumbnail ( Products::Photo ; w * scale ; h * scale )
)
```
**OCR → extract invoice number:**
```
Let ( raw = GetLiveText ( Scan::Image ; "en-US" ) ;
  // Find the line that starts with "Invoice #"
  Let ( lines = Substitute ( raw ; ¶ ; "|" ) ;
    // … parse with custom function or filter
    raw
  )
)
```
