# Text & Text Formatting Functions — Examples

## Contents
- Text Functions
  - Char ( number )
  - Code ( text )
  - Exact ( originalText ; comparisonText )
  - Filter ( textToFilter ; filterText )
  - FilterValues ( textToFilter ; filterValues )
  - GetAsCSS ( text )
  - GetAsDate ( text )
  - GetAsNumber ( text )
  - GetAsSVG ( text )
  - GetAsText ( data )
  - GetAsTime ( text )
  - GetAsTimestamp ( text )
  - GetAsURLEncoded ( text )
  - GetValue ( listOfValues ; valueNumber )
  - Left ( text ; numberOfCharacters )
  - LeftValues ( text ; numberOfValues )
  - LeftWords ( text ; numberOfWords )
  - Length ( text )
  - Lower ( text )
  - Middle ( text ; start ; numberOfCharacters )
  - MiddleValues ( text ; startingValue ; numberOfValues )
  - MiddleWords ( text ; startingWord ; numberOfWords )
  - PatternCount ( text ; searchString )
  - Position ( text ; searchString ; start ; occurrence )
  - Proper ( text )
  - Quote ( text )
  - Replace ( text ; start ; numberOfCharacters ; replacementText )
  - Right ( text ; numberOfCharacters )
  - RightValues ( text ; numberOfValues )
  - RightWords ( text ; numberOfWords )
  - SerialIncrement ( text ; incrementBy )
  - SortValues ( values {; datatype ; locale } )
  - Substitute ( text ; searchString ; replaceString )
  - Trim ( text )
  - TrimAll ( text ; trimSpaces ; trimType )
  - UniqueValues ( values {; datatype ; locale } )
  - Upper ( text )
  - ValueCount ( text )
  - WordCount ( text )
- Text Formatting Functions
  - RGB ( red ; green ; blue )
  - TextColor ( text ; RGB ( red ; green ; blue ) )
  - TextColorRemove ( text {; RGB ( red ; green ; blue )} )
  - TextFont ( text ; fontName )
  - TextFontRemove ( text {; fontToRemove } )
  - TextFormatRemove ( text )
  - TextSize ( text ; fontSize )
  - TextSizeRemove ( text {; sizeToRemove } )
  - TextStyleAdd ( text ; styles )
  - TextStyleRemove ( text ; styles )

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
Returns the Unicode code points of **all** characters in `text`. With more than one character, each code point is a five-digit group, the first character in the lowest five digits. `""` returns empty. Useful with `Get ( TriggerKeystroke )` (tab = 9, return = 13, arrows = 28–31).  
`Code ( "A" )` → `65`  
`Code ( "☺" )` → `9786`  
`Code ( "ab" )` → `9800097`

---

## Exact ( originalText ; comparisonText )
Returns 1 (true) if both values match exactly (case-sensitive); otherwise 0. Text styles are ignored. Container data must also be stored the same way (embedded or by reference).  
`Exact ( "Hello" ; "Hello" )` → `1`  
`Exact ( "Hello" ; "hello" )` → `0`

---

## Filter ( textToFilter ; filterText )
Returns only the characters from *textToFilter* that appear in *filterText*, in original order.  
`Filter ( "A1B2C3" ; "ABC" )` → `ABC`  
`Filter ( "(555) 867-5309" ; "0123456789" )` → `5558675309`

---

## FilterValues ( textToFilter ; filterValues )
Returns only the values from *textToFilter* that appear in *filterValues*, in their original order. **Not** case-sensitive. Every returned value ends with ¶.  
```
FilterValues ( "Plaid¶Canvas¶Suitcase" ; "Plaid¶Canvas" )
// → Plaid¶Canvas¶

FilterValues ( "Plaid¶Canvas¶Suitcase" ; "plaid¶canvas" )
// → Plaid¶Canvas¶
```

---

## GetAsCSS ( text )
Returns text with its FileMaker formatting converted to CSS (Cascading Style Sheets) format.  
`GetAsCSS ( StyledTextField )` → CSS representation of the styled text

