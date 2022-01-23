#from random import seed
from perlin_module import PerlinNoise


class Perlin:
    def __init__(self) -> None:

        self.seed = 0
        # Difference in detail, variety
        self.octaves = 8
        # Higher - more rough
        self.freq = 256 
        # How high or low 
        self.amp = 24 

        self.pNoise = PerlinNoise(self.octaves, self.seed)


    def getHeight(self, x, z):
        y = 0
        y = self.pNoise([x/self.freq, z/self.freq]) * self.amp
        return y

