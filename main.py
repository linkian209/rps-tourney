"""
Double Elimination Rock-Paper-Scissors Tourney
"""
import sys
from classes.tourney import Tourney


# Set up tourney
try:
    players = sys.argv[1:]
    tourney = Tourney(players)
except:
    print('Invalid Number of players. Must be a power of two!')
    sys.exit(1)
    
# Run tourney
tourney.run_upper_bracket()
print('')
tourney.run_lower_bracket()

# Now it is time for the championship.
tourney.run_championship()