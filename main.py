from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController
from first_person_ctr_custom import CustomFirstPersonController 

from mesh_terrain import MeshTerrain
from helper import hex_to_RGB, MemorisePositionHorisontal
from config import PLAYER_HEIGHT, SKY_BLUE, HIGHLIGHT_RANGE 

app = Ursina() #Ursina initiation!, Before Sound!, update()
from sound import step_sound  # Place after ursina initiation
from mob_manager import *
from character_controller import CharacterPhysicsController # put after ursina initiation

#NOTE messy code, refactor later


# Specific for the main file constants
GENERATE_EVERY_TH = 4 # Higher = larger intervals between generations NOTE not higher than 2 
GENERATE_NUM_PER_TIME_RANGE = range(4)
RESET_GEN_LENGTH = 2 # Every two blocks

# Basic set up 
window.color = rgb(*hex_to_RGB(SKY_BLUE))
window.fullscreen = False 
# Place objects, world
sky = Sky()
sky.color = window.color


#TEST smooth follow 
# e = Entity(model='diamond', scale=0.5)
# sf = e.add_script(SmoothFollow(target=player, offset=(2,3,2), speed=1, rotation_speed=1))

terrain = MeshTerrain()
for _ in range(15): terrain.genTerrain()# Make terrain right under the player

def input(key):
    terrain.input(key)# Terrain change on keypress
    if key == 'space':
        player_physics.initiate_jump()# Player jump
        ninja_physics_cotroller.initiate_jump()# Ninja also jumping!
        pass


#player = FirstPersonController(height=PLAYER_HEIGHT)#NOTE, remake FirstPersonController
player = CustomFirstPersonController(height=PLAYER_HEIGHT, terrain=terrain)#NOTE, remake FirstPersonController
player.gravity = -0.0
player.height = PLAYER_HEIGHT
player.camera_pivot.y = PLAYER_HEIGHT #align camera with the player height
#player.cursor.visible = False


#TEST physics controller
player_physics = CharacterPhysicsController(player)



# Previous position trackers for swirl gen reset and step_sound play
pos_track_swirl_rst = MemorisePositionHorisontal(x=player.x, z=player.z)
count_to_gen = 0
def update():
    player_physics.physics(terrain.td)# Gravity, jump-flight, etc.
    terrain.update(player.position, camera)#Highlight terrain for mining and building

    # Mob movement
    #mob_move_to(ninja_physics_cotroller, player.position, terrain_dict=terrain.td) #TEST
        
    ### Generation ### 
    global count_to_gen
    count_to_gen += 0#NOTE: DISABLED
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

app.run()
