# Specialty Functions — Examples (Aggregate, Japanese, Mobile, Miscellaneous)

## Contents
- Aggregate Functions
  - Average ( field {; field...} )
  - Count ( field {; field...} )
  - List ( field {; field...} )
  - Max ( field {; field...} )
  - Min ( field {; field...} )
  - StDev ( field {; field...} )
  - StDevP ( field {; field...} )
  - Sum ( field {; field...} )
  - Variance ( field {; field...} )
  - VarianceP ( field {; field...} )
  - Common patterns
- Japanese Functions
  - DayNameJ ( date )
  - MonthNameJ ( date )
  - YearName ( date ; format )
  - Furigana ( text {; option } )
  - Hiragana ( text )
  - Katakana ( text )
  - KanaHankaku ( text )
  - KanaZenkaku ( text )
  - RomanHankaku ( text )
  - RomanZenkaku ( text )
  - KanjiNumeral ( text )
  - NumToJText ( number ; separator ; characterType )
  - Normalisation pattern (common data-entry workflow)
- Mobile Functions
  - GetAVPlayerAttribute ( attributeName )
  - GetSensor ( sensorName {; option1 ; option2 } )
  - Location ( accuracy {; timeout } )
  - LocationValues ( accuracy {; timeout } )
  - RangeBeacons ( UUID {; timeout ; major ; minor } )
- Miscellaneous Functions
  - ConvertFromFileMakerPath ( filemakerPath ; format )
  - ConvertToFileMakerPath ( standardPath ; format )
  - GetAddonInfo ( addonID )
  - GetBaseTableName ( field )
  - GetFieldName ( field )
  - GetLayoutObjectAttribute ( objectName ; attributeName {; repetitionNumber ; portalRowNumber } )
  - GetLayoutObjectOwnerInfo ( objectID )
  - GetRecordIDsFromFoundSet ( type { ; tableOccurrenceOrPortal } )
  - LayoutObjectUUID
- Persistent Data Functions
  - GetPersistentData ( name ; instanceID )
  - ListPersistentDataIDs ( name )

---

# FileMaker Aggregate Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/aggregate-functions.html  
All 10 aggregate functions with verified syntax, parameters, return types, and usage patterns.  

**Overview:** Aggregate functions operate across repeating field repetitions OR across related records via a relationship. When passed a related field (e.g. `LineItems::Total`), they aggregate across all related records in the current relationship context — this is how sub-totals, counts, and lists are built without scripting.

**Key distinction:**
- `Sum ( LineItems::Amount )` — sums all related LineItems records
- `Sum ( MyField )` — sums all repetitions of a repeating field
- In a self-join or looping context, the relationship context determines which records are included

---

## Average ( field {; field...} )
Returns the arithmetic mean of all non-empty values.  
Parameters: one or more field references (related or repeating).  
Returns: number
```
Average(Exams::Score)
// → the student's average score for all exams she has taken
```
Exclude outliers with a filtered relationship (define a relationship with a range criterion):
```
Average ( FilteredScores::Score )
```
In a summary context — Average of a non-related field uses repetitions:
```
Average ( Survey::Responses )
// → mean of repetitions 1–n
```
---

## Count ( field {; field...} )
Returns the number of non-empty values.  
Parameters: one or more fields.  
Returns: number
```
Count(Payments::Payment)
// → the number of payments made on an account
```
Count with a condition — use a calculation field on the related table:
```
// In LineItems table: IsActive = If ( Status = "Active" ; 1 ; "" )
Count ( LineItems::IsActive )
// → number of active line items only
```
Difference from `Get(FoundCount)`: Count traverses the relationship; Get(FoundCount) reflects the current layout's found set.

---

## List ( field {; field...} )
Returns the non-blank values as a return-delimited list (no trailing ¶). Accepts related fields, repeating fields, several fields, and variables.  
Returns: text
```
List ( Field1 ; Field2 )
// → white¶black   (Field1 = white, Field2 = black)

List ( Related::Field4 )
// → 100¶200¶300   (every related record, in the relationship's sort order)
```
⚠️ With **several** related fields, List uses only the **first** related record — `List ( Contacts::FirstName ; Contacts::LastName )` → `Alice¶Smith`, not every contact. To list a combination per record, define a calculation in the related table and list that:
```
// In Contacts: FullLine = FirstName & " " & LastName
List ( Contacts::FullLine )
// → Alice Smith¶Bob Jones
```
Comma-separated string:
```
Substitute ( List ( Tags::TagName ) ; ¶ ; ", " )
// → Design, Development, Marketing
```
---

