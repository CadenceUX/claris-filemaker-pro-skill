# Specialty Functions — Examples (Aggregate, Japanese, Mobile, Miscellaneous)

---

# FileMaker Aggregate Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/aggregate-functions.html  
All 10 aggregate functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** Aggregate functions operate across repeating field repetitions OR across related records via a relationship. When passed a related field (e.g. `LineItems::Total`), they aggregate across all related records in the current relationship context — this is how sub-totals, counts, and lists are built without scripting.

**Key distinction:**
- `Sum ( LineItems::Amount )` — sums all related LineItems records
- `Sum ( MyField )` — sums all repetitions of a repeating field
- In a self-join or looping context, the relationship context determines which records are included

---

## Average ( field {; field2…} )
Returns the arithmetic mean of all non-empty values.  
Parameters: one or more field references (related or repeating).  
Returns: number

```
Average ( LineItems::UnitPrice )
// → mean price across all related line items
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

## Count ( field {; field2…} )
Returns the number of non-empty values.  
Parameters: one or more fields.  
Returns: number

```
Count ( LineItems::ItemID )
// → number of related line item records (assuming ItemID is never empty)
```

Count with a condition — use a calculation field on the related table:
```
// In LineItems table: IsActive = If ( Status = "Active" ; 1 ; "" )
Count ( LineItems::IsActive )
// → number of active line items only
```

Difference from `Get(FoundCount)`: Count traverses the relationship; Get(FoundCount) reflects the current layout's found set.

---

## List ( field {; field2…} )
Returns a return-delimited list of all non-empty values, in record order.  
Parameters: one or more fields.  
Returns: text

```
List ( Contacts::FullName )
// → Alice Smith¶Bob Jones¶Carol White
```

Multi-field list (values from each field concatenated per record, then newline between records):
```
List ( Contacts::FirstName ; Contacts::LastName )
// → Alice¶Smith¶Bob¶Jones  (interleaved, not paired)
```

⚠️ List does NOT pair fields per record. For paired output, use a calculation field on the related table:
```
// In Contacts: FullLine = FirstName & " " & LastName
List ( Contacts::FullLine )
// → Alice Smith¶Bob Jones
```

Build a comma-separated string:
```
Substitute ( List ( Tags::TagName ) ; ¶ ; ", " )
// → Design, Development, Marketing
```

---

## Max ( field {; field2…} )
Returns the largest value across all non-empty values.  
Parameters: one or more fields.  
Returns: number, date, time, or timestamp (matches field type)

```
Max ( Invoices::DueDate )
// → latest due date across all related invoices
```

```
Max ( Scores::Value )
// → highest score
```

---

## Min ( field {; field2…} )
Returns the smallest value across all non-empty values.  
Parameters: one or more fields.  
Returns: number, date, time, or timestamp

```
Min ( Invoices::DueDate )
// → earliest due date (oldest outstanding invoice)
```

```
Min ( Temperatures::Reading )
```

---

## StDev ( field {; field2…} )
Returns the sample standard deviation (divides by n−1).  
Parameters: one or more fields.  
Returns: number

```
StDev ( Measurements::Value )
// → sample std dev of related measurements
```

Used in quality control / statistical process control calcs.

---

## StDevP ( field {; field2…} )
Returns the population standard deviation (divides by n).  
Parameters: one or more fields.  
Returns: number

```
StDevP ( Measurements::Value )
// → population std dev (use when related records = the entire population)
```

---

## Sum ( field {; field2…} )
Returns the total of all non-empty numeric values.  
Parameters: one or more fields.  
Returns: number

```
Sum ( LineItems::ExtendedPrice )
// → invoice subtotal from all related line items
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

## Variance ( field {; field2…} )
Returns the sample variance (square of StDev — divides by n−1).  
Parameters: one or more fields.  
Returns: number

```
Variance ( Returns::DaysToReturn )
// → variance of return turnaround days
```

---

## VarianceP ( field {; field2…} )
Returns the population variance (square of StDevP — divides by n).  
Parameters: one or more fields.  
Returns: number

```
VarianceP ( SurveyResponses::Rating )
```

