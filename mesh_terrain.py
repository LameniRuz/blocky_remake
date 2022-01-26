from ursina import *
from random import random, uniform
from terrain_change_system import block_type_change

from perlin_controller import Perlin
from helper import evenOrMinusOne
from swirl_engine import SwirlEngine
from terrain_change_system import highlight_block, mine
from config import SIX_AXIS as six_axis, block_names



DEFAULT_BLOCK_TYPE = "soil"


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
            epi = mine(self.td, self.vd, self.subsets, self.numVertices)#NOTE fix mining_system file, for example make it a class, then inherit it here
            if epi:
                self.placeWalls(epi[0], epi[1])
                self.subsets[epi[1]].model.generate()


    def update(self, pos, cam):
        #Highlight looked-at block
        highlight_block(pos, cam, self.td)


    def getBlock(self, x, y, z, subset=True, gap=True, block_type=DEFAULT_BLOCK_TYPE):
        if subset: subset = self.currentSubset # Get default subset value, with workaround

        # If on these coord is a terrain or a gap, return
        if self.td.get(f"x{floor(x)}y{floor(y)}z{floor(z)}") != None: return

        # Extend or add to the vertices of our model
        model = self.subsets[subset].model
        
        #NOTE how do coordinates work in ursina???
        model.vertices.extend([Vec3(x,y,z) + v for v in self.block.vertices])

        # Record, what the terrain is exist on these coords
        self.td[f"x{floor(x)}y{floor(y)}z{floor(z)}"] = block_type #changed "t" to a specific block type
        # Record what above thes terrain is a gap, if its empty for mining wall gen
        if gap:
            upper_block =  self.td.get(f"x{floor(x)}y{floor(y+1)}z{floor(z)}")
            if upper_block == None:
                self.td[f"x{floor(x)}y{floor(y+1)}z{floor(z)}"] = "g"
            

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
        if block_type == block_names.grass:
            uu = 8
            uv = 7
        elif block_type == block_names.soil:
            uu = 10
            uv = 7
        elif block_type == block_names.stone:
            uu = 8
            uv = 5
        elif block_type == block_names.ice:
            uu = 9
            uv = 7
        elif block_type == block_names.snow:
            uu = 8
            uv = 6
        else:
            # If we dont know block type, make it grass
            uu = 8
            uv = 7

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
                #if self.td.get(f"x{floor(x+k)}y{floor(y)}z{floor(z+j)}") == None:
                block_type = block_type_change(y, block_type=DEFAULT_BLOCK_TYPE) 
                self.getBlock(x+k, y, z+j, block_type=block_type)

        # Generate (Draw) current subset model whole
        self.subsets[self.currentSubset].model.generate()
       
        # Current subsets hack
        if self.currentSubset < self.totalSubs - 1:
            self.currentSubset += 1
        else: self.currentSubset = 0

        self.genEngine.move()


    #Place Blocks around mined block if needed, to simulate depth of the earth
    def placeWalls(self, gap_position, sub_num):
        if gap_position == None: return
        for i in range(0,6):
            new_pos = gap_position + (0, 0 ,0) + six_axis[i] #FIXME
            block_type = block_type_change(new_pos.y, surface=False, block_type=DEFAULT_BLOCK_TYPE) 
            self.getBlock(new_pos.x, new_pos.y, new_pos.z, sub_num, False, block_type)
