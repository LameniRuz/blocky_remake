from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from mesh_terrain import MeshTerrain
from helper import hex_to_RGB, MemorisePositionHorisontal
from config import block_names 
from random import random as rd_random

#NOTE messy code, refactor later

# Global constants
PLAYER_STEP_HEIGHT = 2
PLAYER_HEIGHT = 1.86
GRAVITY_FORCE = 9.8
JUMP_HEIGHT = 10
JUMP_LERP_SPEED = 8
# Specific for the main file constants
GENERATE_EVERY_TH = 4 # Higher = larger intervals between generations NOTE not higher than 2 
GENERATE_NUM_PER_TIME_RANGE = range(4)
RESET_GEN_LENGTH = 2 # Every two blocks

# Colors
SKY_BLUE = "#37b7da"

app = Ursina() #Before Sound!, update()

# Basic set up
window.color = rgb(*hex_to_RGB(SKY_BLUE))
window.fullscreen = False 

# Place objects, world
sky = Sky()
sky.color = window.color

player = FirstPersonController(height=PLAYER_HEIGHT)#NOTE, remake FirstPersonController
player.gravity = -0.0
player.height = PLAYER_HEIGHT
player.camera_pivot.y = PLAYER_HEIGHT #align camera with the player height
#player.cursor.visible = False

#TEST physics controller
from character_controller import CharacterPhysicsController # put after ursina initiation
player_physics = CharacterPhysicsController(player)


terrain = MeshTerrain()
for _ in range(12):
    terrain.genTerrain()#Make terrain right under the player

# Previous position trackers for swirl gen reset and step_sound play
pos_track_swirl_rst = MemorisePositionHorisontal(x=player.x, z=player.z)

grounded = False
jumping = False
jumping_target = 0
jump_lerp_speed = JUMP_LERP_SPEED
def input(key):
    player_physics.input(key)#Jump

    global jumping, grounded, jumping_target
    if key == 'space' and grounded:
        jumping = True
        grounded = False
        jumping_target = player.y + JUMP_HEIGHT + PLAYER_HEIGHT
    terrain.input(key)
    if key == 'right mouse up':
        pass

count_to_gen = 0
def update():
    player_physics.update(terrain.td)# Gravity, jump-flight, etc.
    terrain.update(player.position, camera)#Highlight terrain for mining and building

    # Mob movement
    mob_move_to(ninja, player.position, terrain.td)
        
    ### Generation ### 
    global count_to_gen
    count_to_gen += 1
    if count_to_gen == GENERATE_EVERY_TH:
        # Generate terrain at the current swirl position
        count_to_gen = 0
        for _ in GENERATE_NUM_PER_TIME_RANGE: 
            terrain.genTerrain()
    
    rs_stps = RESET_GEN_LENGTH
    # Change subset position, to generate around, based on the player position
    (moved_on_x, moved_on_z) = pos_track_swirl_rst.get_abs_difference(player.x, player.z)
    if moved_on_x > rs_stps or moved_on_z > rs_stps:
        pos_track_swirl_rst.update_positions(player.x, player.z)
        terrain.genEngine.reset(player.x, player.z)
        
from sound import step_sound  # Place after ursina initiation
from mob_manager import *
app.run()
