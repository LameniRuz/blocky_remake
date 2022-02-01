# NOTE make it a proper class later

from ursina import FrameAnimation3d, time, Vec3, lerp, floor
from character_controller import CharacterPhysicsController

#NOTE refactor to class later
ninja = FrameAnimation3d('panda_walk', 2) #Loads an obj sequence as a frame animation.
ninja.texture = 'panda_tex'
ninja.position = Vec3(0, 20, 0)#Ninja falls if spawned underground
ninja.turnSpeed = 1.1
ninja.speed = 1


ninja_physics_cotroller = CharacterPhysicsController(ninja, height=1, step_height=1, step_sound=False)


def mob_move_to(mob, position, terrain_dict, padding=3):#FIXME wiggle bug
    animate_mob = False #Animation switch
    mob_p = mob
    mob = mob_p.entity#FIXME later refactor the class to avoid this

    # Turn towards position
    before_rotation_y = round(mob.rotation_y, 1)
    mob.lookAt(position) #Panda3D lookAt fnc
    mob.rotation = (0, mob.rotation.y + 180, 0) # y + 180 to rotate head forward, stay perp to the ground, x=0,z=0
    target_rotation_y = round(mob.rotation_y, 1)
    #Correct rotation, to make it smoother 
    mob.rotation_y = lerp(before_rotation_y, target_rotation_y, mob.turnSpeed * time.dt)
   
    rotat_diff = before_rotation_y - target_rotation_y 
    if rotat_diff >= 4 or rotat_diff <= -4:
        animate_mob = True


    # Move mob towards position
    distance =  position - mob.position# How far from target
    if distance.length() >= padding:
        mob.position -= mob.forward * mob.speed * time.dt
        #mob_play_animation(mob)
        animate_mob = True

    mob_p.physics(terrain_dict)# Terrain collision*, jumping, etc. FIXME

    if mob_p.jumping == True or not mob_p.grounded:
        animate_mob = True

    # Stop/play walking animation
    if animate_mob:
        mob_play_animation(mob)
    else:
        mob_pause_animation(mob)
        

def mob_play_animation(mob):
    mob.resume()
    mob.is_playing = True
    
def mob_pause_animation(mob):
    mob.pause()
    mob.is_playing = False
    

