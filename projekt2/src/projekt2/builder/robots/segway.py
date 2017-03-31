import logging; logger = logging.getLogger("morse." + __name__)
from morse.builder import *
import morse.core.wheeled_robot
from morse.core import blenderapi
from morse.helpers.components import add_property
from abc import ABCMeta
from morse.helpers.components import add_property
#from morse.helpers.joints import Joint6DoF
#from morse.helpers.controller import PIDController


import math



class Segway(WheeledRobot):
    """
    A template robot model for segway, with a motion controller and a pose sensor.
    """
    def __init__(self, name = None, debug = True):

        # segway.blend is located in the data/robots directory
        WheeledRobot.__init__(self, 'projekt2/robots/segway.blend', name)
        self.properties(classpath = "projekt2.robots.segway.Segway",
                        HasSuspension = False, HasSteering = False,
                        Influence = 0.1, Friction = 0.8, FixTurningSpeed = 1.16,
                        WheelFLName = "left_wheel", WheelFRName = "right_wheel",)

        ###################################
        # Actuators
        ###################################


        # (v,w) motion controller
        # Check here the other available actuators:
        # http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
        self.motion = MotionVWDiff()
        self.motion.translate(0.0, 0.0, 0.0)
        self.motion.rotate(0.0, 0.0, 0)
        self.append(self.motion)
        
#        self.przechylenie=ForceTorque()
#        self.append(self.przechylenie)

        # Optionally allow to move the robot with the keyboard
#        if debug:
#            keyboard = Keyboard()
#            keyboard.rotate(0.0, 0.0, 1.54)
#            keyboard.properties(ControlType = 'Position')
#            self.append(keyboard)

        ###################################
        # Sensors
        ###################################

        self.pose = Pose()
        self.append(self.pose)
        
        self.velocity = Velocity()
        self.append(self.velocity)



