# Numeric Functions — Examples (Number, Financial, Trigonometric, Repeating)

---

# FileMaker Number Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/number-functions.html  
All 18 native number functions with format, parameters, and examples.
Last verified: 2026-06 against live Claris Help Centre.

---

## Abs ( number )
Returns the absolute value of a number (removes the sign).  
`Abs ( -5 )` → `5`  
`Abs ( 5 )` → `5`

---

## Ceiling ( number )
Rounds a number **up** to the next integer, regardless of the decimal value.  
`Ceiling ( 1.1 )` → `2`  
`Ceiling ( -1.1 )` → `-1`  
`Ceiling ( 3.0 )` → `3`

---

## Combination ( setSize ; numberOfChoices )
Returns the number of unique ways to choose `numberOfChoices` items from a set of `setSize` (order does not matter). Useful in statistics and combinatorics; results form Pascal's triangle.  
`Combination ( 5 ; 2 )` → `10` (the pairs from {a,b,c,d,e})  
Probability of a full house in 5-card poker:  
`( 13 * 12 * Combination ( 4 ; 2 ) * Combination ( 4 ; 3 ) ) / Combination ( 52 ; 5 )` → `0.00144057...`

---

## Div ( number ; divisor )
Returns the integer quotient of `number ÷ divisor`, always rounding **toward negative infinity** (equivalent to `Floor ( number / divisor )`).  
`Div ( 2.5 ; 2 )` → `1`  
`Div ( -2.5 ; 2 )` → `-2`  
`Div ( 10 ; 3 )` → `3`

---

## Exp ( number )
Returns the value of the mathematical constant *e* (~2.71828) raised to the power of `number`.  
`Exp ( 1 )` → `2.71828182845904523536...`  
`Exp ( 0 )` → `1`  
`Exp ( 2 )` → `7.38905609893065022723...`

---

## Factorial ( number { ; numberOfFactors } )
Returns the factorial of `number` (n!), stopping at 1 by default, or stopping after `numberOfFactors` multiplications if specified. Useful in statistics and combinatorics.  
`Factorial ( 3 )` → `6` (= 3 × 2 × 1)  
`Factorial ( 5 )` → `120` (= 5 × 4 × 3 × 2 × 1)  
`Factorial ( 10 ; 3 )` → `720` (= 10 × 9 × 8, stops after 3 factors)

---

## Floor ( number )
Rounds a number **down** to the next lower integer, regardless of the decimal value.  
`Floor ( 1.9 )` → `1`  
`Floor ( -1.1 )` → `-2`  
`Floor ( 3.0 )` → `3`

---

## Int ( number )
Drops all digits to the right of the decimal point without rounding. For positive numbers behaves like `Floor`; for negative numbers, truncates toward zero (unlike `Floor`).  
`Int ( 1.9 )` → `1`  
`Int ( -1.9 )` → `-1` ← note: Floor(-1.9) would give -2  
`Int ( 8.999 )` → `8`

---

## Lg ( number )
Returns the base-2 logarithm of `number`.  
`Lg ( 8 )` → `3` (2³ = 8)  
`Lg ( 1 )` → `0`  
`Lg ( 1024 )` → `10`

---

## Ln ( number )
Returns the natural (base-*e*) logarithm of `number`.  
`Ln ( 1 )` → `0`  
`Ln ( Exp(1) )` → `1`  
`Ln ( 10 )` → `2.30258509299404568402...`

---

## Log ( number )
Returns the common (base-10) logarithm of `number`.  
`Log ( 100 )` → `2`  
`Log ( 1000 )` → `3`  
`Log ( 1 )` → `0`

---

## Mod ( number ; divisor )
Returns the remainder after `number` is divided by `divisor`. Useful for unit conversions and cyclic calculations.  
`Mod ( 210 ; 4 )` → `2`  
`Mod ( 10 ; 3 )` → `1`  