## Max ( field {; field...} )
Returns the largest value across all non-empty values.  
Parameters: one or more fields.  
Returns: number, date, time, or timestamp (matches field type)
```
Max(Payments::PaymentDate)
// → the most recent date a payment was made on an account
```
```
Max ( Scores::Value )
// → highest score
```
---

## Min ( field {; field...} )
Returns the smallest value across all non-empty values.  
Parameters: one or more fields.  
Returns: number, date, time, or timestamp
```
Min(Bids::Price)
// → the lowest bid submitted for a contract
```
```
Min ( Temperatures::Reading )
```
---

## StDev ( field {; field...} )
Returns the sample standard deviation (divides by n−1).  
Parameters: one or more fields.  
Returns: number
```
StDev ( Measurements::Value )
// → sample std dev of related measurements
```
Used in quality control / statistical process control calcs.

---

## StDevP ( field {; field...} )
Returns the population standard deviation (divides by n).  
Parameters: one or more fields.  
Returns: number
```
StDevP ( Measurements::Value )
// → population std dev (use when related records = the entire population)
```
---

## Sum ( field {; field...} )
Returns the total of all non-empty numeric values.  
Parameters: one or more fields.  
Returns: number
```
Sum(LineItems::ExtendedPrice)
// totals the amounts for all items on the invoice.
```
Conditional sum — use a calc field on the related table:
```
// In LineItems: TaxableAmount = If ( Taxable = 1 ; ExtendedPrice ; 0 )
Sum ( LineItems::TaxableAmount )
// → sum of only taxable items
```
Running total in a portal (sorted relationship):
```
// Place in a portal row calc field on LineItems layout
Sum ( LineItems_sorted::ExtendedPrice )
// sums all rows above + current when relationship is ordered by row number
```
---

## Variance ( field {; field...} )
Returns the sample variance (square of StDev — divides by n−1).  
Parameters: one or more fields.  
Returns: number
```
Variance(table::Scores)
// → 1.66666666...
```
---

## VarianceP ( field {; field...} )
Returns the population variance (square of StDevP — divides by n).  
Parameters: one or more fields.  
Returns: number
```
VarianceP(table::Scores)
// → 1.25
```
---

## Common patterns

**Invoice sub-total, tax, total:**
```
// Calculation fields in Invoices, via the LineItems relationship
Subtotal     = Sum ( LineItems::ExtendedPrice )
TaxAmount    = Sum ( LineItems::TaxableAmount ) * TaxRate
InvoiceTotal = Subtotal + TaxAmount
```
**Count related with status filter:**
```
// Relationship Invoice_OpenItems: LineItems where Status = "Open"
Count ( Invoice_OpenItems::ItemID )
```
**Duplicate detection:**
```
// Self-join Contacts_sameEmail relates Email = Email
Count ( Contacts_sameEmail::ContactID ) > 1
```
**Summary string:**
```
Let ( [
  names = List ( TeamMembers::FullName ) ;
  total = Count ( TeamMembers::MemberID )
] ;
  Substitute ( names ; ¶ ; ", " ) & " (" & total & " members)"
)
```
**Most recent related date:**
```
Max ( Interactions::InteractionDate )
```
**Running total in a portal / list:** sorting a relationship doesn't limit which records it returns. Use a self-join whose predicates select "this and earlier" rows — `InvoiceID = InvoiceID` **and** `LineNo ≥ LineNo` — then:
```
Sum ( LineItems_upToThis::ExtendedPrice )
```
(For a report, a running-total summary field is simpler.)

---

# FileMaker Japanese Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/japanese-functions.html  
All 12 Japanese language functions with verified syntax, parameters, return types, and usage patterns.  

**Overview:** FileMaker's Japanese functions handle text transformations specific to the Japanese writing system. They cover conversion between kana scripts (hiragana ↔ katakana), width normalisation (hankaku ↔ zenkaku), kanji numeral rendering, number-to-Japanese-text conversion, furigana generation, and Japanese calendar / date-name functions. These functions are particularly important for Japanese-locale databases where data may be entered in multiple scripts or character widths.

