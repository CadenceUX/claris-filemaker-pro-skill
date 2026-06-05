# Design & Container Functions — Examples

---

# FileMaker Design Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/design-functions.html  
All 23 design functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

> **Note:** `LayoutTableNames` does not exist in current FileMaker releases. Use `TableNames` (table occurrences) or `BaseTableNames` (base tables) instead.

**Overview:** Design functions return schema metadata about the current FileMaker file — tables, fields, layouts, relationships, scripts, value lists, and custom functions. They are essential for:
- Dynamic field/layout references that survive schema changes
- MCP/AI tooling that needs to introspect the database
- Developer utilities and admin scripts
- Building data dictionaries and documentation

**Performance note:** Design functions are recalculated frequently and can be slow on large schemas. Prefer storing results in variables (`Set Variable`) rather than using them in unstored calculation fields.

---

## BaseTableIDs ( fileName )
Returns a return-delimited list of internal IDs for every **base table** (not table occurrence) defined in the file. Parallel to `BaseTableNames` — the Nth ID matches the Nth name.  
Parameters: `fileName` — file name string (use `Get(FileName)` for the current file).  
Returns: text

```
BaseTableIDs ( Get(FileName) )
// → "1¶2¶3¶…"  (internal base table IDs)
```

Pair with `BaseTableNames` to build an ID → name lookup:
```
Let ( [
  ids   = BaseTableIDs ( Get(FileName) ) ;
  names = BaseTableNames ( Get(FileName) ) ;
  target = "Contacts" ;
  idx   = ValueCount ( FilterValues ( names ; target ) )  // find position
] ;
  GetValue ( ids ; idx )
)
```

---

## BaseTableNames ( fileName )
Returns a return-delimited list of all **base table** names in the file (not table occurrences — those are returned by `TableNames`).  
Parameters: `fileName` — file name string.  
Returns: text

```
BaseTableNames ( Get(FileName) )
// → "Contacts¶Invoices¶LineItems¶Products"
```

Count base tables:
```
ValueCount ( BaseTableNames ( Get(FileName) ) )
// → 12
```

---

## DatabaseNames
Returns a return-delimited list of all open FileMaker files (databases) accessible from the current session.  
Parameters: none.  
Returns: text

```
DatabaseNames
// → MyApp¶Contacts¶SharedData
```

Useful for cross-file scripts that need to verify a file is open before referencing it:
```
If ( PatternCount ( DatabaseNames ; "SharedData" ) = 0 ;
  Open File [ "SharedData" ]
)
```

---

## FieldBounds ( fileName ; layoutName ; fieldName )
Returns the position and size of a field on a layout as a space-delimited string: `left top right bottom rotation`.  
Parameters: `fileName` — file name (use `Get(FileName)` for current); `layoutName` — layout name; `fieldName` — fully qualified field name.  
Returns: text (`"left top right bottom rotation"`)

```
FieldBounds ( Get(FileName) ; "Contacts" ; "Contacts::Email" )
// → "72 120 400 140 0"  (left=72, top=120, right=400, bottom=140, rotation=0)
```

Extract individual components:
```
Let ( bounds = FieldBounds ( Get(FileName) ; Get(LayoutName) ; "Contacts::Email" ) ;
  GetValue ( Substitute ( bounds ; " " ; ¶ ) ; 1 )   // → left position
)
```

---

## FieldComment ( fileName ; fieldName )
Returns the comment (description) stored on a field in Manage Database.  
Parameters: `fileName`; `fieldName` — fully qualified (`"Table::Field"`).  
Returns: text

```
FieldComment ( Get(FileName) ; "Contacts::Email" )
// → "Primary email address for correspondence"
```

Used in `GetFieldsOnLayout` to supply `[LLM]`-tagged descriptions to AI models:
```
// Field comment: "[LLM] Primary email address for the contact"
FieldComment ( Get(FileName) ; "Contacts::Email" )
// → "[LLM] Primary email address for the contact"
```

