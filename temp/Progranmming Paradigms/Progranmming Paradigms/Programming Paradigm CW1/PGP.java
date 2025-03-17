//Name: Youyao Gao
//Student ID: 20516639
//Date: 4/5/2024
//Compile command: javac -encoding UTF-8 -sourcepath . PGP.java
//Execute command: java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1920m -Xmx1920m PGP <Input.txt > Output.txt
/*
Mentions before the code:
The execute command has already solve the problem of reading input from Input.txt and writing output to Output.txt,
so there is no need to add FileReader and FileWriter.
Instead, System.in and System.out can help to read the input and write the output.
*/

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class PGP {
    // Main method
    public static void main(String[] args) {
        // Initialization and get the input
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
            String line;
            int currentIteration = -1;
            int currentPhase = -1;
            ArrayList<Integer> iterations = new ArrayList<>();
            ArrayList<Integer> phases = new ArrayList<>();
            ArrayList<String> algorithms = new ArrayList<>();
            ArrayList<Integer> elapsedTimes = new ArrayList<>();
            ArrayList<Integer> evaluations = new ArrayList<>();
            ArrayList<Integer> improvements = new ArrayList<>();

            // Patterns to extract specific information from the input lines
            Pattern endsPattern = Pattern.compile("-+ (.+?) Ends");
            Pattern elapsedTimePattern = Pattern.compile("Elapsed Time \\(ms\\): (\\d+)");
            Pattern evaluationsPattern = Pattern.compile("Evaluations: (\\d+)");
            Pattern improvementsPattern = Pattern.compile("Improvements: (\\d+)");

            // Read line from the input
            while ((line = reader.readLine()) != null) {
                // Check Iteration
                if (line.contains("Iteration")) {
                    // Obtain the number after iteration
                    String[] parts = line.split(" ");
                    currentIteration = Integer.parseInt(parts[1]);
                }
                // Check Phase
                if (line.contains("Phase")) {
                    // Obtain the number after iteration
                    String[] parts = line.split(" ");
                    currentPhase = Integer.parseInt(parts[1].replaceAll(":", ""));
                }
                // Initialize currentPhase to 0
                if (line.contains("Phase") && line.contains("Ends")) {
                    currentPhase = 0;
                }
                // Extract and store relevant data when an algorithm ends
                Matcher endsMatcher = endsPattern.matcher(line);
                if (endsMatcher.find()) {
                    iterations.add(currentIteration);
                    phases.add(currentPhase);
                    algorithms.add(endsMatcher.group(1));

                    elapsedTimes.add(Integer.parseInt(findMatch(line, elapsedTimePattern)));
                    evaluations.add(Integer.parseInt(findMatch(line, evaluationsPattern)));
                    improvements.add(Integer.parseInt(findMatch(line, improvementsPattern)));
                }
            }

            //Merge the same iteration, phase, and algorithm
            mergeSame(iterations, phases, algorithms, elapsedTimes, evaluations, improvements);

            // Print out the results
            printResults(iterations, phases, algorithms, elapsedTimes, evaluations, improvements);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Method to find a match for a given pattern in a line
    private static String findMatch(String line, Pattern pattern) {
        Matcher matcher = pattern.matcher(line);
        return matcher.find() ? matcher.group(1) : "0";
    }

    // Method to merge same iteration, phase, and algorithm
    private static void mergeSame(ArrayList<Integer> iterations, ArrayList<Integer> phases, ArrayList<String> algorithms, ArrayList<Integer> elapsedTimes, ArrayList<Integer> evaluations, ArrayList<Integer> improvements) {
        for (int i = 0; i < iterations.size(); i++) {
            for (int j = i + 1; j < iterations.size(); j++) {
                if (iterations.get(i).equals(iterations.get(j)) && phases.get(i).equals(phases.get(j)) && algorithms.get(i).equals(algorithms.get(j))) {
                    elapsedTimes.set(i, elapsedTimes.get(j) + elapsedTimes.get(i));
                    evaluations.set(i, evaluations.get(j) + evaluations.get(i));
                    improvements.set(i, improvements.get(j) + improvements.get(i));
                    // Remove the duplicate entry
                    iterations.remove(j);
                    phases.remove(j);
                    algorithms.remove(j);
                    elapsedTimes.remove(j);
                    evaluations.remove(j);
                    improvements.remove(j);
                    j--;
                }
            }
        }
    }


    // Method to print the results
    private static void printResults(ArrayList<Integer> iterations, ArrayList<Integer> phases, ArrayList<String> algorithms, ArrayList<Integer> elapsedTimes, ArrayList<Integer> evaluations, ArrayList<Integer> improvements) {
        int totalElapsedTime = 0, totalEvaluations = 0, totalImprovements = 0;
        // Outprint the columns
        System.out.println("Iteration,Phase,Algorithm,Elapsed Time (ms),Evaluations,Improvements");

        for (int i = 0; i < iterations.size(); i++) {
            System.out.println(iterations.get(i) + "," + phases.get(i) + "," + algorithms.get(i) + "," + elapsedTimes.get(i) + "," + evaluations.get(i) + "," + improvements.get(i));
            totalElapsedTime += elapsedTimes.get(i);
            totalEvaluations += evaluations.get(i);
            totalImprovements += improvements.get(i);
        }

        System.out.println("-1,-1,All," + totalElapsedTime + "," + totalEvaluations + "," + totalImprovements);
    }
}





