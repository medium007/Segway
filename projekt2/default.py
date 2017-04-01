
from morse.builder import *
from projekt2.builder.robots import Segway



robot = Segway()    # add new robot based on class Segway()


robot.translate(0.0, 0.0, 2.0)
robot.rotate(0.0, 0.0, 0)

robot.add_default_interface('socket')


# set 'fastmode' to True to switch to wireframe mode
env = Environment('outdoors', fastmode = False)
env.set_camera_location([-18.0, -6.7, 10.8])
env.set_camera_rotation([1.09, 0, -1.14])

