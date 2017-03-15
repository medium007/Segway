#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <projekt> environment

Feel free to edit this template as you like!
"""

from morse.builder import *


from projekt.builder.robots import Segway

segway = Segway()
segway.add_default_interface('socket')








env = Environment('outdoors')
env.set_camera_location([5, -5, 6])
env.set_camera_rotation([1.0470, 0, 0.7854])
