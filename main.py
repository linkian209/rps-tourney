"""
Double Elimination Rock-Paper-Scissors Tourney
"""
import sys
import numpy as np
from classes.tourney import Tourney
from classes.qtourney import QTourney
from classes.player import Player
from classes.qplayer import QPlayer

# Figure out what type of tourney this is
if(sys.argv[1] != '-q'):
    # Set up tourney
    try:
        players = [Player(x) for x in sys.argv[1:]]
        tourney = Tourney(players)
    except Exception as e:
        print('Invalid Number of players. Must be a power of two!')
        sys.exit(1)
else:
    # Set up QTourney
    try:
        players = [QPlayer(x, .8, .2, .1) for x in sys.argv[2:]]
        tourney = QTourney(players)
    except Exception as e:
        print(e.message())
        sys.exit(1)
# Run tourney
tourney.run_upper_bracket()
print('')
tourney.run_lower_bracket()

# Now it is time for the championship.
winner = tourney.run_championship()

if(type(winner) is QPlayer):
    np.save('winner_q_table', winner.q_table)