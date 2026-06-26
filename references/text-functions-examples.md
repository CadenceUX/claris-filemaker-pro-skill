# Text & Text Formatting Functions — Examples

---

# FileMaker Text Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/text-functions.html  
All 39 native text functions with format, parameters, and examples.

---

## Char ( number )
Returns the character(s) for the given Unicode code point(s).  
`Char ( 65 )` → `A`  
`Char ( 9786 )` → `☺`

---

## Code ( text )
Returns the Unicode code point for the first character of text.  
`Code ( "A" )` → `65`  
`Code ( "☺" )` → `9786`

---

## Exact ( text1 ; text2 )
Returns 1 (true) if both values match exactly (case-sensitive); otherwise 0.  
`Exact ( "Hello" ; "Hello" )` → `1`  
`Exact ( "Hello" ; "hello" )` → `0`

---

## Filter ( textToFilter ; filterText )
Returns only the characters from *textToFilter* that appear in *filterText*, in original order.  
`Filter ( "A1B2C3" ; "ABC" )` → `ABC`  
`Filter ( "(555) 867-5309" ; "0123456789" )` → `5558675309`

---

## FilterValues ( textToFilter ; filterValues )
Returns only the values (return-delimited) from *textToFilter* that appear in *filterValues*.  
```
FilterValues ( "Plaid¶Canvas¶Suitcase" ; "Plaid¶Canvas" )
// → Plaid¶Canvas¶
```
→ `Banana¶Cherry`

---

## GetAsCSS ( text )
Returns text with its FileMaker formatting converted to CSS (Cascading Style Sheets) format.  
`GetAsCSS ( StyledTextField )` → CSS representation of the styled text

---

## GetAsDate ( text )
Returns text interpreted as a date, typed as Date.  
`GetAsDate ( "12/25/2024" )` → `12/25/2024` (as Date type)  
`GetAsDate ( "25.12.2024" )` → `12/25/2024` (system locale dependent)

---

## GetAsNumber ( text )
Strips all non-numeric characters and returns a Number.  
`GetAsNumber ( "FY2024" )` → `2024`  
`GetAsNumber ( "$1,254.50" )` → `1254.5`  
`GetAsNumber ( "(42)" )` → `-42`

---

## GetAsSVG ( text )
Returns text with its FileMaker formatting converted to SVG (Scalable Vector Graphics) format.  
`GetAsSVG ( StyledTextField )` → SVG XML representation of the styled text

---

## GetAsText ( data )
Returns any data type as Text.  
`GetAsText ( Date ( 12 ; 25 ; 2024 ) )` → `"12/25/2024"`  
`GetAsText ( 42 )` → `"42"`

---

## GetAsTime ( text )
Returns text interpreted as a time, typed as Time.  
`GetAsTime ( "9:30:00" )` → `9:30:00` (as Time type)  
`GetAsTime ( "21:45" )` → `9:45:00 PM`

---

## GetAsTimestamp ( text )
Returns text interpreted as a timestamp, typed as Timestamp.  
`GetAsTimestamp ( "12/25/2024 09:30:00" )` → `12/25/2024 9:30:00 AM` (as Timestamp type)

---

## GetAsURLEncoded ( text )
Returns text encoded for use in a URL (percent-encoding).  
`GetAsURLEncoded ( "hello world" )` → `hello%20world`  
`GetAsURLEncoded ( "name=John&city=New York" )` → `name%3DJohn%26city%3DNew%20York`

---

## GetValue ( listOfValues ; valueNumber )
Returns the value at position *valueNumber* from a return-delimited list.  
`GetValue ( "Apple¶Banana¶Cherry" ; 2 )` → `Banana`  
`GetValue ( "Apple¶Banana¶Cherry" ; 4 )` → `` (empty — beyond list length)

---

## Left ( text ; numberOfCharacters )
Returns the first *numberOfCharacters* characters from the left of text.  
`Left ( "FileMaker" ; 4 )` → `File`  
`Left ( "Hello World" ; 5 )` → `Hello`

---

## LeftValues ( text ; numberOfValues )
Returns the first *numberOfValues* values from a return-delimited list.  
`LeftValues ( "Apple¶Banana¶Cherry¶Date" ; 2 )` → `Apple¶Banana¶`