Convert 24-hour time to 12-hour:  
`Mod ( 16 ; 12 )` → `4` (4 PM)

Convert months to years and remainder:  
`Int ( 31 / 12 ) & " years, " & Mod ( 31 ; 12 ) & " months"` → `2 years, 7 months`

---

## Random
Returns a random number ≥ 0 and < 1. Takes no parameters.  
`Random` → e.g. `0.72341...` (different each evaluation)

Generate a random integer between 1 and N (inclusive):  
`Int ( Random * N ) + 1`

Random integer between 1 and 100:  
`Int ( Random * 100 ) + 1`

---

## Round ( number ; precision )
Rounds `number` to `precision` decimal places. Always rounds up at exactly 0.5. Use a negative `precision` to round to tens, hundreds, etc.  
`Round ( 123.456 ; 2 )` → `123.46`  
`Round ( 14.5 ; 0 )` → `15`  
`Round ( 14.45 ; 1 )` → `14.5`  
`Round ( 29343.98 ; -3 )` → `29000`  
`Round ( 123.456 ; -1 )` → `120`

---

## SetPrecision ( expression ; precision )
Evaluates `expression` with extended decimal precision from 16 to 400 digits. Supports all functions except trigonometric. Does **not** truncate — the result is computed at full precision and then displayed.  
`SetPrecision ( 5 / 9 ; 30 )` → `0.555555555555555555555555555556`  
`SetPrecision ( 1/3 ; 50 )` → `0.33333333333333333333333333333333333333333333333333`

Use within complex expressions:  
`SetPrecision ( If ( field1 > 5 ; Exp ( 50 ) ; Average ( 5/9 ; 1/7 ; 5/7 ) ) ; 25 )`

---

## Sign ( number )
Returns `-1` if `number` is negative, `0` if zero, `1` if positive.  
`Sign ( -42 )` → `-1`  
`Sign ( 0 )` → `0`  
`Sign ( 99 )` → `1`

Useful for conditional logic without If:  
`Sign ( Balance ) * "Overdrawn"` — returns `"Overdrawn"` only when Balance is negative.

---

## Sqrt ( number )
Returns the square root of `number`.  
`Sqrt ( 9 )` → `3`  
`Sqrt ( 2 )` → `1.41421356237309504880...`  
`Sqrt ( 0 )` → `0`

---

## Truncate ( number ; precision )
Removes digits beyond `precision` decimal places **without rounding**. Unlike `Round`, always truncates toward zero.  
`Truncate ( 123.456 ; 2 )` → `123.45`  
`Truncate ( 1.999 ; 0 )` → `1`  
`Truncate ( -1.999 ; 1 )` → `-1.9`

**Truncate vs Int vs Round:**  
`Truncate ( 1.9 ; 0 )` → `1` (no rounding)  
`Int ( 1.9 )` → `1` (same for positive)  
`Round ( 1.9 ; 0 )` → `2` (rounds up)

---

# FileMaker Financial Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/financial-functions.html  
All 4 financial functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** FileMaker's four financial functions cover standard time-value-of-money calculations: present value, future value, loan payments, and net present value of unequal cash flows. All assume **periodic** (equal-interval) payments unless otherwise noted. Interest rates must be expressed **per period** (e.g. annual rate ÷ 12 for monthly calculations).

**Key concepts:**
- `payment` — the fixed payment amount per period (positive = cash in, negative = cash out — convention varies by function; see each)
- `interestRate` — rate per period as a decimal (5% annual monthly = 0.05/12)
- `periods` / `term` — number of payment periods
- Signs follow the cash-flow convention: money you receive is positive, money you pay out is negative

---

