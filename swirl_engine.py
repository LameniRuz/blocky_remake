from ursina import Vec2


class SwirlEngine:
    def __init__(self, subsetWidth):
        self.is_move = True 

        self.subsetWidth = subsetWidth
            

        # Tracks position of current generated turrain subset (at the center)
        # self.pos = Vec2(0,0)
        self.reset(0,0)

        self.directions = [ Vec2(0,1),# (x,z) 
                            Vec2(1,0),
                            Vec2(0,-1),
                            Vec2(-1,0) ]


    def change_direction(self):
        if self.direction < 3:
            self.direction += 1
            if self.direction < 2:
                # Up and right odd runs 1, 1, 3, ...
                self.run = (self.iteration * 2) - 1
            else:
                # Down and left even runs 2,  6
                self.run = self.iteration * 2
        else:
            self.direction = 0 
            self.iteration += 1
            
        

    def move(self):
        # if not self.is_move:
            # print("exiting swirl")
            # return

        if self.count < self.run:
            self.pos.x += self.directions[self.direction].x * self.subsetWidth #x first in Vec2
            self.pos.y += self.directions[self.direction].y * self.subsetWidth #z second in Vec2
            self.count += 1
        else:
            #All runs in the current direction complete
            self.count = 0
            # Change direction of subsets generation/placement
            self.change_direction()
            self.move()

    def reset(self, x, z):
        self.pos = Vec2(x, z)
        # self.pos.x = x #x
        # self.pos.y = z #z
        # How many times do we generate a subset ahead of the current direction
        self.run = 1
        self.iteration = 0
        # Count when we moved and generated all 
        #of our runs in the current direction
        self.count = 0 
        self.direction = 0 # Current direction of generation (0-3) 0,1,2,3

