"""classes.qtourney

This module contains the QTourney class.
"""
from classes.tourney import Tourney
from classes.qmatch import QMatch


class QTourney(Tourney):
    """
    This class contains the Tourney object. It creates the double elimination
    bracket when it is created. It contains methods to then run the individual
    brackets as well as the grand championship.

    Attributes:
        players (list): A list of Player objects in the tourney
        matches (list): A list of Match objects containing all matches played
        wins_needed (int): The number of wins needed to determine a winner of a match
        stages (int): The number of stages in the tourney
        upper_bracket (Node): The upper bracket tree
        lower_bracket (Node): The lower bracket tree

    Inherited Methods:
        make_upper_tree(self, stage, root): Makes upper bracket
        make_lower_tree(self, stage, root): Makes lower bracket
        print_brackets(self): Prints both brackets
        print_upper_bracket(self): Prints upper bracket
        print_lower_bracket(self): Prints lower bracket
        run_upper_bracket(self): Runs the upper bracket
        run_lower_bracket(self): Runs the lower bracket
        run_championship(self): Runs the championship
        victory_screen(self, victor): Creates the victory screen for the winner

    Overridden Methods:
        make_match(player1, player2): Returns a Match Object with
                                      the inputted parameters
    """
    def make_match(self, player1, player2):
        """
        This method returns a QMatch object. This method is intended to be
        overriden by the Q Learning variant.

        Arguments:
            :param self: (Tourney) This Object
            :param player1: (Player) A Player
            :param player2: (Player) Another Player
        
        Returns:
            (QMatch) A QMatch object
        """
        return QMatch(player1, player2, self.wins_needed)