---

## Common patterns

**Invoice sub-total, tax, total:**
```
// On Invoices layout, fields referencing LineItems relationship
Subtotal    = Sum ( LineItems::ExtendedPrice )
TaxAmount   = Sum ( LineItems::TaxableAmount ) * TaxRate
InvoiceTotal = Subtotal + TaxAmount
```

**Count related with status filter:**
```
// Relationship: Invoice_OpenItems (LineItems where Status = "Open")
Count ( Invoice_OpenItems::ItemID )
```

**Unique value detection:**
```
// On a Contacts record, check if email is duplicated elsewhere
Count ( Contacts_sameEmail::ContactID ) > 1
// where Contacts_sameEmail relates on Email field
```

**Build a summary string:**
```
Let ( [
  names  = List ( TeamMembers::FullName ) ;
  total  = Count ( TeamMembers::MemberID ) ;
  joined = Substitute ( names ; ¶ ; ", " )
] ;
  joined & " (" & total & " members)"
)
```

**Get the most recent related date:**
```
Max ( Interactions::InteractionDate )
// → "Last contacted" date, computed from relationship
```

**Portal row running total:**
```
// Calc field in LineItems, uses a self-relationship sorted by line number
Sum ( LineItems_byLine::ExtendedPrice )
```

---

# FileMaker Japanese Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/japanese-functions.html  
All 12 Japanese language functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

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
Returns the Japanese name of the day of the week for a given date.  
Parameters: `date` — a date value.  
Returns: text (Japanese weekday name)

```
DayNameJ ( Date ( 6 ; 4 ; 2026 ) )
// → "水曜日"  (Wednesday = 水曜日)

// All day names:
// 日曜日 (Sunday), 月曜日 (Monday), 火曜日 (Tuesday),
// 水曜日 (Wednesday), 木曜日 (Thursday), 金曜日 (Friday), 土曜日 (Saturday)

DayNameJ ( Get(CurrentDate) )
// → current day name in Japanese
```

Compare with English `DayName()`:
```
DayName ( Get(CurrentDate) ) & " = " & DayNameJ ( Get(CurrentDate) )
// → "Wednesday = 水曜日"
```

---

## MonthNameJ ( date )
Returns the Japanese name for the month of a given date.  
Parameters: `date` — a date value.  
Returns: text (Japanese month name)

```
MonthNameJ ( Date ( 6 ; 1 ; 2026 ) )
// → "6月"  (June = 6月, literally "month 6")

// Japanese month names follow the pattern N月:
// 1月 (January) through 12月 (December)

MonthNameJ ( Get(CurrentDate) )
// → current month name in Japanese
```

---

## YearName ( date ; format )
Returns the Japanese calendar year name for a given date. Japan uses two year systems: the Western (Gregorian) year and the Imperial era year.  
Parameters: `date` — a date value; `format` — numeric code controlling output format.  
Returns: text

**format values:**
| Value | Output | Example (2026) |
|---|---|---|
| 0 | Western year in kanji | 二〇二六 |
| 1 | Imperial era name + year (kanji) | 令和八年 |
| 2 | Imperial era abbreviation + year number | R8 |
| 3 | Full era name + year number (mixed) | 令和8年 |

```
YearName ( Date ( 6 ; 4 ; 2026 ) ; 0 )
// → "二〇二六"  (Western 2026 in kanji)

YearName ( Date ( 6 ; 4 ; 2026 ) ; 1 )
// → "令和八年"  (Reiwa 8, the 8th year of the Reiwa era)

YearName ( Date ( 6 ; 4 ; 2026 ) ; 2 )
// → "R8"  (abbreviated)

YearName ( Date ( 6 ; 4 ; 2026 ) ; 3 )
// → "令和8年"
```

**Imperial era reference:**
- Reiwa (令和) era began 1 May 2019 (year 1 = 2019)
- Heisei (平成) era: 1989–2019
- Showa (昭和) era: 1926–1989

---

## Furigana ( text {; option } )
Converts Japanese text (kanji and mixed text) to its phonetic reading (furigana). The conversion uses FileMaker's built-in Japanese input method to derive the reading.  
Parameters: `text` — Japanese text; `option` — optional numeric code for output character type (default: 0).  
Returns: text (phonetic reading)

