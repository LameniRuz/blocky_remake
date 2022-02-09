"""Subject terrain collisions"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()
player = FirstPersonController(gravity=0)

def update():
    print(round(player.x), round(player.y), round(player.z))
    # player.x += held_keys['d'] * time.dt
    # player.x -= held_keys['a'] * time.dt
    pass

def input(key):
    if key == 'q':
        player.position += (0,-1,0)
    if key == 'e':
        player.position += (0,1,0)
    if key == 'space':
        player.y += 1
        invoke(setattr, player, 'y', player.y-1, delay=.25)


#rect shape in blocks
rect_center_position=Vec3(1,1,1)
width = 3
height = 3
length = 3
#e = Entity(model='cube', color=color.orange, scale_y=2)

for x in range(width):
    for y in range(height):
        for z in range(length):
            e = Entity(position=(x,y,z), model='cube', color=color.orange)
e = Entity(position=(x,y,z), model='cube', color=color.orange)
hl_bl1 = Entity(scale=2.001, model='sphere', color=color.rgba(1,1,1, 0.5), position=rect_center_position)
hl_bl2 = Entity(scale=3.001, model='sphere', color=color.rgba(1,1,1, 0.5), position=rect_center_position)
hl_bl3 = Entity(scale=4.001, model='sphere', color=color.rgba(1,1,1, 0.5), position=rect_center_position)



surrounding_blocks = []

x_move = width + 2
y_move = height + 2 
z_move = length + 2
for x_i in range(-1, x_move, x_move):
    for y_j in range(-1, y_move, y_move):
        for z_k in range(-1, z_move, z_move):
            cube = Entity(position=Vec3(x_i,y_j,z_k), model='cube')
            cube.position+=(x_i,y_j,z_k)
            surrounding_blocks.append(cube)




head_block_position = Vec3(10,10,10)







app.run()