---

## LeftWords ( text ; numberOfWords )
Returns the first *numberOfWords* words from text.  
`LeftWords ( "The quick brown fox" ; 2 )` → `The quick`

---

## Length ( text )
Returns the number of characters in text, including spaces and special characters.  
`Length ( "Hello" )` → `5`  
`Length ( "Hello World" )` → `11`  
`Length ( "" )` → `0`

---

## Lower ( text )
Returns all letters in text as lowercase.  
`Lower ( "FileMaker Pro" )` → `filemaker pro`  
`Lower ( "ABC123" )` → `abc123`

---

## Middle ( text ; startCharacter ; numberOfCharacters )
Returns *numberOfCharacters* characters starting at *startCharacter*.  
`Middle ( "FileMaker" ; 5 ; 4 )` → `Make`  
`Middle ( "Hello World" ; 7 ; 5 )` → `World`

---

## MiddleValues ( text ; startingValue ; numberOfValues )
Returns *numberOfValues* values from a return-delimited list starting at *startingValue*.  
`MiddleValues ( "Apple¶Banana¶Cherry¶Date" ; 2 ; 2 )` → `Banana¶Cherry¶`

---

## MiddleWords ( text ; startingWord ; numberOfWords )
Returns *numberOfWords* words starting at *startingWord*.  
`MiddleWords ( "The quick brown fox" ; 2 ; 2 )` → `quick brown`

---

## PatternCount ( text ; searchString )
Returns the number of times *searchString* occurs in *text* (case-insensitive).  
`PatternCount ( "banana" ; "an" )` → `2`  
`PatternCount ( "Hello World" ; "o" )` → `2`  
`PatternCount ( "FileMaker" ; "xyz" )` → `0`

---

## Position ( text ; searchString ; start ; occurrence )
Returns the character position of the *occurrence*-th instance of *searchString* in *text*, starting search at *start*.  
`Position ( "Hello World" ; "o" ; 1 ; 1 )` → `5`  
`Position ( "Hello World" ; "o" ; 1 ; 2 )` → `8`  
`Position ( "banana" ; "an" ; 1 ; 2 )` → `4`

---

## Proper ( text )
Returns text with the first letter of each word capitalised, all others lowercase.  
`Proper ( "hello world" )` → `Hello World`  
`Proper ( "JOHN SMITH" )` → `John Smith`

---

## Quote ( text )
Returns text enclosed in double quotation marks, with internal quotes escaped.  
`Quote ( "Hello" )` → `"Hello"`  
`Quote ( "He said "hello"" )` → `"He said \"hello\""`

---

## Replace ( text ; startCharacter ; numberOfCharacters ; replacementText )
Replaces *numberOfCharacters* characters in *text* starting at *startCharacter* with *replacementText*.  
`Replace ( "Hello World" ; 7 ; 5 ; "FileMaker" )` → `Hello FileMaker`  
`Replace ( "2024-01-15" ; 5 ; 1 ; "/" )` → `2024/01-15`

---

## Right ( text ; numberOfCharacters )
Returns the last *numberOfCharacters* characters from the right of text.  
`Right ( "FileMaker" ; 5 )` → `Maker`  
`Right ( "Hello World" ; 5 )` → `World`

---

## RightValues ( text ; numberOfValues )
Returns the last *numberOfValues* values from a return-delimited list.  
`RightValues ( "Apple¶Banana¶Cherry¶Date" ; 2 )` → `Cherry¶Date¶`

---

## RightWords ( text ; numberOfWords )
Returns the last *numberOfWords* words from text.  
`RightWords ( "The quick brown fox" ; 2 )` → `brown fox`

---

## SerialIncrement ( text ; incrementBy )
Returns text with the trailing number incremented by *incrementBy*.  
`SerialIncrement ( "INV-001" ; 1 )` → `INV-002`  
`SerialIncrement ( "INV-009" ; 1 )` → `INV-010`  
`SerialIncrement ( "A100" ; 5 )` → `A105`

---