**option values:**
| Value | Output |
|---|---|
| 0 | Hiragana (default) |
| 1 | Katakana |
| 2 | Hankaku (half-width) katakana |
| 3 | Roman (Romaji) |

```
Furigana ( "東京" ; 0 )
// → "とうきょう"  (hiragana reading of 東京 Tokyo)

Furigana ( "東京" ; 1 )
// → "トウキョウ"  (katakana)

Furigana ( "東京" ; 3 )
// → "tōkyō"  or "toukyou" (roman/romaji)

Furigana ( "田中様" ; 0 )
// → "たなかさま"
```

Sorting by pronunciation (readings often differ from visual order):
```
// Use Furigana as a sort key field for kanji names
// so records sort phonetically rather than by stroke order
```

---

## Hiragana ( text )
Converts zenkaku (full-width) katakana to hiragana. Non-katakana characters pass through unchanged.  
Parameters: `text` — text containing katakana.  
Returns: text (katakana converted to hiragana)

```
Hiragana ( "トウキョウ" )
// → "とうきょう"

Hiragana ( "カタカナ" )
// → "かたかな"

Hiragana ( "ABC123" )
// → "ABC123"  (non-katakana unchanged)
```

---

## Katakana ( text )
Converts hiragana to zenkaku (full-width) katakana. Non-hiragana characters pass through unchanged.  
Parameters: `text` — text containing hiragana.  
Returns: text (hiragana converted to katakana)

```
Katakana ( "とうきょう" )
// → "トウキョウ"

Katakana ( "かたかな" )
// → "カタカナ"

Katakana ( "hello" )
// → "hello"  (non-hiragana unchanged)
```

---

## KanaHankaku ( text )
Converts **zenkaku** (full-width, double-byte) katakana to **hankaku** (half-width, single-byte) katakana. Other characters (hiragana, kanji, ASCII) pass through unchanged.  
Parameters: `text` — text containing zenkaku katakana.  
Returns: text

```
KanaHankaku ( "トウキョウ" )
// → "ﾄｳｷｮｳ"  (half-width katakana)

KanaHankaku ( "東京トウキョウ" )
// → "東京ﾄｳｷｮｳ"  (kanji unchanged, katakana narrowed)
```

Use case: legacy systems or barcodes requiring half-width kana output.

---

## KanaZenkaku ( text )
Converts **hankaku** (half-width) katakana to **zenkaku** (full-width) katakana. Inverse of `KanaHankaku`.  
Parameters: `text` — text containing hankaku katakana.  
Returns: text

```
KanaZenkaku ( "ﾄｳｷｮｳ" )
// → "トウキョウ"

KanaZenkaku ( "ｶﾀｶﾅ" )
// → "カタカナ"
```

Use case: normalise imported data from legacy systems into standard full-width format.

---

## RomanHankaku ( text )
Converts **zenkaku** (full-width) alphanumeric characters and punctuation to their **hankaku** (half-width, standard ASCII) equivalents.  
Parameters: `text` — text containing zenkaku roman characters.  
Returns: text

```
RomanHankaku ( "ＡＢＣ１２３" )
// → "ABC123"

RomanHankaku ( "Ｈｅｌｌｏ　Ｗｏｒｌｄ" )
// → "Hello World"
```

Use case: normalise user-entered data before validation or comparison (Japanese keyboards often default to zenkaku for all input).

---

## RomanZenkaku ( text )
Converts **hankaku** (half-width, standard ASCII) alphanumeric characters to **zenkaku** (full-width) characters. Inverse of `RomanHankaku`.  
Parameters: `text` — text containing hankaku (ASCII) characters.  
Returns: text

```
RomanZenkaku ( "ABC123" )
// → "ＡＢＣ１２３"

RomanZenkaku ( "Hello" )
// → "Ｈｅｌｌｏ"
```

Use case: formatting for Japanese print layouts that require full-width presentation of alphanumerics.

---

