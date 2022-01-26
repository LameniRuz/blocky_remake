
def evenOrMinusOne(num):
    if num % 2 == 0:
        return num
    else:
        return num - 1

def hex_to_RGB(hex_string: str) -> tuple:
    r = int(hex_string[1:3], 16)
    g = int(hex_string[3:5], 16)
    b = int(hex_string[5:7], 16)
    return (r,  g,  b)


class MemorisePositionHorisontal:
    def __init__(self, x=0, z=0):
        # Saved Positions
        self.x = x
        self.z = z

    def get_abs_difference(self, x, z):
        return (abs(self.x - x), abs(self.z - z))

    def update_positions(self, x, z):
        self.x = x
        self.z = z




if __name__ == "__main__":
    #Test code
    print(f"32 == {evenOrMinusOne(33)}")
    print(f"32 == {evenOrMinusOne(32)}")
    print(f"0 == {evenOrMinusOne(1)}")