---

## FieldIDs ( fileName ; layoutName )
Returns a return-delimited list of field IDs for all fields on the specified layout.  
Parameters: `fileName`; `layoutName` — use `""` for current layout.  
Returns: text (return-delimited numbers)

```
FieldIDs ( Get(FileName) ; "Contacts" )
// → 1¶3¶7¶12¶...
```

Field IDs are stable across renames — use with `FieldNames` for change-resilient references.

---

## FieldNames ( fileName ; layoutNameOrTableName )
Returns a return-delimited list of field names. When passed a layout name, returns fields on that layout. When passed a table occurrence name, returns all fields in that table.  
Parameters: `fileName`; `layoutNameOrTableName`.  
Returns: text (return-delimited, fully qualified `"Table::Field"` names)

```
FieldNames ( Get(FileName) ; "Contacts" )
// → Contacts::ContactID¶Contacts::FirstName¶Contacts::LastName¶...

FieldNames ( Get(FileName) ; "Contacts Layout" )
// → only fields placed on that layout
```

Check if a field exists:
```
PatternCount ( FieldNames ( Get(FileName) ; "Contacts" ) ; "Contacts::Email" ) > 0
```

Dynamic field iteration with While:
```
While (
  [
    fields = FieldNames ( Get(FileName) ; "Contacts" ) ;
    i = 1 ; out = ""
  ] ;
  i ≤ ValueCount ( fields ) ;
  [
    f   = GetValue ( fields ; i ) ;
    val = GetField ( f ) ;
    out = out & f & ": " & val & ¶ ;
    i   = i + 1
  ] ;
  Trim ( out )
)
```

---

## FieldRepetitions ( fileName ; layoutName ; fieldName )
Returns the number of repetitions displayed on a layout for a repeating field.  
Parameters: `fileName`; `layoutName`; `fieldName` — fully qualified.  
Returns: number

```
FieldRepetitions ( Get(FileName) ; "Schedule" ; "Schedule::Slots" )
// → 7  (7 repetitions shown on this layout)
```

---

## FieldStyle ( fileName ; layoutName ; fieldName )
Returns a number indicating the control style of a field on a layout (edit box, drop-down list, radio buttons, etc.).  
Parameters: `fileName`; `layoutName`; `fieldName`.  
Returns: number

| Value | Style |
|---|---|
| 0 | Standard (edit box) |
| 1 | Drop-down list |
| 2 | Pop-up menu |
| 3 | Checkbox set |
| 4 | Radio button set |
| 5 | Drop-down calendar |
| 6 | Scrolling list |

```
FieldStyle ( Get(FileName) ; "Contacts" ; "Contacts::Status" )
// → 2  (pop-up menu)
```

---

## FieldType ( fileName ; fieldName )
Returns a text description of a field's data type and storage type.  
Parameters: `fileName`; `fieldName` — fully qualified.  
Returns: text (e.g. `"Normal, Text"`, `"Calculated, Number"`, `"Summary, Number"`, `"Global, Text"`)

```
FieldType ( Get(FileName) ; "Contacts::Email" )
// → "Normal, Text"

FieldType ( Get(FileName) ; "Invoices::Total" )
// → "Calculated, Number"

FieldType ( Get(FileName) ; "Invoices::GrandTotal" )
// → "Summary, Number"
```

Check before writing:
```
If ( Left ( FieldType ( Get(FileName) ; "Table::Field" ) ; 10 ) = "Calculated" ;
  "Read-only" ; "Writable"
)
```

---

## GetNextSerialValue ( fileName ; fieldName )
Returns the next serial value that will be assigned to a field when a new record is created.  
Parameters: `fileName`; `fieldName` — fully qualified.  
Returns: text (the serial value as a string, since serials can have prefixes)

