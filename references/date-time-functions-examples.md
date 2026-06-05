# Date, Time & Timestamp Functions — Examples

---

# FileMaker Date Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/date-functions-category.html  
All 10 date functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** FileMaker stores dates internally as the number of days since 1 January 0001. This means date arithmetic is just integer addition/subtraction — no special functions needed for "days between two dates". The functions here handle construction, decomposition, and week/day-of-week calculations.

**Date arithmetic basics:**
```
// Days between two dates — just subtract
Get(CurrentDate) - InvoiceDate     // → number of days outstanding
DueDate - Get(CurrentDate)         // → days until due (negative = overdue)

// Add days to a date
Get(CurrentDate) + 30              // → date 30 days from today
StartDate + 7                      // → one week later

// Date fields store as numbers; always use Date() to construct
Date ( Month ( d ) ; Day ( d ) + 90 ; Year ( d ) )  // → 90 days later (handles month overflow)
```

---

## Date ( month ; day ; year )
Constructs a date value from numeric month, day, and year components. Handles overflow — passing day=32 in a 31-day month rolls to the next month.  
Parameters: `month` (1–12); `day` (1–31, can overflow); `year` (4-digit).  
Returns: date

```
Date ( 6 ; 15 ; 2025 )
// → 15/06/2025

Date ( 12 ; 31 ; 2024 )
// → 31/12/2024
```

First day of current month:
```
Date ( Month ( Get(CurrentDate) ) ; 1 ; Year ( Get(CurrentDate) ) )
```

Last day of current month (day 0 of next month = last day of this month):
```
Date ( Month ( Get(CurrentDate) ) + 1 ; 0 ; Year ( Get(CurrentDate) ) )
```

Add N months safely (avoids invalid dates like Feb 30):
```
Let ( [
  d = StartDate ;
  n = 3  // months to add
] ;
  Date ( Month(d) + n ; Day(d) ; Year(d) )
)
```

Same day next year:
```
Date ( Month ( StartDate ) ; Day ( StartDate ) ; Year ( StartDate ) + 1 )
```

---

## Day ( date )
Extracts the day-of-month component (1–31).  
Parameters: `date` — a date value or expression.  
Returns: number

```
Day ( Get(CurrentDate) )    // → e.g. 4
Day ( Date ( 12 ; 25 ; 2025 ) )  // → 25
```

---

## DayName ( date )
Returns the full English name of the day of the week.  
Parameters: `date`.  
Returns: text

```
DayName ( Get(CurrentDate) )    // → "Thursday"
DayName ( Date ( 1 ; 1 ; 2025 ) )  // → "Wednesday"
```

Useful for display fields and conditional logic:
```
If ( DayName ( Get(CurrentDate) ) = "Saturday" or DayName ( Get(CurrentDate) ) = "Sunday" ;
  "Weekend" ; "Weekday"
)
```

---

## DayOfWeek ( date )
Returns the day of the week as a number (1 = Sunday … 7 = Saturday).  
Parameters: `date`.  
Returns: number

```
DayOfWeek ( Get(CurrentDate) )     // → 5 for Thursday
DayOfWeek ( Date ( 1 ; 1 ; 2025 ) )  // → 4 (Wednesday)
```

ISO weekday (1=Monday … 7=Sunday):
```
Let ( d = DayOfWeek ( myDate ) ;
  If ( d = 1 ; 7 ; d - 1 )
)
```

Next Monday from any date:
```
myDate + Mod ( 9 - DayOfWeek ( myDate ) ; 7 )
```

Skip weekends — next business day:
```
Let ( [
  d   = myDate + 1 ;
  dow = DayOfWeek ( d )
] ;
  Case (
    dow = 1 ; d + 1 ;   // Sunday → Monday
    dow = 7 ; d + 2 ;   // Saturday → Monday
    d
  )
)
```

---

## DayOfYear ( date )
Returns the ordinal day of the year (1–366).  
Parameters: `date`.  
Returns: number

