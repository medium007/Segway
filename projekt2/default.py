
from morse.builder import *
from projekt2.builder.robots import Segway



robot = Segway()    # add new robot based on class Segway()


robot.translate(5.0, 0.0, 1.0)
robot.rotate(0.0, 0.0, 0)

robot.add_default_interface('socket')


# set 'fastmode' to True which is switching to wireframe mode // update
env = Environment('srodowisko/mapa.blend', fastmode = False)
env.set_camera_location([-18.0, -6.7, 10.8])
env.set_camera_rotation([1.09, 0, -1.14])

# can't upload mapa.blend to github, if you have the file uncomment lines below and comment above
#env = Environment('projekt2/environment/mapa.blend')
#env.set_camera_location([10.0, -10.0, 10.0])
#env.set_camera_rotation([1.0470, 0, 0.7854])


