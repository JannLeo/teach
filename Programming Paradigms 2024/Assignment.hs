module Assignment (markdownParser, convertADT,convertADTHTML) where

import           Data.Time.Clock  (getCurrentTime)
import           Data.Time.Format (defaultTimeLocale, formatTime)
import           Instances        (Parser (..))
import           Parser           (eof,trimWhitespace, is, string, isNot, spaces, space, spaces1, digit, noneof)
import           Control.Applicative (optional, some, many, (<|>))
import           Control.Monad    (guard) -- to use guard

data ADT = 
  Italic String
  | Bold String
  | Strikethrough String
  | Link String String        -- link text and URL
  | InlineCode String
  | Footnote Int
  | Image String String String
  | FootnoteRef Int String    -- footnoteRef number and content
  | FreeText String           -- free text containing modifiers
  | Heading Int String        -- heading level and content
  | Blockquote [String]      -- blockquote with multiple lines of text
  | CodeBlock (Maybe String) String    -- optional language identifier and code content
  | OrderedList [[ADT]]       -- ordered list with items, including sublists
  | Table [[ADT]] [[ADT]]     -- header row and content rows of the table
  deriving (Show, Eq)

parseTextOrModifier :: Parser ADT
parseTextOrModifier = 
  parseBold 
  <|> parseItalic 
  <|> parseStrikethrough 
  <|> parseLink 
  <|> parseInlineCode 
  <|> parseFootnote
  <|> parseFreeText

-- Parser for Italic Text (_text_)
parseItalic :: Parser ADT
parseItalic = do
    _ <- is '_'
    content <- some (isNot '_')   -- Use a parser 'isNot' to parse until "_" symbol.
    _ <- is '_'
    return $ Italic content       -- Return the Italic ADT with the parsed content

-- Parser for Bold Text (**text**)
parseBold :: Parser ADT
parseBold = do
    _ <- string "**"
    content <- some (isNot '*')   -- Parse the content until the closing double asterisks
    _ <- string "**"
    return $ Bold content         -- Return the Bold ADT with the parsed content

-- Parser for Strikethrough Text (~~text~~)
parseStrikethrough :: Parser ADT
parseStrikethrough = do
    _ <- string "~~"
    content <- some (isNot '~')     -- Parse the content until the closing double tildes
    _ <- string "~~"
    return $ Strikethrough content  -- Return the Strikethrough ADT with the parsed content

-- Parser for Link ([link text](URL))
parseLink :: Parser ADT
parseLink = do
    _ <- is '['
    linkText <- some (isNot ']')  -- Parse the link text until the closing bracket
    _ <- is ']'
    _ <- is '('
    url <- some (isNot ')')       -- Parse the URL until the closing parenthesis
    _ <- is ')'
    return $ Link linkText url    -- Return the Link ADT with the link text and URL

-- Parser for Inline Code (`code`)
parseInlineCode :: Parser ADT
parseInlineCode = do
    _ <- is '`'
    content <- some (isNot '`')    -- Parse the content until the closing backtick
    _ <- is '`'
    return $ InlineCode content    -- Return the InlineCode ADT with the parsed content

-- Parser for Footnote ([^1])      
parseFootnote :: Parser ADT
parseFootnote = do
    _ <- string "[^"
    number <- some (digit)            -- Parse the footnote number
    _ <- is ']'
    _ <- isNot ':'
    return $ Footnote (read number)   -- Return the Footnote ADT with the parsed number