---

## GetAsDate ( text )
Returns text interpreted as a date, typed as Date.  
Text must be in the date format of the system the **file was created on** — a file created on an en_AU Mac expects `25/12/2024`, a US one `12/25/2024`. Use `Date ( month ; day ; year )` for locale-proof constants. A number is treated as days since 1/1/0001.  
`GetAsDate ( 737342 )` → `10/10/2019` (US display)

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
`GetAsText ( 42 )` → `42`  
`GetAsText ( Date ( 12 ; 25 ; 2024 ) )` returns 12/25/2024 in a US-format file and 25/12/2024 in an Australian one — dates convert using the file's date format.  
For a container: the external path information, or `?` if the data is embedded.

---

## GetAsTime ( text )
Returns text interpreted as a time, typed as Time.  
`GetAsTime ( "9:30:00" )` → `9:30:00` (as Time type)  
`GetAsTime ( "21:45" )` → `9:45:00 PM`

---

## GetAsTimestamp ( text )
Returns text as a timestamp. Text must be a date then a time, in the date and time formats of the system the **file was created on**. A number is read as seconds since 1/1/0001.  
`GetAsTimestamp ( 50000 )` → `1/1/0001 1:53:20 PM` (US display)  
For locale-proof constants use `Timestamp ( Date ( 12 ; 25 ; 2024 ) ; Time ( 9 ; 30 ; 0 ) )`.

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

## Middle ( text ; start ; numberOfCharacters )
Returns *numberOfCharacters* characters starting at *start* (values ≤ 1 start at 1).  
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
Returns text enclosed in double quotation marks, with special characters escaped — protects text from being run by `Evaluate`.  
`Quote ( "Hello" )` → `"Hello"`  
`Quote ( "say \"hello\" fred" )` → `"say \"hello\" fred"`  
`Evaluate ( Quote ( "1 + 2" ) )` → `1 + 2`

---

## Replace ( text ; start ; numberOfCharacters ; replacementText )
Replaces *numberOfCharacters* characters in *text* starting at *start* with *replacementText*. Use `0` characters to insert.  
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

## SortValues ( values {; datatype ; locale } )
Sorts a list of values. Both extra parameters are optional — with neither, values sort as text, ascending, in the file's locale. *Originated: 16.0*  
- *datatype*: 1 text · 2 number · 3 date · 4 time · 5 timestamp. **Negative sorts descending** (`-2` = numbers, high to low).
- *locale*: a name such as `English`, `German`, `Japanese`, `Unicode_Raw`; an unrecognised name returns `?`.

Every returned value ends with ¶.  
`SortValues ( "Banana¶Apple¶Cherry" )` → `Apple¶Banana¶Cherry¶`  
`SortValues ( "10¶2¶20¶1" ; 2 )` → `1¶2¶10¶20¶`  
`SortValues ( "34¶600¶18¶29" ; -2 )` → `600¶34¶29¶18¶`

---

## Substitute ( text ; searchString ; replaceString )
Replaces every occurrence of *searchString* in *text* with *replaceString*. **Case-sensitive** (unlike `PatternCount` and `Position`).  
`Substitute ( "Hello World" ; "World" ; "FileMaker" )` → `Hello FileMaker`  
`Substitute ( "aabbcc" ; "b" ; "x" )` → `aaxxcc`