```
DayOfYear ( Date ( 12 ; 31 ; 2025 ) )  // → 365
DayOfYear ( Date ( 2 ; 28 ; 2024 ) )   // → 59 (2024 is a leap year)
```

Days remaining in year:
```
If ( Mod ( Year ( Get(CurrentDate) ) ; 4 ) = 0 ; 366 ; 365 ) - DayOfYear ( Get(CurrentDate) )
```

---

## Month ( date )
Extracts the month component (1–12).  
Parameters: `date`.  
Returns: number

```
Month ( Get(CurrentDate) )   // → 6
Month ( Date ( 12 ; 25 ; 2025 ) )  // → 12
```

Quarter calculation:
```
Ceiling ( Month ( InvoiceDate ) / 3 )
// → 1 (Q1), 2 (Q2), 3 (Q3), 4 (Q4)
```

Financial year quarter (July–June):
```
Let ( m = Month ( InvoiceDate ) ;
  Ceiling ( If ( m >= 7 ; m - 6 ; m + 6 ) / 3 )
)
```

---

## MonthName ( date )
Returns the full English name of the month.  
Parameters: `date`.  
Returns: text

```
MonthName ( Get(CurrentDate) )    // → "June"
MonthName ( Date ( 12 ; 1 ; 2025 ) )  // → "December"
```

Short month name (first 3 characters):
```
Left ( MonthName ( myDate ) ; 3 )  // → "Jun"
```

---

