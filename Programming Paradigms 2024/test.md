```haskell
-- 这个 Haskell 代码用于实现 Markdown 到 HTML 的转换，不使用任何外部 Haskell 库（除了用于测试的库）。
-- 主要通过手工编写的字符串解析和递归来实现解析逻辑。

module Main where

import Data.Char (isSpace, isDigit)
import System.IO
import Data.Time.Clock
import Data.Time.Format
import Network.Wai
import Network.Wai.Handler.Warp (run)
import Network.HTTP.Types (status200)
import qualified Data.ByteString.Lazy.Char8 as BL

-- 定义 Markdown 数据类型，表示不同的 Markdown 元素结构。
data MarkdownElement = Heading Int String           -- 表示标题，包含级别和内容。
                    | Paragraph String              -- 表示段落，包含文本内容。
                    | Blockquote String             -- 表示块引用，包含引用内容。
                    | OrderedList [String]          -- 表示有序列表，包含多个列表项。
                    | CodeBlock String String       -- 表示代码块，包含语言类型和代码内容。
                    deriving (Show)

-- Part A: Markdown 解析
-- 手工编写的 Markdown 解析器，逐行解析 Markdown 文本。

-- 解析标题。通过 '#' 字符的数量确定标题级别。
headingParser :: String -> Maybe (MarkdownElement, String)
headingParser input =
    let (hashes, rest) = span (=='#') input
    in if not (null hashes) && not (null rest) && head rest == ' '
       then Just (Heading (length hashes) (drop 1 rest), "")
       else Nothing

-- 解析块引用，以 '>' 开头的行。
blockquoteParser :: String -> Maybe (MarkdownElement, String)
blockquoteParser ('>':' ':rest) =
    let (content, remainder) = break (=='
') rest
    in Just (Blockquote content, drop 1 remainder)
blockquoteParser _ = Nothing

-- 解析代码块。代码块以三重反引号开头和结束。
codeBlockParser :: String -> Maybe (MarkdownElement, String)
codeBlockParser input
    | take 3 input == "```" =
        let rest = drop 3 input
            (lang, codeWithEnd) = break (=='
') rest
            code = takeWhile (/= '`') (drop 1 codeWithEnd)
            remainder = dropWhile (/= '`') (drop 1 codeWithEnd)
        in Just (CodeBlock lang code, drop 3 remainder)
    | otherwise = Nothing

-- 解析有序列表，以数字加点开始的行。
orderedListParser :: String -> Maybe (MarkdownElement, String)
orderedListParser input =
    let (num, rest) = span isDigit input
    in if not (null num) && take 1 rest == "."
       then let item = dropWhile isSpace (drop 1 rest)
                (items, remainder) = parseListItems item
            in Just (OrderedList items, remainder)
       else Nothing

-- 解析列表项，直到遇到空行或结束。
parseListItems :: String -> ([String], String)
parseListItems input =
    let (item, rest) = break (=='
') input
    in if null rest
       then ([item], "")
       else let (moreItems, remainder) = parseListItems (drop 1 rest)
            in (item : moreItems, remainder)

-- 主 Markdown 解析器，尝试解析不同的 Markdown 元素。
markdownParser :: String -> [MarkdownElement]
markdownParser [] = []
markdownParser input =
    case headingParser input of
        Just (element, rest) -> element : markdownParser rest
        Nothing -> case blockquoteParser input of
            Just (element, rest) -> element : markdownParser rest
            Nothing -> case codeBlockParser input of
                Just (element, rest) -> element : markdownParser rest
                Nothing -> case orderedListParser input of
                    Just (element, rest) -> element : markdownParser rest
                    Nothing -> [Paragraph input]

-- Part B: HTML 转换
-- 将 MarkdownElement 转换为对应的 HTML 表示。
convertToHTML :: MarkdownElement -> String
convertToHTML (Heading level content) =
    "<h" ++ show level ++ ">" ++ content ++ "</h" ++ show level ++ ">"
convertToHTML (Blockquote content) =
    "<blockquote>" ++ content ++ "</blockquote>"
convertToHTML (CodeBlock lang code) =
    "<pre><code class=\"language-" ++ lang ++ "\">" ++ code ++ "</code></pre>"
convertToHTML (OrderedList items) =
    "<ol>" ++ concatMap (\item -> "<li>" ++ item ++ "</li>") items ++ "</ol>"
convertToHTML (Paragraph content) = "<p>" ++ content ++ "</p>"

-- 生成完整的 HTML 文档。
generateHTML :: [MarkdownElement] -> String
generateHTML elements =
    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<title>Markdown to HTML</title>\n</head>\n<body>\n" ++
    concatMap convertToHTML elements ++
    "\n</body>\n</html>"

-- Part C: Web 功能 - 保存 HTML
-- 运行简单的服务器来接收 HTML 内容并保存到文件。
main :: IO ()
main = do
    putStrLn "Starting server on port 8080..."
    run 8080 app

app :: Application
app req respond = do
    case (requestMethod req, pathInfo req) of
        ("POST", ["save-html"]) -> do
            body <- strictRequestBody req
            currentTime <- getCurrentTime
            let timestamp = formatTime defaultTimeLocale "%Y-%m-%dT%H-%M-%S" currentTime
                filename = "output-" ++ timestamp ++ ".html"
            BL.writeFile filename body
            putStrLn $ "HTML saved as: " ++ filename
            respond $ responseLBS status200 [("Content-Type", "text/plain")] "HTML saved."
        _ ->
            respond $ responseLBS status200 [("Content-Type", "text/plain")] "Unsupported request."

```

