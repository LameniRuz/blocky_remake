from ursina import *
from ursina import collider
from helper import  MemorisePositionHorisontal
from sound import step_sound  # Place after ursina initiation

""" Import this module after Ursina initiation """

#NOTE Merge with the first person controller later?
#NOTE how can we duplicate this in mobs? 
#NOTE Change this so it can inherit from other classes, not use self.entity

# Global constants NOTE make them part of the class
PLAYER_STEP_HEIGHT = 2#less than two breaks
#PLAYER_STEP_HEIGHT = 1#TEST
PLAYER_HEIGHT = 1.86
GRAVITY_FORCE = 9.8
JUMP_HEIGHT = 10
JUMP_LERP_SPEED = 8

#TEST entity
TESTING_VISIBLE=False
# feetHitpos = Entity(model='cube', color=color.rgba(0.01,1.00,0.01,0.85), scale=1.001, block_pos=Vec3(0,0,0), collider=None    , visible=TESTING_VISIBLE)
# poss_st_onENT = Entity(model='cube', color=color.rgba(0.20,0.40,0.01,0.85), scale=1.001, block_pos=Vec3(0,0,0), collider=None , visible=TESTING_VISIBLE)
# poss_st_onENT2 = Entity(model='cube', color=color.rgba(0.30,0.30,0.11,0.85), scale=1.001, block_pos=Vec3(0,0,0), collider=None, visible=TESTING_VISIBLE)
# poss_st_onENT3 = Entity(model='cube', color=color.rgba(0.40,0.10,0.14,0.85), scale=1.001, block_pos=Vec3(0,0,0), collider=None, visible=TESTING_VISIBLE)

class CharacterPhysicsController:
    def __init__(self, entity, height=PLAYER_HEIGHT, step_sound=True, **kwargs):
        self.entity = entity


        # Physics #
        self.blockFound = False
        self.height = height 
        self.step = PLAYER_STEP_HEIGHT
        self.step = PLAYER_STEP_HEIGHT#TESTING
        self.step = 1
        self.gravity_force = GRAVITY_FORCE#Change to fit player and mobs 


        #Jumping
        self.grounded = False
        self.jumping = False
        self.jumping_target = 0
        self.jump_lerp_speed = JUMP_LERP_SPEED
        self.jump_height = JUMP_HEIGHT

        # Previous position trackers for swirl gen reset and step_sound play
        self.pos_track_step_sound = MemorisePositionHorisontal(x=entity.x, z=entity.z)

        #Sound
        self.step_sound = step_sound

       
        self.setCustomAttrs(**kwargs)# Add custom attributes


    def initiate_jump(self):
        if not self.grounded: return
        self.jumping = True
        self.grounded = False
        self.jumping_target = self.entity.y + self.jump_height + PLAYER_HEIGHT
    
    def jump_flight(self): #junky jumping
        head_up_ray = raycast(self.entity.position+(0,self.height+0.3,0), self.entity.up, ignore=(self.entity,))#stop jump if we hit the celling, BUG, wont works
        if floor(self.jumping_target) <= floor(self.entity.y) or head_up_ray.hit:
            self.jumping = False
            self.grounded = False
        else:
            default_lerp = JUMP_LERP_SPEED
            jump_lerp_speed = default_lerp if self.jump_lerp_speed < 0 else self.jump_lerp_speed - 0.01 #Jump slowdown 
            self.entity.y = lerp(self.entity.y, self.jumping_target, jump_lerp_speed * time.dt)

    def physics(self, terrain_dict):
            # feet_hit_direction = self.entity.direction
            # feet_ray = raycast(self.entity.position+(0,0,0), feet_hit_direction, ignore=(self.entity,), distance=.3, debug=True)
            # self.entity.feet_ray_hit = False#rename
            # if feet_ray.hit:
                # self.entity.feet_ray_hit = True

            target = self.entity.y
            self.blockFound=False
            x = round(self.entity.x)
            z = round(self.entity.z)
            y = round(self.entity.y)

            if not self.jumping:
                # Step in pits if they shallow enough, Step over blocks * step
                for i in range(-1, self.step):#without this cant step up on new blocks under
                    block = terrain_dict.get( (x, y+i, z) )
                    # if Found a block under the self.entity
                    if block and block != "g": #"t" now block type
                        target = round(y+i+self.height+1)
                        #print(f"target: {target}")
                        self.blockFound = True
                        if self.step_sound:
                            # Make Step Sounds, for each 1 movement if self.entity on the block (not in the air)
                            (fl_step_mv_on_x, fl_step_mv_on_z ) = self.pos_track_step_sound.get_abs_difference(x, z)
                            if fl_step_mv_on_x > 1 or fl_step_mv_on_z > 1: 
                                self.pos_track_step_sound.update_positions(self.entity.x, self.entity.z)
                                step_sound.play_step_sound(block)
                                 
                if self.blockFound == True:
                    self.grounded = True#jump, test,remove
                else:
                    # Gravity fall :()
                    self.entity.y -= self.gravity_force * time.dt
            else:
                self.jump_flight()

    def setCustomAttrs(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
