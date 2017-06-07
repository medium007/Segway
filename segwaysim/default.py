
from morse.builder import *
from segwaysim.builder.robots import Segway

from math import pi


#-------------------------------------------------------#
#----------SEGWAY INICIALIZATION------------------------#
#-------------------------------------------------------#

#FIRST SEGWAY
robot = Segway()                    # add new robot based on class Segway() (GO TO src/segwaysim/builder and src/segwaysim/robots to see more)


robot.translate(57, -50, -0.1)       # setting robot initial position
robot.rotate(0.0, 0.0, 0)

robot.add_default_interface('socket')

# SECOND SEGWAY
chase = Segway()
chase.translate(59, -40, -0.1)
# chase.rotate(z=0.70*pi)
chase.add_default_interface('socket')

#----------------------------------------------------------------#
#----------------------CAMERA------------------------------------#
#----------------------------------------------------------------#

cam = SemanticCamera()              # camera from 1st person view = what you see being on the first segway
cam.translate(z=2)
cam.translate(x=-3)
cam.rotate(y=0.3,z=pi)
robot.append(cam)
cam.properties(Vertical_Flip=False)
cam.properties(Horizontal_Flip=False)


env = Environment('../data/segwaysim/environment/map_v2.blend', fastmode = False)    # loading environment


env.set_camera_location([63.0, -64.0, 10.0])        # normal camera = to move use WSAD keys
env.set_camera_rotation([1.0470, 0, 0.2854])
env.select_display_camera(cam)