**Japanese writing system quick reference:**
- **Hiragana** (ひらがな) — cursive phonetic script; typically used for native Japanese words and grammar
- **Katakana** (カタカナ) — angular phonetic script; typically used for foreign loan words
- **Kanji** (漢字) — Chinese-origin logographic characters
- **Hankaku** (半角) — half-width characters (standard ASCII width)
- **Zenkaku** (全角) — full-width characters (double-width, standard in Japanese typography)
- **Furigana** (振り仮名) — phonetic reading annotations (ruby text) for kanji

---

## DayNameJ ( date )
Returns the Japanese weekday name.  
Returns: text
```
DayNameJ ( Date ( 1 ; 1 ; 2021 ) )
// → 金曜日
```
---

## MonthNameJ ( date )
Returns the Japanese month name.  
Returns: text
```
MonthNameJ ( Date ( 6 ; 6 ; 2019 ) )
// → 6月
```
---

## YearName ( date ; format )
Returns the Japanese era (emperor) year for a date. `format`: `0` long era name · `1` abbreviated era in parentheses · `2` roman letter (M, T, S, H, R). Any other value means 0. Dates before 8 Sept 1868 return the Western (Seireki) year. The first year of an era shows as 元 with format 1.  
Returns: text
```
YearName ( Date ( 7 ; 15 ; 2026 ) ; 0 )
// → 令和8

YearName ( Date ( 7 ; 15 ; 2026 ) ; 1 )
// → (令)8

YearName ( Date ( 7 ; 15 ; 2026 ) ; 2 )
// → R8

YearName ( Date ( 5 ; 1 ; 2019 ) ; 1 )
// → (令)元
```
Eras: Reiwa (令和) from 1 May 2019 · Heisei (平成) 1989–2019 · Shōwa (昭和) 1926–1989.

---

## Furigana ( text {; option } )
Converts Japanese text (including kanji) to its reading — useful as a sort key, because kanji sort meaningfully only by reading. *Originated: 14.0*  
`option`: `1` hiragana · `2` full-width katakana · `3` full-width romaji · `4` half-width katakana · `5` half-width romaji. Omitted or any other value → hiragana.  
Returns: text
```
Furigana ( "東京都" )
// → とうきょうと

Furigana ( "東京都" ; 2 )
// → トウキョウト

Furigana ( "東京都" ; 4 )
// → ﾄｳｷｮｳﾄ

Furigana ( "東京都" ; 5 )
// → toukyouto
```
---

## Hiragana ( text )
Converts katakana — half-width and full-width — to hiragana.  
Returns: text
```
Hiragana ( "カタカナ" )
// → かたかな

Hiragana ( "ｶﾀｶﾅ" )
// → かたかな
```
---

## Katakana ( text )
Converts hiragana to full-width (zenkaku) katakana.  
Returns: text
```
Katakana ( "ひらがな" )
// → ヒラガナ
```
---

## KanaHankaku ( text )
Converts full-width (zenkaku) katakana to half-width (hankaku) katakana.  
Returns: text
```
KanaHankaku ( "カタカナ" )
// → ｶﾀｶﾅ
```
---

## KanaZenkaku ( text )
Converts half-width (hankaku) katakana to full-width (zenkaku) katakana.  
Returns: text
```
KanaZenkaku ( "ｶﾀｶﾅ" )
// → カタカナ
```
---

## RomanHankaku ( text )
Converts full-width (zenkaku) letters, digits and symbols to half-width (standard ASCII).  
Returns: text
```
RomanHankaku ( "Ｍａｃｉｎｔｏｓｈ" )
// → Macintosh
```
---

## RomanZenkaku ( text )
Converts half-width letters, digits and symbols to full-width (zenkaku).  
Returns: text
```
RomanZenkaku ( "Macintosh" )
// → Ｍａｃｉｎｔｏｓｈ
```
---

## KanjiNumeral ( text )
Converts Arabic digits in text to kanji digits, digit by digit (no place values — for those, use NumToJText).  
Returns: text
```
KanjiNumeral ( "2026年" )
// → 二〇二六年
```
---