## KanjiNumeral ( text )
Converts Arabic (Western) numerals in a text string to their **kanji numeral** equivalents.  
Parameters: `text` — text containing Arabic numerals.  
Returns: text (numerals replaced with kanji)

```
KanjiNumeral ( "2026" )
// → "二〇二六"  (each digit individually: 2=二, 0=〇, 2=二, 6=六)

KanjiNumeral ( "第3回" )
// → "第三回"  (mixed text: numeral converted, other chars unchanged)

KanjiNumeral ( "100" )
// → "一〇〇"
```

Note: This is digit-by-digit conversion (二〇二六), not place-value conversion (二千二十六 = 2,026). For place-value kanji numbers, use `NumToJText()`.

---

## NumToJText ( number ; separator ; characterType )
Converts a number to its Japanese text representation, with control over the separator style and character set. More powerful than `KanjiNumeral()` — supports place-value notation (thousands, ten-thousands, etc.) and multiple output styles.  
Parameters: `number` — the number to convert; `separator` — controls grouping separators; `characterType` — controls output character style.  
Returns: text

**separator values:**
| Value | Behaviour |
|---|---|
| 0 | No separator |
| 1 | Comma separator at each 万 (10,000) boundary |

**characterType values:**
| Value | Output style |
|---|---|
| 0 | Kanji with place-value units (万, 億, etc.) |
| 1 | Full-width Arabic numerals |
| 2 | Half-width Arabic numerals |
| 3 | Kanji digits only (no place-value units) |

```
NumToJText ( 2026 ; 0 ; 0 )
// → "二千二十六"  (place-value kanji)

NumToJText ( 10000 ; 0 ; 0 )
// → "一万"

NumToJText ( 1234567 ; 1 ; 0 )
// → "百二十三万,四千五百六十七"  (with 万-boundary comma)

NumToJText ( 2026 ; 0 ; 1 )
// → "２０２６"  (full-width Arabic)

NumToJText ( 2026 ; 0 ; 2 )
// → "2026"  (half-width Arabic — same as the input number as text)

NumToJText ( 2026 ; 0 ; 3 )
// → "二〇二六"  (digit-by-digit kanji, same as KanjiNumeral)
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
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** FileMaker's mobile functions are exclusively for **FileMaker Go** (iOS/iPadOS). They expose native device hardware: GPS location, sensor data (accelerometer, gyroscope, magnetometer, barometer, ambient light), AV player state, and iBeacon ranging. Always check `Get(Device)` or `Get(ApplicationVersion)` before calling these functions on platforms that don't support them — on FileMaker Pro (desktop), they return empty or an error.

**Platform guard pattern:**
```
// Check before calling any mobile function:
If ( Left ( Get(ApplicationVersion) ; 2 ) = "Go" ;
  Location ( 10 ) ;
  "Not available on this platform"
)
```

---

## GetAVPlayerAttribute ( attributeName )
Returns the current state of the native AV (audio/video) player when a container field is playing media in FileMaker Go. Use in scripts to monitor playback position, duration, or status.  
Parameters: `attributeName` — text name of the attribute to retrieve.  
Returns: varies by attribute

**Common attributeName values:**
| Attribute | Returns | Notes |
|---|---|---|
| `"state"` | text | `"playing"`, `"paused"`, `"stopped"`, `"ended"` |
| `"currentTime"` | number | Playback position in seconds |
| `"duration"` | number | Total media duration in seconds |
| `"rate"` | number | Playback rate (1.0 = normal, 2.0 = double speed) |
| `"isMuted"` | number | 1 if muted, 0 if not |

```
GetAVPlayerAttribute ( "state" )
// → "playing" / "paused" / "stopped"

GetAVPlayerAttribute ( "currentTime" )
// → 47.3  (seconds into playback)

GetAVPlayerAttribute ( "duration" )
// → 183.0  (3 minutes 3 seconds total)

// Remaining time:
GetAVPlayerAttribute("duration") - GetAVPlayerAttribute("currentTime")
// → seconds remaining

