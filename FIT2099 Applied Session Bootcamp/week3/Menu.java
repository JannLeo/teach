import java.util.*;
import java.io.*;

public class Menu {
    public static Action showMenu(List<Action> actions, Camper camper) {
        if (actions == null || actions.isEmpty()) return null;
        char label = 'a';
        for (Action action : actions) {
            System.out.printf("%c: %s%n", label++, action.menuDescription(camper));
        }
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            String line = reader.readLine();
            if (line == null || line.trim().isEmpty()) return null;
            char ch = Character.toLowerCase(line.trim().charAt(0));
            int idx = ch - 'a';
            if (idx >= 0 && idx < actions.size()) return actions.get(idx);
            return actions.get(0);
        } catch (IOException e) {
            return actions.get(0);
        }
    }
}