## WeekOfYear ( date )
Returns the week number of the year (1–54) where week 1 starts on the first Sunday of the year (or January 1 if it's a Sunday).  
Parameters: `date`.  
Returns: number

```
WeekOfYear ( Get(CurrentDate) )       // → e.g. 23
WeekOfYear ( Date ( 1 ; 1 ; 2025 ) )  // → 1
```

---

## WeekOfYearFiscal ( date ; startingDay )
Returns the week number using a custom fiscal week start day.  
Parameters: `date`; `startingDay` — 1 (Sunday) through 7 (Saturday).  
Returns: number

```
WeekOfYearFiscal ( Get(CurrentDate) ; 2 )
// → week number where weeks start on Monday
```

ISO week number (weeks start Monday, week 1 = first week with a Thursday):
```
WeekOfYearFiscal ( myDate ; 2 )
// Close approximation; for strict ISO 8601 use a custom function
```

---

## Year ( date )
Extracts the 4-digit year component.  
Parameters: `date`.  
Returns: number

```
Year ( Get(CurrentDate) )   // → 2026
Year ( Date ( 1 ; 1 ; 2000 ) )  // → 2000
```

Age in years:
```
Let ( [
  today = Get(CurrentDate) ;
  bday  = Contacts::DateOfBirth ;
  years = Year(today) - Year(bday)
] ;
  If (
    Month(today) < Month(bday) or
    ( Month(today) = Month(bday) and Day(today) < Day(bday) ) ;
    years - 1 ;
    years
  )
)
```

---

## Common patterns

**Date range check:**
```
myDate ≥ Date ( 1 ; 1 ; 2025 ) and myDate ≤ Date ( 12 ; 31 ; 2025 )
```

**Business days between two dates (approximate — no public holidays):**
```
Let ( [
  start   = EarlyDate ;
  end     = LateDate ;
  days    = end - start ;
  weeks   = Int ( days / 7 ) ;
  rem     = Mod ( days ; 7 ) ;
  startDow = DayOfWeek ( start ) ;
  // weekend days in remainder
  wkend   = If ( startDow + rem > 7 ; // spans a weekend boundary
    Min ( rem ; 7 - startDow + 1 ) + Max ( 0 ; rem - ( 7 - startDow ) - 5 ) ;
    Max ( 0 ; startDow + rem - 6 )
  )
] ;
  weeks * 5 + rem - wkend
)
```

**First business day of next month:**
```
Let ( [
  firstOfNext = Date ( Month ( Get(CurrentDate) ) + 1 ; 1 ; Year ( Get(CurrentDate) ) ) ;
  dow         = DayOfWeek ( firstOfNext )
] ;
  Case (
    dow = 1 ; firstOfNext + 1 ;   // Sunday
    dow = 7 ; firstOfNext + 2 ;   // Saturday
    firstOfNext
  )
)
```

**Age bracket:**
```
Let ( age = Year(Get(CurrentDate)) - Year(DateOfBirth) ;
  Case (
    age < 18  ; "Minor" ;
    age < 25  ; "18–24" ;
    age < 35  ; "25–34" ;
    age < 50  ; "35–49" ;
    age < 65  ; "50–64" ;
    "65+"
  )
)
```

**Overdue flag:**
```
If ( DueDate < Get(CurrentDate) and Status ≠ "Paid" ; 1 ; 0 )
```

**Format date as ISO 8601 (YYYY-MM-DD) text:**
```
Year ( myDate ) & "-" &
Right ( "0" & Month ( myDate ) ; 2 ) & "-" &
Right ( "0" & Day ( myDate ) ; 2 )
```

**Parse ISO date string to FileMaker date:**
```
Date (
  Middle ( isoString ; 6 ; 2 ) ;  // month
  Right  ( isoString ; 2 ) ;      // day
  Left   ( isoString ; 4 )        // year
)
```

---

# FileMaker Time & Timestamp Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/time-functions-category.html  
All 4 time functions + 1 timestamp function with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** FileMaker stores time values internally as the number of seconds since midnight. This means time arithmetic is just addition/subtraction of seconds — no special functions needed. A `Timestamp` is stored as the number of seconds since the FileMaker epoch (1 January 0001, 00:00:00). Time fields accept `HH:MM:SS` format; Timestamp fields combine a date and time.

**Time arithmetic basics:**
```
// Difference between two times — just subtract (result in seconds)
EndTime - StartTime                // → seconds elapsed
( EndTime - StartTime ) / 3600     // → hours elapsed

// Add 90 minutes to a time
StartTime + ( 90 * 60 )            // → time 90 minutes later

// Construct midnight
Time ( 0 ; 0 ; 0 )                 // → 12:00:00 AM

// Check if a timestamp is today
Date ( Timestamp ) = Get(CurrentDate)
```

---

## Hour ( time )
Extracts the hour component from a time or timestamp value (0–23 for standard times; can exceed 23 for time-duration arithmetic results).  
Parameters: `time` — a time or timestamp value or expression.  
Returns: number

```
Hour ( Get(CurrentTime) )           // → e.g. 14 (2pm)
Hour ( Time ( 9 ; 30 ; 0 ) )       // → 9
Hour ( "14:45:30" )                 // → 14
```

Business hours check:
```
Let ( h = Hour ( Get(CurrentTime) ) ;
  h ≥ 9 and h < 17   // → 1 (True) if between 9am and 5pm
)
```

Duration in hours from a start timestamp:
```
Hour ( Get(CurrentTimestamp) - StartTimestamp )
// Note: works for durations ≤ 24h; for longer durations use:
// ( Get(CurrentTimestamp) - StartTimestamp ) / 3600
```

---

## Minute ( time )
Extracts the minute component from a time or timestamp value (0–59).  
Parameters: `time` — a time or timestamp value or expression.  
Returns: number

```
Minute ( Get(CurrentTime) )         // → e.g. 45
Minute ( Time ( 9 ; 30 ; 0 ) )     // → 30
Minute ( "14:45:30" )               // → 45
```

Round a time down to the nearest 15 minutes:
```
Let ( [
  t = Get(CurrentTime) ;
  h = Hour ( t ) ;
  m = Minute ( t )
] ;
  Time ( h ; m - Mod ( m ; 15 ) ; 0 )
)
```

---

## Seconds ( time )
Extracts the seconds component from a time or timestamp value (0–59; can return fractional seconds if sub-second precision is present).  
Parameters: `time` — a time or timestamp value or expression.  
Returns: number

```
Seconds ( Get(CurrentTime) )        // → e.g. 22
Seconds ( Time ( 9 ; 30 ; 45 ) )   // → 45
```

Total seconds since midnight:
```
Hour ( t ) * 3600 + Minute ( t ) * 60 + Seconds ( t )
// Same as: t  (time values are stored as seconds from midnight)
```

---

## Time ( hours ; minutes ; seconds )
Constructs a time value from numeric hour, minute, and second components. Handles overflow — passing minutes=90 rolls over to hours.  
Parameters: `hours` (0–23, can overflow); `minutes` (0–59, can overflow); `seconds` (0–59, can overflow).  
Returns: time

```
Time ( 9 ; 30 ; 0 )                // → 9:30:00 AM
Time ( 14 ; 0 ; 0 )               // → 2:00:00 PM
Time ( 0 ; 0 ; 0 )                // → 12:00:00 AM (midnight)
Time ( 23 ; 59 ; 59 )             // → 11:59:59 PM
```

Add 2.5 hours to a time:
```
Time ( Hour(StartTime) + 2 ; Minute(StartTime) + 30 ; Seconds(StartTime) )
// Or more simply:
StartTime + ( 2.5 * 3600 )
```

Round a time to the nearest hour:
```
Time ( Hour ( t ) + If ( Minute(t) ≥ 30 ; 1 ; 0 ) ; 0 ; 0 )
```

Convert decimal hours to a Time value:
```
Time ( Int ( decimalHours ) ; ( decimalHours - Int ( decimalHours ) ) * 60 ; 0 )
// e.g. 1.75 → 1:45:00
```

---

## Timestamp ( date ; time )
Constructs a timestamp value by combining a date and a time.  
Parameters: `date` — a date value; `time` — a time value.  
Returns: timestamp

```
Timestamp ( Get(CurrentDate) ; Get(CurrentTime) )
// → current date and time as a Timestamp (same as Get(CurrentTimestamp))

Timestamp ( Date ( 12 ; 31 ; 2025 ) ; Time ( 23 ; 59 ; 59 ) )
// → 31/12/2025 11:59:59 PM

Timestamp ( DueDate ; Time ( 17 ; 0 ; 0 ) )
// → deadline at 5pm on DueDate
```

Convert a timestamp back to its components:
```
// Extract date part
Date ( Timestamp )              // → date value (FileMaker auto-coerces)

// Or explicitly:
Let ( ts = Get(CurrentTimestamp) ;
  Date ( Month(ts) ; Day(ts) ; Year(ts) )
)

// Extract time part
Mod ( ts ; 86400 )              // → seconds since midnight = time
```

Timestamp arithmetic:
```
// Minutes elapsed since a logged timestamp
( Get(CurrentTimestamp) - LoggedTimestamp ) / 60

// Was this record modified in the last 24 hours?
Get(CurrentTimestamp) - Modification_Timestamp < 86400

// Schedule 48 hours from now
Get(CurrentTimestamp) + ( 48 * 3600 )
```

---

## Interaction patterns

Time in a Timestamp field:
```
// Get only the time portion of a timestamp
Mod ( SomeTimestamp ; 86400 )
// → seconds since midnight on that day (= the time)
```

Format a duration as "H:MM":
```
Let ( [
  totalSecs = EndTime - StartTime ;
  h = Div ( totalSecs ; 3600 ) ;
  m = Div ( Mod ( totalSecs ; 3600 ) ; 60 )
] ;
  h & ":" & Right ( "0" & m ; 2 )
)
```

Sort-safe timestamp string (ISO 8601–style):
```
Year(ts) & "-"
  & Right("0" & Month(ts) ; 2) & "-"
  & Right("0" & Day(ts) ; 2) & " "
  & Right("0" & Hour(ts) ; 2) & ":"
  & Right("0" & Minute(ts) ; 2)
```
