from ursina import Entity, collider, floor, camera, color, Vec3
from random import random

from helper import hex_to_RGB
from config import PLAYER_HEIGHT, SIX_AXIS as six_axis, block_names, HIGHLIGHT_RANGE


hl_block = Entity( model='cube', color=color.rgba(1,1,1, 0.5), collider="box" )#FIXME 
hl_block.scale=1.001
hl_block.visible = False


# white_sp = Entity( model='sphere', color=color.rgba(1,1,1, 1), scale=0.3, visible=True )#FIXME 
# red_sp = Entity( model='sphere', color=color.rgb(232, 47, 47), scale=0.3, visible=True )#FIXME 


def highlight_block(pos, camera, td):
    for i in range(1, HIGHLIGHT_RANGE+1):
        # with current position in (+) the camera forward direction i times
        with_pos = pos + (0, PLAYER_HEIGHT, 0) + camera.forward*(i*0.5)
        
        #Pure position (if its center in the block position), 
        # highlight is initiated when the WHITE sphere center goes 'in' the block
        # white_sp.position = with_pos

        x = round(with_pos.x)
        y = floor(with_pos.y)
        z = round(with_pos.z)
            
        #After rounding, highligh center - RED
        #red_sp.position = (x,y,z)
        #print(f"x:{x}, y:{y}, z:{z}")

        hl_block.x = x
        hl_block.y = y + 0.5 #Offset hl obj
        hl_block.z = z
        # If there is block ahead
        block = td.get( (x, y, z) )  
        if block and block != "g":
            #print(mouse.position, mouse.point)
        #    print(mouse.normal, mouse.world_normal)
            hl_block.visible = True 
            break
        else:
            hl_block.visible = False 


def mine(td, vd, subsets, numVertices):
    if not hl_block.visible: return # Mine only if highlighted

    wv = vd.get( (floor(hl_block.x), floor(hl_block.y-0.5), floor(hl_block.z)) )# -0.5, remove Offset of the hl obj
    if not wv: return # Mine only if there are vertices
    hl_block_v = wv[1] # first vertice for this (highlighted) block
    sub_num = wv[0]

    for i in range(hl_block_v + 1, hl_block_v + numVertices + 1):
       #NOTE Maybe use del s[i:j]  with the model.vertices 
       subsets[sub_num].model.vertices[i][1] += 999 #NOTE change this, how can we delete vrt from the array, fast?
       # print(subsets[sub_num].model.vertices[i]) 
       # print(i-hl_block_v)
    # Testing
    # first_vc = hl_block_v + 1
    # last_vc = hl_block_v + numVertices 
    # before_verts = subsets[sub_num].model.vertices[:first_vc]
    # after_verts = subsets[sub_num].model.vertices[last_vc+1:]
    # subsets[sub_num].model.vertices = before_verts + after_verts
    # print(f"after deletion: {len(subsets[sub_num].model.vertices)}")
    # print(f"before - after  : {before - len(subsets[sub_num].model.vertices)}")
    # NOTE Spawn new blocks under the destroyed one 
    
    #subsets[sub_num].model.generate() # Regenerate updated model FIXME

    # g - gap in the terrrain, delete the vertices dictionary enty
    td[ (floor(hl_block.x), floor(hl_block.y-0.5), floor(hl_block.z)) ] = "g" # -0.5, remove Offset of the hl obj
    vd[ (floor(hl_block.x), floor(hl_block.y-0.5), floor(hl_block.z)) ] = None
    return (hl_block.position + (0,-0.5,0), sub_num)


def block_type_change(block_y, surface=True, block_type="") -> str:
    """ Determina block type based on block envirinment"""
    if surface:
        block_type = block_names.grass
        # if high engough, paint snow
        if block_y > 2:
            block_type = block_names.snow 
    # random chance of the stone type if not surface
    else:
        if random() > 0.86:
            block_type = block_names.stone 
    return block_type
       