// Playback percentage:
GetAVPlayerAttribute("currentTime") / GetAVPlayerAttribute("duration") * 100
```

---

## GetSensor ( sensorName {; option1 ; option2 } )
Returns a real-time reading from a named hardware sensor on the iOS/iPadOS device. The function blocks until a reading is available (or times out). Sensor availability depends on the device model.  
Parameters: `sensorName` — text name of the sensor; `option1`, `option2` — optional sensor-specific parameters.  
Returns: number or JSON (depending on sensor)

**Available sensors and their returns:**

| sensorName | Returns | Notes |
|---|---|---|
| `"Acceleration"` | JSON with x, y, z (g-force) | Device acceleration |
| `"Gravity"` | JSON with x, y, z | Gravity component only |
| `"RotationRate"` | JSON with x, y, z (rad/s) | Gyroscope |
| `"Attitude"` | JSON with roll, pitch, yaw (radians) | Device orientation |
| `"MagneticField"` | JSON with x, y, z (microteslas) + accuracy | Magnetometer |
| `"Altitude"` | number (meters above sea level) | Barometric altitude |
| `"Pressure"` | number (kilopascals) | Barometric pressure |
| `"Luminosity"` | number (lux) | Ambient light sensor |

```
GetSensor ( "Acceleration" )
// → {"x":0.012,"y":-0.034,"z":-0.987}  (tilted near-flat, z≈-1g)

GetSensor ( "Altitude" )
// → 42.5  (meters above sea level)

GetSensor ( "Pressure" )
// → 101.325  (kPa at sea level)

// Extract individual axis:
JSONGetElement ( GetSensor("Acceleration") ; "z" )
// → -0.987  (device lying flat, screen up)

// Detect if device is being held upright:
Abs ( JSONGetElement ( GetSensor("Acceleration") ; "z" ) ) < 0.3
// → 1 (True) if device is tilted significantly from flat
```

---

## Location ( accuracy {; timeout } )
Returns the device's current GPS coordinates as a newline-delimited text value.  
Parameters: `accuracy` — desired accuracy in metres (smaller = higher accuracy but slower); `timeout` — optional max seconds to wait for a fix (default: no limit).  
Returns: text — two values separated by a newline: latitude on line 1, longitude on line 2

```
Location ( 10 )
// → "-37.8136\n144.9631"  (Melbourne CBD example)
// Line 1: latitude (-37.8136)
// Line 2: longitude (144.9631)

// Extract latitude:
GetValue ( Location ( 10 ) ; 1 )
// → -37.8136

// Extract longitude:
GetValue ( Location ( 10 ) ; 2 )
// → 144.9631

// With 5-second timeout:
Location ( 50 ; 5 )
// → coordinates within 50m, or empty if no fix within 5 seconds
```

Store coordinates in a script:
```
Set Variable [ $loc     ; Location ( 20 ) ]
Set Variable [ $lat     ; GetValue ( $loc ; 1 ) ]
Set Variable [ $lng     ; GetValue ( $loc ; 2 ) ]
Set Field [ Record::Latitude  ; $lat ]
Set Field [ Record::Longitude ; $lng ]
```

---

## LocationValues ( accuracy {; timeout } )
Like `Location()`, but returns **four values** (more detail): latitude, longitude, altitude, and horizontal accuracy of the fix.  
Parameters: `accuracy` — desired accuracy in metres; `timeout` — optional max seconds to wait.  
Returns: text — four values separated by newlines

```
LocationValues ( 10 )
// → "-37.8136\n144.9631\n42.5\n8.0"
// Line 1: latitude
// Line 2: longitude
// Line 3: altitude (metres above sea level)
// Line 4: horizontal accuracy of this fix (metres)