-- Parser for Footnote Reference ([^1]: text)
parseFootnoteRef :: Parser ADT
parseFootnoteRef = do
    _ <- optional (spaces)          -- Optional leading whitespace before the [^
    _ <- string "[^"
    number <- some digit           -- Parse footnote number (one or more digits)
    _ <- is ']'
    _ <- is ':'
    _ <- optional (spaces)          -- Optional spaces after the colon
    content <- some (isNot '\n')   -- Parse content until a newline
    return $ FootnoteRef (read number) content

-- Parser for Image (![Alt Text](URL "Caption Text"))
parseImage :: Parser ADT
parseImage = do
    _ <- spaces      -- a parser that will parse zero or more spaces (many space)
    _ <- is '!'
    _ <- is '['
    altText <- some (isNot ']')
    _ <- is ']'
    _ <- is '('
    url <- some (noneof " \"")
    _ <- space
    _ <- is '"'
    captionText <- some (isNot '"')
    _ <- is '"'
    _ <- is ')'
    return $ Image altText url captionText


-- Parser for Free Text (any text including modifiers)
parseFreeText :: Parser ADT
parseFreeText = do
    content <- many parseTextOrModifier          -- (isNot '\n')
    _ <- optional (is '\n')
    -- let contentString = concatMap elementToString content
    return $ FreeText (String content)

-- Combined Heading Parser
parseHeading :: Parser ADT
parseHeading = parseHashHeading <|> parseSetextHeading

-- Parser for Heading (# Heading 1)
parseHashHeading :: Parser ADT
parseHashHeading = do
    _ <- optional (spaces)           -- Optional leading whitespace
    hashes <- some (is '#')   -- some-> must has a space after#
    guard (length hashes <= 6)  -- Up to 6 levels of headings
    _ <- space                       -- At least one space after hashes
    content <- some (isNot '\n')
    return $ Heading (length hashes) content

-- Parser for Setext-style Headings (e.g., Heading 1\n======)
parseSetextHeading :: Parser ADT
parseSetextHeading = do
    -- Parse the first line, which is the heading text
    _ <- optional (spaces)
    content <- some (isNot '\n')
    _ <- is '\n'
    -- Parse the second line, which must contain only '=' or '-' characters
    _ <- optional (spaces)
    line <- some (is '=' <|> is '-')
    let level = if head line == '=' then 1 else 2
    guard (all (== head line) line && length line >= 2) -- Ensure at least two `=` or `-` characters and they are all the same
    return $ Heading level (trimWhitespace content)

-- Parser for Blockquote (> text)
parseBlockquote :: Parser ADT
parseBlockquote = do
    lines <- some parseBlockquoteLine
    return $ Blockquote lines   
  where
    parseBlockquoteLine = do
        _ <- optional (spaces)     -- Optional leading whitespace before '>'
        _ <- is '>'
        _ <- optional (spaces)     -- Optional whitespace after '>'
        content <- some (isNot '\n')
        return content

-- Parser for Code Block (``` code content ```)
parseCodeBlock :: Parser ADT
parseCodeBlock = do
    _ <- optional (spaces)           -- Optional leading whitespace before ```
    _ <- string "```"
    optionalLang <- optional (some (isNot '\n'))  -- Optional language identifier
    _ <- is '\n'                    -- Newline
    content <- some (isNot '`')  -- Parse until closing backticks
    _ <- string "```"
    return $ CodeBlock optionalLang content

-- Parser for Ordered List (1. Item)
parseOrderedList :: Parser ADT
parseOrderedList = do
    firstItem <- parseFirstOrderedListItem            -- Parse the first item, which must be `1`
    restItems <- many parseSubsequentOrderedListItem  -- Parse subsequent items
    return $ OrderedList (firstItem : restItems)
  where
    parseFirstOrderedListItem = do
        _ <- optional (string "    ")  -- Optional 4 spaces for sublist (not needed for first level)
        _ <- string "1."
        _ <- spaces1                     -- At least one space after the dot
        content <- some (isNot '\n')  -- Parse the rest of the line
        return [FreeText content]

    parseSubsequentOrderedListItem = do
        _ <- optional (string "    ")  -- Optional 4 spaces for sublist (indicates sublist level)
        num <- some digit         -- Parse the number for subsequent items
        guard (num > "0")         -- Ensure the number is positive
        _ <- is '.'                  -- Must be followed by a dot
        _ <- spaces1                     -- At least one space after the dot
        content <- some (isNot '\n')  -- Parse the rest of the line
        _ <- optional (is '\n')
        return [FreeText content]

--   items <- some listItemParser
--   return $ OrderedList items
-- listItemParser :: Parser listItem
-- listItemParser = do
--   _ <- optional (spaces)
--   number <- digit
--   _ <- is '.'
--   _ <- spaces
--   content <- many (noneof "\n")
--   _ <- is '\n'
--   return $ listItem content   




-- Parser for Table (| Header |)
parseTable :: Parser ADT
parseTable = do
    header <- parseTableRow
    _ <- optional (spaces)
    separator <- parseTableSeparator
    guard (all (>= 3) separator)  -- Ensure each column separator has at least 3 dashes
    rows <- some parseTableRow
    return $ Table [header] rows
  where
    parseTableRow = do
        _ <- optional (spaces)  -- Optional leading whitespace
        _ <- is '|'
        cells <- some parseTableCell
        _ <- is '|'
        return cells

    parseTableCell = do
        _ <- optional (spaces)
        content <- some (isNot '|')
        _ <- optional (spaces)
        _ <- is '|'
        return $ FreeText content

    parseTableSeparator = do
        _ <- optional (spaces)
        _ <- is '|'
        separators <- some parseSeparatorCell
        _ <- is '|'
        return separators

    parseSeparatorCell = do
        _ <- optional (spaces)
        dashes <- some (is '-')
        return (length dashes)


markdownParser :: Parser [ADT]
markdownParser = 
  many(parseItalic 
  <|> parseBold 
  <|> parseStrikethrough 
  <|> parseLink 
  <|> parseInlineCode 
  <|> parseFootnote 
  <|> parseFootnoteRef 
  <|> parseImage 
  <|> parseHeading 
  <|> parseBlockquote 
  <|> parseCodeBlock 
  <|> parseOrderedList 
  <|> parseTable
  <|> parseFreeText)

getTime :: IO String
getTime = formatTime defaultTimeLocale "%Y-%m-%dT%H:%M:%S" <$> getCurrentTime

-- Function generates a complete HTML document as a string.
convertADTHTML :: [ADT] -> String
convertADTHTML adts = 
  "<!DOCTYPE html>\n" ++
    "<html lang=\"en\">\n" ++
    "\n" ++
    "<head>\n" ++
    "    <meta charset=\"UTF-8\">\n" ++
    "    <title>Test</title>\n" ++
    "</head>\n" ++
    "\n" ++
    "<body>\n" ++
    indent 1 (convertADTs adts) ++ 
    "</body>\n" ++
    "\n" ++
    "</html>\n"

-- Function converts a list of ADT (representing parsed Markdown) into an HTML representation, ensuring all elements are converted.
convertADTs :: [ADT] -> String
convertADTs adts = concatMap convertADT adts

-- Function converts an ADT into an HTML representation, ensuring the correct tags are used.
convertADT :: ADT -> String
convertADT (FreeText text) = "<p>" ++ text ++ "</p>\n"
convertADT (Italic text) = "<em>" ++ text ++ "</em>"
convertADT (Bold text) = "<strong>" ++ text ++ "</strong>"
convertADT (Strikethrough text) = "<del>" ++ text ++ "</del>"
convertADT (Link text url) = "<a href=\"" ++ url ++ "\">" ++ text ++ "</a>"
convertADT (InlineCode code) = "<code>" ++ code ++ "</code>"
convertADT (Footnote n) = "<sup><a id=\"fn" ++ show n ++ "ref\" href=\"#fn" ++ show n ++ "\">" ++ show n ++ "</a></sup>"
convertADT (Image altText url captionText) = "<img src=\"" ++ url ++ "\" alt=\"" ++ altText ++ "\" title=\"" ++ captionText ++ "\">"
convertADT (FootnoteRef n content) = "<p id=\"#ref" ++ show n ++ "\">" ++ content ++ "</p>\n"
convertADT (Heading level content) = "<h" ++ show level ++ ">" ++ content ++ "</h" ++ show level ++ ">\n"
convertADT (Blockquote lines) = "<blockquote>\n" ++ concatMap (\line -> "    <p>" ++ line ++ "</p>\n") lines ++ "</blockquote>\n"
convertADT (CodeBlock Nothing content) = "<pre><code>" ++ content ++ "</code></pre>"                                          -- codeblock without languageIdentifier
convertADT (CodeBlock (Just lang) content) = "<pre><code class=\"language-" ++ lang ++ "\">" ++ content ++ "</code></pre>"    -- codeBlock with languageIdentifier
convertADT (OrderedList items) = "<ol>\n" ++ concatMap convertOrderedList items ++ "</ol>\n"    -- Converting an ordered list represented by the ADT OrderedList.
  where                                                                                         -- concatMap convertOrderedList items: Converts each list item into an HTML <li> tag.
    convertOrderedList :: [ADT] -> String
    convertOrderedList adts = "<li>" ++ concatMap convertADT adts ++ "</li>\n"
convertADT (Table header rows) = "<table>\n" ++ convertTableHeader (head header) ++ concatMap convertTableRow rows ++ "</table>\n"
  where
    convertTableHeader :: [ADT] -> String
    convertTableHeader headerRow = "<tr>\n" ++ concatMap (\cell -> "<th>" ++ convertADT cell ++ "</th>\n") headerRow ++ "</tr>\n"

    convertTableRow :: [ADT] -> String
    convertTableRow row = "<tr>\n" ++ concatMap (\cell -> "<td>" ++ convertADT cell ++ "</td>\n") row ++ "</tr>\n"

-- 'indent' function adds indentation (4 spaces per level) to the given content, improving readability of HTML.
indent :: Int -> String -> String
indent level = unlines . map (replicate (level * 4) ' ' ++) . lines
