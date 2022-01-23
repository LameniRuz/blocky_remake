from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from mesh_terrain import MeshTerrain
from helper import hex_to_RGB

# Global constants
PLAYER_STEP_HIGHT = 2
PLAYER_HEIGHT = 1.86
GRAVITY_FORCE = 9.8
GENERATE_EVERY_TH = 2
RESET_GEN_LENGTH = 4



app = Ursina()

# Basic set up
window.color = rgb(*hex_to_RGB("#37b7da"))
window.fullscreen = False 

# Place objects, world
sky = Sky()
sky.color = window.color

player = FirstPersonController()
player.gravity = -0.0
player.cursor.visible = False

terrain = MeshTerrain()

# Previous position
pX = player.x
pZ = player.z


count_to_gen = 0
def update():
    global count_to_gen, pX, pZ
    count_to_gen += 1
    if count_to_gen == GENERATE_EVERY_TH:
        # Generate terrain at the current swirl position
        count_to_gen = 0
        terrain.genTerrain()
    
    rs_stps = RESET_GEN_LENGTH
    # Change subset position, to generate around, based on object position
    if abs(player.x - pX) > rs_stps or abs(player.z - pZ) > rs_stps:
        pX = player.x
        pZ = player.z
        terrain.genEngine.reset(pX, pZ)

    target = player.y
    blockFound=False
    height = PLAYER_HEIGHT 
    step = PLAYER_STEP_HIGHT
    x = floor(player.x + 0.5)
    z = floor(player.z + 0.5)
    y = floor(player.y + 0.5)
    # Step in pits if they shallow enough, Step over blocks * step
    # without jump
    for i in range(-step, step):
        if terrain.td.get(f"x{x}y{y+i}z{z}") == "t":
            target = y+i+height
            blockFound = True
        
    if blockFound == True:
        # Step up or down :), slowly
        player.y = lerp(player.y, target, 6 * time.dt)
    # updateTerrain()
    else:
        # Gravity fall :()
        player.y -= GRAVITY_FORCE * time.dt
        pass




terrain.genTerrain()#FIXME
app.run()