// Extract all four:
Let ( [
  lv  = LocationValues ( 10 ) ;
  lat = GetValue ( lv ; 1 ) ;
  lng = GetValue ( lv ; 2 ) ;
  alt = GetValue ( lv ; 3 ) ;
  acc = GetValue ( lv ; 4 )
] ;
  "Lat: " & lat & "  Lon: " & lng & "  Alt: " & alt & "m  Accuracy: ±" & acc & "m"
)
```

Reject imprecise fixes:
```
Let ( lv = LocationValues ( 10 ; 8 ) ;
  If ( GetValue(lv;4) > 50 ;
    "GPS fix too imprecise (±" & GetValue(lv;4) & "m)" ;
    JSONSetElement ( "{}" ;
      ["lat" ; GetValue(lv;1) ; JSONNumber] ;
      ["lng" ; GetValue(lv;2) ; JSONNumber] ;
      ["alt" ; GetValue(lv;3) ; JSONNumber]
    )
  )
)
```

---

## RangeBeacons ( UUID {; timeout ; major ; minor } )
Scans for nearby Bluetooth Low Energy (BLE) iBeacons that match the given UUID and returns information about each detected beacon as a newline-delimited list.  
Parameters: `UUID` — the iBeacon Proximity UUID (text, standard UUID format); `timeout` — optional seconds to scan (default: implementation-defined); `major` — optional major value filter (0–65535); `minor` — optional minor value filter (0–65535).  
Returns: text — each beacon on a separate line; each line contains tab-separated values: UUID, major, minor, proximity, accuracy (meters), RSSI (signal strength dBm)

```
RangeBeacons ( "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0" )
// → one line per detected beacon, e.g.:
// "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0\t1\t5\timmediate\t0.5\t-58"
// "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0\t1\t12\tnear\t2.1\t-72"

// Filter to specific major beacon group:
RangeBeacons ( "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0" ; 5 ; 1 )
// → only beacons with major=1, scanned for 5 seconds

// Parse first beacon's proximity:
Let ( [
  beacons     = RangeBeacons ( BeaconUUID ) ;
  firstBeacon = GetValue ( beacons ; 1 ) ;
  proximity   = GetValue ( Substitute ( firstBeacon ; Char(9) ; ¶ ) ; 4 )
] ;
  proximity   // → "immediate", "near", "far", or "unknown"
)
```

**Proximity values:** `immediate` (<0.5m), `near` (0.5–3m), `far` (>3m), `unknown` (cannot determine).

Use cases: retail proximity experiences, museum exhibit triggers, warehouse zone detection, indoor navigation, automatic record lookup when entering a tagged area.

---

# FileMaker Miscellaneous Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/miscellaneous-functions.html  
All 9 miscellaneous functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** The Miscellaneous category contains utility functions that do not fit neatly into other categories. They cover path conversion (FileMaker ↔ native OS formats), add-on metadata, field name introspection, layout object attribute inspection, found-set record ID retrieval, and layout object UUID access. Several are essential for dynamic scripting and add-on development.

---

## ConvertFromFileMakerPath ( filemakerPath ; format )
Converts a FileMaker internal path (e.g. `filemac:/Macintosh HD/Users/…` or `filewin:/C:/…`) to a standard OS path or URL.  
Parameters: `filemakerPath` — text in FileMaker path format; `format` — numeric code for output format.  
Returns: text

**format values:**
| Value | Output format |
|---|---|
| 0 | Native OS path (Mac: `/Volume/…`, Win: `C:\…`) |
| 1 | `file://` URL |

```
ConvertFromFileMakerPath ( Get(DocumentsPath) ; 0 )
// Mac → /Users/username/Documents/
// Win → C:\Users\username\Documents\

ConvertFromFileMakerPath ( Get(FilePath) ; 1 )
// → file:///Users/username/Documents/MyFile.fmp12
```

Typical use — pass a FileMaker path to a script or plugin that requires a native path:
```
Let ( nativePath = ConvertFromFileMakerPath ( Get(DocumentsPath) & "export.csv" ; 0 ) ;
  // pass nativePath to a shell command or MBS plugin
  nativePath
)
```

---

## ConvertToFileMakerPath ( standardPath ; format )
Converts a native OS path or URL to a FileMaker internal path format.  
Parameters: `standardPath` — text in native OS or URL format; `format` — numeric code for input format.  
Returns: text

**format values:**
| Value | Input format |
|---|---|
| 0 | Native OS path |
| 1 | `file://` URL |

```
ConvertToFileMakerPath ( "/Users/username/Documents/report.pdf" ; 0 )
// Mac → filemac:/Macintosh HD/Users/username/Documents/report.pdf

ConvertToFileMakerPath ( "C:\\Reports\\q3.xlsx" ; 0 )
// Win → filewin:/C:/Reports/q3.xlsx
```

