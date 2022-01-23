from ursina import *
from random import random, uniform

from perlin_controller import Perlin
from helper import evenOrMinusOne
from swirl_engine import SwirlEngine



class MeshTerrain:
    def __init__(self):

        self.block = load_model('block.obj')
        self.textureAtlas = 'texture_atlas_3.png'
       

        self.subsets = []
        self.totalSubs = 256
        self.subsetWidth = 10 # Even number 
        # Subset generation engine
        self.genEngine = SwirlEngine(self.subsetWidth)
        self.currentSubset = 0

        self.numVertices = len(self.block.vertices)

        # Perlin noise
        self.perlin = Perlin()

        # Terrain Dictionary
        self.td = {}

        for i in range(0, self.totalSubs):
            e = Entity( model=Mesh(), 
                        texture=self.textureAtlas )
            e.texture_scale*=64/e.texture.width
            self.subsets.append(e)

    def getBlock(self, x, y, z):
        # Extend or add to the vertices of our model
        model = self.subsets[self.currentSubset].model

        model.vertices.extend([Vec3(x,y,z) + v for v in self.block.vertices])

        # Record, what the terrain is exist on these coords
        self.td[f"x{floor(x)}y{floor(y)}z{floor(z)}"] = "t"

        # Add random tint color to the blocks
        c = random()-0.7
        model.colors.extend( (Vec4(1-c, 1-c, 1-c, 1),) *
                self.numVertices)

        # Texture atlas coord for the grass
        uu = 8
        uv = 7
        # if high, paint snow
        if y > 2:
            uu = 8
            uv = 6

        model.uvs.extend([Vec2(uu,uv) + u for u in self.block.uvs])
    
    def genTerrain(self):
        #Get curent position as we generate subsets around world
        x = floor(self.genEngine.pos.x) # x
        z = floor(self.genEngine.pos.y) # z 
        y = 0

        d = int(evenOrMinusOne(self.subsetWidth)*0.5)

        for k in range(-d, d):
            for j in range(-d, d):

                y = floor(self.perlin.getHeight(x+k, z+j))
                if self.td.get(f"x{floor(x+k)}y{floor(y)}z{floor(z+j)}") == None:
                    self.getBlock(x+k, y, z+j)
        # Generate (Draw) current subset model whole
        self.subsets[self.currentSubset].model.generate()
       
        # Current subsets hack
        if self.currentSubset < self.totalSubs -1:
            self.currentSubset += 1
        else: self.currentSubset = 0

        self.genEngine.move()


