from ursina import *
from ursina import collider
from ursina.shaders import *
from random import random
from terrain_change_system import block_type_change

from perlin_controller import Perlin
from helper import evenOrMinusOne
from swirl_engine import SwirlEngine
from terrain_change_system import highlight_block, mine, hl_block
from config import SIX_AXIS as six_axis, block_names
from building_system import checkBuildPos, gapShell

# Constants
DEFAULT_BLOCK_TYPE = block_names.soil
TERRAIN_SHADER=None
BLISTER_MINE_COUNT = 1

texture_map = { # <block_type_name>: (<uu>, <uv>), uu, uv - Texture atlas coord
                block_names.soil:  (10, 7),
                block_names.grass: (8, 7),
                block_names.stone: (8, 5),
                block_names.ice: (9,7),
                block_names.snow: (8,6),
}


class MeshTerrain:
    def __init__(self):
        self.block = load_model('block.obj')
        self.textureAtlas = 'texture_atlas_3.png'
       
        self.subsets = []
        self.totalSubs = 1024 
        self.subsetWidth = 6 # Even number 
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

        #FIXME testing blister is to fast
        self.blister_tm = 0

        # Create entities for each subset
        for i in range(0, self.totalSubs):
            e = Entity( model=Mesh(), 
                        texture=self.textureAtlas,
                        shader=TERRAIN_SHADER,
                        )
            e.texture_scale*=64/e.texture.width
            self.subsets.append(e)

    def doMining(self):
            epi = mine(self.td, self.vd, self.subsets, self.numVertices)#NOTE fix terrain_change_system file, for example make it a class, then inherit it here
            if epi:
                self.placeWalls(epi[0], epi[1])
                self.subsets[epi[1]].model.generate()

    def doBuilding(self, block_type=DEFAULT_BLOCK_TYPE):#NOTE remove default block later
        build_pos = checkBuildPos(self.td, self.vd)
        if build_pos:
            (x,y,z, sub_pos) = build_pos
            self.getBlock(x, y, z, subset=sub_pos,block_type=block_type)
            gapShell(x, y, z , self.td)
            self.subsets[sub_pos].model.generate()


    def input(self, key):
        if key=='left mouse up':
            self.doMining()
        if key == 'right mouse up':
            self.doBuilding()

    
    def update(self, pos, cam):
        #Highlight looked-at block
        highlight_block(pos, cam, self.td)

        #blister-mining, NOTE too fust, need to update subset model/ or spawn wall earlier
        if hl_block.visible==True:
            self.blister_tm +=1
            if self.blister_tm == BLISTER_MINE_COUNT:
                self.blister_tm = 0
                if held_keys.get('left mouse') == 1:
                    self.doMining()


    def getBlock(self, x, y, z, subset, gap=True, block_type=DEFAULT_BLOCK_TYPE):
        block = self.td.get( (floor(x), floor(y), floor(z)) )#FIXME is it needed?
        # If on these coord is a terrain, return
        if block != 'g' and block != None: return

        model = self.subsets[subset].model# Extend or add to the vertices of our model
        model.vertices.extend([Vec3(x,y,z) + v for v in self.block.vertices]) #NOTE how do coordinates work in ursina???

        # Record, what the terrain is exist on these coords
        self.td[ (floor(x), floor(y), floor(z)) ] = block_type
        # Record what above the terrain is a gap if its empty, for the mining and wall gen
        if gap:
            upper_block =  self.td.get( (floor(x), floor(y+1), floor(z)) )
            if upper_block == None:
                self.td[ (floor(x), floor(y+1), floor(z)) ] = "g"
            
        # Record subset index and first vertex of this block
        # model.vertices - all vertices in the curent subset model,
        # one model consist from many blocks (their vertices)
        svob = ( subset, len(model.vertices) - (self.numVertices + 1) )
        self.vd[ (floor(x), floor(y), floor(z)) ] = svob

        # Add random tint color to the blocks
        c = random()-0.7
        model.colors.extend( (Vec4(1-c, 1-c, 1-c, 1),) *
                self.numVertices)
        
        uu, uv = texture_map.get(block_type, (None, None))# Get texture coords on the atlas
        
        # Make model show texture from the textureAtlas, according to uu,uv atlas coords
        if uu: model.uvs.extend([Vec2(uu,uv) + u for u in self.block.uvs]) #NOTE Add custom errors


    def genTerrain(self):
        #Get curent position as we generate subsets around the world
        x = floor(self.genEngine.pos.x) # x
        z = floor(self.genEngine.pos.y) # z 
        y = 0

        d = int(evenOrMinusOne(self.subsetWidth)*0.5)

        for k in range(-d, d):
            for j in range(-d, d):
                # Change y coord with the perlin noise
                y = floor(self.perlin.getHeight(x+k, z+j)) 

                # If there is no block or a gap in this position, create it
                if not self.td.get( (floor(x+k), floor(y), floor(z+j)) ):
                    block_type = block_type_change(y, block_type=DEFAULT_BLOCK_TYPE) 
                    self.getBlock(x+k, y, z+j, subset=self.currentSubset, block_type=block_type)

        # Generate (Draw) current subset model whole
        self.subsets[self.currentSubset].model.generate()
       
        # Rotate current subset
        if self.currentSubset < self.totalSubs - 1:
            self.currentSubset += 1
        else: self.currentSubset = 0


        self.genEngine.move()


    #Place Blocks around mined block if needed, to simulate depth of the earth
    def placeWalls(self, gap_position, sub_num):
        if gap_position == None: return
        for i in range(0,6):
            new_pos = gap_position + six_axis[i]
            if not self.td.get( (new_pos.x, new_pos.y, new_pos.z) ):# place walls if there is no gap or block
                block_type = block_type_change(new_pos.y, surface=False, block_type=DEFAULT_BLOCK_TYPE) 
                self.getBlock(new_pos.x, new_pos.y, new_pos.z, sub_num, False, block_type)

        
