
from morse.builder import *
from projekt2.builder.robots import Segway
from projekt2.builder.robots import Chase

from math import pi



robot = Segway()                    # add new robot based on class Segway()


robot.translate(57, -50, 0.0)       # setting robot initial position
robot.rotate(0.0, 0.0, 0)

robot.add_default_interface('socket')

chase = Chase()
chase.translate(50, -42, 0.0)
chase.rotate(z=0.70*pi)
chase.add_default_interface('socket')

cam = SemanticCamera()              # camera from 1st person view
cam.translate(z=2)
cam.translate(x=-3)
cam.rotate(y=0.3,z=pi)
robot.append(cam)
cam.properties(Vertical_Flip=False)
cam.properties(Horizontal_Flip=False)


env = Environment('../data/projekt2/environment/map_v2.blend', fastmode = False)    # loading environment


env.set_camera_location([63.0, -64.0, 10.0])        # normal camera
env.set_camera_rotation([1.0470, 0, 0.2854])
env.select_display_camera(cam)




