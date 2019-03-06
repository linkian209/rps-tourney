"""classes.match

This module contains the Match class.
"""
from classes.game import Game
from classes.player import Player


class Match():
    """
    This object represents a match between 2 players. A certain number of game
    wins are needed to declare a winner of the match.

    Attributes:
        player1 (Player): The first player of the match
        player2 (Player): The second player of the match
        wins_needed (int): The number of wins needed to win the match
        games (list): A list of all of the games(Game) played in the match
        games_played (int): The number of games played in the match
        winner (str): Name of the winner of the match

    Methods:
        play_match(self): Plays out the match and determines the winner
    """
    def __init__(self, player1, player2, wins_needed):
        self.player1 = player1
        self.player2 = player2
        self.wins_needed = wins_needed

    def play_match(self):
        """
        This method plays through the match. It will run through games until
        one player has enough wins to be declared the winner. Then returns a
        dict containing the results in the form:
            {
                'games_played': int,
                'winner': str
            }

        Arguments:
            :param self: This object

        Returns:
            dict: The results of the match.
        """
        self.games = []
        self.games_played = 0
        self.player1.wins = 0
        self.player2.wins = 0
        loop = True
        while(loop):
            self.games_played += 1
            game = Game(self.games_played, self.player1, self.player2)
            print(game)
            if(game.winner == self.player1.name):
                self.player1.wins += 1
            elif(game.winner == self.player2.name):
                self.player2.wins += 1
            else:
                pass

            if(self.player1.wins >= self.wins_needed):
                loop = False

            if(self.player2.wins >= self.wins_needed):
                loop = False

        # Match has ended! Reset player variables and return a dictionary with results
        self.winner = self.player1.name if self.player1.wins >= self.wins_needed else self.player2.name
        self.player1.wins = 0
        self.player2.wins = 0
        return {'games_played': self.games_played, 'winner': self.winner}

    def __str__(self):
        """
        This method returns the string representation of the Match

        Arguments:
            :param self: This object

        Returns:
            str: The string representation of the match
        """
        retval = ""
        if self.games_played is not 0:
            retval = " | {} wins in {} games".format(self.winner, self.games_played)

        return "<Match - {} v. {}{}>".format(self.player1.name, self.player2.name, retval)