## FV ( payment ; interestRate ; periods )
Returns the **future value** of an investment with equal periodic payments at a constant interest rate. Useful for savings calculations — "how much will I have if I save $X/month for N months?"  
Parameters: `payment` — fixed payment per period (positive); `interestRate` — rate per period as decimal; `periods` — number of periods.  
Returns: number (positive = accumulated value)
```
FV(50;.11/12;5 * 12)
// → 3975.90398429...

FV(2000;.12;30) + 5000 * (.12 + 1) ^ 30
// → 632464.97928640...

FV(500;.11/5;60)
// → 61141.65130790...
```
Real-world: project savings goal:
```
Let ( [
  monthly  = Monthly_Contribution ;
  rate     = Annual_Rate / 12 ;
  months   = Years * 12
] ;
  FV ( monthly ; rate ; months )
)
```
---

## NPV ( payment ; interestRate )
Returns the **net present value** of a series of **unequal** future cash flows, discounted at a constant rate. Unlike FV/PV (which assume equal payments), NPV accepts a **repeating field** or a list of values in `payment`.  
Parameters: `payment` — a repeating field or list of cash flows (positive = inflow, negative = outflow); `interestRate` — discount rate per period as decimal.  
Returns: number
```
NPV(Loan;.05)
// → `156.91277445...`, when the repeating field, Loan, contains -2000 (the initial payment), 600, 300, 500, 700, and 400. The result (156.91277445...) is the actual profit in today's dollars that will be realized from this transaction
```
Note: FileMaker's NPV treats `payment` as a repeating field; each repetition is one period's cash flow. Period 0 (initial investment) is typically subtracted from the result manually.

---

## PMT ( principal ; interestRate ; term )
Returns the **payment amount** required per period to fully repay a loan of `principal` over `term` periods at `interestRate` per period. The result is negative (cash flowing out to repay the loan).  
Parameters: `principal` — loan amount (positive); `interestRate` — rate per period as decimal; `term` — number of payment periods.  
Returns: number (negative = payment you make)
```
PMT(21000;.069/12;48)
// → the payment amount `$501.90`
```
Total interest paid over the life of a loan:
```
Let ( [
  p = LoanAmount ;
  r = AnnualRate / 12 ;
  n = TermYears * 12 ;
  monthly = Abs ( PMT ( p ; r ; n ) )
] ;
  monthly * n - p   // total paid minus principal = total interest
)
```
---

## PV ( payment ; interestRate ; periods )
Returns the **present value** of an investment that makes equal periodic payments — the lump sum today that is equivalent to receiving `payment` each period for `periods` periods, discounted at `interestRate`. Useful for valuing an annuity or calculating how much to invest now to receive a fixed income stream.  
Parameters: `payment` — fixed payment received per period (positive); `interestRate` — rate per period as decimal; `periods` — number of periods.  
Returns: number (negative = amount you must invest today; use Abs() for display)
```
PV(500;.05;5)
// → 2164.73833531...
```
Pension/retirement: how long will savings last?
```
// If you have $500,000 and withdraw $3,000/month at 4% return,
// PV tells you the present value of your withdrawal plan.
// If PV ≥ savings, the plan is sustainable:
Abs ( PV ( 3000 ; 0.04/12 ; 240 ) )   // 20-year horizon
// → approx 495,975 (just under $500k, so barely sustainable at 20 years)
```
---

## Combined example: Loan amortisation summary
```
Let ( [
  principal   = 300000 ;
  annualRate  = 0.0625 ;
  termYears   = 30 ;
  r           = annualRate / 12 ;
  n           = termYears * 12 ;
  monthly     = Abs ( PMT ( principal ; r ; n ) ) ;
  totalPaid   = monthly * n ;
  totalInterest = totalPaid - principal
] ;
  "Monthly payment: $" & Round ( monthly ; 2 ) & ¶
  & "Total paid: $" & Round ( totalPaid ; 2 ) & ¶
  & "Total interest: $" & Round ( totalInterest ; 2 )
)
// → Monthly payment: $1,847.15
//   Total paid: $664,973.61
//   Total interest: $364,973.61
```
---

