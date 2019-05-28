# Run the game in old-school monochrome vector graphics mode.

import space_rocks

this_game = space_rocks.Game(False,     # Debug mode?
                             True,      # Monochrome mode?
                             25)        # Target FPS
this_game.animate()
