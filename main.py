"""
Double Elimination Rock-Paper-Scissors Tourney
"""
from classes.tourney import Tourney

# Set up tourney
players = ['Skyline', 'Taco Bell', 'Chipotle', 'Moe\'s']
tourney = Tourney(players)

# Run tourney
tourney.run_upper_bracket()
print('')
tourney.run_lower_bracket()

# Now it is time for the championship.
tourney.run_championship()