---

## GetAddonInfo ( addonID )
Returns a JSON object containing metadata about a FileMaker add-on (name, version, description, author, minimum FileMaker version required, etc.).  
Parameters: `addonID` — the text identifier of the add-on (as defined in the add-on manifest).  
Returns: text (JSON)

```
GetAddonInfo ( "com.example.myaddon" )
// → {"name":"My Add-on","version":"1.2.0","description":"…","author":"…","minVersion":"19.0"}

// Extract the version:
JSONGetElement ( GetAddonInfo ( "com.example.myaddon" ) ; "version" )
// → "1.2.0"
```

---

## GetBaseTableName ( field )
Returns the name of the **base table** (not the table occurrence) that contains the specified field. Useful when you have multiple table occurrences pointing to the same base table and need to identify the actual table.  
Parameters: `field` — a field reference (not a field name string — use the field itself as the parameter).  
Returns: text

```
GetBaseTableName ( Customers::Name )
// → "Customers"  (even if the TO is named "Customers_Archive")

GetBaseTableName ( Orders_Portal::Amount )
// → "Orders"  (returns base table, not the TO name)
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
GetFieldName ( Customers::Name )
// → "Customers::Name"

GetFieldName ( Self )
// → "CurrentTO::CurrentField"  (when used inside that field's own calc)
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
Returns the value of a named **layout object attribute** at runtime — position, size, visibility, style, fill colour, bounds, content, and more. Requires the layout object to have a name set in the Inspector.  
Parameters: `objectName` — text name of the layout object; `attributeName` — name of the attribute to retrieve; `repetitionNumber` — optional (for repeating fields); `portalRowNumber` — optional (for portal rows).  
Returns: varies by attribute (number, text, or JSON)

**Common attributeName values:**
| Attribute | Returns |
|---|---|
| `"bounds"` | JSON with top, left, bottom, right (layout units) |
| `"left"`, `"top"`, `"right"`, `"bottom"` | Individual position values |
| `"width"`, `"height"` | Dimensions in layout units |
| `"visible"` | 1 (visible) or 0 (hidden) |
| `"content"` | Field value or button label text |
| `"isFocused"` | 1 if the object currently has focus |
| `"enabled"` | 1 if the object is enabled |
| `"style"` | CSS-like style info as JSON |

```
GetLayoutObjectAttribute ( "TotalAmount" ; "content" )
// → current displayed value of the field named "TotalAmount"

GetLayoutObjectAttribute ( "StatusPanel" ; "visible" )
// → 1 or 0

GetLayoutObjectAttribute ( "CustomerName" ; "bounds" )
// → {"top":120,"left":80,"bottom":148,"right":400}

GetLayoutObjectAttribute ( "CustomerName" ; "width" )
// → 320

// Check if a portal row object is visible:
GetLayoutObjectAttribute ( "LineItemQty" ; "visible" ; 1 ; 3 )
// → visibility of repetition 1, portal row 3
```

Responsive layout logic:
```
// Conditionally show a panel based on another object's position:
If ( GetLayoutObjectAttribute ( "Sidebar" ; "visible" ) ;
  "Sidebar is showing" ; "Sidebar is hidden" )
```

---

## GetLayoutObjectOwnerInfo ( objectID )
Returns a JSON object describing which layout and table own a layout object, identified by its internal numeric objectID.  
Parameters: `objectID` — the internal numeric ID of the layout object (obtain via `LayoutObjectUUID`).  
Returns: text (JSON)

```
GetLayoutObjectOwnerInfo ( 1234 )
// → {"layoutName":"Invoice Detail","tableName":"Invoices","fileID":1}
```

---

## GetRecordIDsFromFoundSet ( type )
Returns the record IDs of all records in the current found set as either a newline-delimited list or a JSON array.  
Parameters: `type` — `0` for newline-delimited list; `1` for JSON array.  
Returns: text

```
GetRecordIDsFromFoundSet ( 0 )
// → "101\n105\n108\n112"  (newline-separated record IDs)

