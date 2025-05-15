from __future__ import annotations
from data_structures.array_set import ArraySet
from data_structures.referential_array import ArrayR
from data_structures.array_list import ArrayList
from enums import TeamGameResult
from game_simulator import GameSimulator, GameSimulationOutcome
from dataclasses import dataclass
from team import Team
from algorithms.mergesort import mergesort


@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html

    Do not make any changes to this class.
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game] | ArrayList[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        self.games = games
        self.week: int = week

    def __iter__(self):
        """
        Complexity:
            Best Case Complexity:O(1) sets index to 0, constant-time operation
            Worst Case Complexity:O(1) sets index to 0, constant-time operation
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Complexity:
            Best Case Complexity: O(1) one condition then return, constant-time operation
            Worst Case Complexity: O(1) one condition then return, constant-time operation
        """
        if self._index < len(self.games):   #competitions still not fully iterated
            game = self.games[self._index]  #current game
            self._index += 1
            return game
        raise StopIteration   #stop iter


class Season:

    def __init__(self, teams: ArrayR[Team] | ArrayList[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity:O(NlogN * comp(T)) where N is the length of the list and comp is the cost of comparison for the object type T (the elements in the list).
            Worst Case Complexity:O(NlogN * comp(T)) where N is the length of the list and comp is the cost of comparison for the object type T (the elements in the list).
        """

        self.teams = teams    #all the game team
        self.leaderboard = mergesort(self.teams,key=lambda team: (-team.points, team.name))   #initial leaderboard in descending order of points
        self.schedule = self._generate_schedule()   #generate game schedule


    def _generate_schedule(self) -> ArrayList[ArrayList[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayList[ArrayList[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        
        Do not make any changes to this function.
        """
        num_teams: int = len(self.teams)
        weekly_games: ArrayList[ArrayList[Game]] = ArrayList()
        flipped_weeks: ArrayList[ArrayList[Game]] = ArrayList()
        games: ArrayList[Game] = ArrayList()

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: ArrayList[Game] = ArrayList()
            flipped_week: ArrayList[Game] = ArrayList()
            used_teams: ArraySet = ArraySet(len(self.teams))

            week_game_no: int = 0
            for game in games:
                if game.home_team.name not in used_teams and game.away_team.name not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.name)
                    used_teams.add(game.away_team.name)

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(current_week)
            flipped_weeks.append(flipped_week)
            week += 1

        for flipped_week in flipped_weeks:
            weekly_games.append(flipped_week)
        
        return weekly_games

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume GameSimulator.simulate() is O(1)
            Remember to define your variables in your complexity.

            Best Case Complexity: O(n^2) through each week is O(n) then each have game, so through each game is O(n^2)
            Worst Case Complexity: O(n^2) through each week is O(n) then each have game, so through each game is O(n^2)
        """
        for week in self.schedule:   #through each week         O(n) weeks
            for game in week:     #through each game in each week     O(n^2)

                outcome = GameSimulator.simulate(game.home_team, game.away_team)   #simulate game   O(1)
                home = game.home_team
                away = game.away_team

                for scorer in outcome.goal_scorers:    #through all goal scorers      O(1)
                    for player in home.get_players():       #find goal scorer in home team  O(1)
                        if player.name == scorer:
                            player.goals += 1     
                            break
                    else:
                        for player in away.get_players():    ##find goal scorer in away team  O(1)
                            if player.name == scorer:
                                player.goals += 1
                                break

                if outcome.home_goals > outcome.away_goals:     #home win     O(1)
                    home_result = TeamGameResult.WIN
                    away_result = TeamGameResult.LOSS

                elif outcome.home_goals < outcome.away_goals:   #away win    O(1)
                    home_result = TeamGameResult.LOSS
                    away_result = TeamGameResult.WIN

                else:                                           #draw      O(1)
                    home_result = TeamGameResult.DRAW
                    away_result = TeamGameResult.DRAW

                home.add_result(home_result)
                away.add_result(away_result)

        self.leaderboard = mergesort(self.leaderboard,key=lambda team: (-team.points, team.name))   #update leaderboard after season    O(n log n)

    def delay_week_of_games(self, orig_week: int, new_week: int | None = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (int or None): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(1) when end week game delay 
            Worst Case Complexity: O(n) when inserting into the middle
        """
        index = orig_week - 1     #index python is start 0 so -1
        week = self.schedule.delete_at_index(index)   #remove game in original week
        if new_week is None:   #if none, end of season
            self.schedule.append(week)
        else:
            self.schedule.insert(new_week - 1, week)    #insert to new week

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1) just return the length, constant-time operation
            Worst Case Complexity: O(1) just return the length, constant-time operation
        """ 
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
