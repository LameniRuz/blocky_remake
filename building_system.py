from ursina import floor, mouse
from config import SIX_AXIS as six_axis 
from terrain_change_system import hl_block

def checkBuildPos(td, vd): 
    if not hl_block.visible: return #NOTE Without this is fun, try to add toggle of this to a game mode AIRBUILD

    # Adjust build site, since build-tool-entity (hl_block) offset.
    pos = hl_block.position + (0,-0.5,0) 

    wv = vd.get((pos.x, pos.y, pos.z))
    if wv: #TEST for AIRBUILD 
        sub_num = wv[0] #Get subset of the build base block
    else: sub_num = 0

    # Build direction change, with the hl_block/camera ray collision
    if mouse.normal:
        pos.x += round(mouse.normal.x)
        pos.y += round(mouse.normal.y)
        pos.z += round(mouse.normal.z)
    else:
        pos.y += 1
         
    # Store in convenient variables and floor.
    x = floor(pos.x)
    y = floor(pos.y)
    z = floor(pos.z)
    # if no block is here, return coords
    block = td.get((x,y,z))
    if block != 'g' and block !=None:
        return None
    return (x,y,z, sub_num)

def gapShell(x, y, z, td):
    """ Create gap 'shell' around the placed block at the coords if there is empty space""" 
    for i in range(6):
        p_x = x + six_axis[i][0]
        p_y = y + six_axis[i][1]
        p_z = z + six_axis[i][2]
        if not td.get((p_x, p_y, p_z)):
            td[(p_x,p_y,p_z)] = 'g'



