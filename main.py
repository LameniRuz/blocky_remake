from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from mesh_terrain import MeshTerrain
from helper import hex_to_RGB, MemorisePositionHorisontal
from config import block_names 
#from sound import StepSound, grass_audio
from random import random

#NOTE messy code, refactor later

# Global constants
PLAYER_STEP_HEIGHT = 2
PLAYER_HEIGHT = 1.86
GRAVITY_FORCE = 9.8
JUMP_HEIGHT = 10
JUMP_LERP_SPEED = 8


# Specific for the main file constants
GENERATE_EVERY_TH = 2 # Higher = slower
RESET_GEN_LENGTH = 2 

# Colors
SKY_BLUE = "#37b7da"

app = Ursina() #Before Sound!, update()

# Basic set up
window.color = rgb(*hex_to_RGB(SKY_BLUE))
window.fullscreen = False 

# Sound
#step_sound_controll = StepSound()
grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)
sounds_for_blocks = { block_names.grass:  grass_audio, block_names.snow: snow_audio}
pitches_min_dict = { block_names.grass:  0.7, block_names.snow: 0.3}

# Place objects, world
sky = Sky()
sky.color = window.color

player = FirstPersonController(height=PLAYER_HEIGHT)#NOTE, remake FirstPersonController
player.gravity = -0.0
player.height = PLAYER_HEIGHT
player.camera_pivot.y = PLAYER_HEIGHT #align camera with the player height
#player.cursor.visible = False


terrain = MeshTerrain()

for _ in range(12):
    terrain.genTerrain()#Make terrain right under the player


# Previous position trackers for swirl gen reset and step_sound play
pos_track_swirl_rst = MemorisePositionHorisontal(x=player.x, z=player.z)
pos_track_step_sound = MemorisePositionHorisontal(x=player.x, z=player.z)

grounded = False
jumping = False
jumping_target = 0
jump_lerp_speed = JUMP_LERP_SPEED
def input(key):
    global jumping, grounded, jumping_target
    if key == 'space' and grounded:
        jumping = True
        grounded = False
        jumping_target = player.y + JUMP_HEIGHT + PLAYER_HEIGHT
    terrain.input(key)
    if key == 'right mouse up':
        #print(f"mouse normal: {mouse.normal}")
        pass



# test4 = Entity(parent=camera.ui, model='quad', color=color.rgb(83, 212, 231), scale=0.1, rotation_z=45)#TEST
#print(f"test4 blue position: {test4.position}")
# print(f"camera privot position: {player.camera_pivot.position}")
# player.camera_pivot.y = PLAYER_HEIGHT
# print(f"camera privot position 2: {player.camera_pivot.position}")

count_to_gen = 0
def update():
    #print(f"player camera thing poition {player.cursor.position}")

    ### Generation ### 
    global count_to_gen
    count_to_gen += 1
    if count_to_gen == GENERATE_EVERY_TH:
        # Generate terrain at the current swirl position
        count_to_gen = 0
        terrain.genTerrain()

        # Highlight
        if count_to_gen % 2 == 0:
            terrain.update(player.position, camera)
    
    rs_stps = RESET_GEN_LENGTH
    # Change subset position, to generate around, based on the player position
    (moved_on_x, moved_on_z) = pos_track_swirl_rst.get_abs_difference(player.x, player.z)
    if moved_on_x > rs_stps or moved_on_z > rs_stps:
        pos_track_swirl_rst.update_positions(player.x, player.z)
        terrain.genEngine.reset(player.x, player.z)

    ### Player Physics ### 
    target = player.y
    blockFound=False
    height = PLAYER_HEIGHT 
    step = PLAYER_STEP_HEIGHT
    x = floor(player.x + 0.5)
    z = floor(player.z + 0.5)
    y = floor(player.y + 0.5)

    global jumping, grounded, jumping_target
    if not jumping:
        # Step in pits if they shallow enough, Step over blocks * step
        for i in range(-step, step):
            block = terrain.td.get( (floor(x), floor(y+i), floor(z)) )
            # if Found a block under the player
            if block and block != "g": #"t" now block type
                target = y+i+height
                blockFound = True
                # Make Step Sounds, for each 1 movement if player on the block (not in the air)
                (fl_step_mv_on_x, fl_step_mv_on_z ) = pos_track_step_sound.get_abs_difference(x, z)
                if fl_step_mv_on_x > 1 or fl_step_mv_on_z > 1: 
                    pos_track_step_sound.update_positions(player.x, player.z)
                    play_step_sound(block)
                         
        if blockFound == True:
            # Step up or down :), slowly
            if round(player.y, 1) != round(target, 1):#NOTE edit this 
                player.y = lerp(player.y, target, 6 * time.dt)
            else: 
                grounded = True
            if floor(player.y) == floor(target):#NOTE edit this
                grounded = True
            # print(f"player.y: {player.y}, target: {target}")
            # print(f"round player.y: {round(player.y)}, round target: {round(target)}")
            # print(f"floor player.y: {floor(player.y)}, round target: {floor(target)}")
                # print(f"Grounded!")
        else:
            # Gravity fall :()
            player.y -= GRAVITY_FORCE * time.dt
    else:
        #Start junky jumping
        if floor(jumping_target - 0.5) == floor(player.y):
            jumping = False
        global jump_lerp_speed 
        default_lerp = JUMP_LERP_SPEED
        jump_lerp_speed = default_lerp if jump_lerp_speed < 0 else jump_lerp_speed - 0.01
        player.y = lerp(player.y, jumping_target, jump_lerp_speed * time.dt)



### Helper Functions ###
def play_step_sound(block):
    step_sound = sounds_for_blocks.get(block)
    min_pitch = pitches_min_dict.get(block)
    if not step_sound: step_sound = grass_audio 
    if not min_pitch: min_pitch = 0.7
    if step_sound.playing == False:
        step_sound.pitch = random() + min_pitch
        step_sound.play()


app.run()
