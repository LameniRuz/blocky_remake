from ursina import Entity, floor, camera, color, Vec3
from random import random

from helper import hex_to_RGB
from config import PLAYER_HEIGHT, SIX_AXIS as six_axis, block_names

HIGHLIGHT_RANGE=14


bte = Entity( model='cube', color=color.rgba(1,1,1, 0.5) )#FIXME 
bte.scale=1.001
bte.visible = False


def highlight_block(pos, camera, td):
    
    for i in range(1, HIGHLIGHT_RANGE+1):
        # with current position in (+) the camera forward direction i times
        with_pos = pos + camera.forward * i

        x = floor(with_pos.x)
        y = floor(with_pos.y + PLAYER_HEIGHT)
        z = floor(with_pos.z)
        
        bte.x = x
        bte.y = y + 0.5
        bte.z = z
        
        # If there is block ahead
        block = td.get(f"x{floor(x)}y{floor(y)}z{floor(z)}")
        if block and block != "g":
            bte.visible = True 
            break
        else:
            bte.visible = False 

def mine(td, vd, subsets, numVertices):
    # Mine only if highlighted
    if not bte.visible: return

    wv = vd.get(f"x{floor(bte.x)}y{floor(bte.y-0.5)}z{floor(bte.z)}")
    if not wv: return # Mine only if there are vertices
    hl_block_v = wv[1] # first vertice for this (highlighted) block
    sub_num = wv[0]

       
    #for i in range(hl_block_v + 1, hl_block_v + numVertices + 1):
    for i in range(hl_block_v + 1, hl_block_v + numVertices + 1):
       #FIXME
       #NOTE
       #Maybe use del s[i:j]  with the model.vertices 
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
    
    subsets[sub_num].model.generate()

    # g - gap in the terrrain, delete the vertices dictionary enty
    td[f"x{floor(bte.x)}y{floor(bte.y-0.5)}z{floor(bte.z)}"] = "g"
    vd[f"x{floor(bte.x)}y{floor(bte.y-0.5)}z{floor(bte.z)}"] = None

    return (bte.position + Vec3(0,-0.5,0), sub_num)





# Testing
# def mine(td, vd, subsets, numVertices):
    # # Mine only if highlighted
    # if not bte.visible: return

    # wv = vd.get(f"x{floor(bte.x)}y{floor(bte.y)}z{floor(bte.z)}")
    # hl_block_v = wv[1] # first vertice for this (highlighted) block
    # sub_num = wv[0]

    # #for i in range(hl_block_v + 1, hl_block_v + numVertices + 1):
    # for i in range(hl_block_v, hl_block_v + numVertices + 1):
       # #FIXME
       # #NOTE
       # #Maybe use del s[i:j] or del s[i:j:k] with the model.vertices 
       # subsets[sub_num].model.vertices[i][1] += 999 #NOTE change this, how can we delete vrt from the array, fast
       # print(subsets[sub_num].model.vertices[i]) #NOTE change this, how can we delete vrt from the array, fast
       # print(i-hl_block_v)

    # subsets[sub_num].model.generate()

def block_type_change(block_y, surface=True, block_type="") -> str:
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
       