# FileMaker Trigonometric Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/trigonometric-functions.html  
All 9 trigonometric functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** FileMaker's trigonometric functions work in **radians** (not degrees). Use `Degrees()` and `Radians()` to convert. All functions return numeric values with FileMaker's standard precision (~15 significant digits).

**Key constants and conversions:**
```
Pi                              // → 3.14159265358979323846…
Radians ( 180 )                 // → Pi  (π radians = 180°)
Degrees ( Pi )                  // → 180

// Common angle shortcuts:
Radians ( 90 )                  // → π/2  (90°)
Radians ( 45 )                  // → π/4  (45°)
Radians ( 360 )                 // → 2π   (full circle)
```
---

## Pi
A constant — returns the value of π (pi) to FileMaker's full numeric precision.  
Parameters: none.  
Returns: number
```
Pi * 15
// → 47.124
```
---

## Degrees ( angleInRadians )
Converts an angle from **radians to degrees**.  
Parameters: `angleInRadians` — angle in radians.  
Returns: number (degrees)
```
Degrees(Atan(1))
// → 45

Degrees(1.0472)
// → 60.00014030...
```
Display an angle result in degrees:
```
Degrees ( Atan ( opposite / adjacent ) )
// → angle in degrees from an Atan result
```
---

## Radians ( angleInDegrees )
Converts an angle from **degrees to radians**.  
Parameters: `angleInDegrees` — angle in degrees.  
Returns: number (radians)
```
Radians(45)
// → .78539816...
```
---

## Sin ( angleInRadians )
Returns the **sine** of an angle (opposite/hypotenuse in a right triangle).  
Range of results: -1 to 1.  
Parameters: `angleInRadians` — angle in radians.  
Returns: number
```
Sin(Radians(60))
// → .86602

Sin(.610865)
// → .57357624...
```
Vertical component of a vector (e.g. for layout positioning):
```
Let ( [
  angle  = Radians ( BearingDegrees ) ;
  length = VectorLength
] ;
  length * Sin ( angle )    // → vertical displacement
)
```
---

## Cos ( angleInRadians )
Returns the **cosine** of an angle (adjacent/hypotenuse in a right triangle).  
Range of results: -1 to 1.  
Parameters: `angleInRadians` — angle in radians.  
Returns: number
```
Cos(1.047)
// → .50017107...

Cos(Radians(60))
// → .5
```
Horizontal component of a vector:
```
VectorLength * Cos ( Radians ( BearingDegrees ) )
```
---

## Tan ( angleInRadians )
Returns the **tangent** of an angle (opposite/adjacent in a right triangle; equivalent to Sin/Cos).  
Undefined at ±90°, ±270°, etc. (returns a very large number near these angles).  
Parameters: `angleInRadians` — angle in radians.  
Returns: number
```
Tan(.13)
// → .13073731...

Tan(Radians(34))
// → .6745085
```
Calculate height from distance and angle:
```
// Surveying: height of a building given distance (d) and elevation angle (a):
d * Tan ( Radians ( ElevationAngleDegrees ) )
```
---

## Acos ( number )
Returns the **arccosine** (inverse cosine) of a number — the angle (in radians) whose cosine equals `number`.  
Domain: -1 to 1 (outside this range returns empty/error).  
Range of results: 0 to π (0° to 180°).  
Parameters: `number` — a value between -1 and 1.  
Returns: number (radians)
```
Acos(-0.5)
// → 2.0943951

Acos(-0.5)*180/Pi
// → 120

Degrees(Acos(-0.5))
// → 120
```
---

## Asin ( number )
Returns the **arcsine** (inverse sine) of a number — the angle (in radians) whose sine equals `number`.  
Domain: -1 to 1.  
Range of results: -π/2 to π/2 (-90° to 90°).  
Parameters: `number` — a value between -1 and 1.  
Returns: number (radians)
```
Asin(-0.5)
// returns` -0.523598776`.

Degrees(Asin(-0.5))
// → -30
```
---

