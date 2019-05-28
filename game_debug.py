# Run the game in debug mode.

import space_rocks

this_game = space_rocks.Game(True,      # Debug mode?
                             False,     # Monochrome mode?
                             25)        # Target FPS
this_game.animate()
