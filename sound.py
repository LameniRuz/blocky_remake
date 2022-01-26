# from ursina import Audio
# from math import floor 
# from random import random
""" DOESNT WORK, sound controll needs to be after game engine enitiation"""
# from config import block_names

# # Add new sounds settings here 
# pitches_min_dict = { block_names.grass:  0.7, block_names.snow: 0.3}

# class StepSound():
    # def __init__(self):
        # #self.sounds_d = sounds_dict
        # self.sounds_for_blocks = sounds_for_blocks
        # self.pitches_min_d = pitches_min_dict


    # def try_play_steps(self, block_type):
        # st_sound = self.sounds_for_blocks.get(block_type)
        # if st_sound.playing == False:
            # st_min_pitch = self.pitches_min_d[block_type]
            # st_sound.pitch = round(random() + st_min_pitch)
            # st_sound.play()
        


    # def try_play(self, sound_key_name: str) -> int:
        # st_sound = self.sounds_d.get(sound_key_name)
        # st_min_pitch = self.pitches_min_d.get(sound_key_name)
        # #if not st_sound or not st_min_pitch: return 0# Dictionary or sound_key_name is wrong NOTE Add custom error?
        # # Play sound if it is not playing rn with a pitch
        # if st_sound.playing == False:
            # st_sound.pitch = round(random() + st_min_pitch)
        #return 0









