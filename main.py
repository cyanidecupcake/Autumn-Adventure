"""
Plague Pumpkins
"""



'''Folk Round by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/3770-folk-round
License: http://creativecommons.org/licenses/by/4.0/'''

'''Chimes by richcraftstudios
Link: https://freesound.org/people/richcraftstudios/sounds/454610
Attribution 3.0 Unported (CC BY 3.0) '''

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Plague Pumpkins"

CHARACTER_SCALING = .5
TILE_SCALING = .5


#Player Movement
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = .6
PLAYER_JUMP_SPEED = 13

#Edge Detection
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100



class MyGame(arcade.Window):
    """
    Main application class."""

    def __init__(self, width, height, title):
        # Call the parent class and set up the window
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Sprite Lists

        self.player_list = None
        self.platforms_list = None
        self.loot_list = None
        self.walls_list = None

        #Player Variable
        self.player_sprite = None


        #Physics Engine
        self.physics_engine = None

        #Scrolling Tracker
        self.view_bottom = 0
        self.view_left = 0

        #Score
        self.score = 10


        #Load Sounds
        self.soundtrack = arcade.load_sound("sounds/folk-round-by-kevin-macleod-from-filmmusic-io.mp3")
        self.lootSound = arcade.load_sound("sounds/chimes-by-richcraftstudios.wav")







    def setup(self):
        # Create your sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        self.platforms_list = arcade.SpriteList()
        self.loot_list = arcade.SpriteList()
        self.walls_list = arcade.SpriteList()


        #playerSetup
        image_source = "images/hedgehog_a.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)


        #Load Map
        # Name of map file to load
        map_name = "map.tmx"
        # Name of the layer in the file that has our platforms/platformss
        platforms_layer_name = 'Platforms'
        loot_layer_name = 'Loot'
        walls_layer_name = 'Walls'


        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Load Layers
        self.platforms_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
        self.loot_list = arcade.tilemap.process_layer(my_map, loot_layer_name, TILE_SCALING)
        self.walls_list = arcade.tilemap.process_layer(my_map, walls_layer_name, TILE_SCALING)




        #Create Physics Engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.platforms_list,
                                                             GRAVITY)


        #Score
        self.score = 10


        #Play Music
        arcade.play_sound(self.soundtrack)



    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists
        self.player_list.draw()
        self.platforms_list.draw()
        self.loot_list.draw()
        self.walls_list.draw()


        #Draw score
        score_text = f"{self.score}"
        arcade.draw_text(score_text, 930 + self.view_left, 600 + self.view_bottom,
                         arcade.csscolor.ORANGE, 30)





    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.physics_engine.update()


        #---SCROLLING---

        changed = False

        #scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        #scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        #scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        #scroll down
        bottom_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)



        #---LOOT COLLISION DETECTION---
        loot_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.loot_list)
        for loot in loot_hit_list:
            #remove loot
            loot.remove_from_sprite_lists()
            #change score
            arcade.play_sound(self.lootSound)
            self.score += 1


        #---WALLS COLLISION DETECTION---
        walls_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.walls_list)
        for wall in walls_hit_list:
            self.player_sprite.change_x = -1



    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.Q:
                exit()




    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0








def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()



if __name__ == "__main__":
    main()