## Atan ( number )
Returns the **arctangent** (inverse tangent) of a number — the angle (in radians) whose tangent equals `number`.  
Domain: any real number.  
Range of results: -π/2 to π/2 (-90° to 90°).  
Parameters: `number` — any real number.  
Returns: number (radians)
```
Atan(1)
// → .78539816...

Degrees(Atan(1))
// → 45
```
Bearing/heading from coordinate differences (2-argument atan, atan2):
```
// FileMaker has no Atan2; simulate it:
Let ( [
  dx = X2 - X1 ;
  dy = Y2 - Y1 ;
  angle = Degrees ( Atan ( dy / dx ) )
] ;
  Case (
    dx > 0              ; angle ;
    dx < 0 and dy ≥ 0  ; angle + 180 ;
    dx < 0 and dy < 0  ; angle - 180 ;
    dy > 0              ; 90 ;
    dy < 0              ; -90 ;
    0   // dx=0, dy=0: undefined
  )
)
```
---

## Practical examples

**Distance between two GPS coordinates (Haversine formula):**
```
Let ( [
  lat1 = Radians ( Lat1 ) ;
  lat2 = Radians ( Lat2 ) ;
  dLat = Radians ( Lat2 - Lat1 ) ;
  dLon = Radians ( Lon2 - Lon1 ) ;
  a    = Sin(dLat/2)^2 + Cos(lat1) * Cos(lat2) * Sin(dLon/2)^2 ;
  c    = 2 * Atan ( Sqrt(a) / Sqrt(1-a) ) ;
  R    = 6371   // Earth radius in km
] ;
  Round ( R * c ; 2 )    // → distance in km
)
```
**X/Y coordinates on a circle (e.g. clock face or pie chart layout positions):**
```
Let ( [
  angleDeg = ( itemIndex / totalItems ) * 360 ;
  angleRad = Radians ( angleDeg ) ;
  r        = 200   // radius in layout units
] ;
  // X: centre_x + r * Cos(angle)
  // Y: centre_y + r * Sin(angle)
  "x=" & Round( 400 + r * Cos(angleRad) ; 0 )
  & " y=" & Round( 300 + r * Sin(angleRad) ; 0 )
)
```
---

# FileMaker Repeating Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/repeating-functions.html  
All 3 repeating functions with verified syntax, parameters, return types, and usage patterns.  
Last verified: 2026-06 against live Claris Help Centre.

**Overview:** Repeating fields store multiple values in a single field, indexed 1 through N (where N is the number of repetitions configured in the field definition). FileMaker's three Repeating functions let you: extend a non-repeating value across all repetitions of a calculation (`Extend`), access a specific repetition by index (`GetRepetition`), and retrieve the last non-blank value from a repeating field (`Last`). Repeating fields are a legacy feature; consider JSON arrays or related records for new designs, but these functions remain essential for maintaining existing solutions.

**Repeating field basics:**
```
// A repeating field "Scores" with 5 repetitions might hold:
// Scores[1] = 85, Scores[2] = 90, Scores[3] = 78, Scores[4] = "", Scores[5] = ""

// Access in a calculation context uses repetition syntax, but the
// calc itself evaluates for repetition 1 by default unless used in a
// repeating context or combined with GetRepetition().
```
---

## Extend ( non-repeatingField )
Makes a non-repeating (single-value) field available as if it had as many repetitions as the repeating field it is being combined with in a calculation. Without `Extend`, using a non-repeating field in a repeating calculation only populates repetition 1; `Extend` propagates the value across all repetitions.  
Parameters: `non-repeatingField` — any non-repeating field or expression.  
Returns: a repeating value (same type as the input)
```
Extend(TaxRate) * Quantity * ItemPrice
// → 1.197`, `.6606`, and `1.497` when `TaxRate` contains `.06`; the repeating field Quantity contains `1`, `3`, and `5`; and the repeating field ItemPrice contains `19.95`, `3.67`, and `4.99
```
Apply a global tax rate across a repeating price field:
```
// "UnitPrice" is repeating (5 reps), "TaxRate" is non-repeating
UnitPrice * Extend ( 1 + TaxRate )
```
Conditional across repetitions using a non-repeating flag:
```
// Show 0 if record is cancelled, otherwise the repeating values:
If ( Extend ( Status = "Cancelled" ) ; 0 ; Scores )
```
---