## NumToJText ( number ; separator ; characterType )
Converts a number to Japanese text. Blank or out-of-range values for either option mean 0.  
`separator`: `0` none · `1` comma every 3 digits · `2` 万 / 億 units · `3` every unit (十, 百, 千, 万, 億)  
`characterType`: `0` half-width digits · `1` full-width digits · `2` kanji · `3` traditional kanji (大字)  
Returns: text
```
NumToJText ( 123456789 ; 1 ; 0 )
// → 123,456,789

NumToJText ( 123456789 ; 2 ; 0 )
// → 1億2345万6789

NumToJText ( 123456789 ; 3 ; 2 )
// → 一億二千三百四十五万六千七百八十九

NumToJText ( 2026 ; 3 ; 3 )
// → 弐阡弐拾六
```
---

## Normalisation pattern (common data-entry workflow)

Japanese users may enter the same data in multiple character forms. A normalisation calculation ensures consistent storage:
```
Let ( [
  // Step 1: convert any hankaku katakana → zenkaku katakana
  s1 = KanaZenkaku ( InputName ) ;
  // Step 2: convert any zenkaku roman → hankaku (standard ASCII)
  s2 = RomanHankaku ( s1 ) ;
  // Step 3: convert hiragana → katakana (store katakana as canonical)
  s3 = Katakana ( s2 )
] ;
  s3
)
```
---

# FileMaker Mobile Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/mobile-functions.html  
All 5 mobile functions with verified syntax, parameters, return types, and usage patterns.  

**Overview:** these functions read device hardware in **FileMaker Go** (iOS / iPadOS): location, sensors, AV player state and iBeacons. Elsewhere they return empty, so branch on the client first.

**Platform guard pattern:**
```
// Check before calling any mobile function:
If ( Left ( Get ( ApplicationVersion ) ; 2 ) = "Go" ;   // "Go …" on iPhone, "Go_iPad …" on iPad
  Location ( 10 ) ;
  "Not available on this platform"
)
```
---

## GetAVPlayerAttribute ( attributeName )
FileMaker Go only. Returns a setting of the audio, video or image currently (or most recently) played. Before anything has played: empty or 0. *Originated: 14.0*  
Main attributes:
- `playbackState` — 0 stopped · 1 playing · 2 paused
- `position`, `startOffset`, `endOffset`, `duration` — seconds
- `sourceType` (0 none · 1 URL · 2 field · 3 layout object · 4 active object) and `source`
- `presentation` — 0 embedded · 1 full screen · 2 full screen only · 3 audio only · 4 embedded only
- `volume`, `zoom`, `hideControls`, `disableInteraction`, `pictureInPicture`, `externalPlayback` …
- `triggerEvent`, `triggerEventDetail` — why OnObjectAVPlayerChange / OnFileAVPlayerChange fired
- `all` — every attribute

Returns: text or number
```
If [ GetAVPlayerAttribute ( "playbackState" ) = 1 ]
    AVPlayer Set Playback State [ Stopped ]
End If
```
---

## GetSensor ( sensorName {; option1 ; option2 } )
FileMaker Go only (iOS / iPadOS). Returns a sensor reading; availability depends on the device. *Originated: 17.0*  
Sensor names (case as shown):
- Battery: `batteryLevel` (0.0–1.0), `batteryStatus` (1 unplugged · 2 charging · 3 full)
- Location: `location`, `locationValues` — option1 accuracy (m), option2 timeout (s)
- Motion: `attitude` (roll, pitch, yaw), `rotationRate`, `accelerationByUser`, `accelerationByGravity`, `speed`, `heading`
- Magnetic: `magneticField`, `compassMagneticHeading`, `compassTrueHeading`
- Pedometer: `stepCount`, `stepDistance`, `stepFloorsUp`, `stepFloorsDown` — option1 seconds to look back
- `airPressure`
- `available` — lists the sensors this device supports

Multi-value readings come back as return-delimited lists. Returns: text or number.
```
GetSensor ( "stepCount" ; 3600 )
// → 8000 if the user took 8000 steps in the past hour

GetSensor ( "available" )
```
---

## Location ( accuracy {; timeout } )
FileMaker Go only — FileMaker Pro returns empty. Returns one line: `latitude, longitude, accuracy` (accuracy in metres achieved). `accuracy` is the requested accuracy in metres; `timeout` is in seconds, **default 60**. Returns empty if no location is received.  
Returns: text
```
Location ( 100 ; 40 )
// → +37.343123, -122.017593, +65.000000
```
Store coordinates (split on the commas):
```
Set Variable [ $loc ; Value: Substitute ( Location ( 20 ; 30 ) ; ", " ; ¶ ) ]
Set Field [ Record::Latitude  ; GetValue ( $loc ; 1 ) ]
Set Field [ Record::Longitude ; GetValue ( $loc ; 2 ) ]
```
For separate values plus altitude, use LocationValues.

