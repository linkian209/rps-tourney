"""classes.game

This module contains the Game class.
"""
from classes.player import Player
from classes.enums import Choice


class Game():
    """
    This class represents a single game in a match. It takes an ID and two
    players and then determines the winner of the game.

    Attributes:
        game_id (int): The ID of the game
        player1 (Player): Player 1
        player1_throw (dict): The choice of player 1
        player2 (Player): Player 2
        player2_throw (dict): The choice of player 2
        winner (str): The name of the winning player
        game_result (str): Result of the game

    Methods:
        play_game(self): Play the game using the inputted game_id and players
    """
    def __init__(self, game_id, player1, player2):
        """
        This method initializes the player with the game_id and players, then
        plays out the game.

        Arguments:
            :param self: This object
            :param game_id: The game id as an int
            :param player_1: The first player as a Player
            :param player_2: The second player as a Player
        """
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.winner = self.play_game()

    def play_game(self):
        """
        This method plays out the game. Both players throw then we determine
        the winner. We then return the name of the winner.

        Arguments:
            :param self: This object
        
        Returns:
            str: The name of the winner
        """
        self.player1_throw = self.player1.throw()
        self.player2_throw = self.player2.throw()

        # Resolve game
        # Tie - Easiest
        if(self.player1_throw['choice'] is self.player2_throw['choice']):
            self.game_result = 'Tie Game!'
            return None
        # Player 1 throws Rock
        elif(self.player1_throw['choice'] is Choice.ROCK):
            # Player 1 wins on a Scissors
            if(self.player2_throw['choice'] is Choice.SCISSORS):
                self.game_result = '{} wins!'.format(self.player1.name)
                return self.player1.name
            else:
                self.game_result = '{} wins!'.format(self.player2.name)
                return self.player2.name
        # Player 1 throws Scissors
        elif(self.player1_throw['choice'] is Choice.SCISSORS):
            # Player 1 wins on a Paper
            if(self.player2_throw['choice'] is Choice.PAPER):
                self.game_result = '{} wins!'.format(self.player1.name)
                return self.player1.name
            else:
                self.game_result = '{} wins!'.format(self.player2.name)
                return self.player2.name
        # Player 1 throws Paper
        else:
            # Player 1 wins on a Rock
            if(self.player2_throw['choice'] is Choice.ROCK):
                self.game_result = '{} wins!'.format(self.player1.name)
                return self.player1.name
            else:
                self.game_result = '{} wins!'.format(self.player2.name)
                return self.player2.name
        
    def __str__(self):
        """
        This method returns the string representation of the game.

        Arguments:
            :param self: This object

        Returns:
            str: The string representation of the game 
        """   
        return '''
        Game {}
        ---------------
        {} threw {}.
        {} threw {}.
        {}
        '''.format(
            self.game_id, self.player1.name, self.player1_throw['str'], 
            self.player2.name, self.player2_throw['str'], self.game_result)

    def __repr__(self):
        """
        This method returns a string representation of the game.

        Arguments:
            :param self: This object

        Returns:
            str: The string representation
        """
        return "<Game - {} v. {} | {} wins>".format(self.player1.name, self.player2.name, self.winner)