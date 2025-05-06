from __future__ import annotations
from data_structures.referential_array import ArrayR
from enums import TeamGameResult, PlayerPosition
from player import Player
from typing import Collection, TypeVar
from data_structures.array_list import ArrayList

T = TypeVar("T")


class Team:
    POSITIONS = tuple(PlayerPosition)   # enumerate positions of all player in a fixed order

    def __init__(self, team_name: str, initial_players: ArrayR[Player], history_length: int) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            initial_players (ArrayR[Player]): The players the team starts with initially
            history_length (int): The number of `GameResult`s to store in the history

        Returns:
            None

        Complexity:
            Best Case Complexity: O(n) each initial player need add to list
            Worst Case Complexity: O(n) each initial player need add to list, total position are four, max is O(4n), min O(n)
        """
        self.name = team_name  
        self.points = 0   #total score starts at 0

        self.players = ArrayList()   #main list store all players

        self.players_position = ArrayR(len(self.POSITIONS))  #list of players to each position
        for index in range(len(self.POSITIONS)):
            self.players_position[index] = ArrayList[Player]()

        self.history_length = history_length
        self.history = ArrayList()   # recent competition results

        self.posts = ArrayList()   # record daily post

        for index in range(len(initial_players)):   #ddd initial players to team by position
            player = initial_players[index]
            self.players.append(player)

            position_index = self.POSITIONS.index(player.position) #find the players' position index
            self.players_position[position_index].append(player) #ad player in list by their position


    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(n) need to find the position of player
            Worst Case Complexity: O(n) need to find the position of player
        """
        self.players.append(player)   #add player to main list
        position_index = self.POSITIONS.index(player.position)  # find position
        self.players_position[position_index].append(player)  #add to position list

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) position of player is the first one
            Worst Case Complexity: O(n) the player is at the end of the position
        """
        self.players.remove(player)  #remove from main list
        position_index = self.POSITIONS.index(player.position) #find posi
        self.players_position[position_index].remove(player)  #remove


    def get_players(self, position: PlayerPosition | None = None) -> Collection[Player]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (PlayerPosition or None): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder.
            
            This includes the ArrayR, which was previously prohibited.

        Complexity:
            Best Case Complexity: O(1) the position is given and is the first position
            Worst Case Complexity: O(n^2) position is none so every time of for loop need do self.POSITIONS.index(position)
        """
        if position is not None:    #if position id given then return sublist
            position_index = self.POSITIONS.index(position)
            return self.players_position[position_index]

        result = ArrayList()    #if there is no position return whole result of player of all position
        for position in self.POSITIONS:

            position_index = self.POSITIONS.index(position)
            item = self.players_position[position_index]

            for index in range(len(item)):   #add player one by one at each position
                result.append(item[index])

        return result


    def add_result(self, result: TeamGameResult) -> None:
        """
        Add the `result` to this `Team`'s history

        Args:
            result (GameResult): The result to add
            
        Complexity:
            Best Case Complexity:  O(1) just append if not out of history length
            Worst Case Complexity:  O(n) if need delete_at_index so delete the old result means each other result will go left
        """
        self.points += result.value   #update point by result

        self.history.append(result)   

        if len(self.history) > self.history_length:     #if max remove oldest one
            self.history.delete_at_index(0)



    def get_history(self) -> Collection[TeamGameResult] | None:
        """
        Returns the `GameResult` history of the team.
        If the team has played less than this team's `history_length`,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the result should be a container with 4 objects in this order:
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        If this method is called before the team has played any games,
        return None the reason for this is explained in the specification.

        Returns:
            Collection[GameResult]: The most recent `GameResult`s for this team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(1) just length check and return
            Worst Case Complexity: O(1) just length check and return
        """
        if len(self.history) == 0:
            return None
        return self.history


    
    def make_post(self, post_date: str, post_content: str) -> None:
        """
        Publish a team blog `post` for a particular `post_date`.
       
        A `Team` can have one published post per day. Any duplicate
        posts should overwrite the original post for that day.
        
        Args:
            `post_date` (`str`) - The date of the post
            `post_content` (`str`) - The content of the post
        
        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) post is the first or already at the first index
            Worst Case Complexity: O(n) search through all posts to check for date
        """
        for index in range(len(self.posts)):
            date, _ = self.posts[index]
            if date == post_date:
                self.posts[index] = (post_date, post_content)  # cover old content
                return
        self.posts.append((post_date, post_content))   # add new post


    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity: 
            Best Case Complexity: O(1) ArrayList length
            Worst Case Complexity: O(1) ArrayList length
        """
        return len(self.players)


    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity analysis not required.
        """
        return "Team({}, Points: {}, Players: {}, History: {}, Posts: {})".format(
            self.name,
            self.points,
            len(self.players),
            len(self.history),
            len(self.posts)
        )

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure.
        """
        return str(self)