```
GetNextSerialValue ( Get(FileName) ; "Invoices::InvoiceNumber" )
// → "INV-1042"
```

Useful for displaying "next invoice number" before creating the record.

---

## LayoutIDs ( fileName )
Returns a return-delimited list of layout IDs for all layouts in the file.  
Parameters: `fileName`.  
Returns: text

```
LayoutIDs ( Get(FileName) )
// → 1¶2¶3¶...
```

---

## LayoutNames ( fileName )
Returns a return-delimited list of all layout names in the file.  
Parameters: `fileName`.  
Returns: text

```
LayoutNames ( Get(FileName) )
// → Contacts¶Contacts List¶Invoice¶Invoice List¶...
```

Check if a layout exists before navigating to it:
```
If ( PatternCount ( LayoutNames ( Get(FileName) ) ; "Archive" ) = 0 ;
  Show Custom Dialog [ "Layout 'Archive' not found" ] ;
  Go to Layout [ "Archive" ]
)
```

Count layouts:
```
ValueCount ( LayoutNames ( Get(FileName) ) )
```

---

## LayoutObjectNames ( fileName ; layoutName )
Returns a return-delimited list of all named layout objects on the specified layout.  
Parameters: `fileName`; `layoutName`.  
Returns: text

```
LayoutObjectNames ( Get(FileName) ; "Dashboard" )
// → ChartPanel¶SummaryTable¶RefreshButton¶...
```

Check before using `Navigate to Object` or `Refresh Object`:
```
If ( PatternCount ( LayoutObjectNames ( Get(FileName) ; Get(LayoutName) ) ; "myPanel" ) > 0 ;
  Navigate to Object [ Object Name: "myPanel" ]
)
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
Returns a return-delimited list describing all relationships for the specified table occurrence.  
Parameters: `fileName`; `tableName` — table occurrence name.  
Returns: text (each line: `relatedTableOccurrence¶criteriaField¶relatedField`)

```
RelationInfo ( Get(FileName) ; "Invoices" )
// → LineItems¶Invoices::InvoiceID¶LineItems::InvoiceID¶...
```

---

## ScriptIDs ( fileName )
Returns a return-delimited list of script IDs for all scripts in the file.  
Parameters: `fileName`.  
Returns: text

```
ScriptIDs ( Get(FileName) )
// → 1¶2¶3¶...
```

---

## ScriptNames ( fileName )
Returns a return-delimited list of all script names in the file.  
Parameters: `fileName`.  
Returns: text

```
ScriptNames ( Get(FileName) )
// → OnOpen¶ProcessInvoices¶SyncContacts¶...
```

Check if a script exists before calling:
```
If ( PatternCount ( ScriptNames ( Get(FileName) ) ; "SyncContacts" ) > 0 ;
  Perform Script [ "SyncContacts" ]
)
```

---

## TableIDs ( fileName )
Returns a return-delimited list of table IDs for all base tables in the file.  
Parameters: `fileName`.  
Returns: text

```
TableIDs ( Get(FileName) )
```

Table IDs are stable across renames — use as permanent references in tooling.

---

## TableNames ( fileName )
Returns a return-delimited list of base table names (not table occurrences) in the file.  
Parameters: `fileName`.  
Returns: text

```
TableNames ( Get(FileName) )
// → Contacts¶Invoices¶LineItems¶Products¶...
```

Difference from `FieldNames` with a TO name: `TableNames` returns base table names; the relationship graph may have multiple TOs per base table.

Check if a table exists:
```
PatternCount ( TableNames ( Get(FileName) ) ; "Archive" ) > 0
```

---

## ValueListIDs ( fileName )
Returns a return-delimited list of value list IDs in the file.  
Parameters: `fileName`.  
Returns: text

---

## ValueListItems ( fileName ; valueListName )
Returns a return-delimited list of the items in the specified value list.  
Parameters: `fileName`; `valueListName` — the name of the value list.  
Returns: text

```
ValueListItems ( Get(FileName) ; "Status Values" )
// → New¶Active¶On Hold¶Closed
```

Convert to JSON array for API payload:
```
JSONMakeArray ( ValueListItems ( Get(FileName) ; "Status Values" ) ; ¶ ; JSONString )
// → ["New","Active","On Hold","Closed"]
```

Validate a value against a value list:
```
PatternCount (
  ¶ & ValueListItems ( Get(FileName) ; "Status Values" ) & ¶ ;
  ¶ & Self & ¶
) > 0
```

---

## ValueListNames ( fileName )
Returns a return-delimited list of all value list names in the file.  
Parameters: `fileName`.  
Returns: text

```
ValueListNames ( Get(FileName) )
// → Status Values¶Product Categories¶Countries¶...
```

---

## WindowNames {( fileName )}
Returns a return-delimited list of names of all open windows. If `fileName` is omitted, returns windows for the current file.  
Parameters: `fileName` — optional; omit for current file.  
Returns: text

```
WindowNames                    // all windows in current file
WindowNames ( Get(FileName) ) // same, explicit
WindowNames ( "SharedData" )  // windows in a different open file
```

Check if a specific window is already open:
```
PatternCount ( WindowNames ; "Invoice Detail" ) > 0
// → 1 if the window exists, 0 if not
```

Close all windows except the current one:
```
// (In a script — iterate WindowNames and close each)
Set Variable [ $windows ; Value: WindowNames ]
Set Variable [ $current ; Value: Get(WindowName) ]
Set Variable [ $i ; Value: 1 ]
Loop
  Set Variable [ $w ; Value: GetValue ( $windows ; $i ) ]
  Exit Loop If [ $w = "" ]
  If [ $w ≠ $current ]
    Select Window [ Name: $w ]
    Close Window []
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
    fields = FieldNames ( Get(FileName) ; "Contacts" ) ;
    i = 1 ; dict = ""
  ] ;
  i ≤ ValueCount ( fields ) ;
  [
    f    = GetValue ( fields ; i ) ;
    type = FieldType ( Get(FileName) ; f ) ;
    dict = dict & f & " → " & type & ¶ ;
    i    = i + 1
  ] ;
  Trim ( dict )
)
```

**Confirm file and layout exist before navigating (safe cross-file open):**
```
If [ PatternCount ( DatabaseNames ; "SharedData" ) = 0 ]
  Open File [ "SharedData" ]
  Pause/Resume Script [ Duration: 0.5 ]
