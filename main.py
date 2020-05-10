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
PLAYER_MOVEMENT_SPEED = 1.2
GRAVITY = .5
PLAYER_JUMP_SPEED = 13

PLAYER_START_X = 64
PLAYER_START_Y = 225

#Edge Detection
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        #setup parent class
        super().__init__()

        #default face-right
        self.character_face_direction = RIGHT_FACING

        #Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING


        #Track out state
        self.jumping = False




        # --- Load Textures ---

        main_path = "images/hedgehog/hedgehog"     


        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        
        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)


    def update_animation(self, delta_time: float = 1/60):
        
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING


        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7: #was originally 2
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]







class MyGame(arcade.Window):
    """
    Main application class."""

    def __init__(self, width, height, title):
        # Call the parent class and set up the window
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.SLATE_BLUE) #LIGHT_BLUE

        # Sprite Lists
        self.background_list = None
        
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
        self.background_list = arcade.SpriteList()

        self.player_list = arcade.SpriteList()
        self.platforms_list = arcade.SpriteList()
        self.loot_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        
        self.pumpkin_list = arcade.SpriteList()

        self.enemy_list = arcade.SpriteList()

        #playerSetup
        self.player_sprite = PlayerCharacter() 

        
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)


        #Load Map
        # Name of map file to load
        map_name = "map.tmx"
        # Name of the layer in the file that has our platforms/platformss
        background_layer_name = 'Background'
        platforms_layer_name = 'Platforms'
        loot_layer_name = 'Loot'
        wall_layer_name = 'Walls'
        
        
        pumpkin_layer_name = "Pumpkins"

        enemy_layer_name = "Enemy"


        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Load Map Layers
        self.background_list = arcade.tilemap.process_layer(my_map, background_layer_name, TILE_SCALING)
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
        arcade.play_sound(self.soundtrack)


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
        self.background_list.draw()
        
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


        #Update animations

        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        self.player_list.update_animation(delta_time)


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



        #--PUMPKIN BOUNCE ON WALLS + PLATFORMS--
        for pumpkin in self.pumpkin_list:
            pumpkin.center_x += pumpkin.change_x
            walls_hit = arcade.check_for_collision_with_list(pumpkin, self.wall_list)
            platforms_hit = arcade.check_for_collision_with_list(pumpkin,self.platforms_list)
            for walls in walls_hit:
                if pumpkin.change_x > 0:
                    #pumpkin.right = walls.left
                    pumpkin.change_x = 0
                elif pumpkin.change_x < 0:
                    #pumpkin.left = walls.right
                    pumpkin.change_x = 0
            if len(walls_hit) > 0:
                pumpkin.change_x *=-1

            for platforms in platforms_hit:
                if pumpkin.change_x > 0:
                    #pumpkin.right = platforms.left
                    pumpkin.change_x = 0
                elif pumpkin.change_x < 0:
                    #pumpkin.left = platforms.right
                    pumpkin.change_x = 0
            if len(platforms_hit) > 0:
                pumpkin.change_x *=-1


        #--PUMPKIN AS SOLID?--
        #Technically works, but can glitch out
        """for player in self.player_list:
            player.center_x += player.change_x
            pumpkin_hit = arcade.check_for_collision_with_list(player, self.pumpkin_list)
            for pumpkin in pumpkin_hit:
                if player.change_x > 0:
                    #pumpkin.right = walls.left
                    player.change_x = 0
                elif player.change_x < 0:
                    #pumpkin.left = walls.right
                    player.change_x = 0
            if len(walls_hit) > 0:
                player.change_x *=-1"""



            



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






    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.player_sprite.change_x = 3
            #if self.pumpkin_engine.can_jump():
                #self.player_sprite.change_y = PLAYER_JUMP_SPEED #jump on pumpkins
        elif key == arcade.key.Q:
            exit()


        #PUMPKIN SLIDE            
        if key == arcade.key.D:
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.pumpkin_list)) > 0:
                for pumpkin in self.pumpkin_list:
                    pumpkin.change_x = 4
                        
        if key == arcade.key.A:
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.pumpkin_list)) > 0:
                for pumpkin in self.pumpkin_list:
                    pumpkin.change_x = -4
       




    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

        if key == arcade.key.UP:
            self.player_sprite.change_x = 0

        #PUMPKIN SLIDE STOP
        if key == arcade.key.D or key == arcade.key.A:
            for pumpkin in self.pumpkin_list:
                pumpkin.change_x = 0   








def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()



if __name__ == "__main__":
    main()
