# Date, Time & Timestamp Functions — Examples

---

# FileMaker Date Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/date-functions.html  
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
Date ( 10 ; 10 ; 2019 )
// → 10/10/2019

Date ( 13 ; 1 ; 2019 )
// → 1/1/2020 (one month after December 1, 2019)

Date ( 6 ; 0 ; 2019 )
// → 5/31/2019 (one day before June 1, 2019)

Date ( 6 ; -2 ; 2019 )
// → 5/29/2019 (three days before June 1, 2019)

Date ( 7 ; 12 ; 2019 ) - Date ( 7 ; 2 ; 2019 )
// → 10
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
Day ( "5/15/2019" )
// → `15`. This example assumes that the system date format is MM/DD/YYYY

Day ( DateSold )
// → the day of the month stored in DateSold
```
---

## DayName ( date )
Returns the full English name of the day of the week.  
Parameters: `date`.  
Returns: text
```
DayName ( Date ( 10 ; 7 ; 2019 ) )
// → Monday

DayName ( ProjectDue )
// → `Monday` when ProjectDue is 10/7/2019

DayName ( "10/7/2019" )
// → Monday
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
DayOfWeek ( "10/8/2019" )
// → 3

DayOfWeek ( Date ( 10 ; 9 ; 2019 ) )
// → 4

DayOfWeek ( ProjectDue )
// → `4 `when the date in ProjectDue is 10/9/2019
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
DayOfYear ( Billing Date )
// → `32`, when Billing Date is 2/1/2019
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
Month ( "3/19/2019" )
// → `3`. This example assumes that the operating system date format is set to MM/DD/YYYY
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
MonthName ( "6/6/2019" )
// → June
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
WeekOfYear ( "1/1/2019" )
// → 1

WeekOfYear ( ProjectDue )
// → `5`, when ProjectDue is 2/2/2019
```
---

## WeekOfYearFiscal ( date ; startingDay )
Returns the week number using a custom fiscal week start day.  
Parameters: `date`; `startingDay` — 1 (Sunday) through 7 (Saturday).  
Returns: number
```
WeekOfYearFiscal ( Date ( 1 ; 7 ; 2008 ) ; 1 )
// → 2

WeekOfYearFiscal ( Date ( 1 ; 1 ; 2009 ) ; 5 )
// → 1

WeekOfYearFiscal ( Date ( 1 ; 2 ; 2009 ) ; 1 )
// → 53
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
Year ( DateSold )
// → the year stored in DateSold

Year ( "5/5/2019" )
// → 2019
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

Source: https://help.claris.com/en/pro-help/content/time-functions.html  
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
Hour ( "12:15:23" )
// → 12
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
Minute ( "12:15:23" )
// → 15
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
Seconds ( "12:15:23" )
// → 23
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
Time(4;14;32)
// → 4:14:32

Time(4.5;10;30)
// → 4:40:30

Time(4;15;70)
// → 4:16:10
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
Timestamp ( Date ( 10 ; 21 ; 2019 ) ; Time ( 9 ; 10 ; 30 ) )
// → 10/21/2019 9:10:30 AM
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