End If
If [ PatternCount ( LayoutNames ( "SharedData" ) ; "Reports" ) > 0 ]
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
Last verified: 2026-06 against live Claris Help Centre.

> **Note:** `CipherEncrypt`, `CipherDecrypt`, `CipherGenerateKey`, `ContainerDecryptSalt`, and `VerifyCertificate` were removed in FileMaker 19. Use the `Crypt*` family instead.

---

## Base64Decode ( text {; fileNameWithExtension } )

Returns container or text. Decodes a Base64-encoded string back to binary (container) or plain text. Supply `fileNameWithExtension` to store the result as a named container file.

```
Base64Decode ( Base64Encode ( myContainer ) )   // round-trip: recovers original data

// Store as a named PNG container:
Base64Decode ( encodedText ; "logo.png" )
```

---

## Base64Encode ( data )

Returns text. Encodes any data (text or container) as a Base64 string. Useful for REST API payloads and email attachments.

```
Base64Encode ( Invoice::Signature )   // → "iVBORw0KGgoAAAANS…"
Base64Encode ( "Hello" )              // → "SGVsbG8="
```

---

## Base64EncodeRFC ( RFCNumber ; data )

Returns text. Like `Base64Encode` but lets you choose the RFC variant. Common values: `4648` (standard), `4648S` (URL-safe, no padding), `2045` (MIME, 76-char line breaks).