## SortValues ( listOfValues ; sortType { ; locale } )
Returns a return-delimited list sorted by *sortType*: 1=text, 2=numeric, 3=date, 4=time, 5=timestamp.  
`SortValues ( "Banana¶Apple¶Cherry" ; 1 )` → `Apple¶Banana¶Cherry¶`  
`SortValues ( "10¶2¶20¶1" ; 2 )` → `1¶2¶10¶20¶`

---

## Substitute ( text ; searchString ; replaceString )
Replaces every occurrence of *searchString* in *text* with *replaceString*.  
`Substitute ( "Hello World" ; "World" ; "FileMaker" )` → `Hello FileMaker`  
`Substitute ( "aabbcc" ; "b" ; "x" )` → `aaxxcc`

Substitute also accepts lists to replace multiple strings in one call:  
`Substitute ( "Hello World" ; ["Hello" ; "World"] ; ["Goodbye" ; "FileMaker"] )` → `Goodbye FileMaker`

---

## Trim ( text )
Removes leading and trailing spaces from text.  
`Trim ( "  Hello World  " )` → `Hello World`  
`Trim ( "  spaces  " )` → `spaces`

---

## TrimAll ( text ; trimSpaces ; trimType )
Removes or normalises spaces based on *trimType* and *trimSpaces* settings.  
- *trimSpaces*: 1 = trim all spaces, 0 = normalise only  
- *trimType*: 0 = all spaces, 1 = leading/trailing only  
`TrimAll ( "Hello   World" ; 1 ; 0 )` → `Hello World` (collapses multiple spaces)

---

## UniqueValues ( listOfValues { ; sortType ; locale } )
Returns a return-delimited list with duplicate values removed.  
`UniqueValues ( "Apple¶Banana¶Apple¶Cherry¶Banana" ; 1 )` → `Apple¶Banana¶Cherry¶`

---

## Upper ( text )
Returns all letters in text as uppercase.  
`Upper ( "FileMaker Pro" )` → `FILEMAKER PRO`  
`Upper ( "hello" )` → `HELLO`

---

## ValueCount ( listOfValues )
Returns the count of values in a return-delimited list.  
`ValueCount ( "Apple¶Banana¶Cherry" )` → `3`  
`ValueCount ( "" )` → `0`

---

## WordCount ( text )
Returns the count of words in text.  
`WordCount ( "The quick brown fox" )` → `4`  
`WordCount ( "FileMaker" )` → `1`  
`WordCount ( "" )` → `0`

---

*Source: https://help.claris.com/en/pro-help/content/text-functions.html*  
*Individual pages: https://help.claris.com/en/pro-help/content/{function-slug}.html*

---

# FileMaker Text Formatting Functions — Syntax & Examples

Source: https://help.claris.com/en/pro-help/content/text-formatting-functions.html  
All 10 native text formatting functions with format, parameters, and examples.

Text formatting functions operate on fields of type text, text constants (in quotations), and expressions with a text result. **Note:** Text formatting is lost if the result is stored in a non-text field type.

---

## RGB ( red ; green ; blue )
Returns an integer from 0 to 16777215 by combining colour values.  
Parameters: `red`, `green`, `blue` — each a numeric expression from 0 to 255.  
Returns: number  
Formula: `red × 65536 + green × 256 + blue`

`RGB ( 255 ; 0 ; 0 )` → `16711680` (red)  
`RGB ( 0 ; 255 ; 0 )` → `65280` (green)  
`RGB ( 0 ; 0 ; 255 )` → `255` (blue)  
`RGB ( 0 ; 0 ; 0 )` → `0` (black)  
`RGB ( 255 ; 255 ; 255 )` → `16777215` (white)  
`RGB ( 255 ; 165 ; 0 )` → `16744192` (orange)

Combine with TextColor to display FirstName in orange and LastName in purple:
```
RGB(255;0;0)
// → `16711680` representing red

RGB(0;255;0)
// → `65280` representing green

RGB(0;0;255)
// → `255` representing blue

RGB(0;0;0)
// → `0` representing black

RGB(255;255;255)
// → `16777215` representing white
```
---

## TextColor ( text ; RGB ( red ; green ; blue ) )
Changes the colour of `text` to the colour specified by the RGB function.  
Returns: text (with colour applied)

