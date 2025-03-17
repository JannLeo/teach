import Data.List (intercalate)

type State = [Char]
type Path = [State]
type Solution = [Path]

solutionPath :: Path -> IO ()
solutionPath path
  | not (isValidInput0 (head path)) || not (isValidInput0 (last path)) = putStrLn "Invalid input, please change your states."
  | isValidInput1 (head path) || isValidInput1 (last path) = putStrLn "On the west bank, the wolf will eat the goat, please change your states."
  | isValidInput2 (head path) || isValidInput2 (last path) = putStrLn "On the west bank, the goat will eat the cabbage, please change your states."
  | isValidInput3 (head path) || isValidInput3 (last path) = putStrLn "On the east bank, the wolf will eat the goat, please change your states."
  | isValidInput4 (head path) || isValidInput4 (last path) = putStrLn "On the east bank, the goat will eat the cabbage, please change your states."
  | isValidInput5 (head path) || isValidInput5 (last path) = putStrLn "On the west bank, the wolf will eat the goat and the goat will eat the cabbage, please change your states."
  | isValidInput6 (head path) || isValidInput6 (last path) = putStrLn "On the east bank, the wolf will eat the goat and the goat will eat the cabbage, please change your states."
  | otherwise = do
      let finalState = last path
          initialPaths = [init path]
          allPaths = exploreAllPaths finalState initialPaths
          shortestPaths = findShortestPaths allPaths
          formattedShortestPaths = intercalate ", " $ map formatPath shortestPaths
          stepsCount = calculateSteps (head shortestPaths)
          pathsOutput = "Shortest paths are: " ++ formattedShortestPaths
          tripsOutput = "Least number of trips is: " ++ show stepsCount
      putStrLn "All possible paths are:"
      mapM_ (putStrLn . formatPath) allPaths
      putStrLn pathsOutput
      putStrLn tripsOutput

exploreAllPaths :: State -> Solution -> Solution
exploreAllPaths _ [] = []
exploreAllPaths targetState paths = concatMap (explorePath targetState) paths
  where
    explorePath target path
      | last path == target = [path]
      | otherwise =
          let possibleMoves = move (last path)
              validMoves = filter (`notElem` path) possibleMoves
              newPaths = map (\nextMove -> path ++ [nextMove]) validMoves
          in concatMap (explorePath target) newPaths

findShortestPaths :: Solution -> Solution
findShortestPaths paths =
    let minLength = minimum $ map length paths
    in filter ((== minLength) . length) paths

formatPath :: Path -> String
formatPath = concatMap (\state ->   formatState state  )

formatState :: State -> String
formatState state = "[" ++ intercalate ", " (map (\c -> "'" ++ [c] ++ "'") state) ++ "]"

calculateSteps :: Path -> Int
calculateSteps path = length path - 1

isValidInput0 :: [Char] -> Bool
isValidInput0 xs = xs `elem` validInputs
  where
    validInputs = [['w','w','w','w'],['w','w','w','e'],['w','w','e','w'],['w','e','w','w'],['e','w','w','w'],['w','w','e','e'],['w','e','w','e'],['e','w','w','e'],['w','e','e','w'],['e','w','e','w'],['e','e','w','w'],['w','e','e','e'],['e','w','e','e'],['e','e','w','e'],['e','e','e','w'],['e','e','e','e']]

isValidInput1 :: [Char] -> Bool
isValidInput1 xs = xs `elem` validInputs
  where
    validInputs = [['e','w','w','e']]

isValidInput2 :: [Char] -> Bool
isValidInput2 xs = xs `elem` validInputs
  where
    validInputs = [['e','e','w','w']]

isValidInput3 :: [Char] -> Bool
isValidInput3 xs = xs `elem` validInputs
  where
    validInputs = [['w','e','e','w']]

isValidInput4 :: [Char] -> Bool
isValidInput4 xs = xs `elem` validInputs
  where
    validInputs = [['w','w','e','e']]

isValidInput5 :: [Char] -> Bool
isValidInput5 xs = xs `elem` validInputs
  where
    validInputs = [['e','w','w','w']]

isValidInput6 :: [Char] -> Bool
isValidInput6 xs = xs `elem` validInputs
  where
    validInputs = [['w','e','e','e']]

showPath :: Path -> String
showPath = concatMap (\state -> "[" ++ state ++ "] ")

move:: State -> Path
move [f, w, g, c] = filter isPossible[crossFarmer[f, w, g, c], crossWolf[f, w, g, c],crossGoat[f, w, g, c], crossCabbage[f, w, g, c]]

isPossible :: State -> Bool
isPossible [f, w, g, c] =
    not (f /= w && f /= g && w == g) && not (f /= g && f /= c && g == c)  

crossFarmer:: State -> State
crossFarmer [f, w, g, c] = [cross f, w, g, c]

crossWolf:: State -> State
crossWolf [f, w, g, c] 
   | f == w = [cross f, cross w, g, c]  
   | otherwise = [f, w, g, c]  

crossGoat:: State -> State
crossGoat [f, w, g, c] 
    | f == g = [cross f, w, cross g, c]  
    | otherwise = [f, w, g, c]  

crossCabbage:: State -> State
crossCabbage [f, w, g, c] 
    | f == c = [cross f, w, g, cross c]  
    | otherwise = [f, w, g, c]  

cross :: Char -> Char
cross xs
  | xs == 'e' = 'w'
  | xs == 'w' = 'e'