```
Base64EncodeRFC ( 4648 ; myContainer )   // Standard Base64
Base64EncodeRFC ( "4648S" ; myContainer ) // URL-safe, no padding
Base64EncodeRFC ( 2045 ; myContainer )   // MIME-safe for email
```

---

## CryptAuthCode ( data ; algorithm ; key )

Returns container (binary HMAC). Generates a Hash-based Message Authentication Code for verifying data integrity. Algorithm options: `"SHA256"`, `"SHA384"`, `"SHA512"`, `"MD5"`, `"SHA1"`.

```
CryptAuthCode ( payload ; "SHA256" ; secretKey )
// → binary HMAC — encode for transmission:
Base64Encode ( CryptAuthCode ( payload ; "SHA256" ; secretKey ) )
```

---

## CryptDecrypt ( container ; key )

Returns container. Decrypts container data previously encrypted with `CryptEncrypt`. Key must match.

```
CryptDecrypt ( Secrets::EncryptedDoc ; encryptionKey )
```

---

## CryptDecryptBase64 ( text ; key )

Returns container. Decrypts Base64-encoded text previously produced by `CryptEncryptBase64`.

```
CryptDecryptBase64 ( Secrets::EncryptedBase64 ; encryptionKey )
```

---

## CryptDigest ( data ; algorithm )

Returns container (binary hash). Computes a one-way cryptographic hash. Algorithm options: `"SHA256"`, `"SHA384"`, `"SHA512"`, `"MD5"`, `"SHA1"`.

```
// SHA-256 fingerprint of a field, hex-encoded:
HexEncode ( CryptDigest ( Document::Body ; "SHA256" ) )
```

---

## CryptEncrypt ( data ; key )

Returns container. Encrypts data using AES-256-GCM. Store the key separately and securely.

```
CryptEncrypt ( SensitiveData::SSN ; encryptionKey )
```

---

## CryptEncryptBase64 ( data ; key )

Returns text (Base64). Encrypts data and Base64-encodes the result — convenient for storing encrypted text in a text field.

```
CryptEncryptBase64 ( SensitiveData::CreditCard ; encryptionKey )
// → Base64 string, safe to store in a text field
```

---

## CryptGenerateSignature ( data ; algorithm ; privateRSAKey ; keyPassword )

Returns container (binary signature). Signs data using an RSA private key. Algorithm: `"SHA256"`, `"SHA384"`, `"SHA512"`.

```
CryptGenerateSignature ( payload ; "SHA256" ; rsaPrivateKeyContainer ; keyPassword )
```

---

## CryptVerifySignature ( data ; algorithm ; publicRSAKey ; signature )

Returns number. Verifies an RSA signature against the public key. Returns `1` if valid, `0` if not.

```
If ( CryptVerifySignature ( payload ; "SHA256" ; rsaPublicKey ; signatureContainer ) = 1 ;
  "Signature valid" ;
  "INVALID — data may have been tampered with"
)
```

---

## GetContainerAttribute ( field ; attributeName )

Returns text. Reads metadata from a container field. Common `attributeName` values: `"filename"`, `"filesize"`, `"width"`, `"height"`, `"content type"`, `"image EXIF"`.

```
GetContainerAttribute ( Photos::Image ; "filename" )   // → "headshot.jpg"
GetContainerAttribute ( Photos::Image ; "filesize" )   // → "204800"
GetContainerAttribute ( Photos::Image ; "width" )      // → "1200"
GetContainerAttribute ( Photos::Image ; "content type" ) // → "image/jpeg"
```

---

## GetHeight ( field )

Returns number (pixels). Returns the pixel height of the image stored in a container field. Returns `0` for non-image content.

```
GetHeight ( Products::Photo )   // → 600
```

---

## GetLiveText ( container ; language )

Returns text. Performs on-device OCR and returns recognised text from an image. Requires FileMaker Go or FileMaker Pro 19.4+. `language` is a BCP 47 tag e.g. `"en"`, `"ja"`, `"fr"`.

