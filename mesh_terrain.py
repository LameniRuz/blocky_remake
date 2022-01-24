from ursina import *
from random import random, uniform

from perlin_controller import Perlin
from helper import evenOrMinusOne
from swirl_engine import SwirlEngine
from mining_system import highlight_block, mine



class MeshTerrain:
    def __init__(self):

        self.block = load_model('block.obj')
        self.textureAtlas = 'texture_atlas_3.png'
       

        self.subsets = []
        self.totalSubs = 3 
        self.subsetWidth = 4 # Even number 
        # Subset generation engine
        self.genEngine = SwirlEngine(self.subsetWidth)
        self.currentSubset = 0

        self.numVertices = len(self.block.vertices)

        # Perlin noise for terrain gen
        self.perlin = Perlin()

        # Terrain Dictionary for generation, to know if the block already exist
        self.td = {}

        # Vertex Dictionary for mining
        self.vd = {}

        # Create entities for each subset
        for i in range(0, self.totalSubs):
            e = Entity( model=Mesh(), 
                        texture=self.textureAtlas )
            e.texture_scale*=64/e.texture.width
            self.subsets.append(e)

    def input(self, key):
        if key=='left mouse up':
            mine(self.td, self.vd, self.subsets, self.numVertices)#NOTE fix mining_system file, for example make it a class, then inherit it here

    def update(self, pos, cam):
        #Highlight looked-at block
        highlight_block(pos, cam, self.td)


    def getBlock(self, x, y, z, subset=True):
        if subset: subset = self.currentSubset # Get default subset value, with workaround

        # Extend or add to the vertices of our model
        model = self.subsets[subset].model
        
        #NOTE how do coordinates work in ursina???
        model.vertices.extend([Vec3(x,y,z) + v for v in self.block.vertices])

        # Record, what the terrain is exist on these coords
        self.td[f"x{floor(x)}y{floor(y)}z{floor(z)}"] = "t"

        # Record subset index and first vertex of this block
        # model.vertices - all vertices in the curent subset model,
        # one model consist from many blocks (their vertices)
        svob = ( subset, len(model.vertices) - (self.numVertices + 1) )
        self.vd[f"x{floor(x)}y{floor(y)}z{floor(z)}"] = svob

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
        
        # Make model show texture from the textureAtlas, according to uu,uv atlas coords
        model.uvs.extend([Vec2(uu,uv) + u for u in self.block.uvs])
    
    def genTerrain(self):
        #Get curent position as we generate subsets around world
        x = floor(self.genEngine.pos.x) # x
        z = floor(self.genEngine.pos.y) # z 
        y = 0

        d = int(evenOrMinusOne(self.subsetWidth)*0.5)

        for k in range(-d, d):
            for j in range(-d, d):
                
                # Change y coord with the perlin noise
                y = floor(self.perlin.getHeight(x+k, z+j)) 

                # If there is no block in this position, create it
                if self.td.get(f"x{floor(x+k)}y{floor(y)}z{floor(z+j)}") == None:
                    self.getBlock(x+k, y, z+j)

        # Generate (Draw) current subset model whole
        self.subsets[self.currentSubset].model.generate()
       
        # Current subsets hack
        if self.currentSubset < self.totalSubs - 1:
            self.currentSubset += 1
        else: self.currentSubset = 0

        self.genEngine.move()


