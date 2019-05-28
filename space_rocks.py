# Do a visualisation of DeepRacer logs.

import cartesian_coordinates as cc
import pygame                           # 2d games engine.
import random
import datetime                         # Needed for tracing.

# If debugging is turned on, send the parm message to stdout.
def trace(vis, message):
    if vis.debug:
        print(datetime.datetime.now(), message)


class Rock:

    def __init__(self, vis, size):

        self.size = size
        self.vertices = []

        # Rock is based on a polygon (straight edged circle).
        if self.size == 'Large':
            self.radius = random.randint(30, 50)
        elif self.size == "Medium":
            self.radius = random.randint(15, 25)
        else:
            self.radius = random.randint(10, 15)

        self.rotation = 0                                   # Current rotation of the rock in degrees.

        max_rotation_velocity = round(100 / vis.target_fps)
        self.rotation_speed = random.randint(- max_rotation_velocity, max_rotation_velocity) # Degrees per tick
        if self.rotation_speed == 0:                         # No rotation would look boring.
            self.rotation_speed = 1

        vertex_count = 12                                    # Number of vertices that will make up this rock.
        slice_size = 360 / vertex_count                     # Good for this to be an integer.

        for v_num in range(vertex_count):
            if self.size == "Large":
                vertex = [0, self.radius + random.randint(-15, 15)]
            elif self.size == "Medium":
                vertex = [0, self.radius + random.randint(-7, 7)]
            else:
                vertex = [0, self.radius + random.randint(-5, 5)]

            vertex = cc.rotate_around_origin(vertex, slice_size * v_num)
            self.vertices.append(vertex)

        self.kill = False                # Should this rock be killed off?
        self.collision = False

        self.exploding = False
        self.explosion_step = 0

        if vis.monochrome:
            self.colour = vis.WHITE
        else:
            self.colour = (random.randint(60, 200), random.randint(60, 200), random.randint(60, 200))

        trace(vis, self.size + ' rock created.')

    def place_on_side_of_screen(self, vis):

        start_side = random.randint(1, 4)                   # 1=Top, 2=Bottom, 3=Left, 4=Right
        if start_side == 1:                                 # From the top of screen.
            self.coords = [random.randint(vis.border, vis.screen_size[0] - vis.border), vis.top_dead]

            if self.coords[0] <= vis.screen_size[0] / 2:    # Left hand side of top of screen.
                self.drift = [10 * random.randint(1, 3) / vis.target_fps,
                              10 * random.randint(2, 4) / vis.target_fps]   # So drift rightwards and downwards.
            else:
                self.drift = [10 * random.randint(-3, -1) / vis.target_fps,
                              10 * random.randint(2, 4) / vis.target_fps]     # Otherwise drift leftwards and downwards.

        if start_side == 2:                                 # Bottom
            self.coords = [random.randint(vis.border, vis.screen_size[0] - vis.border), vis.bottom_dead]

            if self.coords[0] <= vis.screen_size[0] / 2:    # Left hand side of top of screen.
                self.drift = [10 * random.randint(1, 3) / vis.target_fps,
                              10 * random.randint(-4, -2) / vis.target_fps]   # So drift rightwards and upwards.
            else:
                self.drift = [random.randint(-3, -1), random.randint(-4, -2)]     # Otherwise drift leftwards and upwards.

        if start_side == 3:
            self.coords = [-100, random.randint(200, 400)]
            self.drift = [10 * random.randint(2, 4) / vis.target_fps,
                          10 * random.randint(-3, 3) / vis.target_fps]

        if start_side == 4:
            self.coords = [900, random.randint(200, 400)]
            self.drift = [10 * random.randint(-4, -2) / vis.target_fps,
                          10 * random.randint(-3, 3) / vis.target_fps]

    # Has the rock strayed outside of the game screen? If so, it will be marked to be killed off.
    def check_onscreen(self, vis):
        if (self.coords[0] < vis.left_dead
                or self.coords[0] > vis.right_dead
                or self.coords[1] < vis.top_dead
                or self.coords[1] > vis.bottom_dead):
            self.kill = True

    # Method is to check whether the vertex is inside any of the triangles that make up the rock.
    def check_collision(self, vertex):
        self.collision = False                      # Start bu assuming that vertex is outside all triangles.

        # Before doing the triangle analysis, do a simple clipping test.
        # Imagine a square around the centre of the rock. Is the vertex inside that square?
        if (vertex[0] > self.coords[0] - self.radius - 15           # 15 is the most that can randomly be added to a vertex
        and vertex[0] < self.coords[0] + self.radius + 15           # at the time that the rock was created.
        and vertex[1] > self.coords[1] - self.radius - 15
        and vertex[1] < self.coords[1] + self.radius + 15):

            # If the vertex is inside the square, then it is worth checking each triangle that makes up the
            # rock in turn, to see if it is inside any of them.
            prev_vertex = self.vertices[-1]  # This is so we have 3 points for first triangle.

            for triangle_vertex in self.vertices:
                if cc.is_inside_triangle(vertex, self.position(prev_vertex), self.position(triangle_vertex), self.coords):
                    self.collision = True
                prev_vertex = triangle_vertex

    def position(self, vertex):
        rotated = cc.rotate_around_origin(vertex, self.rotation)
        return cc.translation(rotated, self.coords)

    def explode(self, vis):
        if self.explosion_step < vis.target_fps:    # Higher FPS mean, more animation steps for explosion!
            self.explosion_step += 1
        else:
            self.kill = True                        # Explosion animation is over, so kill off the rock.

        if self.explosion_step == int(0.5 * vis.target_fps):  # Half way through the explosion animation, maybe spawn new rocks.
            if self.size in ['Large', 'Medium']:
                for i in range(2):
                    if self.size == 'Large':
                        new_rock = Rock(vis, 'Medium')
                    else:
                        new_rock = Rock(vis, 'Small')

                    # Give it position that is near it's parent.
                    new_rock.coords = cc.translation(self.coords, [random.randint(-25, 25), random.randint(-25, 25)])

                    new_drift_x = self.drift[0] + 10 * random.randint(-1, 1) / vis.target_fps     # New rocks's drift will be similar to
                    new_drist_y = self.drift[1] + 10 * random.randint(-1, 1) / vis.target_fps    # parent.

                    new_rock.drift = [new_drift_x, new_drist_y]

                    vis.rocks.append(new_rock)                              # Add the new rocks to the game.


    def draw(self, vis):
        prev_vertex = self.vertices[-1]                     # This will make it a complete polygon.

        for vertex in self.vertices:
            if not self.exploding:
                if vis.monochrome:
                    pygame.draw.line(vis.screen, vis.WHITE, self.position(prev_vertex), self.position(vertex), 1)

                # TODO refactor to draw whole polygon in one go, rather than drawing a number of triangles.
                else:
                    triangle = []
                    triangle.append(self.position(prev_vertex))
                    triangle.append(self.position(vertex))
                    triangle.append(self.coords)
                    pygame.draw.polygon(vis.screen, self.colour, triangle, 0)

            else:
                # Higher FPS mean more explosion steps, so lower speed of explosion per step.
                scaled_vertex = cc.scale(vertex, 5 * self.explosion_step / vis.target_fps)
                [x, y] = self.position(scaled_vertex)
                if vis.monochrome:
                    pygame.draw.circle(vis.screen, vis.WHITE, [int(x), int(y)], 1, 1)
                else:
                    pygame.draw.circle(vis.screen, self.colour, [int(x), int(y)], 4, 4)

            prev_vertex = vertex

    def move(self):
        self.rotation += self.rotation_speed
        self.coords = cc.translation(self.coords, self.drift)


