from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from mesh_terrain import MeshTerrain
from helper import hex_to_RGB

#NOTE messy code, refactor later

# Global constants
PLAYER_STEP_HEIGHT = 2
PLAYER_HEIGHT = 1.86
GRAVITY_FORCE = 9.8
JUMP_HEIGHT = 10
JUMP_LERP_SPEED = 8

# Specific for the main file constants
GENERATE_EVERY_TH = 2 # Higher = slower
RESET_GEN_LENGTH = 4 

# Colors
SKY_BLUE = "#37b7da"



app = Ursina()

# Basic set up
window.color = rgb(*hex_to_RGB(SKY_BLUE))
window.fullscreen = False 

# Place objects, world
sky = Sky()
sky.color = window.color

player = FirstPersonController()
player.gravity = -0.0
#player.height = PLAYER_HEIGHT
player.cursor.visible = False

terrain = MeshTerrain()

# Previous position
pX = player.x
pZ = player.z

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

count_to_gen = 0

def update():
    global count_to_gen, pX, pZ
    count_to_gen += 1
    if count_to_gen == GENERATE_EVERY_TH:
        # Generate terrain at the current swirl position
        count_to_gen = 0
        terrain.genTerrain()

        # Highlight
        if count_to_gen % 2 == 0:
            terrain.update(player.position, camera)
    
    rs_stps = RESET_GEN_LENGTH
    # Change subset position, to generate around, based on object position
    if abs(player.x - pX) > rs_stps or abs(player.z - pZ) > rs_stps:
        pX = player.x
        pZ = player.z
        terrain.genEngine.reset(pX, pZ)

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
            if terrain.td.get(f"x{x}y{y+i}z{z}") == "t":
                target = y+i+height
                blockFound = True
        
        if blockFound == True:
            # Step up or down :), slowly
            player.y = lerp(player.y, target, 6 * time.dt)
            if floor(player.y) == floor(target):
                grounded = True
                print(f"Grounded!")
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




terrain.genTerrain()#FIXME
app.run()
