
from ursina import Vec3, held_keys, time, Entity, color
from ursina import *



# TESTING entities  for visualisation #
#ent = Entity(model='sphere', scale=20, double_sided=True)
bumpdir = Entity(model='cube',color=color.rgba(0.3,0.9,0,0.65), block_pos=Vec3(0,0,0))# Add collider
mypos = Entity(model='cube', color=color.rgba(0.8,0.4,0,0.85), block_pos=Vec3(0,0,0))# Add collider
white_sp = Entity( model='sphere', color=color.rgba(1,1,1, 1), scale=0.8, visible=True )
red_sp = Entity( model='sphere', color=color.rgba(0.9, .18, .18, 0.5), scale=0.8, visible=True ) 
purple_sp = Entity( model='sphere', color=color.rgba(0.90,0.40,1.00,0.7), scale=0.8, visible=True ) 
blue_sp = Entity( model='sphere', color=color.rgba(0.00,0.67,1.00, 0.7), scale=0.8, visible=True ) 
blue_sp_2 = Entity( model='sphere', color=color.rgba(0.00,0.67,1.00, 0.7), scale=0.8, visible=True ) 

blue_sp_3 = Entity( model='sphere', color=color.rgba(0.00,0.67,1.00, 0.7), scale=0.8, visible=True ) 
blue_sp_4 = Entity( model='sphere', color=color.rgba(0.00,0.67,1.00, 0.7), scale=0.8, visible=True ) 
red_sp_2 = Entity( model='sphere', color=color.rgb(232, 47, 47), scale=0.8, visible=True ) 
red_sp = Entity( model='sphere', color=color.rgba(0.9, .18, .18, 0.5), scale=0.8, visible=True ) 
red_sp_3 = Entity( model='sphere', color=color.rgba(0.9, .19, .19, 0.5), scale=0.8, visible=True ) 

coll_list = []
for i in range(12):
    bte_ = Entity(model='cube', color=color.rgba(1.00,0.42,0.30, 0.65), block_pos=Vec3(i,5,0))# Add collider
    bte_.scale=1.0009
    bte_.scale_y = 1.5
    #bte_.scale_y = 3 
    bte_.visible = True 
    bte_.collider = 'box'
    coll_list.append(bte_)
    


hl_list = []
for i in range(12):
    bte = Entity(model='cube', color=color.rgba(0.1,0.4,0,0.55), position=Vec3(i,0,0))# Add collider
    bte.scale=1.0009
    bte.visible = True 
    bte.collider = 'box'
    hl_list.append(bte)


COLLIDER_PLACEMENT_DIRECTIONS = [
(1,0,0),
(-1,0,0),
(0,0,1),
(0,0,-1),
(-1,0,-1),
(1,0,1),
(1,0,-1),
(-1,0,1),
]

def collide_wall(creature, terrain_dict):
    x = round(creature.x)
    y = round(creature.y)
    z = round(creature.z)
    creature_pos_r = Vec3(x,y,z) 

    block_on_head_y = round(creature.height - 0.5 )# - 0.5 block offset
    increase_y_to_head = Vec3(0, block_on_head_y, 0) 

    for idx, directiton in enumerate(COLLIDER_PLACEMENT_DIRECTIONS):
        blc_pos_check = creature_pos_r + increase_y_to_head + directiton 
        spawn_collider_on_blc(blc_pos_check, terrain_dict, idx)


def spawn_collider_on_blc(block_pos, terrain_dict, collider_idx):
    coll_block = coll_list[collider_idx]
    r_x = round(block_pos.x)
    r_y = round(block_pos.y)
    r_z = round(block_pos.z)

    block = terrain_dict.get( (r_x, r_y, r_z) )
    if block and block != 'g':
        # print("block found")
        #There is a block in that block_pos
        coll_block.block_pos = (r_x, r_y, r_z)#offset needed, NOTE maybe place it always near the player, only turn on the collision here (to prevent other mobs from colliding with emoty space (player still active coll_block))

        #NOTE collider boxes needs to be disabled if the block gets destroyed
        coll_block.collider = 'box'
        coll_block.visible = True#for the TEST
        coll_block.position = Vec3(r_x, r_y+0.5, r_z)#0.5 block offset, to place coll_block model in the same position as a block one
    else:
        coll_block.collider = None
        coll_block.visible = False#for the TEST


