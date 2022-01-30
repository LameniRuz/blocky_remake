from ursina import Audio
from math import floor 
from random import random as rd_random
from config import block_names
"""  Sound control needs to be imported after the game engine initiation"""

# Add new sounds settings here 
grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

sounds_for_blocks = { block_names.grass:  grass_audio, block_names.snow: snow_audio}
pitches_min_dict = { block_names.grass:  0.7, block_names.snow: 0.3}

class StepSound():
    def __init__(self):
        self.sounds_for_blocks = sounds_for_blocks
        self.pitches_min_dict = pitches_min_dict

    def play_step_sound(self, block):
        step_sound = self.sounds_for_blocks.get(block)
        min_pitch = self.pitches_min_dict.get(block)
        if not step_sound: step_sound = grass_audio
        if not min_pitch: min_pitch = 0.7
        if step_sound.playing == False:
            step_sound.pitch = rd_random() + min_pitch
            step_sound.play()

step_sound = StepSound()
