package game;

import edu.monash.fit2099.engine.displays.Display;

public class Application {
    public static void main(String[] args) {
        Display terminalDisplay = new Display();
        Earth earth = new Earth(terminalDisplay);
        try{
            for (String line : FancyMessage.GAME_TITLE.split("\n")) {
                new Display().println(line);
                try {
                    Thread.sleep(200);
                } catch (Exception exception) {
                    exception.printStackTrace();
                }
            }

            earth.constructWorld();
            earth.run();
        }
        catch (Exception e) {
            // General exception, to help debugging.
            e.printStackTrace();
        }
    }
}