class Bullet:
    def __init__(self, vis, origin, angle):

        self.coords = origin
        self.angle = angle
        self.drift = cc.rotate_around_origin([0, 20], self.angle)        # Incremental drift this bullet will do each tick.

        self.kill = False

    def draw(self, vis):
        if vis.monochrome:
            pygame.draw.circle(vis.screen, vis.WHITE, cc.integer_coord(self.coords), 1, 1)
        else:
            pygame.draw.circle(vis.screen, vis.RED, cc.integer_coord(self.coords), 2, 2)

    def move(self):
        self.coords = cc.translation(self.coords, self.drift)

    def check_onscreen(self, vis):
        if (self.coords[0] < vis.left_dead
                or self.coords[0] > vis.right_dead
                or self.coords[1] < vis.top_dead
                or self.coords[1] > vis.bottom_dead):
            self.kill = True



class Visualise:

    def __init__(self, debug, monochrome, target_fps):

        self.debug = debug
        self.monochrome = monochrome
        self.target_fps = target_fps

        # XXX
        self.ship_angle = 0


        # Initialize the game engine.
        pygame.init()

        # Define the colors we will use in RGB format.
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = [255, 0, 0]

        # Set the height and width of the viewport.
        self.screen_size = [800, 600]
        self.screen_centre = [int(self.screen_size[0] / 2), int(self.screen_size[1] / 2)]


        self.border = 100

        # These are the edges of the zone where graphical objects are born and die.
        self.left_dead = - self.border
        self.top_dead = -self.border
        self.right_dead = self.screen_size[0] + self.border
        self.bottom_dead = self.screen_size[1] + self.border

        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.myfont = pygame.font.SysFont('Courier New', 20)

        pygame.display.set_caption('Space Rocks')

        num_rocks = 20
        self.rocks = []
        for r in range(num_rocks):
            new_rock = Rock(self, 'Large')
            new_rock.place_on_side_of_screen(self)
            self.rocks.append(new_rock)

        self.bullets = []


    def draw_text(self, text, x, y, colour):
        textsurface = self.myfont.render(text, False, colour)
        self.screen.blit(textsurface, (x, y))

    # This one method coordinates the drawing of all of the graphical elements in the game.
    def draw_all_elements(self):
        # Clear the screen and set the screen background.
        self.screen.fill(self.BLACK)

        for r in self.rocks:                    # Draw each rock.
            r.draw(self)

        for b in self.bullets:                  # Draw each bullet.
            b.draw(self)

        if self.debug:
#            pygame.draw.circle(self.screen, self.RED, self.screen_centre, 2, 2)

            self.draw_text('FPS = ' + str(round(self.clock.get_fps())), 10, 10, self.WHITE)

        pygame.display.flip()

    def animate(self):
        # Loop until the user clicks the close button.
        done = False

        while not done:

            self.clock.tick(self.target_fps)



            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop


            # TODO - put in own class 'key_handling'
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.ship_angle += 10
            if keys[pygame.K_RIGHT]:
                self.ship_angle -= 10
            if keys[pygame.K_z] and len(self.bullets) < 10:
                self.bullets.append(Bullet(self, self.screen_centre, self.ship_angle))

            for b in self.bullets:
                b.move()
                b.check_onscreen(self)
                if b.kill:
                    self.bullets.remove(b)
                    trace(self, 'Bullet removed, bullets left=' + str(len(self.bullets)))



            for r in self.rocks:
                r.move()
                r.check_onscreen(self)

                # Check whether this rock has been hit by a bullet.
                if not r.exploding:
                    for b in self.bullets:
                        r.check_collision(b.coords)
                        if r.collision:
                            r.exploding = True
                            b.kill = True                   # This bullet has killed a rock, so it must be killed itself too.

                # TODO need to reintroduce check whether rock has hit the spaceship.
#                r.check_collision(self.screen_centre)
#                 if r.collision:
#                     r.exploding = True

                # This rock is exploding, so do the steps of the explosion animation - including possibly, creating
                # child rocks.
                if r.exploding:
                    r.explode(self)

                if r.kill:
                    if not r.exploding:  # Must be getting killed due to being at edge of screen.
                        new_rock = Rock(self, r.size)       # Make new rock. Same size as one that is about to be removed.
                        new_rock.place_on_side_of_screen(self)
                        self.rocks.append(new_rock)

                    self.rocks.remove(r)                    # Rock is to be killed, so remove it from the list of rocks.

                    trace(self, r.size + ' rock removed, rocks left=' + str(len(self.rocks)))

            self.draw_all_elements()

            if done:
                break

        # Be IDLE friendly
        pygame.quit()