Multiple substitutions: each bracket is one `[ search ; replace ]` **pair**, applied in order (a later pair can change an earlier pair's output):  
`Substitute ( "Hello World" ; [ "Hello" ; "Goodbye" ] ; [ "World" ; "FileMaker" ] )` → `Goodbye FileMaker`  
⚠️ `[ "Hello" ; "World" ]` means *replace Hello **with** World* — `Substitute ( "Hello World" ; ["Hello" ; "World"] ; ["Goodbye" ; "FileMaker"] )` → `World World`.

---

## Trim ( text )
Removes leading and trailing spaces from text.  
`Trim ( "  Hello World  " )` → `Hello World`  
`Trim ( "  spaces  " )` → `spaces`

---

## TrimAll ( text ; trimSpaces ; trimType )
Removes or inserts spaces, mainly for mixing **roman** and **non-roman** (CJK) text. For plain leading/trailing spaces use `Trim`.  
- *trimSpaces*: `1` also removes **full-width** spaces; `0` keeps them.  
- *trimType* (spacing between non-roman and roman characters; non-roman ↔ non-roman spaces are always removed):  
  `0` remove; one space between roman words · `1` always one half-width space between non-roman and roman · `2` reduce multiple spaces to one, add none · `3` remove all spaces.

`TrimAll ( "Hello   World" ; 1 ; 0 )` → `Hello World`  
`TrimAll ( "  FileMaker  Pro " ; 0 ; 3 )` → `FileMakerPro`

---

## UniqueValues ( values {; datatype ; locale } )
Returns the list with duplicates removed, in original order — it does **not** sort. *datatype* (1–5, as SortValues) and *locale* only change how uniqueness is judged; `Unicode_Raw` makes it case- and accent-sensitive. *Originated: 16.0*  
`UniqueValues ( "Apple¶Banana¶Apple¶Cherry¶Banana" )` → `Apple¶Banana¶Cherry¶`  
`UniqueValues ( "34¶600¶18¶600¶18.0" ; 2 )` → `34¶600¶18¶`

---

## Upper ( text )
Returns all letters in text as uppercase.  
`Upper ( "FileMaker Pro" )` → `FILEMAKER PRO`  
`Upper ( "hello" )` → `HELLO`

---

## ValueCount ( text )
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
`RGB ( 255 ; 165 ; 0 )` → `16753920` (orange)

Combine with TextColor — FirstName in orange, LastName in purple:
```
TextColor ( FirstName ; RGB ( 255 ; 165 ; 0 ) ) & " " & TextColor ( LastName ; RGB ( 160 ; 32 ; 240 ) )
```
---

## TextColor ( text ; RGB ( red ; green ; blue ) )
Changes the colour of `text` to the colour specified by the RGB function. Not supported in FileMaker WebDirect.  
Returns: text (with colour applied)

`TextColor ( "Warning" ; RGB ( 255 ; 0 ; 0 ) )` → `Warning` rendered in red  
`TextColor ( StatusField ; RGB ( 0 ; 128 ; 0 ) )` → field text rendered in green

---

## TextColorRemove ( text {; RGB ( red ; green ; blue )} )
Removes font colours from text. Without the optional RGB parameter, removes all colours; with it, removes only the specified colour.  
Returns: text

`TextColorRemove ( ColouredField )` → all colour removed  
`TextColorRemove ( ColouredField ; RGB ( 255 ; 0 ; 0 ) )` → only red removed; other colours retained

---

## TextFont ( text ; fontName )
Changes the font of `text` to `fontName` (exact spelling). Formatting is lost if the result is stored in a non-text field.  
Legacy: older releases documented a third `fontScript` parameter. The engine still accepts it, but current Claris docs omit it — don't add it to new code.  
Returns: text

`TextFont ( "Hello" ; "Courier" )` → `Hello` in Courier  
`TextFont ( TitleField ; "Arial" )` → TitleField text rendered in Arial

---

## TextFontRemove ( text {; fontToRemove } )
Removes all fonts, or only `fontToRemove`, reverting that text to the field's default font. (Legacy `fontScript` third parameter: as TextFont.)  
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

## TextSizeRemove ( text {; sizeToRemove } )
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

`TextStyleAdd ( "Plaid" ; Italic )` returns Plaid in italics  
`TextStyleAdd ( FirstName ; Bold + Underline )` → **Sophie** underlined  
`TextStyleAdd ( "draft" ; Uppercase )` → *displays* as DRAFT; the stored text is still `draft`. To change the data, use `Upper`.

Reset then re-style in one expression:
```
TextStyleAdd ( TextStyleAdd ( FirstName ; Plain ) ; Italic )
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