GetRecordIDsFromFoundSet ( 1 )
// → "[101,105,108,112]"  (JSON array)

// Count of IDs in result:
ValueCount ( GetRecordIDsFromFoundSet ( 0 ) )
// Same as Get(FoundCount) but gives you the actual IDs

// Check if a specific record ID is in the found set:
PatternCount ( ¶ & GetRecordIDsFromFoundSet(0) & ¶ ; ¶ & targetID & ¶ ) > 0
```

Common use — pass the found set to a script for batch processing:
```
// In a calculation to generate a script parameter:
JSONSetElement ( "{}" ;
  ["recordIDs" ; GetRecordIDsFromFoundSet(1) ; JSONArray] ;
  ["timestamp" ; Get(CurrentTimestamp) ; JSONString]
)
```

---

## LayoutObjectUUID
Returns the **UUID** (Universal Unique Identifier) of the layout object in which this calculation is being evaluated. No parameters — this is a constant in the context of a specific layout object.  
Parameters: none.  
Returns: text (UUID string)

```
LayoutObjectUUID
// → "3F2504E0-4F89-11D3-9A0C-0305E82C3301"  (example UUID)
```

Use cases — uniquely identify which object triggered an event, store object IDs for cross-reference in add-on development, or track layout objects in a dynamic UI system.

```
// Log which object was clicked (in a button script trigger):
Set Field [ Log::LastObjectClicked ; LayoutObjectUUID ]

// Store in JSON for later reference:
JSONSetElement ( "{}" ; "clickedObject" ; LayoutObjectUUID ; JSONString )
```

---

# FileMaker Persistent Data Functions — Syntax & Examples (FM 26+)

Source: https://help.claris.com/en/pro-help/content/persistent-data-functions.html  
2 persistent data functions introduced in FileMaker Pro 26 (2026).  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** The persistent data store is a key-value store that survives session end and file close. Entries are keyed by a **name** and an **instance ID**, allowing multiple values under the same name. Use `Configure Persistent Data` (script step) to write/delete entries; use these functions to read them.

---

## GetPersistentData ( name ; instanceID )
*Introduced in FileMaker Pro 26 (2026).*  
Returns a value from the persistent data store by name and instance ID.  
Parameters: `name` — text key; `instanceID` — text or number identifying the specific instance.  
Returns: text (the stored value, or empty if not found)

```
GetPersistentData ( "lastRunDate" ; 1 )
// → "2026-06-10"  (value stored for name="lastRunDate", instance=1)
```

Read multiple instances of the same key:
```
Let ( [
  ids   = ListPersistentDataIDs ( "syncToken" ) ;
  first = GetValue ( ids ; 1 ) ;
  token = GetPersistentData ( "syncToken" ; first )
] ;
  token
)
```

---

## ListPersistentDataIDs ( name )
*Introduced in FileMaker Pro 26 (2026).*  
Returns a return-delimited list of all instance IDs stored under the specified name in the persistent data store.  
Parameters: `name` — the key name to query.  
Returns: text (return-delimited list of instance IDs; empty if no instances exist)

```
ListPersistentDataIDs ( "syncToken" )
// → "1¶2¶3"  (three instances stored under "syncToken")
```

Enumerate all instances of a key and read each value:
```
Let ( [
  ids   = ListPersistentDataIDs ( "cachedResult" ) ;
  count = ValueCount ( ids )
] ;
  // Use in a script with a loop:
  // Set Variable [ $i = 1 ]
  // Loop
  //   Set Variable [ $id = GetValue ( ids ; $i ) ]
  //   Set Variable [ $val = GetPersistentData ( "cachedResult" ; $id ) ]
  //   ... process $val ...
  //   Set Variable [ $i = $i + 1 ]
  //   Exit Loop If [ $i > $count ]
  // End Loop
  count & " instances found"
)
```

Check whether any instance exists before reading:
```
If ( IsEmpty ( ListPersistentDataIDs ( "userPrefs" ) ) ;
  "No preferences saved yet" ;
  GetPersistentData ( "userPrefs" ; 1 )
)
```
