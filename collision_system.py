
from ursina import Vec3, held_keys, time, Entity, color
from ursina import *



# TESTING entities  for visualisation #
#ent = Entity(model='sphere', scale=20, double_sided=True)
#bumpdir = Entity(model='cube',color=color.rgba(0.3,0.9,0,0.65), block_pos=Vec3(0,0,0))# Add collider
mypos = Entity(model='cube', color=color.rgba(0.8,0.4,0,0.85), scale=1.001, block_pos=Vec3(0,0,0))# Add collider
# white_sp = Entity( model='sphere', color=color.rgba(1,1,1, 1), scale=0.8, visible=True )
# red_sp = Entity( model='sphere', color=color.rgba(0.9, .18, .18, 0.5), scale=0.8, visible=True ) 
# purple_sp = Entity( model='sphere', color=color.rgba(0.90,0.40,1.00,0.7), scale=0.8, visible=True ) 
# blue_sp = Entity( model='sphere', color=color.rgba(0.00,0.67,1.00, 0.7), scale=0.8, visible=True ) 
# blue_sp_2 = Entity( model='sphere', color=color.rgba(0.00,0.67,1.00, 0.7), scale=0.8, visible=True ) 

# blue_sp_3 = Entity( model='sphere', color=color.rgba(0.00,0.67,1.00, 0.7), scale=0.8, visible=True ) 
# blue_sp_4 = Entity( model='sphere', color=color.rgba(0.00,0.67,1.00, 0.7), scale=0.8, visible=True ) 
# red_sp_2 = Entity( model='sphere', color=color.rgb(232, 47, 47), scale=0.8, visible=True ) 
# red_sp = Entity( model='sphere', color=color.rgba(0.9, .18, .18, 0.5), scale=0.8, visible=True ) 
# red_sp_3 = Entity( model='sphere', color=color.rgba(0.9, .19, .19, 0.5), scale=0.8, visible=True ) 




bte_head = Entity(model='cube', color=color.rgba(0.67, 0.00, 1.00, 0.65), block_pos=Vec3(10,6,0))
bte_head.scale=1.0009
bte_head.visible = True 
bte_head.collider = 'box'

coll_list_2d = []
for i in range(8):#TESTING
    coll_list_2d.append([])
    for j in range(6):#FIXME index out of range if height higher than 6
        bte_2d = Entity(model='cube', color=color.rgba(0.67, 0.00, 1.00, 0.65), block_pos=Vec3(i,6,0))
        bte_2d.scale=1.0009
        bte_2d.scale_y = 1.5
        #bte_.scale_y = 3 
        bte_2d.visible = True 
        bte_2d.collider = 'box'
        coll_list_2d[i].append(bte_2d)


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

COLLIDER_PLACEMENT_DIRECTIONS_ENUM = enumerate(COLLIDER_PLACEMENT_DIRECTIONS)

def collide_wall(creature, terrain_dict):
    x = round(creature.x)
    y = round(creature.y)
    z = round(creature.z)
    creature_pos_r = Vec3(x,y,z) 

    #Test entities
    mypos.position = creature_pos_r #TEST

    block_on_head_y = round(creature.height)
    
    #spawn collider above the head
    spawn_collider_on_blc(creature_pos_r + (0, block_on_head_y+1-.1, 0), terrain_dict, coll_block=bte_head)

    for idx, directiton in enumerate(COLLIDER_PLACEMENT_DIRECTIONS):
         blc_pos_check = creature_pos_r + directiton
         for colldr_y_increase in range(0, block_on_head_y+1):
             blc_pos_check_2 = blc_pos_check + (0, colldr_y_increase, 0)
             coll_block = coll_list_2d[idx][colldr_y_increase]
             spawn_collider_on_blc(blc_pos_check_2, terrain_dict, coll_block=coll_block)

def spawn_collider_on_blc(block_pos, terrain_dict, coll_block):
    r_x = round(block_pos.x)
    r_y = round(block_pos.y)
    r_z = round(block_pos.z)

    block = terrain_dict.get( (r_x, r_y, r_z) )
    if block and block != 'g':
        #There is a block in that block_pos
        coll_block.block_pos = (r_x, r_y, r_z)

        coll_block.collider = 'box'
        coll_block.visible = True#for the TEST
        coll_block.position = Vec3(r_x, r_y, r_z)
    else:
        coll_block.collider = None
        coll_block.visible = False#for the TEST






