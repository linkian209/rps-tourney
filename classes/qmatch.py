"""classes.qmatch

This module contains the QMatch class.
"""
from classes.qgame import QGame
from classes.qplayer import QPlayer
from classes.match import Match


class QMatch(Match):
    """
    This object represents a match between 2 QPlayers. A certain number of game
    wins are needed to declare a winner of the match. It overrides the play_match
    function to account for QPlayers learning.

    Inherited Attributes:
        player1 (Player): The first player of the match
        player2 (Player): The second player of the match
        wins_needed (int): The number of wins needed to win the match
        games (list): A list of all of the games(Game) played in the match
        games_played (int): The number of games played in the match
        winner (str): Name of the winner of the match

    Overridden Methods:
        play_match(self): Plays out the match and determines the winner
    """
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
            game = QGame(self.games_played, self.player1, self.player2, self.games)
            print(game)
            if(game.winner == self.player1.name):
                self.player1.wins += 1
            elif(game.winner == self.player2.name):
                self.player2.wins += 1
            else:
                # ???
                pass

            # Let QPlayers learn
            self.player1.learn(self.games.copy(), game)
            self.player2.learn(self.games.copy(), game)

            if(self.player1.wins >= self.wins_needed):
                loop = False

            if(self.player2.wins >= self.wins_needed):
                loop = False

            self.games.append(game)

        # Match has ended! Reset player variables and return a dictionary with results
        self.winner = self.player1.name if self.player1.wins >= self.wins_needed else self.player2.name
        self.player1.wins = 0
        self.player2.wins = 0
        return {'games_played': self.games_played, 'winner': self.winner}