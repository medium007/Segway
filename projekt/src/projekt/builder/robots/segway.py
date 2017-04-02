from morse.builder import *
from projekt.builder.actuators import Wheels
from projekt.builder.actuators import Ruch

class Segway(GroundRobot):
    """
    A template robot model for segway, with a motion controller and a pose sensor.
    """
    def __init__(self, name = None, debug = True):

        # segway.blend is located in the data/robots directory
        GroundRobot.__init__(self, 'projekt/robots/segway.blend', name)
        self.properties(classpath = "projekt.robots.segway.Segway")

        ###################################
        # Actuators
        ###################################


        # (v,w) motion controller
        # Check here the other available actuators:
        # http://www.openrobots.org/morse/doc/stable/components_library.html#actuators
        self.motion = Ruch()
        
        self.append(self.motion)
        
        self.orientation = Orientation()
        self.append(self.orientation)
        self.wheels = Wheels()
        self.append(self.wheels)
        
        
        
    
        

        # Optionally allow to move the robot with the keyboard
        if debug:
            keyboard = Keyboard()
            keyboard.properties(ControlType = 'Position')
            self.append(keyboard)

        ###################################
        # Sensors
        ###################################

        self.pose = Pose()
        self.append(self.pose)


