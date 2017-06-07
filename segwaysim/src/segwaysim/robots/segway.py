import logging; logger = logging.getLogger("morse." + __name__)
import morse.core.robot
import morse.core.wheeled_robot
from morse.helpers.components import add_property




class Segway(morse.core.wheeled_robot.MorsePhysicsRobot):
    """ 
    Class definition for the segway robot.
    """

    _name = 'segway robot'

    def __init__(self, obj, parent=None):
        """ Constructor method

        Receives the reference to the Blender object.
        Optionally it gets the name of the object's parent,
        but that information is not currently used for a robot.
        """

        logger.info('%s initialization' % obj.name)
        morse.core.wheeled_robot.MorsePhysicsRobot.__init__(self, obj, parent)

        # Do here robot specific initializations
        logger.info('Component initialized')

    def default_action(self):
        """ Main loop of the robot
        """

        # This is usually not used (responsibility of the actuators
        # and sensors). But you can add here robot-level actions.
       


        pass