def collide_wall_old(creature, terrain_dict):
    #NOTE Refactor later + fix ghosting with the vertical movement + vertical collide_wall delay
    #NOTE maybe just spawn_collider_on_blc around the player like axis in the config file and make it double layered box
    x = round(creature.x)
    y = round(creature.y)
    z = round(creature.z)
    creature_pos_r = Vec3(x,y,z) 

    block_on_head_y = round(creature.height - 0.5 )# - 0.5 block offset
    increase_y_to_head = (0, block_on_head_y, 0)

    # Creature directions without y
    creature_forward = creature.forward
    creature_forward.y=0 
    creature_left = creature.left
    creature_left.y=0

    
    # Main positions to check for a block and spawn collider 
    blc_forward_pos = creature_pos_r + creature_forward + increase_y_to_head
    red_sp.position = blc_forward_pos
    
    #Edited with the true direction not with forward
    #Directional
    # creature_direction = creature.direction
    # blc_forward_pos = creature_pos_r + creature_direction + increase_y_to_head
    # red_sp.position = blc_forward_pos

    
    #To prevent directional ghosting
    blc_forward_direction_pos = creature_pos_r + creature.direction + increase_y_to_head
    spawn_collider_on_blc(block_pos=blc_forward_direction_pos, terrain_dict=terrain_dict, collider_idx=10)
    red_sp_3.position = blc_forward_direction_pos


    blc_back_pos = creature_pos_r - creature_forward + increase_y_to_head #is back needed with the directional approach

    blc_left_pos = creature_pos_r + creature_left + increase_y_to_head 
    white_sp.position = blc_left_pos

    blc_right_pos = creature_pos_r - creature_left + increase_y_to_head 
    purple_sp.position = blc_right_pos


    blc_up_pos = Vec3(0,1,0) + creature_pos_r + increase_y_to_head
    blc_down_pos = Vec3(0,1,0) + creature_pos_r + increase_y_to_head


    #Prevent fazing through diagonal direction if there is no block there #NOTE or simply can check blc left + 1  in direction
    # Forward-left-right
    forward_left = creature_pos_r + creature_left * Vec3(0.5,0.5,0.5)
    forward_left = forward_left + creature_forward * Vec3(0.5,0.5,0.5)
    # forward_left = creature_pos_r  + creature_left * Vec3(0.5,0.5,0.5)
    # forward_left = forward_left + creature_direction * Vec3(0.5,0.5,0.5)


    #half of 1 forward, half left and half of 1 forward and right
    forward_right = creature_pos_r - creature_left * Vec3(0.5,0.5,0.5)
    forward_right = forward_right + creature_forward * Vec3(0.5,0.5,0.5)
    blue_sp.position = forward_right + increase_y_to_head
    blue_sp_2.position = forward_left + increase_y_to_head

    spawn_collider_on_blc(block_pos=forward_right+increase_y_to_head, terrain_dict=terrain_dict, collider_idx=7)
    spawn_collider_on_blc(block_pos=forward_left+increase_y_to_head, terrain_dict=terrain_dict, collider_idx=6)


    backwards_left = creature_pos_r + creature_left * Vec3(0.5,0.5,0.5)
    # print(f"creature_forward: {creature_forward}")
    backwards_left = forward_left - creature_forward 
    backwards_right = creature_pos_r - creature_left * Vec3(0.5,0.5,0.5)
    backwards_right = forward_right - creature_forward 
    #blue_sp_3.position = backwards_left + increase_y_to_head - creature_forward*Vec3(0.5,0.5,0.5)#why need to go full one back
    blue_sp_3.position = backwards_left + increase_y_to_head
    blue_sp_4.position = backwards_right + increase_y_to_head
    spawn_collider_on_blc(block_pos=backwards_right+increase_y_to_head, terrain_dict=terrain_dict, collider_idx=8)
    spawn_collider_on_blc(block_pos=backwards_left+increase_y_to_head, terrain_dict=terrain_dict, collider_idx=9)


    #This can be done just using whe axis like the one from the config NOTE remake later
    spawn_collider_on_blc(block_pos=blc_forward_pos, terrain_dict=terrain_dict, collider_idx=0)
    spawn_collider_on_blc(block_pos=blc_back_pos, terrain_dict=terrain_dict, collider_idx=1)
    red_sp_2.position = blc_back_pos

    spawn_collider_on_blc(block_pos=blc_left_pos, terrain_dict=terrain_dict, collider_idx=2)
    spawn_collider_on_blc(block_pos=blc_right_pos, terrain_dict=terrain_dict, collider_idx=3)

    spawn_collider_on_blc(block_pos=blc_up_pos, terrain_dict=terrain_dict, collider_idx=4)
    spawn_collider_on_blc(block_pos=blc_down_pos, terrain_dict=terrain_dict, collider_idx=5)

    
    #Test entities
    mypos.position = creature_pos_r
    
     