---

## LocationValues ( accuracy {; timeout } )
FileMaker Go only. Returns **six** return-delimited values: latitude · longitude · altitude (m) · horizontal accuracy (m) · vertical accuracy (m) · age of the reading (minutes). Timeout default 60 s.  
Returns: text
```
LocationValues ( 100 ; 40 )
// → 37.406489¶-121.983428¶0.0545050¶65¶10¶0.001236
```
Reject imprecise fixes:
```
Let ( lv = LocationValues ( 10 ; 8 ) ;
  If ( GetValue ( lv ; 4 ) > 50 ;
    "GPS fix too imprecise (±" & GetValue ( lv ; 4 ) & " m)" ;
    JSONSetElement ( "{}" ;
      [ "lat" ; GetValue ( lv ; 1 ) ; JSONNumber ] ;
      [ "lng" ; GetValue ( lv ; 2 ) ; JSONNumber ] ;
      [ "alt" ; GetValue ( lv ; 3 ) ; JSONNumber ]
    )
  )
)
```
---

## RangeBeacons ( UUID {; timeout ; major ; minor } )
FileMaker Go only. Returns one line per nearby iBeacon matching `UUID` (and optional major / minor), as **comma-separated** values: UUID, major, minor, proximity, accuracy (m; negative = unknown), RSSI (dB). `timeout` defaults to **5 seconds**. *Originated: 15.0*  
`proximity`: `0` unknown · `1` immediate · `2` near · `3` far. Empty if nothing matches or Location Services is off; `?` for an invalid query.  
Returns: text
```
RangeBeacons ( "D9B9EC1F-XXXX-YYYY-80A9-1E39D4CEA95C" )
// → D9B9EC1F-XXXX-YYYY-80A9-1E39D4CEA95C, 5, 1, 3, 14.68, -79
```
---

# FileMaker Miscellaneous Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/miscellaneous-functions.html  
All 9 miscellaneous functions with verified syntax, parameters, return types, and usage patterns.  

**Overview:** The Miscellaneous category contains utility functions that do not fit neatly into other categories. They cover path conversion (FileMaker ↔ native OS formats), add-on metadata, field name introspection, layout object attribute inspection, found-set record ID retrieval, and layout object UUID access. Several are essential for dynamic scripting and add-on development.

---

## ConvertFromFileMakerPath ( filemakerPath ; format )
Converts a FileMaker path (`file:`, `filemac:`, `filewin:`, `image:`, `movie:`, `fmnet:` …) to a standard path. *Originated: 19.0*  
`format` (named constant or number): `PosixPath` (1) — `/directory/file` · `WinPath` (2) — `C:\directory\file` · `URLPath` (3) — `file:///…`, or `fmp://host/…` for an `fmnet:` path. Returns `?` if the path can't be converted to that format.  
Returns: text
```
ConvertFromFileMakerPath ( "file:/Macintosh HD/etc/hosts" ; PosixPath )
// → /etc/hosts

ConvertFromFileMakerPath ( "file:/Macintosh HD/etc/hosts" ; URLPath )
// → file:///etc/hosts
```
Pass a native path to a plug-in or shell command:
```
ConvertFromFileMakerPath ( Get ( DocumentsPath ) & "export.csv" ; PosixPath )
```
---

## ConvertToFileMakerPath ( standardPath ; format )
The reverse: converts a standard path in `format` (`PosixPath` 1, `WinPath` 2, `URLPath` 3) to a FileMaker path. `fmp://` URLs become `fmnet:` paths; everything else gets the `file` prefix. *Originated: 19.0*  
Returns: text
```
ConvertToFileMakerPath ( "/Users/John Smith/Documents/test.xlsx" ; PosixPath )
// → file:/Macintosh HD/Users/John Smith/Documents/test.xlsx   (Mac, boot volume "Macintosh HD")

ConvertToFileMakerPath ( "C:\Users\John Smith\Documents\test.xlsx" ; WinPath )
// → file:/C:/Users/John Smith/Documents/test.xlsx
```
---

