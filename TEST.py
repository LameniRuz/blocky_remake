from ursina import *
app = Ursina()
window.borderless = False



e = Entity(
model = 'cube',
color = color.pink,
position = (-2, 0, 10) )

e2 = Entity(
model = 'cube',
color = color.rgb(1,1,1),
position = (0, 0, 40) )

e3 = Entity(
model = 'cube',
color = color.pink,
position = (2, 0, 10) )


forward=True
def input(key):
    global forward
    if key == 'w':
        forward = True
        # camera.position += (0.,0.,0.3)
    elif key == 's':
        forward = False
        # camera.position -= (0.,0.,0.3)


def update():
    if forward:
        camera.position += (0.,0.,0.3)
    else:
        camera.position += (0.,0.,-0.3)

app.run()
