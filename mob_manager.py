# NOTE make it a proper class later

from ursina import FrameAnimation3d, time, Vec3
from character_controller import CharacterPhysicsController

#NOTE refactor to class later
ninja = FrameAnimation3d('panda_walk', 1) #Loads an obj sequence as a frame animation.
ninja.texture = 'panda_tex'
ninja.position = Vec3(0, 20, 0)#Ninja falls if spawned underground
ninja.turnSpeed = 0.1
ninja.speed = 1


ninja_physics_cotroller = CharacterPhysicsController(ninja, height=1, step_height=1)


def mob_move_to(mob, position, terrain_dict, padding=10):
    mob_p = mob
    mob = mob_p.entity#FIXME later refactor the class to avoid this

    # Turn towards position
    mob.lookAt(position, mob.turnSpeed * time.dt) #Panda3D lookAt fnc, turn speed is broken
    mob.rotation = (0, mob.rotation.y + 180, 0)# y + 180 to rotate head forward


    # Move mob towards position
    distance =  position - mob.position# How far from target
    if distance.length() >= padding:
        mob.position -= mob.forward * mob.speed * time.dt
        mob.resume()# Animation
        mob.is_playing = True
    else:
        mob.pause()# Animation
        mob.is_playing = False

    mob_p.physics(terrain_dict)# Terrain collision*, jumping, etc. FIXME

    if mob_p.jumping == True or not mob_p.grounded:
        mob.resume()# Animation
        mob.is_playing = True
        


    
    

    