```
GetLiveText ( CapturedImage ; "en" )
// → "Invoice #1042¶Total: $450.00"
```

---

## GetLiveTextAsJSON ( container ; language )

Returns text (JSON). Like `GetLiveText` but includes bounding-box coordinates for each recognised text region.

```
Let ( json = GetLiveTextAsJSON ( CapturedImage ; "en" ) ;
  JSONGetElement ( json ; "[0].text" )
)
// → first recognised text block
```

---

## GetTextFromPDF ( container )

Returns text. Extracts embedded text from a PDF stored in a container. Does not OCR scanned pages — the PDF must contain actual text.

```
GetTextFromPDF ( Documents::Contract )
// → full body text of the PDF
```

Search for a clause:
```
PatternCount ( GetTextFromPDF ( Documents::Contract ) ; "indemnification" ) > 0
```

---

## GetThumbnail ( field ; width ; height )

Returns container. Generates a thumbnail of the container image scaled to fit within `width` × `height` pixels, preserving aspect ratio.

```
GetThumbnail ( Products::Photo ; 100 ; 100 )   // → container with ≤100×100px image
```

---

## GetWidth ( field )

Returns number (pixels). Returns the pixel width of the image stored in a container field. Returns `0` for non-image content.

```
GetWidth ( Products::Photo )   // → 1200
```

---

## HexDecode ( data {; fileNameWithExtension } )

Returns container or text. Decodes a hexadecimal-encoded string back to binary. Inverse of `HexEncode`.

```
HexDecode ( HexEncode ( myContainer ) )   // round-trip
HexDecode ( hexString ; "document.pdf" )  // restore as named PDF container
```

---

## HexEncode ( data )

Returns text. Encodes any data as a lowercase hexadecimal string. Useful for hashing workflows and debugging binary data.

```
HexEncode ( CryptDigest ( payload ; "SHA256" ) )
// → "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
```

---

## ReadQRCode ( container )

Returns text. Decodes a QR code or barcode from an image in a container field. Returns the encoded text value.

```
ReadQRCode ( ScannedBadge::Image )   // → "EMP-00423"
```

---

## TextDecode ( container ; encoding )

Returns text. Converts container data (raw bytes) to a text string using the specified encoding. Common encodings: `"UTF-8"`, `"UTF-16"`, `"ISO-8859-1"`, `"Shift-JIS"`.

```
TextDecode ( importedFile ; "UTF-8" )    // read a UTF-8 text file from container
TextDecode ( legacyFile ; "ISO-8859-1" ) // decode Latin-1 encoded file
```

---

## TextEncode ( text ; encoding ; lineEndings )

Returns container. Converts text to container data using the specified encoding and line-ending style. `lineEndings`: `"Windows"` (CRLF), `"Mac"` (CR), `"Unix"` (LF).

```
TextEncode ( myText ; "UTF-8" ; "Unix" )    // → container for export or sending
TextEncode ( myText ; "UTF-16" ; "Windows" ) // Windows UTF-16 text file
```

---

## VerifyContainer ( field )

Returns number. Checks the integrity of container data. Returns `1` if the data is intact, `0` if corrupted or missing.

```
If ( VerifyContainer ( Documents::Attachment ) = 0 ;
  "⚠️ Container data is corrupted or missing" ;
  "OK"
)
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
  computed   = Base64Encode ( CryptAuthCode ( payload ; "SHA256" ; secret ) ) ;
  received   = WebhookData::HmacHeader
] ;
  computed = received
)
// → 1 if payload is authentic
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
Let ( raw = GetLiveText ( Scan::Image ; "en" ) ;
  // Find the line that starts with "Invoice #"
  Let ( lines = Substitute ( raw ; ¶ ; "|" ) ;
    // … parse with custom function or filter
    raw
  )
)
```
