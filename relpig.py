"""
Platformer Game
"""
import arcade


# constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"


# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)


# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 45

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 64
PLAYER_START_Y = 218

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None
        self.player_list = None
        self.enemy_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None
        self.physics__enemy_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0
        self.vida= 3

        self.cientifico=25

        # donde esta el borde derecho del mapa?
        self.end_of_map = 0

        # Level
        self.level = 3

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        self.game_over = arcade.load_sound("sounds/gameover2.wav")

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        self.winner = arcade.load_texture("images/winner.png")
        self.gameover = arcade.load_texture("images/game_over.png")

        self.background = arcade.load_texture("images/fondo1.png")


        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0
        self.vida= 3

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        #Creamos el jugador
        self.player_sprite = arcade.AnimatedWalkingSprite()

        self.player_sprite.stand_right_textures = []
        self.player_sprite.stand_right_textures.append(arcade.load_texture("images/player_1/protagonista1.png",
                                                                    scale=CHARACTER_SCALING))
        self.player_sprite.stand_left_textures = []
        self.player_sprite.stand_left_textures.append(arcade.load_texture("images/player_1/protagonista1.png",
                                                                   scale=CHARACTER_SCALING, mirrored=True))

        self.player_sprite.walk_right_textures = []

        self.player_sprite.walk_right_textures.append(arcade.load_texture("images/player_1/protagonista3.png",
                                                                   scale=CHARACTER_SCALING))
        self.player_sprite.walk_right_textures.append(arcade.load_texture("images/player_1/protagonista4.png",
                                                                   scale=CHARACTER_SCALING))
        #self.player_sprite.walk_right_textures.append(arcade.load_texture("images/player_1/protagonista3.png",
        #                                                           scale=CHARACTER_SCALING))
        #self.player_sprite.walk_right_textures.append(arcade.load_texture("images/player_1/protagonista4.png",
        #                                                           scale=CHARACTER_SCALING))

        self.player_sprite.walk_left_textures = []

        #self.player_sprite.walk_left_textures.append(arcade.load_texture("images/player_1/protagonista1.png",
        #                                                          scale=CHARACTER_SCALING, mirrored=True))
        #self.player_sprite.walk_left_textures.append(arcade.load_texture("images/player_1/protagonista2.png",
        #                                                          scale=CHARACTER_SCALING, mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("images/player_1/protagonista3.png",
                                                                  scale=CHARACTER_SCALING, mirrored=True))
        self.player_sprite.walk_left_textures.append(arcade.load_texture("images/player_1/protagonista4.png",
                                                                  scale=CHARACTER_SCALING, mirrored=True))

        self.player_sprite.walk_up_textures = []

        self.player_sprite.walk_up_textures.append(arcade.load_texture("images/player_1/protagonista5.png",
                                                                         scale=CHARACTER_SCALING, mirrored=True))

        self.player_sprite.texture_change_distance = 20


        # Set up the player, specifically placing it at these coordinates.
        #self.player_sprite = arcade.Sprite("images/player_1/protagonista1.png", CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y

        self.player_list.append(self.player_sprite)

        # ---- Draw an enemy on the groud ---- #

        # Creamos el jugador
        self.enemy_sprite = arcade.AnimatedWalkingSprite()

        self.enemy_sprite.stand_right_textures = []
        self.enemy_sprite.stand_right_textures.append(arcade.load_texture("images/enemies/pasti1.png",
                                                                          scale=CHARACTER_SCALING,mirrored=True))
        self.enemy_sprite.stand_left_textures = []
        self.enemy_sprite.stand_left_textures.append(arcade.load_texture("images/enemies/pasti1.png",
                                                                         scale=CHARACTER_SCALING))

        self.enemy_sprite.walk_right_textures = []

        self.enemy_sprite.walk_right_textures.append(arcade.load_texture("images/enemies/pasti1.png",
                                                                          scale=CHARACTER_SCALING,mirrored=True))
        self.enemy_sprite.walk_right_textures.append(arcade.load_texture("images/enemies/pasti2.png",
                                                                          scale=CHARACTER_SCALING,mirrored=True))


        self.enemy_sprite.walk_left_textures = []


        self.enemy_sprite.walk_left_textures.append(arcade.load_texture("images/enemies/pasti1.png",
                                                                         scale=CHARACTER_SCALING))
        self.enemy_sprite.walk_left_textures.append(arcade.load_texture("images/enemies/pasti2.png",
                                                                         scale=CHARACTER_SCALING))

        self.enemy_sprite.texture_change_distance = 20

       # Posicion inicial del enemigo
        self.enemy_sprite.center_x = PLAYER_START_X + 240
        self.enemy_sprite.center_y = PLAYER_START_Y + 100

        # Limite del enemigo
        self.enemy_sprite.change_x = 2
        self.enemy_sprite.boundary_left = PLAYER_START_X + 70
        self.enemy_sprite.boundary_right = PLAYER_START_X + 400


        self.enemy_list.append(self.enemy_sprite)


        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'plataforma'
        # Name of the layer that has items for pick-up
        coins_layer_name = 'monedas'
        # Name of the layer that has items for foreground
        foreground_layer_name = 'frente'
        # Name of the layer that has items for background
        background_layer_name = 'fondo'
        # Name of the layer that has items we shouldn't touch
        dont_touch_layer_name = "notocar"

        # Map name

        if level==-1:
            map_name = 'game over.tmx'
        map_name = f"nivel_1.tmx"
        # Read in the tiled map
        my_map = arcade.read_tiled_map(map_name, TILE_SCALING)

        # -- Walls
        # Grab the layer of items we can't move through
        map_array = my_map.layers_int_data[platforms_layer_name]

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = len(map_array[0]) * GRID_PIXEL_SIZE

        # -- Background
        self.background_list = arcade.generate_sprites(my_map, background_layer_name, TILE_SCALING)

        # -- Foreground
        self.foreground_list = arcade.generate_sprites(my_map, foreground_layer_name, TILE_SCALING)

        # -- Platforms
        self.wall_list = arcade.generate_sprites(my_map, platforms_layer_name, TILE_SCALING)

        # -- Platforms
        self.wall_list = arcade.generate_sprites(my_map, platforms_layer_name, TILE_SCALING)

        # -- Coins
        self.coin_list = arcade.generate_sprites(my_map, coins_layer_name, TILE_SCALING)

        # -- Don't Touch Layer
        self.dont_touch_list = arcade.generate_sprites(my_map, dont_touch_layer_name, TILE_SCALING)

        self.end_of_map = (len(map_array[0]) - 1) * GRID_PIXEL_SIZE

        # --- Other stuff
        # Set the background color
        if my_map.backgroundcolor:
            arcade.set_background_color(my_map.backgroundcolor)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)
        self.physics__enemy_engine = arcade.PhysicsEnginePlatformer(self.enemy_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        if self.level==7:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                     SCREEN_WIDTH, SCREEN_HEIGHT, self.winner)

        elif self.vida==-1:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                     SCREEN_WIDTH, SCREEN_HEIGHT, self.gameover)

        else:
         # Draw our sprites
         self.wall_list.draw()
         self.background_list.draw()
         self.wall_list.draw()
         self.coin_list.draw()
         self.dont_touch_list.draw()
         self.player_list.draw()
         self.foreground_list.draw()
         self.enemy_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 20 + self.view_left, self.view_bottom + SCREEN_HEIGHT -40 ,
                         arcade.csscolor.WHITE, 18)

        # Draw our score on the screen, scrolling it with the viewport
        vida_text = f"Vidas: {self.vida}"
        arcade.draw_text(vida_text, 20 + self.view_left, self.view_bottom + SCREEN_HEIGHT - 20,
                         arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if self.vida<0:
            self.level=1
            self.setup(1)


        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)

        self.physics_engine.update()
        self.physics__enemy_engine.update()
        self.player_sprite.update_animation()
        self.enemy_sprite.update_animation()


        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        # Track if we need to change the viewport
        changed_viewport = False

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(self.player_sprite, self.dont_touch_list):
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # Cuando el jugador se choca con un enemigo.
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        for enemy in enemy_hit_list:
            arcade.play_sound(self.game_over)
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            '''enemy.remove_from_sprite_lists()'''

            self.vida -= 1

            if self.vida == -1:
                self.level = -1


        # Cuando el jugador cambia de nivel.
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1

            # Load the next level
            self.setup(self.level)

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

        # Check each enemy
        for enemy in self.enemy_list:
            # If the enemy hit a wall, reverse
            if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                enemy.change_x *= -1
            # If the enemy hit the left boundary, reverse
            elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                enemy.change_x *= -1
            # If the enemy hit the right boundary, reverse
            elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                enemy.change_x *= -1


def main():
    """ Main method """
    window = MyGame()
    window.setup(window.level)
    arcade.run()


if __name__ == "__main__":
    main()