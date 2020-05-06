"""
Plague Pumpkins
"""



'''Folk Round by Kevin MacLeod
Link: https://incompetech.filmmusic.io/song/3770-folk-round
License: http://creativecommons.org/licenses/by/4.0/'''

'''Chimes by richcraftstudios
Link: https://freesound.org/people/richcraftstudios/sounds/454610
Attribution 3.0 Unported (CC BY 3.0) '''

'''Oof by maxmakessounds
Link: https://freesound.org/people/maxmakessounds/sounds/353541/
Attribution 3.0 Unported (CC BY 3.0) '''

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Plague Pumpkins"

CHARACTER_SCALING = .5
TILE_SCALING = .5


#Player Movement
PLAYER_MOVEMENT_SPEED = 1
GRAVITY = .5
PLAYER_JUMP_SPEED = 13
PUMPKIN_MOVEMENT_SPEED = 1

PLAYER_START_X = 64
PLAYER_START_Y = 225

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
        self.wall_list = None

        self.pumpkin_list = None

        self.enemy_list = None


    
        

        #Player Variable
        self.player_sprite = None
        self.pumpkin_sprite = None



        #Physics Engine
        self.physics_engine = None

        #Scrolling Tracker
        self.view_bottom = 0
        self.view_left = 0

        #Score
        self.score = 10
        self.damage = 0



        #Load Sounds
        self.damageSound = False

        
        self.soundtrack = arcade.load_sound("sounds/folk-round-by-kevin-macleod-from-filmmusic-io.mp3")
        self.lootSound = arcade.load_sound("sounds/chimes-by-richcraftstudios.wav")
        self.oof = arcade.load_sound("sounds/oof-by-maxmakessounds.wav")






    def setup(self):
        # Create your sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        self.platforms_list = arcade.SpriteList()
        self.loot_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        
        self.pumpkin_list = arcade.SpriteList()

        self.enemy_list = arcade.SpriteList()

        #playerSetup
        image_source = "images/hedgehog_a.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)


        #Load Map
        # Name of map file to load
        map_name = "map.tmx"
        # Name of the layer in the file that has our platforms/platformss
        platforms_layer_name = 'Platforms'
        loot_layer_name = 'Loot'
        wall_layer_name = 'Walls'
        
        pumpkin_layer_name = "Pumpkins"

        enemy_layer_name = "Enemy"


        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Load Map Layers
        self.platforms_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
        self.loot_list = arcade.tilemap.process_layer(my_map, loot_layer_name, TILE_SCALING)
        self.wall_list = arcade.tilemap.process_layer(my_map, wall_layer_name, TILE_SCALING)

        self.pumpkin_list = arcade.tilemap.process_layer(my_map, pumpkin_layer_name, TILE_SCALING)

        self.enemy_list = arcade.tilemap.process_layer(my_map, enemy_layer_name, TILE_SCALING)


        #Create Physics Engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.platforms_list,
                                                             GRAVITY)
        
        #self.pumpkin_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                               #self.pumpkin_list,
                                                               #GRAVITY)

        self.wall_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                          self.wall_list,
                                                          GRAVITY)
        
        #Score
        self.score = 10


        #Play Music
        #arcade.play_sound(self.soundtrack)


        #Enemy Moves +1 
        for enemy in self.enemy_list:
            enemy.change_x = 1


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
        self.wall_list.draw()
        
        self.pumpkin_list.draw()

        self.enemy_list.draw()


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
        self.physics_engine.update() #solid object + jump
        #self.pumpkin_engine.update() #solid object + jump (on pumpkins)
        self.wall_engine.update() #solid object


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


        #---FALL OFF WORLD ---
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            

            
        #---LOOT COLLISION DETECTION---
        loot_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.loot_list)
        for loot in loot_hit_list:
            #remove loot
            loot.remove_from_sprite_lists()
            #change score
            arcade.play_sound(self.lootSound)
            self.score += 1


        #--ENEMY BOUNCE ON WALLS + PLATFORMS--
        for enemy in self.enemy_list:
            enemy.center_x += enemy.change_x
            walls_hit = arcade.check_for_collision_with_list(enemy, self.wall_list)
            platforms_hit = arcade.check_for_collision_with_list(enemy,self.platforms_list)
            for walls in walls_hit:
                if enemy.change_x > 0:
                    enemy.right = walls.left
                elif enemy.change_x < 0:
                    enemy.left = walls.right       
            if len(walls_hit) > 0:
                enemy.change_x *=-1

            for platforms in platforms_hit:
                if enemy.change_x > 0:
                    enemy.right = platforms.left
                elif enemy.change_x < 0:
                    enemy.left = platforms.right       
            if len(platforms_hit) > 0:
                enemy.change_x *=-1




        #---ENEMY DOES DAMAGE
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
            self.damage = True
            if self.damageSound == False:
                arcade.play_sound(self.oof)
            self.damageSound = True
            
        
        if self.damage == True and len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) < 1:
            
            self.score -=1
            self.damage = False
            self.damageSound = False






        
        #--PUMPKIN COLLISION DETECTION
        self.pumpkin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                self.pumpkin_list)
        self.pumpkin_list.update()
        
                






    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
            #if self.pumpkin_engine.can_jump():
                #self.player_sprite.change_y = PLAYER_JUMP_SPEED #jump on pumpkins
        elif key == arcade.key.Q:
            exit()


        #if key == arcade.key.D:
            #for pumpkin in self.pumpkin_hit_list:
                #pumpkin.change_x = PUMPKIN_MOVEMENT_SPEED                       

        #if key == arcade.key.A:
               # print("PUMPKIN BACK")

       




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
