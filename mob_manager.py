# NOTE make it a proper class later

from ursina import FrameAnimation3d, time, Vec3


ninja = FrameAnimation3d('panda_walk', 1) #Loads an obj sequence as a frame animation.
ninja.texture = 'panda_tex'
ninja.position = Vec3(0, -2, 0)
ninja.turnSpeed = 0.
ninja.speed = 1


def mob_move_to(mob, position, terrain_dict, padding=0):
    # Turn towards position
    mob.lookAt(position, mob.turnSpeed * time.dt) #Panda3D lookAt fnc
    mob.rotation = (0, mob.rotation.y + 180, 0)# y + 180 to rotate head forward

    # Move mov towards position
    mob.position -= mob.forward * mob.speed * time.dt