## GetRepetition ( repeatingField ; number )
Returns the value of a specific repetition of a repeating field. This is the primary way to access individual repetitions in a calculation when you know the index at runtime (rather than design time).  
Parameters: `repeatingField` — a repeating field; `number` — the repetition index (1-based).  
Returns: same type as the field
```
GetRepetition ( ParcelBids ; 2 )
// → 1200

GetRepetition ( ParcelBids ; 5 )
// → nothing
```
Dynamic access — access the repetition matching the current record count:
```
GetRepetition ( MonthlyBudget ; Month ( Get(CurrentDate) ) )
// → budget for the current month (1=Jan, 12=Dec)
```
Sum selected repetitions:
```
GetRepetition ( Values ; 1 ) + GetRepetition ( Values ; 2 ) + GetRepetition ( Values ; 3 )
```
Find the index of the first non-blank repetition:
```
Let ( [
  r1 = GetRepetition ( Scores ; 1 ) ;
  r2 = GetRepetition ( Scores ; 2 ) ;
  r3 = GetRepetition ( Scores ; 3 )
] ;
  Case (
    not IsEmpty(r1) ; 1 ;
    not IsEmpty(r2) ; 2 ;
    not IsEmpty(r3) ; 3 ;
    0
  )
)
```
Build a ¶-delimited list from a repeating field (often needed to bridge to modern patterns):
```
Let ( [
  r1 = GetRepetition ( Tags ; 1 ) ;
  r2 = GetRepetition ( Tags ; 2 ) ;
  r3 = GetRepetition ( Tags ; 3 )
] ;
  List ( r1 ; r2 ; r3 )
)
// List() ignores empty values — safe to call with all reps
```
---

## Last ( repeatingField )
Returns the value of the **last non-blank repetition** in a repeating field. Useful for "current value" patterns where repetitions are used as a simple history log (earliest to latest, left to right).  
Parameters: `repeatingField` — a repeating field.  
Returns: same type as the field
```
Last(ParcelBids)
// → `1500` if ParcelBids is a number field defined to repeat with ten values and contains the values 2500, 1200, and 1500
```
Running-total pattern — use a repeating field as a simple log:
```
// Each script run sets the next empty repetition.
// Last() always gives the most recent entry.
Last ( AuditLog )    // → most recent audit entry
```
Check if all repetitions are filled (Last on a full field = last repetition):
```
not IsEmpty ( GetRepetition ( Scores ; 10 ) )
// True = all 10 repetitions are filled (or at least rep 10 is)
```
---

## Interaction patterns

Convert repeating field to JSON array (bridging legacy to modern):
```
// For a repeating field with known max repetitions (e.g. 5):
Let ( [
  vals = List (
    GetRepetition(Scores;1) ; GetRepetition(Scores;2) ;
    GetRepetition(Scores;3) ; GetRepetition(Scores;4) ;
    GetRepetition(Scores;5)
  ) ;
  count = ValueCount ( vals )
] ;
  // Build JSON array from the list
  Substitute (
    JSONSetElement ( "[]" ; [0 ; GetValue(vals;1) ; JSONNumber] ) ;
    // ...extend pattern for each value
    "" ; ""
  )
)
// In practice, use a While() loop for arbitrary repetition counts
```
Sum all non-blank repetitions using Aggregate functions:
```
// Aggregate functions naturally work across repetitions:
Sum ( Scores )       // → sum of all non-blank repetitions
Max ( Scores )       // → highest value across all repetitions
Count ( Scores )     // → number of non-blank repetitions
```