`TextColor ( "Warning" ; RGB ( 255 ; 0 ; 0 ) )` → `Warning` rendered in red  
`TextColor ( StatusField ; RGB ( 0 ; 128 ; 0 ) )` → field text rendered in green

---

## TextColorRemove ( text { ; RGB ( red ; green ; blue ) } )
Removes font colours from text. Without the optional RGB parameter, removes all colours; with it, removes only the specified colour.  
Returns: text

`TextColorRemove ( ColouredField )` → all colour removed  
`TextColorRemove ( ColouredField ; RGB ( 255 ; 0 ; 0 ) )` → only red removed; other colours retained

---

## TextFont ( text ; fontName { ; fontScript } )
Changes the font of `text` to `fontName`. Optional `fontScript` specifies the font script (e.g. "Roman", "Japanese").  
Returns: text

`TextFont ( "Hello" ; "Courier" )` → `Hello` in Courier  
`TextFont ( TitleField ; "Arial" )` → TitleField text rendered in Arial

---

## TextFontRemove ( text { ; fontToRemove { ; fontScript } } )
Removes all fonts or a specific font from text. Without parameters it removes all fonts; with `fontToRemove` it removes only that font.  
Returns: text

`TextFontRemove ( FormattedField )` → all font assignments removed  
`TextFontRemove ( FormattedField ; "Arial" )` → only Arial removed; other fonts retained

---

## TextFormatRemove ( text )
Removes all text formatting (colour, font, size, style) from text in a single action.  
Returns: text (plain, unformatted)

`TextFormatRemove ( StyledField )` → plain text with no formatting  

Useful for normalising styled text before storage or comparison:
```
TextFormatRemove ( "Plaid" )
// → the word `Plaid` without any text formatting applied
```
---

## TextSize ( text ; fontSize )
Changes the font size of `text` to `fontSize` (in points).  
Returns: text

`TextSize ( "Heading" ; 18 )` → `Heading` at 18pt  
`TextSize ( BodyField ; 11 )` → BodyField text at 11pt

---

## TextSizeRemove ( text { ; sizeToRemove } )
Removes all font sizes from text, or only the specified `sizeToRemove`.  
Returns: text

`TextSizeRemove ( FormattedField )` → all font-size assignments removed  
`TextSizeRemove ( FormattedField ; 18 )` → only 18pt size removed

---

## TextStyleAdd ( text ; styles )
Adds one or more styles to `text`. Combine multiple styles with the `+` operator.  
Returns: text  

Available style names (not case-sensitive, no spaces):  
`Plain` `Bold` `Italic` `Underline` `HighlightYellow` `Condense` `Extend` `Strikethrough` `SmallCaps` `Superscript` `Subscript` `Uppercase` `Lowercase` `Titlecase` `WordUnderline` `DoubleUnderline` `AllStyles`

**Notes:**
- `Plain` removes all styles when used alone.
- `Plain` is ignored when combined with other styles.
- Negative values are not valid.

`TextStyleAdd ( "Plaid" ; Italic )` → *Plaid* (italic)  
`TextStyleAdd ( FirstName ; Bold + Underline )` → **Sophie** underlined  
`TextStyleAdd ( "draft" ; Uppercase )` → `DRAFT`

Reset then re-style in one expression:
```
TextStyleAdd ( "Plaid" ; Italic )
// → the word `Plaid` in italics

TextStyleAdd ( FirstName ; Bold+Underline )
// → `Sophie` in bold, underlined text when the FirstName field contains Sophie
```
Use with `Let` for multiple style blocks:
```
Let ( [
  TitleStyle = SmallCaps + Titlecase ;
  BodyStyle = Plain
] ;
  TextStyleAdd ( titleField ; TitleStyle ) & "¶¶" & TextStyleAdd ( bodyField ; BodyStyle )
)
```
---

## TextStyleRemove ( text ; styles )
Removes one or more styles from `text`. Use `AllStyles` to strip everything.  
Returns: text

`TextStyleRemove ( BoldField ; Bold )` → bold removed  
`TextStyleRemove ( FormattedField ; AllStyles )` → all styles removed  
`TextStyleRemove ( FormattedField ; Bold + Italic )` → bold and italic removed, other styles kept
