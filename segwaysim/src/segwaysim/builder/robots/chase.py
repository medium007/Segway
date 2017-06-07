import logging; logger = logging.getLogger("morse." + __name__)
from morse.builder import *
import morse.core.wheeled_robot






import math



class Chase(WheeledRobot):

    def __init__(self, name = None, debug = True):


        WheeledRobot.__init__(self, 'segwaysim/robots/chase.blend', name)
        self.properties(classpath = "segwaysim.robots.chase.Chase",
                        HasSuspension = False, HasSteering = False,
                        Influence = 0.1, Friction = 0.8, FixTurningSpeed = 1.16,
                        WheelFLName = "left_wheel", WheelFRName = "right_wheel",)

        ###################################
        # Actuators
        ###################################

        self.motion = MotionVWDiff()  # v omega motion controller
        self.motion.translate(0.0, 0.0, 0.0)
        self.motion.rotate(0.0, 0.0, 0)
        self.append(self.motion)




        ###################################
        # Sensors
        ###################################

        self.pose = Pose()     # pose sensor
        self.append(self.pose)
        
        self.velocity = Velocity()     #velocity sensor
        self.append(self.velocity)



