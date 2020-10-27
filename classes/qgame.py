"""classes.qgame

This module contains the QGame class.
"""
from classes.qplayer import QPlayer
from classes.enums import Choice
from classes.game import Game


class QGame(Game):
    """
    This class represents a single game in a QMatch. It takes an ID, two
    players, and the match history and then determines the winner of the game.

    Attributes:
        game_id (int): The ID of the game
        player1 (Player): Player 1
        player1_throw (dict): The choice of player 1
        player2 (Player): Player 2
        player2_throw (dict): The choice of player 2
        winner (str): The name of the winning player
        game_result (str): Result of the game

    Overriden Methods:
        play_game(self, history): Play the game using the inputted parameters
    """
    def __init__(self, game_id, player1, player2, history):
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
        self.winner = self.play_game(history)

    def play_game(self, history):
        """
        This method plays out the game. Both players throw then we determine
        the winner. We then return the name of the winner.

        Arguments:
            :param self: This object
            :param history: (list(Game)) A list of games
        
        Returns:
            str: The name of the winner
        """
        self.player1_throw = self.player1.throw(history.copy())
        self.player2_throw = self.player2.throw(history.copy())

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