## GetAddonInfo ( addonID )
Returns JSON describing an installed or packaged add-on, looked up by its UUID. Keys: `APIVers`, `Installed` (`Name`, `UUID`, `UsesLayoutPayload`, `UsesRelationship`) and `Package` (`Name`, `UUID`). *Originated: 19.2.2*  
Returns: text (JSON)
```
GetAddonInfo ( "B79DDD6D-DDF2-4370-A3C9-F9DEF2C52992" )
```
Pair with GetLayoutObjectOwnerInfo to find which add-on a layout object belongs to.

---

## GetBaseTableName ( field )
Returns the name of the **base table** (not the table occurrence) that contains the specified field. Useful when you have multiple table occurrences pointing to the same base table and need to identify the actual table.  
Parameters: `field` — a field reference (not a field name string — use the field itself as the parameter).  
Returns: text
```
GetBaseTableName(x)
// → the name of a table reference passed into a custom function as parameter `x`

GetBaseTableName(Evaluate(<fieldName>))
// → the name of a table based on the data stored in `<fieldName>`

GetBaseTableName(Evaluate(Get(ActiveFieldName)))
// → the table name for a field that has the focus when executed
```
Validation: ensure a relationship points to the expected base table:
```
If ( GetBaseTableName ( RelatedTable::ID ) ≠ "Invoices" ;
  "Warning: unexpected base table" ; "" )
```
---

## GetFieldName ( field )
Returns the **fully qualified field name** (TableOccurrence::FieldName) of a field reference as a text string. Unlike referencing a field directly, this works even when the field's name or table occurrence name changes — as long as the calculation is re-evaluated. Critical for dynamic scripting patterns.  
Parameters: `field` — a field reference.  
Returns: text
```
GetFieldName(x)
// → the name of a field reference passed into a custom function as parameter `x`

GetFieldName(Evaluate(<fieldName>))
// → the name of a field based on the data stored in `<fieldName>`

GetFieldName(Evaluate(Get(ActiveFieldName)))
// → the fully qualified name of the field that has the focus when executed
```
Dynamic sort/find using field names:
```
// Store the field name to sort by
Let ( sortField = GetFieldName ( Invoices::DueDate ) ;
  // Pass sortField to a script parameter for dynamic sorting
  sortField
)
```
Self-referential validation (field knows its own name):
```
Let ( fieldName = GetFieldName ( Self ) ;
  // Log or display which field triggered this calc
  fieldName
)
```
---

## GetLayoutObjectAttribute ( objectName ; attributeName {; repetitionNumber ; portalRowNumber } )
Returns an attribute of a **named** object on the current layout. *Originated: 8.5*  
Attributes:
- State: `objectType`, `hasFocus`, `containsFocus`, `isFrontPanel`, `isActive`, `isObjectHidden` (1 when hidden for the current record)
- Geometry: `bounds` (space-separated: left top right bottom rotation), `left`, `right`, `top`, `bottom`, `width`, `height`, `rotation`, `startPoint`, `endPoint`
- Content: `source` (web viewer URL, field name, container reference…), `content` (displayed content), `enclosingObject`, `containedObjects`

Returns: text
```
Set Field [ Search::Homepage ; GetLayoutObjectAttribute ( "Web Viewer" ; "source" ) ]

If ( GetLayoutObjectAttribute ( "Sidebar" ; "isObjectHidden" ) ; "Sidebar is hidden" ; "Sidebar is showing" )
```
---

## GetLayoutObjectOwnerInfo ( objectID )
Returns JSON about who owns a layout object — the layout it's on and, if any, the add-on instance it belongs to. `objectID` is the object's **UUID** (see LayoutObjectUUID) or an add-on instance's owner ID, as text. *Originated: 19.2.2*  
Returns: text (JSON — `APIVers`, `Object.UUID`, `Object.Index`, `Object.Name`, `Object.Owners.Add-on.InstanceID`, `Object.Owners.Layout.UUID` / `.Name`)
```
GetLayoutObjectOwnerInfo ( "970E9CAE-D6FA-40DE-ACFA-14D110731F82" )
```
---

