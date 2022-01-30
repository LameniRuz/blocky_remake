from ursina import *
from helper import  MemorisePositionHorisontal
from sound import step_sound  # Place after ursina initiation

""" Import this module after Ursian initiation """

#NOTE Merge with the first person controller later?
#NOTE how can we dublocate this in mobs? 

# Global constants NOTE make them part of the class
PLAYER_STEP_HEIGHT = 2
PLAYER_HEIGHT = 1.86
GRAVITY_FORCE = 9.8
JUMP_HEIGHT = 10
JUMP_LERP_SPEED = 8

class CharacterPhysicsController:
    def __init__(self, entity):
        self.entity = entity


        # Physics #
        self.blockFound = False
        self.height = PLAYER_HEIGHT
        self.step = PLAYER_STEP_HEIGHT
        self.gravity_force = GRAVITY_FORCE#Change to fit player and mobs 


        #Jumping
        self.grounded = False
        self.jumping = False
        self.jumping_target = 0
        self.jump_lerp_speed = JUMP_LERP_SPEED
        self.jump_height = JUMP_HEIGHT

        # Previous position trackers for swirl gen reset and step_sound play
        self.pos_track_step_sound = MemorisePositionHorisontal(x=entity.x, z=entity.z)


    def initiate_jump(self):
        if not self.grounded: return
        self.jumping = True
        self.grounded = False
        self.jumping_target = self.entity.y + self.jump_height + PLAYER_HEIGHT
    
    def jump_flight(self): #junky jumping
        if floor(self.jumping_target - 0.5) <= floor(self.entity.y):
            self.jumping = False
        default_lerp = JUMP_LERP_SPEED
        jump_lerp_speed = default_lerp if self.jump_lerp_speed < 0 else self.jump_lerp_speed - 0.01 #Jump slowdown 
        self.entity.y = lerp(self.entity.y, self.jumping_target, jump_lerp_speed * time.dt)


    def physics(self, terrain_dict):
            target = self.entity.y
            self.blockFound=False
            x = floor(self.entity.x + 0.5)
            z = floor(self.entity.z + 0.5)
            y = floor(self.entity.y + 0.5)

            if not self.jumping:
                # Step in pits if they shallow enough, Step over blocks * step
                for i in range(-self.step, self.step):
                    block = terrain_dict.get( (floor(x), floor(y+i), floor(z)) )
                    # if Found a block under the self.entity
                    if block and block != "g": #"t" now block type
                        target = y+i+self.height
                        self.blockFound = True
                        # Make Step Sounds, for each 1 movement if self.entity on the block (not in the air)
                        (fl_step_mv_on_x, fl_step_mv_on_z ) = self.pos_track_step_sound.get_abs_difference(x, z)
                        if fl_step_mv_on_x > 1 or fl_step_mv_on_z > 1: 
                            self.pos_track_step_sound.update_positions(self.entity.x, self.entity.z)
                            step_sound.play_step_sound(block)
                                 
                if self.blockFound == True:
                    # Step up or down :), slowly
                    if round(self.entity.y, 1) != round(target, 1):#NOTE edit this 
                        self.entity.y = lerp(self.entity.y, target, 6 * time.dt)
                    else: 
                        self.grounded = True
                    if floor(self.entity.y) == floor(target):#NOTE edit this
                        self.grounded = True
                else:
                    # Gravity fall :()
                    self.entity.y -= self.gravity_force * time.dt
            else:
                self.jump_flight()

    def input(self, key):
        if key == 'space':
            self.initiate_jump()

    def update(self, terrain_dict):
        self.physics(terrain_dict)

