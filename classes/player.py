"""classes.player

This module contains the player class.

"""
from random import randint


class Player():
    """
    The player class contains the things needed for the player to play.
    
    Attributes:
        name (str): The name of the player
        options (list): An enumeration of the options that it can throw when
                        playing
        wins (int): Number of games won
        losses (int): Number of games lost

    Methods:
        throw(self): Throws rock, paper, or scissors.
    """
    def __init__(self, name):
        """
        Initializes the player.

        Arguments:
            :param self: The object
            :param name: The name of the player
        """
        self.name = name
        self.options = {1: 'Rock', 2: 'Paper', 3: 'Scissors'}
        self.wins = 0
        self.losses = 0

    def __str__(self):
        """
        Returns the string representation of the player.

        Arguments:
            :param self: The object

        Returns:
            str: The string representation of the player
        """
        return self.name

    def throw(self):
        """
        This method is used to actually play rock, paper, scissors. It throws
        one of the available options in the form:
            {
                'choice': int,
                'str': str
            }

        Arguments:
            :param self: The object

        Returns:
            dict: A dictionary containing the int representation and the
                  string representation of the choice thrown.
        """
        choice = randint(1, len(self.options))
        return {'choice': choice, 'str': self.options[choice]}