## GetRecordIDsFromFoundSet ( type { ; tableOccurrenceOrPortal } )
Returns the record IDs of the current found set, in its current order. With the optional second parameter (FM 26) it returns the records related through a table occurrence (in the relationship's sort order), or shown in a named portal (with its filter and sort). *Originated: 22.0*  
Returns: text

| type | Constant | Result |
|---|---|---|
| 0 | `ValueNumber` | return-delimited list: `1¶5¶21¶22¶23¶7` |
| 1 | `JSONString` | `["1","5","21","22","23","7"]` |
| 2 | `JSONNumber` | `[1,5,21,22,23,7]` |
| 3 | `ValueNumberRanges` | `1¶5¶21-23¶7` |
| 4 | `JSONStringRanges` | `["1","5","21-23","7"]` |

An empty found set returns `""` (types 0 and 3) or `[]` (JSON types). Pass the result to **Go to List of Records** to restore the found set later.
```
// Is a record in the found set?
PatternCount ( ¶ & GetRecordIDsFromFoundSet ( 0 ) & ¶ ; ¶ & $targetID & ¶ ) > 0
```
Pass the found set to a script:
```
JSONSetElement ( "{}" ;
  [ "recordIDs" ; GetRecordIDsFromFoundSet ( JSONNumber ) ; JSONArray ] ;
  [ "layout"    ; Get ( LayoutName ) ; JSONString ]
)
```
---

## LayoutObjectUUID
Returns the UUID of the layout object whose calculation is being evaluated. Works **only** in a web viewer's **Web Address** calculation — anywhere else, including scripts, it returns `?`. *Originated: 19.2.2*  
Returns: text
```
If ( LayoutObjectUUID = "393877C5-D0A2-43D0-88B5-08F9305852DA" ; 1 ; 0 )
// → 1 in the Web Address box of the web viewer with that UUID
```
Pass the web viewer's own UUID to its JavaScript:
```
"data:text/html,<script>var UUID = " & Quote ( LayoutObjectUUID ) & ";</script>…"
```
---

# FileMaker Persistent Data Functions — Syntax & Examples (FM 26+)

Source: https://help.claris.com/en/pro-help/content/persistent-data-functions.html  
2 persistent data functions, introduced in FileMaker Pro 26.

**Overview:** the persistent data store is a set of named values saved in the file's **schema**, not its record data. Entries persist across sessions until deleted and are shared by every user of the file. Each entry is a **name** plus an optional **instance ID** (a namespace, e.g. an add-on instance), holding any FileMaker data type.
- Write or delete with the **Configure Persistent Data** script step — needs **Full Access** (or a script granted it). Reading doesn't.
- Names and instance IDs aren't case-sensitive.
- Entries travel with a clone, but the **Data Migration Tool does not copy them** (they're schema, not record data) — re-create them after a migration.

---

## GetPersistentData ( name ; instanceID )
Returns the stored value, in the data type it was stored with. **If no entry matches, returns `?`** (error 10), not empty. `""` as instanceID matches an entry stored without one. *Originated: 26.0*  
Returns: text, number, date, time, timestamp or container
```
GetPersistentData ( "AppVersion" ; "" )
// → 2.1.0
```
Fall back to a default when the entry doesn't exist:
```
Let ( config = GetPersistentData ( "com.example.settings" ; $instanceID ) ;
  If ( config = "?" ; "{}" ; config )
)
```
---

## ListPersistentDataIDs ( name )
Returns the instance IDs stored under `name`, in creation order. An entry with an empty instance ID shows as a blank line. Empty if there are none. *Originated: 26.0*  
Returns: text (return-delimited)
```
ListPersistentDataIDs ( "com.example.addon.script" )
// → 38EA3124-9CFD-4490-A634-A0A72A613145
//   E53DE16C-282E-44B0-BDB8-D59B15419D1B
//
//   B2F4C8D1-5A3E-4F9B-8C7D-1E6A9B4D2F5C
```
Read every instance (script):
```
Set Variable [ $ids ; Value: ListPersistentDataIDs ( "cachedResult" ) ]
Set Variable [ $i ; Value: 1 ]
Loop [ Flush: Always ]
  Exit Loop If [ $i > ValueCount ( $ids ) ]
  Set Variable [ $val ; Value: GetPersistentData ( "cachedResult" ; GetValue ( $ids ; $i ) ) ]
  # … process $val …
  Set Variable [ $i ; Value: $i + 1 ]
End Loop
```
Use the real instance ID returned by ListPersistentDataIDs — an invented one like `1` returns `?`.

---

